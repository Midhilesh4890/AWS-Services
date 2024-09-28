import boto3
import logging
import os
from dotenv import load_dotenv

load_dotenv('.env')  # Make sure this points to the correct .env file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


logging.info('Initializing S3 client')
# Initialize the S3 client using environment variables
s3_client = boto3.client(
    's3',
    region_name=os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

logging.info('Initialized S3 client')
def list_buckets():
    """ List all buckets in the S3 account """
    try:
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        logging.info(f"Listed {len(buckets)} buckets.")
        return buckets
    except Exception as e:
        logging.error(f"Failed to list buckets: {str(e)}")
        raise


def create_bucket(bucket_name):
    """ Create a bucket in S3 with appropriate region specification """
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': os.getenv('AWS_DEFAULT_REGION')}
        )
        logging.info(f"Bucket created: {bucket_name}")
    except Exception as e:
        logging.error(f"Failed to create bucket: {str(e)}")
        raise


def delete_bucket(bucket_name):
    """ Delete a bucket in S3 """
    try:
        # Delete all objects in the bucket first
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        for obj in response.get('Contents', []):
            s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
        s3_client.delete_bucket(Bucket=bucket_name)
        logging.info(f"Bucket deleted: {bucket_name}")
    except Exception as e:
        logging.error(f"Failed to delete bucket: {str(e)}")
        raise


def upload_file(bucket_name, file_path, key):
    """ Upload a file to an S3 bucket """
    try:
        with open(file_path, 'rb') as data:
            s3_client.upload_fileobj(data, bucket_name, key)
        logging.info(f"File uploaded: {key} to bucket: {bucket_name}")
    except Exception as e:
        logging.error(f"Failed to upload file: {str(e)}")
        raise


def delete_file(bucket_name, key):
    """ Delete a file from an S3 bucket """
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=key)
        logging.info(f"File deleted: {key} from bucket: {bucket_name}")
    except Exception as e:
        logging.error(f"Failed to delete file: {str(e)}")
        raise