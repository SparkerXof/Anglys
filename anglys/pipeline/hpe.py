import cv2 as cv
from pipeline.video import VideoInput
from pipeline.model.blazepose import BlazePoseModel
from tqdm import tqdm
import json


class HumanPoseEstimation:
    """
    BlazePose-based 3D human pose esimation
    """
    def __init__(self, model_path: str, detection_confidence: float = 0.5):
        self.model = BlazePoseModel(model_path, detection_confidence)
    def run(self, video: VideoInput):
        print("=== Estimating human pose on video ===")
        result = []
        for i in tqdm(range(video.total_frames)):
            ret, frame = video.cap.read()
            if not ret:
                break
            pose = self.model.estimate(frame, i, video.frametime, len(result) <= 0)
            if pose:
                result.append(pose)
            else:
                result = []
        print("Processed frames:", len(result))
        return result
