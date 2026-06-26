import numpy as np
from scipy.signal import find_peaks
from scipy import interpolate

DISTANCE = 20

class KeyParameters:
    def get_velocities(self, angles_timeline):
        velocity_timeline = [[0 for i in range(len(angles_timeline[0]))]]

        for i in range(len(angles_timeline)):
            timestamp = []
            for j in range(len(velocity_timeline[0])):
                if i == 0:
                    timestamp.append(0)
                else:
                    timestamp.append(angles_timeline[i][j]-angles_timeline[i-1][j])
            velocity_timeline.append(timestamp)
        return velocity_timeline
    
    def split_to_phases(self, angle_timeline, velocity_timeline, framerate):
        a_timeline = np.array(angle_timeline).T
        v_timeline = np.array(velocity_timeline).T

        left_leg_min_peaks, _ = find_peaks(a_timeline[0], distance=DISTANCE)
        left_leg_phases = []
        left_leg_velocity_phases = []
        for i in [0, 1, 2]:
            point_phase = []
            velocity_phase = []
            for j in range(1, len(left_leg_min_peaks)):
                if left_leg_min_peaks[j]-left_leg_min_peaks[j-1] < framerate*0.5:
                    continue
                a_line = a_timeline[i][left_leg_min_peaks[j-1]:left_leg_min_peaks[j]]
                v_line = v_timeline[i][left_leg_min_peaks[j-1]:left_leg_min_peaks[j]]
                arr_old = np.linspace(0, 1, len(a_line))
                arr_new = np.linspace(0, 1, 100)
                a_f = interpolate.interp1d(arr_old, a_line, kind='cubic')
                v_f = interpolate.interp1d(arr_old, v_line, kind='cubic')
                point_phase.append(a_f(arr_new))
                velocity_phase.append(v_f(arr_new))
            left_leg_phases.append(point_phase)
            left_leg_velocity_phases.append(velocity_phase)
        
        right_leg_min_peaks, _ = find_peaks(a_timeline[3], distance=DISTANCE)
        right_leg_phases = []
        right_leg_velocity_phases = []
        for i in [3, 4, 5]:
            point_phase = []
            for j in range(1, len(right_leg_min_peaks)):
                a_line = a_timeline[i][right_leg_min_peaks[j-1]:right_leg_min_peaks[j]]
                v_line = v_timeline[i][right_leg_min_peaks[j-1]:right_leg_min_peaks[j]]
                arr_old = np.linspace(0, 1, len(a_line))
                arr_new = np.linspace(0, 1, 100)
                a_f = interpolate.interp1d(arr_old, a_line, kind='cubic')
                v_f = interpolate.interp1d(arr_old, v_line, kind='cubic')
                point_phase.append(a_f(arr_new))
                velocity_phase.append(v_f(arr_new))
            right_leg_phases.append(point_phase)
            right_leg_velocity_phases.append(velocity_phase)
        
        return left_leg_phases, left_leg_velocity_phases, right_leg_phases, right_leg_velocity_phases
