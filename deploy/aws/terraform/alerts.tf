# Lab 2, task 4: CloudWatch alerts for ECS CPU and ALB p95 latency.
# Supply the email without saving it in the repository:
#   $env:TF_VAR_lab2_alert_email = Read-Host "Email for AWS alerts"

variable "lab2_alert_email" {
  description = "Email address to receive lab 2 CloudWatch alarm notifications"
  type        = string

  validation {
    condition     = can(regex("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", var.lab2_alert_email))
    error_message = "Enter a valid email address for CloudWatch alerts."
  }
}

data "aws_caller_identity" "lab2" {}

resource "aws_sns_topic" "lab2_alerts" {
  name = "${var.project}-lab2-alerts"
}

# Preserve account-owner permissions and permit these CloudWatch alarms to publish.
resource "aws_sns_topic_policy" "lab2_alerts" {
  arn = aws_sns_topic.lab2_alerts.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AccountOwnerAccess"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.lab2.account_id}:root"
        }
        Action = [
          "sns:GetTopicAttributes",
          "sns:SetTopicAttributes",
          "sns:AddPermission",
          "sns:RemovePermission",
          "sns:DeleteTopic",
          "sns:Subscribe",
          "sns:ListSubscriptionsByTopic",
          "sns:Publish"
        ]
        Resource = aws_sns_topic.lab2_alerts.arn
      },
      {
        Sid    = "CloudWatchAlarmPublish"
        Effect = "Allow"
        Principal = {
          Service = "cloudwatch.amazonaws.com"
        }
        Action   = "sns:Publish"
        Resource = aws_sns_topic.lab2_alerts.arn
        Condition = {
          StringEquals = {
            "aws:SourceAccount" = data.aws_caller_identity.lab2.account_id
          }
          ArnLike = {
            "aws:SourceArn" = "arn:aws:cloudwatch:${var.region}:${data.aws_caller_identity.lab2.account_id}:alarm:${var.project}-lab2-*"
          }
        }
      }
    ]
  })
}

resource "aws_sns_topic_subscription" "lab2_email" {
  topic_arn = aws_sns_topic.lab2_alerts.arn
  protocol  = "email"
  endpoint  = var.lab2_alert_email
}

resource "aws_cloudwatch_metric_alarm" "lab2_cpu_high" {
  alarm_name          = "${var.project}-lab2-cpu-high"
  alarm_description   = "ECS service CPU exceeds 70% for 2 consecutive minutes"
  comparison_operator = "GreaterThanThreshold"
  threshold           = 70
  evaluation_periods  = 2
  datapoints_to_alarm = 2
  period              = 60
  statistic           = "Average"
  namespace           = "AWS/ECS"
  metric_name         = "CPUUtilization"

  dimensions = {
    ClusterName = aws_ecs_cluster.main.name
    ServiceName = "${var.project}-service"
  }

  treat_missing_data = "notBreaching"
  alarm_actions      = [aws_sns_topic.lab2_alerts.arn]
  ok_actions         = [aws_sns_topic.lab2_alerts.arn]
  depends_on         = [aws_sns_topic_policy.lab2_alerts]
}

resource "aws_cloudwatch_metric_alarm" "lab2_latency_high" {
  alarm_name          = "${var.project}-lab2-latency-high"
  alarm_description   = "ALB target response time p95 exceeds 0.5 seconds for 2 consecutive minutes"
  comparison_operator = "GreaterThanThreshold"
  threshold           = 0.5
  evaluation_periods  = 2
  datapoints_to_alarm = 2
  period              = 60
  extended_statistic  = "p95"
  namespace           = "AWS/ApplicationELB"
  metric_name         = "TargetResponseTime"

  dimensions = {
    LoadBalancer = aws_lb.app.arn_suffix
  }

  treat_missing_data = "notBreaching"
  alarm_actions      = [aws_sns_topic.lab2_alerts.arn]
  ok_actions         = [aws_sns_topic.lab2_alerts.arn]
  depends_on         = [aws_sns_topic_policy.lab2_alerts]
}
