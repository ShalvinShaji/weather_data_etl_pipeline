resource "aws_glue_job" "weather_data_cleaning" {
  name     = "weather_data_cleaning"
  role_arn = var.glue_role_arn
  
  command {
    script_location = "s3://${var.script_bucket}/glue_scripts/raw_to_silver.py"
    python_version  = "3"
  }
  
  default_arguments = {
    "--job-bookmark-option" = "job-bookmark-enable"
    "--enable-metrics"      = "true"
    "--S3_BUCKET_NAME"      = var.script_bucket
    "--JOB_NAME"            = "weather_data_cleaning"
  }
  
  worker_type       = "G.1X"
  number_of_workers = 2

}