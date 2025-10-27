resource "aws_s3_bucket" "weather_data" {
  bucket = "weather-data-bucket-sha283"
}

resource "aws_s3_object" "raw_folder" {
  bucket = aws_s3_bucket.weather_data.id
  key    = "raw/"
}

resource "aws_s3_object" "silver_folder" {
  bucket = aws_s3_bucket.weather_data.id
  key    = "silver/"
}

resource "aws_s3_object" "gold_folder" {
  bucket = aws_s3_bucket.weather_data.id
  key    = "gold/"
}
resource "aws_s3_object" "glue_scripts" {
  bucket = aws_s3_bucket.weather_data.id
  key    = "glue_scripts/"
}