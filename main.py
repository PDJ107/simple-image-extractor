from fastapi import FastAPI, UploadFile, status
from ImageExtractor import ImageExtractor
from S3Uploader import S3Uploader

app = FastAPI()
extractor = ImageExtractor()
S3Uploader = S3Uploader()

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
    extractor.load_video_from_tempfile(file.file)
    images = extractor.extract(extract_num=10, save_local=False)
    s3_endpoint = S3Uploader.upload_images(0, images)
    extractor.release()
    return {"user_id": 0, "s3_endpoint": s3_endpoint}