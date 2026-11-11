resource "aws_cloudwatch_log_group" "app" { #шоб писати логи
  name              = "/ecs/${var.project}-app"
  retention_in_days = 7
}

resource "aws_ecs_cluster" "main" { #тут ECS організовує наші services і tasks
  name = "${var.project}-cluster"

  setting {
    name  = "containerInsights" #розширений моніторинг ECS у CloudWatch
    value = "enabled"
  }
}

#інструкція(скільки ресурсів отримає кожна нова Task)
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project}-app"
  network_mode             = "awsvpc" #кожен таск отримує свою іп
  requires_compatibilities = ["FARGATE"]

  cpu    = "256"
  memory = "512" #мб

  execution_role_arn = aws_iam_role.ecs_task_execution.arn #права ECS для запуску контейнера

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  container_definitions = jsonencode([ #опис самого контейнера який працює в таск
    {
      name      = "app"
      image     = "${aws_ecr_repository.app.repository_url}:1.3" #початковий імедж
      essential = true

      portMappings = [ #мережевий порт
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
        },
        {
          name  = "REDIS_URL"
          value = "rediss://${aws_elasticache_replication_group.redis.primary_endpoint_address}:6379/0"
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

#підтримує застосунок живим (сервіс)
resource "aws_ecs_service" "app" {
  name            = "${var.project}-service"
  cluster         = aws_ecs_cluster.main.id #сервіс працює в кластері
  task_definition = aws_ecs_task_definition.app.arn

  desired_count = 1
  launch_type   = "FARGATE"

  health_check_grace_period_seconds = 120 # 120 сек на старт

  network_configuration {
    subnets = module.vpc.private_subnets

    security_groups = [
      aws_security_group.app.id
    ]

    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn #при створ нової таск ecs реєстує її в тарнгт груп
    container_name   = "app"
    container_port   = 5000
  }

  depends_on = [
    aws_lb_listener.http #сервіс створюється тільки якщо вже є лісенер
  ]

  #Після створення Service ігнорити
  lifecycle {
    ignore_changes = [
      desired_count,  #кількість контейнерів контролює Auto Scaling
      task_definition #версію застосунку оновлює GitHub Actions
    ]
  }

}
