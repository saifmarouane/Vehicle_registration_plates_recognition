
# License Plate Detection and Text Extraction Project
<div>
    <img src="car1.jpeg" alt="License Plate Example 1" style="width: 45%; display: inline-block;">
    <img src="car2.jpg" alt="License Plate Example 2" style="width: 45%; display: inline-block;">
</div>
## Overview

This project leverages YOLO (You Only Look Once) for detecting license plates in video frames and EasyOCR for extracting text from those plates. The process involves training a YOLO model on annotated images, predicting license plates in a video, and displaying the detected text.

## Requirements

- Python 3.10 or higher
- Ultralytics YOLOv8
- OpenCV
- EasyOCR
- Google Colab (or local environment with appropriate CUDA setup)

## Setup

1. **Clone the Repository** 
 
Install Required Libraries: If using Google Colab, you can install the libraries directly in a notebook cell:

python
Copier le code
!pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
!pip install easyocr opencv-python
Prepare Your Dataset:

Annotate your dataset using tools like Roboflow or LabelImg.
Ensure the dataset is structured correctly with images and corresponding annotation files.
Training the YOLO Model
Train the YOLO model using the following command in a Colab notebook or terminal:

bash
Copier le code
!yolo task=detect mode=train data=/content/plate-detect-1/data.yaml epochs=20 imgsz=640 model=yolov10b.pt
data.yaml: Path to your dataset configuration file.
epochs: Number of training epochs.
imgsz: Size of images used for training.
Predicting License Plates in a Video
The following code reads a video file, processes each frame, detects license plates, and extracts the text:

python
Copier le code
import cv2
import easyocr
from google.colab.patches import cv2_imshow

# Initialize EasyOCR




# Replace with your video path
video_path = '/content/video.mp4'
process_video(video_path)
Code Breakdown
EasyOCR Initialization: Initializes the OCR reader for text extraction.
Video Processing: Opens the video file and processes each frame:
Saves the current frame as an image.
Uses YOLO to detect license plates.
Reads text from the annotated image using EasyOCR.
Draws bounding boxes around detected plates and displays the text.




The following sections explain how I structured the code and the main steps involved in processing the video and recognizing license plates.

### 1. Load Models

I load two YOLO models:
- **coco_model**: This model detects general objects, such as vehicles (cars, trucks, buses).
- **license_plate_detector**: This model is trained to specifically detect vehicle license plates here  yolo (1).

```python
coco_model= YOLO('yolov8n.pt')
license_plate_detector = YOLO('C:\\Users\\GO\\Desktop\\anpr\\Vehicle_registration_plates_recognition\\best (1).pt')
2. Process the Video Input
I load the video from the specified path. Each frame of the video is processed to detect vehicles and license plates.

python
Copier le code
cap=cv2.VideoCapture('C:\\Users\\GO\\Desktop\\plate\\video.mp4')
3. Detect and Track Vehicles
For each frame of the video, I use the coco_model to detect vehicles like cars, trucks, buses (IDs 2, 3, 5, 7). Then, I use a tracking algorithm (SORT) to assign unique IDs to each detected vehicle.

python
Copier le code
detections = coco_model(frame)[0]
track_ids = mot_tracker.update(np.asarray(detections_))
4. Detect License Plates
After detecting and tracking the vehicles, I apply the license_plate_detector model to identify license plates in the frame. Once the plates are detected, I crop and process the plate for better recognition.

python
Copier le code
license_plates = license_plate_detector(frame)[0]
5. Recognize the License Plate
Using OpenCV, I convert the cropped license plate to grayscale and apply binary thresholding to enhance the characters. The utility function read_license_plate is then used to extract the license plate number as text.

python
Copier le code
license_text, license_score = read_license_plate(license_plate_crop_thresh)
6. Output Results
The results are stored in a dictionary where each frame number is mapped to a vehicle ID and license plate information. Finally, these results are written to a CSV file for further use.

python
Copier le code
write_csv(results, './test.csv')
Additional Functions
I also created utility functions:

get_car: Associates the detected license plate with a specific vehicle.
read_license_plate: Reads the license plate number from the processed image.
write_csv: Writes the results into a CSV file.
Running the Script