import numpy as np

class Angles:
    def scalar(self, a, b):
        if len(a) == 3 and len(b) == 3:
            return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
        raise ValueError("Point is not 3d")
    def lenght(self, a):
        if len(a) == 3:
            return np.sqrt(a[0]*a[0] + a[1]*a[1] + a[2]*a[2])
        raise ValueError("Point is not 3d")
    def side(self, a, b):
        cross = np.cross(a, b)
        if cross[2] > 0:
            return 1
        return -1

    def run(self, points_timeline):
        angles_timeline = []
        for P in points_timeline:
            V = [
                np.subtract(P[1], P[0]),
                np.subtract(P[2], P[1]),
                np.subtract(P[3], P[2]),
                np.subtract(P[5], P[4]),
                np.subtract(P[7], P[6]),
                np.subtract(P[8], P[7]),
                np.subtract(P[9], P[8]),
                np.subtract(P[11], P[10])
            ]
            left_lat = np.cross(V[3], V[2])
            left_up_foot = np.cross(left_lat, V[3])
            right_lat = np.cross(V[7], V[6])
            right_up_foot = np.cross(right_lat, V[7])
            angles = [
                np.sign(V[3][0])*-1*self.side(V[0], V[1])*np.arccos((self.scalar(V[0], V[1]))/(self.lenght(V[0])*self.lenght(V[1]))),
                np.sign(V[3][0])*self.side(V[1], V[2])*np.arccos((self.scalar(V[1], V[2]))/(self.lenght(V[1])*self.lenght(V[2]))),
                np.sign(V[3][0])*-1*self.side(V[2], left_up_foot)*np.arccos((self.scalar(V[2], left_up_foot))/(self.lenght(V[2])*self.lenght(left_up_foot))),
                np.sign(V[3][0])*-1*self.side(V[4], V[5])*np.arccos((self.scalar(V[4], V[5]))/(self.lenght(V[4])*self.lenght(V[5]))),
                np.sign(V[3][0])*self.side(V[5], V[6])*np.arccos((self.scalar(V[5], V[6]))/(self.lenght(V[5])*self.lenght(V[6]))),
                np.sign(V[3][0])*-1*self.side(V[6], right_up_foot)*np.arccos((self.scalar(V[6], right_up_foot))/(self.lenght(V[6])*self.lenght(right_up_foot))),
            ]
            angles_timeline.append(angles)
        return angles_timeline

