import boto3
import logging

def create_glue_crawler(crawler_name, role, database_name, s3_target_path):
    """
    Create a Glue crawler to catalog files in an S3 bucket

    :param crawler_name: Name of the Glue crawler
    :param role: IAM role for the crawler
    :param database_name: Glue database to store the metadata
    :param s3_target_path: S3 path for the crawler to target
    """
    glue_client = boto3.client('glue')
    try:
        response = glue_client.create_crawler(
            Name=crawler_name,
            Role=role,
            DatabaseName=database_name,
            Targets={
                'S3Targets': [{'Path': s3_target_path}]
            }
        )
        return response
    except boto3.exceptions.ClientError as e:
        logging.error(e)
        return None

def start_glue_crawler(crawler_name):
    """
    Start a Glue crawler

    :param crawler_name: Name of the Glue crawler
    """
    glue_client = boto3.client('glue')
    try:
        response = glue_client.start_crawler(Name=crawler_name)
        return response
    except boto3.exceptions.ClientError as e:
        logging.error(e)
        return None
