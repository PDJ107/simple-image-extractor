import os, argparse
import cv2


class ImageExtractor: 

    def __init__(self, video_path):

        self.video = cv2.VideoCapture(video_path)
        self.video_path = video_path
        self.total_frame = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

        self.s = int(self.total_frame / self.fps)
        self.m = int(self.s / 60)
        self.h = int(self.m / 60)

    def extract(self, extract_num, save_path):
        
        if int(self.video.get(1)) != 0: self.video.set(1, 0)

        count = 0
        extract_frame = int(self.total_frame / extract_num)

        while(self.video.isOpened()):
            ret, frame = self.video.read()
            if not ret: break
            if(int(self.video.get(1)) % extract_frame == 0):
                
                cv2.imwrite(os.path.join(save_path, f"{count}.jpg"), frame)
                print('Saved frame :', str(int(self.video.get(1))))
                count += 1

    def __str__(self):
        return f"\nVideo Path : {self.video_path}\n" \
            + f"Total Frame : {self.total_frame}\n" \
            + f"Width :       {self.width}\n" \
            + f"Height :      {self.height}\n" \
            + f"Fps :         {self.fps}\n" \
            + f"Length :      {self.h}h {self.m}m {self.s}s\n"
        
    def release(self):
        self.video.release()

def main(args):
    extractor = ImageExtractor(args.video_path)
    print(("="*100) + str(extractor) + ("="*100))

    # 추출
    extractor.extract(args.extract_num, args.save_path)
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

    if not os.path.exists("./video"): os.makedirs("./video")
    if not os.path.exists("./result"): os.makedirs("./result")

    main(args)