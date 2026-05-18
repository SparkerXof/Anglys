import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

KEYPOINTS_NAMES = ["Левая нога. Тазобедренный сустав", 
                    "Левая нога. Коленный сустав", 
                    "Левая нога. Голеностопный сустав", 
                    "Правая нога. Тазобедренный сустав", 
                    "Правая нога. Коленный сустав", 
                    "Правая нога. Голеностопный сустав",]

class Output:
    def run(self, raw_pose_timeline, raw_angles_timeline, filtered_pose_timeline, filtered_angles_timeline, video, pdf_output):
        print("=== Estimation output ===")
        timeline_lenght = len(filtered_angles_timeline)
        print("Processed frames:", timeline_lenght)
        

        filtered_timelines = np.array(filtered_angles_timeline).T
        raw_timelines = np.array(raw_angles_timeline).T

        with PdfPages(pdf_output) as pdf:
            idx = 0
            for raw_timeline, filtered_timeline in zip(raw_timelines, filtered_timelines):
                plt.figure()
                for i in range(len(raw_timeline)):
                    if raw_timeline[i] != None:
                        raw_timeline[i] = np.rad2deg(raw_timeline[i])
                plt.plot(raw_timeline, color='r', linestyle='--')
                plt.plot(np.rad2deg(filtered_timeline), color='g')
                plt.xlim(0)
                plt.xlabel("Кадры, N")
                plt.ylim(0, 180)
                plt.ylabel("Угол сгибания, °")
                plt.title(KEYPOINTS_NAMES[idx])
                pdf.savefig()
                plt.close()
                idx += 1
        
        i = 0
        estimation_start = video.total_frames-timeline_lenght
        video.cap = cv.VideoCapture(video.filepath)
        while True:
            ret, frame = video.cap.read()
            if not ret:
                break
            if i > estimation_start:
                for j in range(len(filtered_pose_timeline[0])):
                    cv.circle(frame, (int(video.resolution[0]*filtered_pose_timeline[i-estimation_start][j][0]), int(video.resolution[1]*filtered_pose_timeline[i-estimation_start][j][1])), 5, (0,255,0), -1)
                    if len(raw_pose_timeline[i-estimation_start][j]) > 0:
                        cv.circle(frame, (int(video.resolution[0]*raw_pose_timeline[i-estimation_start][j][0]), int(video.resolution[1]*raw_pose_timeline[i-estimation_start][j][1])), 5, (0,0,255), -1)
                for idx, j in enumerate([1, 2, 3, 7, 8, 9]):
                    cv.putText(frame, str(np.rad2deg(filtered_angles_timeline[i-estimation_start][idx])), (int(video.resolution[0]*filtered_pose_timeline[i-estimation_start][j][0]), int(video.resolution[1]*filtered_pose_timeline[i-estimation_start][j][1])), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA)
            video.output.write(frame)
            i += 1