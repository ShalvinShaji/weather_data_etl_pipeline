output "api_fetch_lambda_role" {
  value = aws_iam_role.api_fetch_lambda_role.arn
}

output "glue_processing_role" {
  value = aws_iam_role.glue_processing_role.arn
}