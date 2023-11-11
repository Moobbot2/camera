import cv2
import os
import matplotlib.pyplot as plt

def check_has_face_image(imagePath, cascPath):
    # Check if the XML file exists
    if not os.path.isfile(cascPath):
        print(f"Error: Cascade file not found at {cascPath}")
        return

    # Create a CascadeClassifier
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Check if the CascadeClassifier was loaded successfully
    if faceCascade.empty():
        print(f"Error: CascadeClassifier not loaded successfully from {cascPath}")
        return

    # Read the image
    image = cv2.imread(imagePath)

    # Check if the image is loaded successfully
    if image is None:
        print(f"Error: Unable to load image from {imagePath}")
        return

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    print(f"Found {len(faces)} faces!")
    if(faces > 0):
        return True

    # # Draw rectangles around the faces
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # # Display the image with rectangles around faces
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.axis("off")
    # plt.show()

# Provide the full paths to the image and XML file
cascPath = os.path.abspath('./haarcascade_frontalface_default.xml')


# Thư mục chứa các tệp tin ảnh
img_directory = './output/frame_1'
img_directory_err = './output/frame_0'

# Lấy danh sách tên tệp tin trong thư mục img_directory
img_files = set([os.path.splitext(file) for file in os.listdir(img_directory)])

for filename in img_files:
    print(filename)
    # Di chuyển tệp tin vào thư mục đích
    imagePath = os.path.join(img_directory, filename)
    new_img_file_path = os.path.join(img_directory_err, filename + '.jpg')
    if not check_has_face_image(imagePath, cascPath):
        os.rename(imagePath, new_img_file_path)
        # if os.path.isfile(imagePath):
        #     os.remove(imagePath)
        
    