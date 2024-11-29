import os
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import gradio as gr

def download_youtube_video(url, start_time=0, end_time=None):
    try:
        # Download the video
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_path = stream.download(filename="downloaded_video.mp4")

        # Load the video
        clip = VideoFileClip(video_path)
        if end_time:
            clip = clip.subclip(start_time, end_time)

        # Save the trimmed video
        output_path = "trimmed_video.mp4"
        clip.write_videofile(output_path, codec="libx264")
        
        return output_path

    except Exception as e:
        return f"Error: {e}"

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## YouTube Video Downloader and Editor")

    url = gr.Textbox(label="YouTube Video URL")
    start_time = gr.Number(label="Start Time (in seconds)", value=0)
    end_time = gr.Number(label="End Time (in seconds, optional)", value=None)

    output_video = gr.Video(label="Trimmed Video")
    download_btn = gr.Button("Download & Trim")

    download_btn.click(download_youtube_video, inputs=[url, start_time, end_time], outputs=output_video)

demo.launch()
