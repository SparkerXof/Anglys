from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import numpy as np

class PostProcess:
    def init_kalman_filter(self, start_point, frametime: float):
        kf = KalmanFilter(dim_x=6, dim_z=3)
        first = np.array(start_point)
        kf.x = np.array([first[0], first[1], first[2], 0., 0., 0.])
        dt = frametime/1000
        kf.F = np.array([[1, 0, 0, dt, 0, 0],
                         [0, 1, 0, 0, dt, 0],
                         [0, 0, 1, 0, 0, dt],
                         [0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 0, 1]])
        kf.H = np.array([[1, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0]])
        kf.R = np.eye(3) * 0.1
        q_var = 5
        q_pos = Q_discrete_white_noise(dim=2, dt=dt, var=q_var)
        kf.Q = np.eye(6)
        kf.Q[0:2, 0:2] = q_pos
        kf.Q[2:4, 2:4] = q_pos
        kf.Q[4:6, 4:6] = q_pos
        kf.P = np.eye(6) * 10
        kf.P[3:, 3:] *= 1000

        return kf
    def run(self, pose_timeline, frametime: float):
        print("\n=== Postprocessing 3D points ===")
        filtered_pose_timeline = [[None for i in range(len(pose_timeline[0]))] for i in range(len(pose_timeline))]
        for i in range(len(pose_timeline[0])):
            kf = self.init_kalman_filter(pose_timeline[0][i], frametime)
            filtered_pose_timeline[0][i] = pose_timeline[0][i]
            for j in range(1, len(pose_timeline)):
                new_point = np.array(pose_timeline[j][i])
                kf.predict()
                if len(new_point) == 3:
                    kf.update(new_point)
                filtered_pose_timeline[j][i] = np.array(kf.x[:3].copy())
        return filtered_pose_timeline