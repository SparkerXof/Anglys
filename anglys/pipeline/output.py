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
    def run(self, raw_pose_timeline, filtered_pose_timeline, 
            left_leg_phases, right_leg_phases, angles_timeline, 
            left_leg_velocity_phases, right_leg_velocity_phases, start,
            bad_left_leg_phases, bad_right_leg_phases,
            video, pdf_output):
        print("=== Estimation output ===")
        timeline_lenght = len(filtered_pose_timeline)

        with PdfPages(pdf_output) as pdf:
            idx = 0
            for phase, bad_phase, velocity in zip(left_leg_phases, bad_left_leg_phases, left_leg_velocity_phases):
                plt.figure()
                fig, ax = plt.subplots(1, 2)
                avg_phase = np.mean(phase, axis=0)
                avg_bad_phase = np.mean(bad_phase, axis=0)
                ax[0].plot(np.linspace(0, 100, 100), np.rad2deg(avg_phase), color='g', label='Сглаженные углы')
                ax[0].plot(np.linspace(0, 100, 100), np.rad2deg(avg_bad_phase), color='red', linewidth=0.5, linestyle='--', label='Сырые углы')
                ax[0].plot(np.linspace(0, 100, 100), [0]*100, color='gray', linewidth=0.5, linestyle='--')
                ax[0].set_xlim(0, 100)
                ax[0].set_xlabel("Цикл ходьбы, %")
                ax[0].set_ylabel("Угол сгибания, °")
                ax[0].legend()
                avg_velocity = np.mean(velocity, axis=0)
                ax[1].plot(np.linspace(0, 100, 100), np.rad2deg(avg_velocity), color='b')
                ax[1].plot(np.linspace(0, 100, 100), [0]*100, color='gray', linewidth=0.5, linestyle='--')
                ax[1].set_xlim(0, 100)
                ax[1].set_xlabel("Цикл ходьбы, %")
                ax[1].set_ylabel("Угловая скорость, °/с")
                fig.suptitle(KEYPOINTS_NAMES[idx])
                fig.set_figwidth(12)
                fig.set_figheight(6)
                pdf.savefig()
                plt.close()
                idx += 1
            for phase, bad_phase, velocity in zip(right_leg_phases, bad_right_leg_phases, right_leg_velocity_phases):
                plt.figure()
                fig, ax = plt.subplots(1, 2)
                avg_phase = np.mean(phase, axis=0)
                avg_bad_phase = np.mean(bad_phase, axis=0)
                ax[0].plot(np.linspace(0, 100, 100), np.rad2deg(avg_phase), color='g', label='Сглаженные углы')
                ax[0].plot(np.linspace(0, 100, 100), np.rad2deg(avg_bad_phase), color='red', linewidth=0.5, linestyle='--', label='Сырые углы')
                ax[0].plot(np.linspace(0, 100, 100), [0]*100, color='gray', linewidth=0.5, linestyle='--')
                ax[0].set_xlim(0, 100)
                ax[0].set_xlabel("Цикл ходьбы, %")
                ax[0].set_ylabel("Угол сгибания, °")
                ax[0].legend()
                avg_velocity = np.mean(velocity, axis=0)
                ax[1].plot(np.linspace(0, 100, 100), np.rad2deg(avg_velocity), color='b')
                ax[1].plot(np.linspace(0, 100, 100), [0]*100, color='gray', linewidth=0.5, linestyle='--')
                ax[1].set_xlim(0, 100)
                ax[1].set_xlabel("Цикл ходьбы, %")
                ax[1].set_ylabel("Угловая скорость, °/с")
                fig.suptitle(KEYPOINTS_NAMES[idx])
                fig.set_figwidth(12)
                fig.set_figheight(6)
                pdf.savefig()
                plt.close()
                idx += 1
        
        i = 0
        estimation_start = start
        estimation_end = estimation_start+len(angles_timeline)
        video.cap = cv.VideoCapture(video.filepath)
        while True:
            ret, frame = video.cap.read()
            if not ret:
                break
            if i > estimation_start and i < estimation_end:
                for j in range(len(filtered_pose_timeline[0])):
                    cv.circle(frame, (int(video.resolution[0]*filtered_pose_timeline[i-estimation_start][j][0]), int(video.resolution[1]*filtered_pose_timeline[i-estimation_start][j][1])), 5, (0,255,0), -1)
                for idx, j in enumerate([1, 2, 3, 7, 8, 9]):
                    cv.putText(frame, str(np.round(np.rad2deg(angles_timeline[i-estimation_start][idx]), 2)), (int(video.resolution[0]*filtered_pose_timeline[i-estimation_start][j][0]), int(video.resolution[1]*filtered_pose_timeline[i-estimation_start][j][1])), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv.LINE_AA)
            video.output.write(frame)
            i += 1
        with PdfPages("test_1.pdf") as pdf:
            timeline = np.array(angles_timeline).T
            plt.figure()
            plt.plot(timeline[3], color='g')
            pdf.savefig()
            plt.close()
            plt.figure()
            plt.plot(timeline[3], color='g')
            pdf.savefig()
            plt.close()
