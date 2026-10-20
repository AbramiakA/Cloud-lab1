resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com" #GitHub Actions видає OIDC tokens

  client_id_list = [
    "sts.amazonaws.com"
  ]
}

data "aws_iam_policy_document" "github_assume_role" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRoleWithWebIdentity" #дозволити взяти цю IAM Role через GitHub OIDC
    ]

    principals {
      type = "Federated" #зовнішня система, якій довіряємо через federated

      identifiers = [
        aws_iam_openid_connect_provider.github.arn # який Federated Provider може використовувати це правило
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"

      values = [
        "sts.amazonaws.com"
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:sub"

      values = [
        "repo:${var.github_repository}:ref:refs/heads/main"
      ]
    }
  }
}

resource "aws_iam_role" "github_actions" {
  name = "${var.project}-github-actions-role"

  assume_role_policy = data.aws_iam_policy_document.github_assume_role.json
}

resource "aws_iam_role_policy" "github_actions" {
  name = "${var.project}-github-actions-policy"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Sid    = "ECRAuthorization"
        Effect = "Allow"

        Action = [
          "ecr:GetAuthorizationToken"
        ]

        Resource = "*"
      }, #це дія авторизації в самому ECR і вона не обмежується ARN конкретного repository

      {
        Sid    = "ECRPush"
        Effect = "Allow"

        Action = [
          "ecr:BatchCheckLayerAvailability", #Чи є вже цей layer у ECR
          "ecr:InitiateLayerUpload",         #почати завантаження нового layer
          "ecr:UploadLayerPart",             #завантажувати шматки layer
          "ecr:CompleteLayerUpload",         #закінчити завантаження layer
          "ecr:PutImage"                     #зареєструвати image manifest і tag
        ]

        Resource = aws_ecr_repository.app.arn
      }, #тільки наш lab1-app repository

      {
        Sid    = "ECSDescribeTaskDefinition"
        Effect = "Allow"

        Action = [
          "ecs:DescribeTaskDefinition" #прочитати поточну Task Definition
        ]

        Resource = "*"
      },

      {
        Sid    = "ECSRegisterTaskDefinition"
        Effect = "Allow"

        Action = [
          "ecs:RegisterTaskDefinition" #зареєструвати нову revision
        ]

        Resource = "${aws_ecs_task_definition.app.arn_without_revision}:*"
      },

      {
        Sid    = "ECSService"
        Effect = "Allow"

        Action = [
          "ecs:UpdateService",   #оновити Service на нову Task Definition
          "ecs:DescribeServices" #прочитати поточний стан ECS Service
        ]

        Resource = aws_ecs_service.app.arn
      },

      {
        Sid    = "PassExecutionRole"
        Effect = "Allow"

        Action = [
          "iam:PassRole"
        ]

        Resource = aws_iam_role.ecs_task_execution.arn
      }
    ]
  })
}