AI Face Swap Studio

A face-swapping application built with InsightFace, ONNX Runtime, and Gradio, supporting both image-to-image and image-to-video face swaps through a simple web interface.

Features
Swap a source face onto a target image
Swap a source face onto every face detected in a target video
Web-based UI powered by Gradio — no command-line arguments needed
Uses buffalo_l for face detection/analysis and inswapper_128 for face swapping
Tech Stack
Python
InsightFace (FaceAnalysis, model_zoo) — face detection and swapping
OpenCV — image/video I/O and processing
ONNX Runtime — model inference
Gradio — web interface
FFmpeg — video encoding/processing

Setup
1. Clone the repo
bash
git clone https://github.com/<your-username>/face-swap-studio.git
cd face-swap-studio
2. Install dependencies
bash
pip install -r requirements.txt
3. Download the model weight

This project uses the InSwapper 128 face-swap model (inswapper_128.onnx, ~530MB). It is not included in this repository due to GitHub's file size limits.

Download it from Hugging Face: 👉 https://huggingface.co/ezioruan/inswapper_128.onnx/tree/main

Place the downloaded file in the weights/ folder:

face-swap-studio/
└── weights/
    └── inswapper_128.onnx
4. Set your FFmpeg path

Update the FFMPEG_PATH variable in main.py to point to your local FFmpeg installation.

5. Run the app
bash
python main.py

This launches a local Gradio interface where you can upload a source face and a target image/video.

How It Works
Face detection — FaceAnalysis (buffalo_l) detects and analyzes faces in both the source and target inputs.
Face swapping — the inswapper_128 ONNX model swaps the source face onto each detected face in the target.
Output — the result is written back out as an image (image_result.jpg) or a processed video file.
Project Structure
face-swap-studio/
├── main.py              # Core swap logic + Gradio interface
├── requirements.txt      # Python dependencies
├── weights/              # Model weights (download separately, see Setup)
├── images/               # Sample/input images
├── videos/                # Sample/output videos
└── README.md
Ethical Use

This project is intended for educational and research purposes — exploring computer vision and face-analysis pipelines. Face-swapping technology can be misused to create misleading or non-consensual media. Please:

Only use this tool with images/videos you have the right to use
Do not use it to impersonate real people without their consent
Do not use it to create misleading, harmful, or defamatory content
Acknowledgements
InsightFace for the face analysis and swapping models
inswapper_128 weights hosted on Hugging Face