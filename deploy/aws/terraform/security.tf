resource "aws_security_group" "app" {
  name        = "${var.project}-app-sg"
  description = "Security group for ECS Fargate application"
  vpc_id      = module.vpc.vpc_id

  tags = {
    Name = "${var.project}-app-sg"
  }
}

resource "aws_security_group" "db" {
  name        = "${var.project}-db-sg"
  description = "Security group for RDS MySQL"
  vpc_id      = module.vpc.vpc_id

  tags = {
    Name = "${var.project}-db-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "db_from_app" {
  security_group_id            = aws_security_group.db.id
  referenced_security_group_id = aws_security_group.app.id

  from_port   = 3306
  to_port     = 3306
  ip_protocol = "tcp"
}

resource "aws_security_group" "alb" {
  name        = "${var.project}-alb-sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = module.vpc.vpc_id

  tags = {
    Name = "${var.project}-alb-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "alb_http" {
  security_group_id = aws_security_group.alb.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 80
  to_port     = 80
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "alb_to_app" {
  security_group_id            = aws_security_group.alb.id
  referenced_security_group_id = aws_security_group.app.id

  from_port   = 5000
  to_port     = 5000
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "app_from_alb" {
  security_group_id            = aws_security_group.app.id
  referenced_security_group_id = aws_security_group.alb.id

  from_port   = 5000
  to_port     = 5000
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "app_to_db" {
  security_group_id            = aws_security_group.app.id
  referenced_security_group_id = aws_security_group.db.id

  from_port   = 3306
  to_port     = 3306
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "app_https" {
  security_group_id = aws_security_group.app.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "app_dns_udp" {
  security_group_id = aws_security_group.app.id

  cidr_ipv4   = module.vpc.vpc_cidr_block
  from_port   = 53
  to_port     = 53
  ip_protocol = "udp"
}

resource "aws_vpc_security_group_egress_rule" "app_dns_tcp" {
  security_group_id = aws_security_group.app.id

  cidr_ipv4   = module.vpc.vpc_cidr_block
  from_port   = 53
  to_port     = 53
  ip_protocol = "tcp"
}