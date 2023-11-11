from pytube import YouTube
import cv2
import os
import matplotlib.pyplot as plt


def download_youtube_video(video_url, output_path, new_filename):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the highest resolution stream
        video_stream = yt.streams.get_highest_resolution()

        # Download the video with the specified filename
        video_stream.download(output_path, filename=new_filename)

        print(
            f"Video downloaded successfully to: {os.path.join(output_path, new_filename)}")
    except Exception as e:
        print(f"Error: {e}")


def check_has_face(frame, cascPath):
    # Check if the XML file exists
    if not os.path.isfile(cascPath):
        print(f"Error: Cascade file not found at {cascPath}")
        return False

    # Create a CascadeClassifier
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Check if the CascadeClassifier was loaded successfully
    if faceCascade.empty():
        print(
            f"Error: CascadeClassifier not loaded successfully from {cascPath}")
        return False

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    print(f"Found {len(faces)} faces!")

    return len(faces) > 0

def extract_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Extract the filename without extension
    video_filename = os.path.splitext(os.path.basename(video_path))[0]

    # Create the output folder based on the video filename
    output_folder = os.path.join(output_folder, video_filename)
    os.makedirs(output_folder, exist_ok=True)

    # Get frames and save them to the output folder
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Save the frame as an image
        frame_filename = os.path.join(
            output_folder, f"frame_{frame_count:04d}.png")
        check_frame = check_has_face(frame, cascPath)
        if check_frame:
            cv2.imwrite(frame_filename, frame)

    # Release the video capture object
    cap.release()


global cascPath
cascPath = os.path.abspath('./haarcascade_frontalface_default.xml')

def main():
    # Replace with the actual video URL
    youtube_url = "https://www.youtube.com/watch?v=8wK1w3T2Rfo"
    output_folder = "./output"  # Change this to the desired output folder
    new_video_filename = "8wK1w3T2Rfo.mp4"  # Specify the new filename here

    # Download YouTube video with the new filename
    download_youtube_video(youtube_url, output_folder, new_video_filename)

    print("Start get frame video")
    # Extract frames from the downloaded video
    video_path = os.path.join(output_folder, new_video_filename)
    extract_frames(video_path, output_folder)

    # Optionally, delete the downloaded video
    os.remove(video_path)
    print(f"Downloaded video '{os.path.basename(video_path)}' deleted.")


if __name__ == "__main__":
    main()
