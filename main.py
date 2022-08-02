from fastapi import FastAPI, UploadFile, status
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

app = FastAPI()
extractor = ImageExtractor()

# sqs = boto3.resource(
#     'sqs',
#     aws_access_key_id=settings.AWS_ACCESS_KEY,
#     aws_secret_access_key=settings.AWS_SECRET_KEY,
#     region_name=settings.AWS_REGION
# )
#
# queue = sqs.get_queue_by_name(QueueName=settings.AWS_QUEUE_NAME)



@app.get("/")
def root():
    return {"message": "Hello"}

@app.post("/upload/", status_code=status.HTTP_200_OK)
async def upload_video_file(file: UploadFile):

    return {"user_id": 0, "3d_item_id": 0}