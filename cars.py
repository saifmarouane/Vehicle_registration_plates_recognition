from ultralytics import YOLO
import cv2
from sort.sort import *
from util import *
mot_tracker = Sort()
 #load models 
coco_model= YOLO('yolov8n.pt')
results = {}

cap=cv2.VideoCapture('C:\\Users\\GO\\Desktop\\plate\\video.mp4')
license_plate_detector = YOLO('C:\\Users\\GO\Desktop\\anpr\\Vehicle_registration_plates_recognition\\best (1).pt')
#load video
def detect(cap):
    results = {} 
    vehicles = [2, 3, 5, 7]

    # read frames
    frame_nmr = -1
    ret = True

    while ret and frame_nmr < 2  :
        frame_nmr += 1
        ret, frame = cap.read()
        if ret:
            results[frame_nmr] = {}
            # detect vehicles
            detections = coco_model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])

            # track vehicles
            track_ids = mot_tracker.update(np.asarray(detections_))

            # detect license plates
            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                # assign license plate to car
                xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

                if car_id != -1:

                    # crop license plate
                    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                    # process license plate
                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
                #cv2.imshow('originale_',license_plate_crop_gray)
                #cv2.imshow('originale_dd',license_plate_crop_thresh)
                #cv2.waitKey(0)
                license_text,license_score=read_license_plate(license_plate_crop_thresh)
                #write results

                if license_text is not None:
                    results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                    'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                        'text': license_text,
                                                                        'bbox_score': score,
                                                                        'text_score': license_score}}

    # write results
    #print(results)
    write_csv(results, './test.csv')
    return results
#detect(cap)