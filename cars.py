from ultralytics import YOLO
import cv2
 #load models 
coco_model= YOLO('yolov8n.pt')
#load video
cap=cv2.VideoCapture('C:\\Users\\GO\\Desktop\\plate\\video.mp4')
print(cap)
ret = True
frame_nbr=-1
vehicules_id=[2.0]
vehicules_=[]
if ret :

    frame_nbr +=1
    ret,frame= cap.read()
    if ret and frame_nbr < 10 :
        detections=coco_model(frame)[0]
        for detection in detections.boxes.data.tolist():
            x1,y1,x2,y2,score,id=detection
            if int(id) in vehicules_id:
                vehicules_id.append([x1,y1,x2,y2,score])
        print(vehicules_id)
        #track objects plate are moving  we sh

