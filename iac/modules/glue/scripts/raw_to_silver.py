import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME','S3_BUCKET_NAME'])
S3_BUCKET = args['S3_BUCKET_NAME']

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from Raw S3 layer
raw_dynamicframe = glueContext.create_dynamic_frame.from_options(
    connection_type = "s3",
    connection_options = {"paths": [f"s3://{S3_BUCKET}/raw/"]},
    format = "csv"
)

# Convert to Spark DataFrame for processing
df = raw_dynamicframe.toDF()

# YOUR MAIN LOGIC GOES HERE
# Data cleaning, deduplication, null handling, transformations
df.show()

# Convert back to DynamicFrame
cleaned_dynamicframe = DynamicFrame.fromDF(df, glueContext, "cleaned_dynamicframe")

# Write to Silver S3 layer
glueContext.write_dynamic_frame.from_options(
    frame = cleaned_dynamicframe,
    connection_type = "s3",
    connection_options = {"path": f"s3://{S3_BUCKET}/silver/"},
    format = "parquet"
)

job.commit()