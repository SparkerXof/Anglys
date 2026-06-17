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
        raw_results = []
        empty = True
        start = 0
        for i in tqdm(range(video.total_frames)):
            ret, frame = video.cap.read()
            if not ret:
                break
            pose, raw_pose = self.model.estimate(frame, i, video.frametime, empty)
            if pose:
                if empty:
                    start = i
                    result = []
                    raw_results = []
                result.append(pose)
                raw_results.append(raw_pose)
                empty = False
            else:
                empty = True
        print("Processed frames:", len(result))
        return start, result, raw_results
