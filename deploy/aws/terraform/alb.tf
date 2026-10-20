resource "aws_lb" "app" {
  name               = "${var.project}-alb"
  internal           = false #публічний
  load_balancer_type = "application"

  security_groups = [
    aws_security_group.alb.id
  ]

  subnets = module.vpc.public_subnets
}

#список цілей, куди ALB може відправляти запити
resource "aws_lb_target_group" "app" {
  name        = "${var.project}-tg"
  port        = 5000 #flack слухає порт 5000
  protocol    = "HTTP"
  target_type = "ip" #ecs_service додає ip
  vpc_id      = module.vpc.vpc_id

  health_check {
    path                = "/health"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 15
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}


#що ALB слухає ззовні і що робити з цим трафіком
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward" #передати далі у Target Group
    target_group_arn = aws_lb_target_group.app.arn
  }
}