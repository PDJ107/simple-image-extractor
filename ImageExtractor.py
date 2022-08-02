import os
import argparse
#from rembg.bg import remove
import cv2
from pathlib import Path
from PIL import Image
import tempfile

class ImageExtractor: 

    def __init__(self) -> None:
        self.video = None
        self.tf = None

    def load_video_from_path(self, video_path: str = "./video/test.mp4"):
        self.video = cv2.VideoCapture(video_path)
        self.load_video_info()

    def load_video_from_tempfile(self, file):
        tf = tempfile.NamedTemporaryFile(delete=True)
        tf.write(file.read())
        tf.seek(0)
        self.video = cv2.VideoCapture(tf.name)
        self.load_video_info()
        self.tf = tf

    def load_video_info(self):
        self.total_frame = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

        self.s = int(self.total_frame / self.fps)
        self.m = int(self.s / 60)
        self.h = int(self.m / 60)

    def extract(self, extract_num: int = 10, save_path: str = "./result", remove_bg: bool = False) -> None:
        assert self.video != None

        if int(self.video.get(1)) != 0: self.video.set(1, 0)

        count = 0
        extract_frame = int(self.total_frame / extract_num)

        while(self.video.isOpened()):
            ret, frame = self.video.read()
            if not ret: break
            if(int(self.video.get(1)) % extract_frame == 0):

                #if remove_bg: frame = remove(frame)

                cv2.imwrite(os.path.join(save_path, f"{count}.jpg"), frame)

                print('Saved frame :', str(int(self.video.get(1))))
                count += 1

    def convert_webp(self, save_path: str):
        for target in os.listdir(save_path):
            image_path = os.path.join(save_path, target)
            self.image_to_webp(Path(image_path))

    def image_to_webp(self, image_path: str):
        result_path = image_path.with_suffix(".webp")

        image = Image.open(image_path)  # Open image
        image.save(result_path, format="webp")  # Convert image to webp

    def __str__(self) -> str:
        assert self.video != None
        return f"\nVideo Path : {self.video_path}\n" \
            + f"Total Frame : {self.total_frame}\n" \
            + f"Width :       {self.width}\n" \
            + f"Height :      {self.height}\n" \
            + f"Fps :         {self.fps}\n" \
            + f"Length :      {self.h}h {self.m}m {self.s}s\n"
        
    def release(self) -> None:
        self.video.release()
        if self.tf != None: self.tf.close()

def main(args: argparse):
    extractor = ImageExtractor()
    extractor.load_video_from_path(args.video_path)
    print(("="*100) + str(extractor) + ("="*100))

    # 추출
    extractor.extract(args.extract_num, args.save_path, args.remove_bg)
    extractor.convert_webp(args.save_path)
    extractor.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract images from video")
    parser.add_argument(
        "--video_path",
        default="./video/test.mp4",
        type=str
    )
    parser.add_argument(
        "--save_path",
        default="./result",
        type=str
    )
    parser.add_argument(
        "--extract_num",
        default=10,
        type=int
    )
    parser.add_argument(
        "--remove_bg",
        default=False, 
        type=bool
    )
    args = parser.parse_args()

    if not os.path.exists("video"): os.makedirs("video")
    if not os.path.exists("result"): os.makedirs("result")

    main(args)