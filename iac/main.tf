module "iam" {
  source = "./modules/iam"
}

module "s3"{
  source = "./modules/s3"
}


module "lambda" {
  source         = "./modules/lambda"
  api_fetch_lambda_role = module.iam.api_fetch_lambda_role
  weather_data_s3_bucket_name  = module.s3.weather_bucket_name
}

module "glue" {
  source = "./modules/glue"
  glue_role_arn = module.iam.glue_processing_role
  script_bucket = module.s3.weather_bucket_name
}