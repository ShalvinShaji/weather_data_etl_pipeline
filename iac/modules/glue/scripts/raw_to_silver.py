import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME','S3_BUCKET_NAME'])
S3_BUCKET = args['S3_BUCKET_NAME']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(GlueContext)
job.init(args['JOB_NAME'], args)

# Read with DynamicFrame - automatically handles schema differences
raw_dynamicframe = glueContext.create_dynamic_frame.from_options(
    connection_type = "s3",
    connection_options = {"paths": [f"s3://{S3_BUCKET}/raw/"]},
    format = "json"
)

print("Raw DynamicFrame count:", raw_dynamicframe.count())
print("Raw DynamicFrame schema:")
raw_dynamicframe.printSchema()

# Convert to DataFrame for processing
df = raw_dynamicframe.toDF()

# Extract fields with null handling for missing columns
df_flat = df.select(
    # Location fields
    col("location.name").alias("city"),
    col("location.region").alias("region"), 
    col("location.country").alias("country"),
    col("location.lat").alias("latitude"),
    col("location.lon").alias("longitude"),
    
    # Current weather fields
    col("current.temp_c").alias("temperature_c"),
    col("current.temp_f").alias("temperature_f"),
    col("current.wind_kph").alias("wind_speed_kph"),
    col("current.wind_dir").alias("wind_direction"),
    col("current.pressure_mb").alias("pressure_mb"),
    col("current.humidity").alias("humidity"),
    col("current.precip_mm").alias("precipitation_mm"),
    
    # Optional fields (will be null if not present)
    col("current.feelslike_c").alias("feels_like_c"),
    col("current.visibility_km").alias("visibility_km"),
    col("current.uv").alias("uv_index"),
    col("current.air_quality.pm2_5").alias("pm2_5"),
    col("current.air_quality.pm10").alias("pm10")
)

print("Processed DataFrame schema:")
df_flat.printSchema()
print("Sample data:")
df_flat.show(10)

# Write as single CSV
df_flat.coalesce(1).write \
    .option("header", "true") \
    .mode("overwrite") \
    .csv(f"s3://{S3_BUCKET}/silver/")

print("Job completed successfully! Schema differences handled.")
job.commit()