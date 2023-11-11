import cv2
import os

def extract_frames(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get frames and save them to the output folder
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Save the frame as an image
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, frame)

    # Release the video capture object
    cap.release()

if __name__ == "__main__":
    video_path = "./output/x7P4GxuM88A.mp4"  # Change this to the path of your video file
    output_folder = "./output/x7P4GxuM88A"  # Change this to the desired output folder

    extract_frames(video_path, output_folder)
