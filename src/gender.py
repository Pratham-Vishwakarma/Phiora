import cv2
import numpy as np

def gender_detect(image_path, net):
    img = cv2.imread(image_path)

    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.1, 5)
    
    if len(faces) > 0:
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        # Draw face detection (DNN)
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                # Get face bounding box and scale to original image size
                box = detections[0, 0, i, 3:7] * np.array([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])  # Scale box to resized image
                # s1, s2, s3, s4 = box.astype(int)
                (x, y, w, h) = box.astype(int)
                face_ratio = w/h
                cv2.rectangle(img, (x, y), (w, h), (0, 255, 0), 2)
        if face_ratio > 0.95:
            return "male"
        else:
            return "female"
    return "unknown"