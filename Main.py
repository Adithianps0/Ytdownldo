import os
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import gradio as gr

def download_and_trim_youtube_video(url, start_time=0, end_time=None):
    try:
        # Download the video
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_path = stream.download(filename="downloaded_video.mp4")

        # Load and trim the video
        clip = VideoFileClip(video_path)
        if end_time:
            clip = clip.subclip(start_time, end_time)

        # Save the trimmed video
        output_path = "trimmed_video.mp4"
        clip.write_videofile(output_path, codec="libx264")

        return output_path
    except Exception as e:
        return str(e)

with gr.Blocks() as demo:
    gr.Markdown("## YouTube Video Downloader and Editor")

    url_input = gr.Textbox(label="YouTube Video URL")
    start_time_input = gr.Number(label="Start Time (in seconds)", value=0)
    end_time_input = gr.Number(label="End Time (in seconds, optional)", value=None)
    
    download_btn = gr.Button("Download & Trim")
    download_link = gr.File(label="Download Your Video")

    def process_video(url, start_time, end_time):
        video_path = download_and_trim_youtube_video(url, start_time, end_time)
        return video_path if os.path.isfile(video_path) else None

    download_btn.click(process_video, inputs=[url_input, start_time_input, end_time_input], outputs=download_link)

demo.launch(share=True)
