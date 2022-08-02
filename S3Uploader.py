import time

from pydantic import BaseSettings
import boto3
import io
from time import strftime

class Settings(BaseSettings):
    APP_ENV: str = 'dev'
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str
    AWS_S3_BUCKET_NAME: str
    class Config:
        env_file = 'config.env'

settings = Settings()

class S3Uploader:
    def __init__(self):
        self.s3 = boto3.resource(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket = self.s3.Bucket(settings.AWS_S3_BUCKET_NAME)

    def upload_images(self, user_id, images):

        prefix = f"{user_id}/{strftime('%Y%m%d%I%M%S', time.localtime())}"
        for i, image in enumerate(images):
            image_name = f"{prefix}/{i}.jpg"

            in_mem_file = io.BytesIO()
            image.convert("RGB").save(in_mem_file, format="jpeg")
            in_mem_file.seek(0)

            self.bucket.put_object(Body=in_mem_file, Key=image_name)

        return prefix

