#вдень від 8 до 23, 2–3 Tasks
resource "aws_appautoscaling_scheduled_action" "day" {
    name = "lab1-day-scaling"
    service_namespace = aws_appautoscaling_target.ecs.service_namespace
    resource_id = aws_appautoscaling_target.ecs.resource_id
    scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension

    schedule = "cron(0 8 * * ? *)"
    timezone = "Europe/Kyiv"

    scalable_target_action {
        min_capacity = 2
        max_capacity = 3
    }
}

#вночі від 23 до 8, 1 Task
resource "aws_appautoscaling_scheduled_action" "night" {
    name = "lab1-night-scaling"
    service_namespace = aws_appautoscaling_target.ecs.service_namespace
    resource_id = aws_appautoscaling_target.ecs.resource_id
    scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension

    schedule = "cron(0 23 * * ? *)"
    timezone = "Europe/Kyiv"

    scalable_target_action {
        min_capacity = 1
        max_capacity = 1
    }
}
