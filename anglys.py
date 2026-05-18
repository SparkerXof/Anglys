from src.video import VideoInput
from src.hpe import HumanPoseEstimation
from src.postprocess import PostProcess
from src.angle import Angles
from src.output import Output
import os, sys

def main(video_input: str, model_path: str, video_output: str = "output.avi", pdf_output: str = "anglys_plots.pdf"):
    video = VideoInput(video_input, video_output)
    hpe = HumanPoseEstimation(model_path)
    postprocess = PostProcess()
    angles = Angles()
    output = Output()

    video.write_data()
    raw_pose_timeline = hpe.run(video)
    raw_angles_timeline = angles.run(raw_pose_timeline)
    filtered_pose_timeline = postprocess.run(raw_pose_timeline, video.frametime)
    filtered_angles_timeline = angles.run(filtered_pose_timeline)
    output.run(raw_pose_timeline, raw_angles_timeline, filtered_pose_timeline, filtered_angles_timeline, video, pdf_output)

    video.cap.release()

def help():
    print("""
Usage: python anglys.py [options] -i <input> -m <model_path>

Options:
    -i   Input video file
    -o   Output video file
    -p   Output PDF file of graphs
    -m   BlazePose-based model path
    -h   Write help text
    """)

if __name__ == '__main__':
    if (not '-i' in sys.argv) or (not '-m' in sys.argv) or ('-h' in sys.argv):
        help()
    else:
        video_input = sys.argv[sys.argv.index('-i')+1]
        model_path = sys.argv[sys.argv.index('-m')+1]
        video_output = sys.argv[sys.argv.index('-o')+1] if '-o' in sys.argv else "output.avi"
        pdf_output = sys.argv[sys.argv.index('-o')+1] if '-p' in sys.argv else "anglys_plots.pdf"
        main(video_input=video_input, model_path=model_path, video_output=video_output, pdf_output=pdf_output)
