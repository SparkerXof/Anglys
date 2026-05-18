import numpy as np

class Angles:
    def scalar(self, a, b):
        return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
    def lenght(self, a):
        return np.sqrt(a[0]*a[0] + a[1]*a[1] + a[2]*a[2])
    def run(self, points_timeline):
        angles_timeline = []
        for P in points_timeline:
            V = [
                np.subtract(P[1], P[0]) if (len(P[0]) > 0 and len(P[1]) > 0) else [],
                np.subtract(P[2], P[1]) if (len(P[1]) > 0 and len(P[2]) > 0) else [],
                np.subtract(P[3], P[2]) if (len(P[2]) > 0 and len(P[3]) > 0) else [],
                np.subtract(P[5], P[4]) if (len(P[4]) > 0 and len(P[5]) > 0) else [],
                np.subtract(P[7], P[6]) if (len(P[6]) > 0 and len(P[7]) > 0) else [],
                np.subtract(P[8], P[7]) if (len(P[7]) > 0 and len(P[8]) > 0) else [],
                np.subtract(P[9], P[8]) if (len(P[8]) > 0 and len(P[9]) > 0) else [],
                np.subtract(P[10], P[11]) if (len(P[10]) > 0 and len(P[11]) > 0) else [],
            ]
            angles = [
                np.arccos((self.scalar(V[0], V[1]))/(self.lenght(V[0])*self.lenght(V[1]))) if (len(V[0]) > 0 and len(V[1]) > 0) else None,
                np.arccos((self.scalar(V[1], V[2]))/(self.lenght(V[1])*self.lenght(V[2]))) if (len(V[1]) > 0 and len(V[2]) > 0) else None,
                np.arccos((self.scalar(V[2], V[3]))/(self.lenght(V[2])*self.lenght(V[3])))+(np.pi/2) if (len(V[2]) > 0 and len(V[3]) > 0) else None,
                np.arccos((self.scalar(V[4], V[5]))/(self.lenght(V[4])*self.lenght(V[5]))) if (len(V[4]) > 0 and len(V[5]) > 0) else None,
                np.arccos((self.scalar(V[5], V[6]))/(self.lenght(V[5])*self.lenght(V[6]))) if (len(V[5]) > 0 and len(V[6]) > 0) else None,
                np.arccos((self.scalar(V[6], V[7]))/(self.lenght(V[6])*self.lenght(V[7])))+(np.pi/2) if (len(V[6]) > 0 and len(V[7]) > 0) else None,
            ]
            angles_timeline.append(angles)
        return angles_timeline

