resource "aws_ecr_repository" "app" {
  name         = "lab1-app"
  force_delete = true
}