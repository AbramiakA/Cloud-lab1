
# Визначаємо, скільки ECS tasks може працювати
resource "aws_appautoscaling_target" "ecs" {
    service_namespace  = "ecs"
    resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.app.name}"
    scalable_dimension = "ecs:service:DesiredCount"

    min_capacity = 1
    max_capacity = 3
}

# Налаштовуємо масштабування залежно від CPU
resource "aws_appautoscaling_policy" "ecs_cpu" {
    name        = "${var.project}-cpu-autoscaling"
    policy_type = "TargetTrackingScaling"

    service_namespace  = aws_appautoscaling_target.ecs.service_namespace
    resource_id        = aws_appautoscaling_target.ecs.resource_id
    scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension

    target_tracking_scaling_policy_configuration {
        target_value       = 60.0
        scale_out_cooldown = 60
        scale_in_cooldown  = 300

        predefined_metric_specification {
            predefined_metric_type = "ECSServiceAverageCPUUtilization"
        }
    }
}
