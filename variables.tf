variable "base_name" {
  description = "Application Name"
  default     = "poweroff"
  type        = string
}

variable "log_retention_days" {
  description = "Cloudwatch Log Retation Days"
  default     = 90
  type        = number
}

variable "extra_tags" {
  type        = map(string)
  description = "Additional Tag to add"
}

# Set cloudwatch events for shutingdown instances
# trigger lambda functuon every hours.
# Cron time must be in UTC format.
# cf doc : https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
variable "cloudwatch_schedule_expression" {
  description = "Define the aws cloudwatch event rule schedule expression"
  type        = string
  default     = "cron(01 * * * * *)"
}