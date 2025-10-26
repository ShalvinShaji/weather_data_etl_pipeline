variable "api_fetch_lambda_role" {
  description = "ARN of the IAM role for Lambda"
  type        = string
}

variable "weather_data_s3_bucket_name" {
  type = string
}