import cv2 as cv

class VideoInput:
    """
    Storing video file and its data
    filepath - path to input video
    """
    def __init__(self, filepath: str, out: str = 'output.avi'):
        self.filepath = filepath
        self.cap = cv.VideoCapture(filepath)
        self.framerate = int(self.cap.get(cv.CAP_PROP_FPS))
        self.frametime = int((1/self.framerate)*1000)
        self.total_frames = int(self.cap.get(cv.CAP_PROP_FRAME_COUNT))
        self.resolution = (int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
        self.output = cv.VideoWriter(out, cv.VideoWriter_fourcc(*"XVID"), 25.0, self.resolution)
    def write_data(self):
        print("=== Input video data ===")
        print(f"Resolution: {self.resolution}")
        print(f"FPS: {self.framerate}")
        print(f"Total frames count: {self.total_frames}\n")