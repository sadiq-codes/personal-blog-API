import os
import boto3

# Initiate S3 client

s3 = boto3.client(
               "s3",
               aws_access_key_id=os.environ.get("SPACES_ACCESS_ID"),
               aws_secret_access_key=os.environ.get("SPACES_SECRET_KEY")
)
