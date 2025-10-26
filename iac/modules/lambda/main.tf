data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir = "${path.module}/src"
  output_path = "${path.module}/src/lambda.zip"
}

resource "aws_lambda_function" "weather_api_fetcher_lambda" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "weather_api_fetcher_lambda"
  role          = var.api_fetch_lambda_role
  handler       = "weather_fetcher.lambda_handler"
  runtime       = "python3.9"
  timeout       = 30
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  layers = [aws_lambda_layer_version.weather_api_fetcher_lambda_layer.arn]

  environment {
    variables = {
      SECRET_ARN = aws_secretsmanager_secret.weather_api_key.arn
      S3_BUCKET_ARN = var.weather_data_s3_bucket_name
    }
  }
}

resource "aws_cloudwatch_event_rule" "five_minute_api_fetch_lambda" {
  name                = "every-five-minutes"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "trigger_api_fetch_lambda" {
  rule = aws_cloudwatch_event_rule.five_minute_api_fetch_lambda.name
  arn  = aws_lambda_function.weather_api_fetcher_lambda.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.weather_api_fetcher_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.five_minute_api_fetch_lambda.arn
}

data "archive_file" "weather_api_fetcher_lambda_layer" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_layer"
  output_path = "${path.module}/weather_api_fetcher_lambda_layer.zip"
}

resource "aws_lambda_layer_version" "weather_api_fetcher_lambda_layer" {
  filename   = data.archive_file.weather_api_fetcher_lambda_layer.output_path
  layer_name = "weather_api_fetcher_lambda_layer"
  compatible_runtimes = ["python3.9"]
  source_code_hash    = data.archive_file.weather_api_fetcher_lambda_layer.output_base64sha256
}



resource "aws_secretsmanager_secret" "weather_api_key" {
  name = "weather_api_key"
}

resource "aws_secretsmanager_secret_version" "weather_api_key" {
  secret_id = aws_secretsmanager_secret.weather_api_key.id
  secret_string = jsonencode({
    access_key = "YOUR_ACTUAL_API_KEY_HERE"
  })
}

