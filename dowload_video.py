from pytube import YouTube

def download_youtube_video(video_url, output_path):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the highest resolution stream
        video_stream = yt.streams.get_highest_resolution()

        # Download the video
        video_stream.download(output_path)

        print(f"Video downloaded successfully to: {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=x7P4GxuM88A"  # Replace with the actual video URL
    output_path = "output"  # Change this to the desired output folder

    download_youtube_video(youtube_url, output_path)
