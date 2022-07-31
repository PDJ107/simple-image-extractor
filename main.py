from fastapi import FastAPI
from ImageExtractor import ImageExtractor
from pydantic import BaseSettings
import boto3

class Settings(BaseSettings):
    APP_ENV: str = 'dev'
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str
    AWS_QUEUE_NAME: str
    class Config:
        env_file = 'config.env'

settings = Settings()
sqs = boto3.resource(
    'sqs',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION
)
app = FastAPI()
extractor = ImageExtractor()

# Create the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName=settings.AWS_QUEUE_NAME)

@app.get("/")
def root():
    # You can now access identifiers and attributes
    print(queue.url)
    print(queue.attributes.get('DelaySeconds'))

    return {"message": "Hello"}

