resource "aws_cloudwatch_dashboard" "lab2" {
  dashboard_name = "${var.project}-lab2-dashboard"

  dashboard_body = jsonencode({  #описує що  буде на панелі
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "ECS Tasks: desired and running"
          region = var.region
          period = 60
          stat   = "Average"
          view   = "timeSeries"
          metrics = [
            ["ECS/ContainerInsights", "DesiredTaskCount", "ServiceName", "${var.project}-service", "ClusterName", aws_ecs_cluster.main.name, { label = "Desired Tasks" }],
            ["ECS/ContainerInsights", "RunningTaskCount", "ServiceName", "${var.project}-service", "ClusterName", aws_ecs_cluster.main.name, { label = "Running Tasks" }]
          ]
          yAxis = { left = { min = 0 } }
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          title  = "ECS CPU utilization (%)"
          region = var.region
          period = 60
          stat   = "Average"
          view   = "timeSeries"
          metrics = [
            ["AWS/ECS", "CPUUtilization", "ClusterName", aws_ecs_cluster.main.name, "ServiceName", "${var.project}-service"]
          ]
          yAxis = { left = { min = 0, max = 100 } }
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 6
        width  = 12
        height = 6
        properties = {
          title  = "ALB requests per minute"
          region = var.region
          period = 60
          stat   = "Sum"
          view   = "timeSeries"
          metrics = [
            ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", aws_lb.app.arn_suffix]
          ]
          yAxis = { left = { min = 0 } }
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 6
        width  = 12
        height = 6
        properties = {
          title  = "ALB target response time (p95, seconds)"
          region = var.region
          period = 60
          stat   = "p95"
          view   = "timeSeries"
          metrics = [
            ["AWS/ApplicationELB", "TargetResponseTime", "LoadBalancer", aws_lb.app.arn_suffix]
          ]
          yAxis = { left = { min = 0 } }
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 12
        width  = 24
        height = 6
        properties = {
          title  = "ALB target HTTP 5xx responses per minute"
          region = var.region
          period = 60
          stat   = "Sum"
          view   = "timeSeries"
          metrics = [
            ["AWS/ApplicationELB", "HTTPCode_Target_5XX_Count", "LoadBalancer", aws_lb.app.arn_suffix]
          ]
          yAxis = { left = { min = 0 } }
        }
      }
    ]
  })
}
