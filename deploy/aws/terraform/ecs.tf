resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${var.project}-app"
  retention_in_days = 7
}

resource "aws_ecs_cluster" "main" {
  name = "${var.project}-cluster"
}

#інструкція
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project}-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  cpu    = "256"
  memory = "512"

  execution_role_arn = aws_iam_role.ecs_task_execution.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  container_definitions = jsonencode([
    {
      name      = "app"
      image     = "${aws_ecr_repository.app.repository_url}:1.0"
      essential = true

      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "PORT"
          value = "5000"
        }
      ]

      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_ssm_parameter.database_url.arn
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"

        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.app.name # логи контейнера відправляй у AWS CloudWatch Log
          "awslogs-region"        = var.region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

#підтримує застосунок живим
resource "aws_ecs_service" "app" {
  name            = "${var.project}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn

  desired_count = 1
  launch_type   = "FARGATE"

  health_check_grace_period_seconds = 120

  network_configuration {
    subnets = module.vpc.private_subnets

    security_groups = [
      aws_security_group.app.id
    ]

    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 5000
  }

  depends_on = [
    aws_lb_listener.http
  ]
}