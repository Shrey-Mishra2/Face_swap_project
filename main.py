import gradio as gr
import cv2
import os
import subprocess
from insightface.app import FaceAnalysis
from insightface.model_zoo import model_zoo

FFMPEG_PATH = r"C:\Users\Sarang Mishra\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"

# Load models once
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0, det_size=(640, 640))
swapper = model_zoo.get_model("weights/inswapper_128.onnx")


# -------------------------
# IMAGE ➜ IMAGE
# -------------------------
def swap_image(source_path, target_path):

    source_img = cv2.imread(source_path)
    target_img = cv2.imread(target_path)

    source_face = app.get(source_img)[0]
    faces = app.get(target_img)

    for face in faces:
        target_img = swapper.get(target_img, face, source_face, paste_back=True)

    output_path = "image_result.jpg"
    cv2.imwrite(output_path, target_img)

    return output_path


# -------------------------
# IMAGE ➜ VIDEO
# -------------------------
def swap_video(source_path, video_path):

    source_img = cv2.imread(source_path)
    source_face = app.get(source_img)[0]

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    temp_video = "temp_no_audio.mp4"
    final_video = "final_output.mp4"

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = app.get(frame)

        for face in faces:
            frame = swapper.get(frame, face, source_face, paste_back=True)

        out.write(frame)

    cap.release()
    out.release()

    # Proper browser encoding
    subprocess.run([
        FFMPEG_PATH,
        "-y",
        "-i", temp_video,
        "-i", video_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-map", "0:v:0",
        "-map", "1:a:0?",
        final_video
    ])

    os.remove(temp_video)

    return final_video


# -------------------------
# UI
# -------------------------

with gr.Blocks() as demo:
    gr.Markdown("#AI Face Swap Studio")

    with gr.Tab("Image ➜ Image"):
        src1 = gr.Image(label="Source Face", type="filepath")
        tgt1 = gr.Image(label="Target Image", type="filepath")
        out1 = gr.Image(label="Result")
        btn1 = gr.Button("Swap Image")
        btn1.click(swap_image, [src1, tgt1], out1)

    with gr.Tab("Image ➜ Video"):
        src2 = gr.Image(label="Source Face", type="filepath")
        vid2 = gr.Video(label="Target Video")
        out2 = gr.Video(label="Result Video")
        btn2 = gr.Button("Swap Video")
        btn2.click(swap_video, [src2, vid2], out2)

demo.launch()