from pipeline.video import VideoInput
from pipeline.hpe import HumanPoseEstimation
from pipeline.postprocess import PostProcess
from pipeline.angle import Angles
from pipeline.params import KeyParameters
from pipeline.output import Output
import cv2 as cv
import os, sys

def main(video_input: str, model_path: str, video_output: str = "output.avi", pdf_output: str = "anglys_plots.pdf"):
    video = VideoInput(video_input, video_output)
    hpe = HumanPoseEstimation(model_path)
    postprocess = PostProcess()
    angles = Angles()
    parameters = KeyParameters()
    output = Output()

    video.write_data()
    raw_pose_timeline = hpe.run(video)
    filtered_pose_timeline = postprocess.run_3d(raw_pose_timeline, video.frametime)
    angles_timeline = angles.run(filtered_pose_timeline)
    velocity_timeline = parameters.get_velocities(angles_timeline, video.framerate)
    left_leg_phases, left_leg_velocity_phases, right_leg_phases, right_leg_velocity_phases = parameters.split_to_phases(angles_timeline, velocity_timeline, video.framerate)
    output.run(raw_pose_timeline, filtered_pose_timeline, 
                left_leg_phases, right_leg_phases, angles_timeline, 
                left_leg_velocity_phases, right_leg_velocity_phases, 
                video, pdf_output)

    video.cap.release()

def help():
    print("""
Usage: python anglys.py [options] -i <input> -m <model_path>

Options:
    -i   Input video file
    -m   BlazePose-based model path
    -o   Output video file
    -p   Output PDF file of graphs
    -h   Write help text
    """)

if __name__ == '__main__':
    if (not '-i' in sys.argv) or (not '-m' in sys.argv) or ('-h' in sys.argv):
        help()
    else:
        video_input = sys.argv[sys.argv.index('-i')+1]
        model_path = sys.argv[sys.argv.index('-m')+1]
        video_output = sys.argv[sys.argv.index('-o')+1] if '-o' in sys.argv else "output.avi"
        pdf_output = sys.argv[sys.argv.index('-p')+1] if '-p' in sys.argv else "anglys_plots.pdf"
        main(video_input=video_input, model_path=model_path, video_output=video_output, pdf_output=pdf_output)