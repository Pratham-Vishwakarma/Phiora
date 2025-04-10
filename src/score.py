import cv2
import mediapipe as mp
import numpy as np
from math import sqrt

def calculate_score(image_path, net):

    img = cv2.imread(image_path)
    height = 500
    scale_factor = height / img.shape[0]  # Calculate scale ratio
    width = int(img.shape[1] * scale_factor)  # Maintain aspect ratio
    img = cv2.resize(img, (width, height))

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=True,      # Set True for single images
        max_num_faces=1,             # Detect only one face
        refine_landmarks=True,       # More precise landmark detection
        min_detection_confidence=0.5 # Confidence threshold
    )

    # DNN Face Detection
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    # Convert the image to RGB for Mediapipe processing
    results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    while True:
        img_copy = img.copy()

        # Draw face detection (DNN)
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])  # Scale box to resized image
                _, s2, _, _ = box.astype(int)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                
                ih, iw, _ = img_copy.shape

                # Top Of Head (1)
                landmark = face_landmarks.landmark[10]     
                xp1, yp1 = int(landmark.x * iw), (s2 - (int(landmark.y * ih) - s2))
                cv2.circle(img_copy, (xp1, yp1), 1, (0, 0, 255), -1)

                # Chin (2)
                landmark = face_landmarks.landmark[175] #152
                xp2, yp2 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp2, yp2), 1, (0, 0, 255), -1)

                # Pupil Of Left Eye (3.1)
                landmark = face_landmarks.landmark[468]
                xp3_1, yp3_1 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp3_1, yp3_1), 1, (0, 0, 255), -1)

                # Pupil Of Right Eye (3.2)
                landmark = face_landmarks.landmark[473]
                xp3_2, yp3_2 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp3_2, yp3_2), 1, (0, 0, 255), -1)

                #Center of the pupil (3)
                xp3, yp3 = int((xp3_1 + xp3_2) / 2), int((yp3_1 + yp3_2) / 2)
                cv2.circle(img_copy, (xp3, yp3), 1, (0, 0, 255), -1)

                # nose (4)
                landmark = face_landmarks.landmark[4]
                xp4, yp4 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp4, yp4), 1, (0, 0, 255), -1)

                # Center Of The Lip (5)
                landmark = face_landmarks.landmark[14]
                xp5, yp5 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp5, yp5), 1, (0, 0, 255), -1)

                # Left Of Bottom Of Nose (6) 
                landmark = face_landmarks.landmark[48] #115 #129 #64 #48 #219
                xp6, yp6 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp6, yp6), 1, (0, 0, 255), -1)
                
                # Right Of Bottom Of Nose (7)
                landmark = face_landmarks.landmark[278] #344 #358 #294 #331 #439 #278
                xp7, yp7 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp7, yp7), 1, (0, 0, 255), -1)
                    
                # Left Of Outside Of Eye (8)
                landmark = face_landmarks.landmark[226] #130 #33 #226
                xp8, yp8 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp8, yp8), 1, (0, 0, 255), -1)
                
                # Right Of Outside Of Eye (9)
                landmark = face_landmarks.landmark[446] #359 #263 #446
                xp9, yp9 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp9, yp9), 1, (0, 0, 255), -1)

                # Draw Leftmost Point (10)
                landmark = face_landmarks.landmark[34]
                xp10, yp10 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp10, yp10), 1, (0, 0, 255), -1)

                # Draw Rightmost Point (11)
                landmark = face_landmarks.landmark[264]
                xp11, yp11 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp11, yp11), 1, (0, 0, 255), -1)

                # Hairline (12)
                xp12 , yp12 = xp1, s2+10
                cv2.circle(img_copy, (xp12, yp12), 1, (0, 0, 255), -1)

                # Top Of The Lip (13)
                landmark = face_landmarks.landmark[0]
                xp13, yp13 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp13, yp13), 1, (0, 0, 255), -1)

                # Bottom Of The Lip (14)
                landmark = face_landmarks.landmark[17]
                xp14, yp14 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp14, yp14), 1, (0, 0, 255), -1)

                #Bottom of the Nose (15)
                landmark = face_landmarks.landmark[2]
                xp15, yp15 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp15, yp15), 1, (0, 0, 255), -1)
            
                #left of lips (16)
                landmark = face_landmarks.landmark[61]
                xp16, yp16 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp16, yp16), 1, (0, 0, 255), -1)

                #right of lips (17)
                landmark = face_landmarks.landmark[291]
                xp17, yp17 = int(landmark.x * iw), int(landmark.y * ih)
                cv2.circle(img_copy, (xp17, yp17), 1, (0, 0, 255), -1)

            break

    def safe_divide(numerator, denominator):
        if denominator != 0:
            return numerator / denominator
        else:
            return 0  # or float('inf'), or any value you prefer for division by zero

    # Calculating the ratios
    ratio = []
    deviation = []
    normal_score = []
    avg_score = 0

    # # Append each ratio while checking for zero denominators
    ratio.append(safe_divide(sqrt(((xp2 - xp1)**2)+((yp2 - yp1)**2)), sqrt(((xp10 - xp11)**2)+((yp10 - yp11)**2)))) # 2-1/10-11
    ratio.append(safe_divide(sqrt(((xp3 - xp1)**2)+((yp3 - yp1)**2)), sqrt(((xp5 - xp3)**2)+((yp5 - yp3)**2)))) # 3-1/5-3
    # ratio.append(safe_divide(sqrt(((xp2 - xp4)**2)+((yp2 - yp4)**2)), sqrt(((xp2 - xp5)**2)+((yp2 - yp5)**2)))) # 2-4/2-5
    ratio.append(safe_divide(sqrt(((xp2 - xp4)**2)+((yp2 - yp4)**2)), sqrt(((xp2 - xp13)**2)+((yp2 - yp13)**2)))) # 2-4/2-5

    ratio.append(safe_divide(sqrt(((xp2 - xp4)**2)+((yp2 - yp4)**2)), sqrt(((xp4 - xp3)**2)+((yp4 - yp3)**2)))) # 2-4/4-3
    # ratio.append(safe_divide(sqrt(((xp6 - xp7)**2)+((yp6 - yp7)**2)), sqrt(((xp5 - xp4)**2)+((yp5 - yp4)**2)))) # 6-7/5-4
    ratio.append(safe_divide(sqrt(((xp6 - xp7)**2)+((yp6 - yp7)**2)), sqrt(((xp13 - xp4)**2)+((yp13 - yp4)**2)))) # 6-7/5-4
    ratio.append(safe_divide(sqrt(((xp8 - xp9)**2)+((yp8 - yp9)**2)), sqrt(((xp3 - xp12)**2)+((yp3 - yp12)**2)))) # 8-9/3-12
    # ratio.append(safe_divide(sqrt(((xp14 - xp13)**2)+((yp14 - yp13)**2)), sqrt(((xp7 - xp6)**2)+((yp7 - yp6)**2)))) # 14-13/7-6
    # ratio.append(safe_divide(sqrt(((xp15 - xp14)**2)+((yp15 - yp14)**2)), sqrt(((xp7 - xp6)**2)+((yp7 - yp6)**2)))) # 14-13/7-6
    # ratio.append(safe_divide(sqrt(((xp15 - xp13)**2)+((yp15 - yp13)**2)), sqrt(((xp7 - xp6)**2)+((yp7 - yp6)**2)))) # 14-13/7-6
    # ratio.append(safe_divide(sqrt(((xp15 - xp5)**2)+((yp15 - yp5)**2)), sqrt(((xp7 - xp6)**2)+((yp7 - yp6)**2)))) # 14-13/7-6
    ratio.append(safe_divide(sqrt(((xp17 - xp16)**2)+((yp17 - yp16)**2)), sqrt(((xp7 - xp6)**2)+((yp7 - yp6)**2)))) # 17-16/7-6

    # GOLDEN_RATIO = 1.61803398875

    # for d in deviation:
    #     # The closer to golden ratio, the higher the score.
    #     normal_score.append(1 - (d / GOLDEN_RATIO))

    ##

    # for i in range(len(ratio)):
    #     deviation.append(np.abs(ratio[i]-1.61803398875))

    # max_deviation = max(deviation)

    # for i in range(len(deviation)):
    #     normal_score.append(1-(deviation[i]/max_deviation))

    # avg_score = np.average(normal_score)

    # score = (avg_score)*10

    GOLDEN_RATIO = 1.61803398875

    deviation = [abs(r - GOLDEN_RATIO) for r in ratio]
    normal_score = [max(0, 1 - (d / GOLDEN_RATIO)) for d in deviation]
    avg_score = np.average(normal_score)
    score = avg_score * 10

    return ratio, deviation, round(score, 2), img_copy
