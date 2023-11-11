from pytube import YouTube
import cv2 #opencv 4.6.0
import os

def download_youtube_video(video_url, output_path, new_filename):
    try:
        yt = YouTube(video_url)
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path, filename=new_filename)

        print(f"Video downloaded successfully to: {os.path.join(output_path, new_filename)}")
    except Exception as e:
        print(f"Error: {e}")

def check_has_face(frame, cascade_classifier):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    print(f"Found {len(faces)} faces!")
    return len(faces) > 0

def extract_frames(video_path, output_folder, cascade_classifier):
    cap = cv2.VideoCapture(video_path)

    video_filename = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = os.path.join(output_folder, video_filename)
    os.makedirs(output_folder, exist_ok=True)

    frame_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")

            if check_has_face(frame, cascade_classifier):
                cv2.imwrite(frame_filename, frame)
    finally:
        cap.release()

def main():
    youtube_url = "https://www.youtube.com/watch?v=8wK1w3T2Rfo"
    output_folder = "./output"
    new_video_filename = "8wK1w3T2Rfo.mp4"

    cascPath = os.path.abspath('./haarcascade_frontalface_default.xml')
    cascade_classifier = cv2.CascadeClassifier(cascPath)

    try:
        download_youtube_video(youtube_url, output_folder, new_video_filename)
        print("Start extracting frames from the video.")
        video_path = os.path.join(output_folder, new_video_filename)
        extract_frames(video_path, output_folder, cascade_classifier)
    finally:
        os.remove(video_path)
        print(f"Downloaded video '{os.path.basename(video_path)}' deleted.")

if __name__ == "__main__":
    main()
