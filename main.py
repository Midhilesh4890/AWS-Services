# main.py

from s3_utils import upload_file_to_s3
from glue_utils import create_glue_crawler, start_glue_crawler

# Parameters
file_name = 'path/to/your/file.csv'
bucket_name = 'your-bucket-name'
crawler_name = 'your-crawler-name'
iam_role = 'arn:aws:iam::your-account-id:role/your-glue-role'
database_name = 'your-database-name'
s3_target_path = f's3://{bucket_name}/path/to/csv/'

# Upload CSV to S3
upload_success = upload_file_to_s3(file_name, bucket_name)
if upload_success:
    print("File uploaded successfully.")

# Create and start the Glue crawler
create_response = create_glue_crawler(crawler_name, iam_role, database_name, s3_target_path)
if create_response:
    print("Crawler created successfully.")
    start_response = start_glue_crawler(crawler_name)
    if start_response:
        print("Crawler started successfully.")
