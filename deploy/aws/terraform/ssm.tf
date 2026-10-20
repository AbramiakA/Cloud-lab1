resource "aws_ssm_parameter" "database_url" {
  name = "/${var.project}/DATABASE_URL"
  type = "SecureString"

  value = "mysql://${aws_db_instance.main.username}:${random_password.db.result}@${aws_db_instance.main.address}:${aws_db_instance.main.port}/${aws_db_instance.main.db_name}"
}
