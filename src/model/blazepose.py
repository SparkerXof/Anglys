import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
draw_landmarks = mp.tasks.vision.drawing_utils.draw_landmarks
POSE_LANDMARKS = mp.tasks.vision.PoseLandmarksConnections.POSE_LANDMARKS
NormalizedLandmark = mp.tasks.components.containers.NormalizedLandmark

LEGS_LANDMARKS = [11, 23, 25, 27, 29, 31, 12, 24, 26, 28, 30, 32]

class BlazePoseModel:
    def __init__(self, model_path: str, detection_confidence: float = 0.5):
        self.options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.VIDEO,
            num_poses=1,
            min_pose_detection_confidence=detection_confidence
        )
        self.landmarker = PoseLandmarker.create_from_options(self.options)
    def estimate(self, frame, frame_id: int, frametime: int, empty: bool):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        pose_landmarks = self.landmarker.detect_for_video(mp_image, frame_id*frametime).pose_landmarks
        pose = []
        if len(pose_landmarks) > 0:
            for p_id in LEGS_LANDMARKS:
                if pose_landmarks[0][p_id].visibility >= self.options.min_pose_detection_confidence or empty:
                    pose.append([pose_landmarks[0][p_id].x, pose_landmarks[0][p_id].y, pose_landmarks[0][p_id].z])
                else:
                    pose.append([])
        else:
            return None
        return pose