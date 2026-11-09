resource "aws_ecr_repository" "app" {   #наш репо в AWS ECR
  name         = "lab1-app"
  force_delete = true  #можна видалити навіть якщо є імеджі
}