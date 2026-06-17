import numpy as np

class Angles:
    def scalar(self, a, b):
        if len(a) == len(b):
            return np.dot(a, b)
    def length(self, a):
        return np.linalg.norm(a)
    def angle_between(self, v1, v2):
        cos_angle = self.scalar(v1, v2) / (self.length(v1) * self.length(v2) + 1e-8)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        return np.arccos(cos_angle)
    def get_2d_vector(self, p1, p2):
        return np.array([p2[0] - p1[0], p2[1] - p1[1]])
    def joint_angle(self, p_prev, p_center, p_next):
        v1 = self.get_2d_vector(p_center, p_prev)
        v2 = self.get_2d_vector(p_center, p_next)
        angle = self.angle_between(v1, v2)
        cross = v1[0] * v2[1] - v1[1] * v2[0]
        
        return angle if cross >= 0 else -angle

    def calc_angles(self, p):
        torso_up = self.get_2d_vector(p[0], p[1])
        thigh = self.get_2d_vector(p[1], p[2])
        hip_angle = self.angle_between(torso_up, thigh)
        cross = torso_up[0]*thigh[1] - torso_up[1]*thigh[0]
        hip_angle = hip_angle*np.sign(cross)

        thigh_vec = self.get_2d_vector(p[2], p[1])
        shin_vec = self.get_2d_vector(p[3], p[2])
        knee_angle = self.angle_between(thigh_vec, shin_vec)

        shin_vec = self.get_2d_vector(p[3], p[2])
        shin_vec = shin_vec / self.length(shin_vec)
        foot_vec = self.get_2d_vector(p[5], p[4])
        foot_len = self.length(foot_vec)
        foot_dir = foot_vec / foot_len
        perp_to_shin = np.array([-shin_vec[1], shin_vec[0]])
        foot_proj = self.scalar(foot_dir, perp_to_shin)
        foot_vert = self.scalar(foot_dir, shin_vec)
        ankle_angle = np.arctan2(foot_vert, foot_proj)
        
        return [hip_angle, knee_angle, ankle_angle]

    def run(self, points_timeline):
        angles_timeline = []
        for P in points_timeline:
            left = self.calc_angles(P[:6])
            right = self.calc_angles(P[6:])
            angles_timeline.append(np.concatenate((left, right), axis=None))
        return angles_timeline

