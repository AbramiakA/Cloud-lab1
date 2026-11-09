output "service_url" {
  value = "http://${aws_lb.app.dns_name}"  #виводить публічний урл ALB, через який можна відкрити
}