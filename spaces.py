import os
from boto3 import session

# Initiate session
session = session.Session()
client = session.client('s3',
                        region_name='nyc3',
                        endpoint_url="https://nyc3.digitaloceanspaces.com",
                        aws_access_key_id=os.environ.get("SPACES_ACCESS_ID"),
                        aws_secret_access_key=os.environ.get("SPACES_SECRET_KEY"))

