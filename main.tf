

resource "aws_cloudwatch_event_rule" "cw_rule" {
  name                = "${var.base_name}-event"
  description         = "Trigger lambda scheduler"
  schedule_expression = var.cloudwatch_schedule_expression
}

resource "aws_cloudwatch_event_target" "cw_target" {
  target_id = "${var.base_name}-lambda"
  rule      = aws_cloudwatch_event_rule.cw_rule.name
  arn       = aws_lambda_function.main.arn
}

resource "aws_lambda_permission" "allow_execution_from_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  principal     = "events.amazonaws.com"
  function_name = aws_lambda_function.main.function_name
  source_arn    = aws_cloudwatch_event_rule.cw_rule.arn
}


data "aws_iam_policy_document" "lambda_policy_doc" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "ec2:DescribeRegions",
      "ec2:DescribeInstances",
      "ec2:DescribeInstances",
      "ec2:DescribeInstanceStatus",
      "ec2:StopInstances",
      "ec2:StartInstances",
      "ec2:DescribeTags",
      "ec2:DescribeSpotInstanceRequests",
      "rds:ListTagsForResource",
      "rds:DescribeDBClusters",
      "rds:StartDBCluster",
      "rds:StopDBCluster",
      "rds:DescribeDBInstances",
      "rds:StartDBInstance",
      "rds:StopDBInstance",
      "autoscaling:DescribeScalingProcessTypes",
      "autoscaling:DescribeAutoScalingGroups",
      "autoscaling:DescribeTags",
      "autoscaling:SuspendProcesses",
      "autoscaling:ResumeProcesses",
      "autoscaling:UpdateAutoScalingGroup",
      "autoscaling:DescribeAutoScalingInstances",
      "autoscaling:TerminateInstanceInAutoScalingGroup",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role_policy" "lambda_policy" {
  name   = "${var.base_name}-policy"
  role   = aws_iam_role.lambda_role.id
  policy = data.aws_iam_policy_document.lambda_policy_doc.json
}



resource "aws_iam_role" "lambda_role" {
  name = "${var.base_name}-lambda-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
  tags               = var.extra_tags
}

resource "aws_cloudwatch_log_group" "lambda_log" {
  name              = "/aws/lambda/${var.base_name}"
  retention_in_days = var.log_retention_days
  tags              = var.extra_tags
}


locals {
  file_location = "${path.module}/src/main.py"
  filename      = "code.zip"
}


data "archive_file" "lambda" {
  type        = "zip"
  source_file = local.file_location
  output_path = local.filename
}


resource "aws_lambda_function" "main" {
  filename         = local.filename
  function_name    = "${var.base_name}-lambda"
  description      = "${var.base_name}-lambda"
  timeout          = 600
  memory_size      = 256
  runtime          = "python3.8"
  role             = aws_iam_role.lambda_role.arn
  handler          = "main.lambda_handler"
  source_code_hash = data.archive_file.lambda.output_base64sha256

  tags = merge(
    var.extra_tags,
    {
      Name = "${var.base_name}-lambda"
    },
  )

}
