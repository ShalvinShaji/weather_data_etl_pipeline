import json
import config
from datetime import datetime
import requests
import os
import boto3

SECRET_ARN = os.environ['SECRET_ARN']
S3_BUCKET = "weather-data-bucket-prod"  # Your bucket name

def lambda_handler(event, context):
    try:
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=SECRET_ARN)
        secret = json.loads(response['SecretString'])
        API_KEY = secret['access_key']
        API_BASE_URL = secret['api_url']
        
        s3_client = boto3.client('s3')
        current_time = datetime.now()
        
        for city in config.cities:
            API_URL = f"{API_BASE_URL}current.json?key={API_KEY}&q={city}&aqi=yes"
            data = requests.get(API_URL).json()
            
            # Create S3 path
            year = current_time.strftime("%Y")
            month = current_time.strftime("%m")
            day = current_time.strftime("%d")
            hour = current_time.strftime("%H")
            minute = current_time.strftime("%M")
            
            s3_key = f"raw/{year}/{month}/{day}/{hour}/{city}_{minute}.json"
            
            # Upload to S3
            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=json.dumps(data)
            )
            
        print(f"Weather data saved to S3 for {len(config.cities)} cities")
        
        return {
            'statusCode': 200,
            'cities_processed': len(config.cities),
            'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'error': str(e)
        }