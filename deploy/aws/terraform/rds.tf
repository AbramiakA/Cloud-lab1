resource "random_password" "db" {
  length  = 20
  special = false
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.project}-db-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "${var.project}-db-subnet-group"
  }
}

resource "aws_db_instance" "main" {
  identifier = "${var.project}-db"

  engine         = "mysql"
  instance_class = "db.t4g.micro"

  allocated_storage = 20
  storage_type      = "gp3"

  db_name  = "ecommerce_db"
  username = "appuser"
  password = random_password.db.result

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]

  publicly_accessible = false
  multi_az            = false

  skip_final_snapshot = true
  deletion_protection = false

  storage_encrypted = true
}