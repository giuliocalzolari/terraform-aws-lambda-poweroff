
output "lambda_arn" {
  description = "AWS Lambda ARN"
  value       = aws_lambda_function.main.arn
}


output "lambda_function_last_modified" {
  description = "The date Lambda function was last modified"
  value       = aws_lambda_function.main.last_modified
}

output "lambda_function_version" {
  description = "Latest published version of your Lambda function"
  value       = aws_lambda_function.main.version
}

output "lambda_iam_role_name" {
  description = "IAM role name"
  value       = aws_iam_role.lambda_role.name
}

output "lambda_iam_role_arn" {
  description = "IAM role ARN"
  value       = aws_iam_role.lambda_role.arn
}

output "cloudwatch_event_rule_id" {
  description = "Cloudwatch rule ID"
  value       = aws_cloudwatch_event_rule.cw_rule.id
}


output "log_group_name" {
  description = "The name of the scheduler log group"
  value       = aws_cloudwatch_log_group.lambda_log.name
}

output "log_group_arn" {
  description = "The Amazon Resource Name (ARN) specifying the log group"
  value       = aws_cloudwatch_log_group.lambda_log.arn
}
