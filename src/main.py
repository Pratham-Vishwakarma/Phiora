# Final Project - Phiora.
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import numpy as np
import os
import sys
import math

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def upload_image():
    # Open a file dialog for the user to select an image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp;*.tiff;*.jfif;*.svg;*.ppm;*.pgm;*.heic;*.bpg;*.ico;*.jpe;*.jp2;*.jps;*.pbm;*.pcx;*.pic;*.pict;*.pnm;*.psd;*.rgb;*.rgba;*.tga;*.tif")]
    )
    if file_path:
        try:
            # Load DNN Face Detection model
            net = cv2.dnn.readNetFromCaffe(resource_path("models\\deploy.prototxt"), resource_path("models\\res10_300x300_ssd_iter_140000.caffemodel"))

            # Example for setting image dimensions
            face_mesh = mp.solutions.face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )

            # Load the image
            img = cv2.imread(file_path)
            height = 400
            width = int((img.shape[0] * height) / img.shape[1])
            img = cv2.resize(img, (height, width))

            # DNN Face Detection
            blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            net.setInput(blob)
            detections = net.forward()

            # Convert the image to RGB for Mediapipe processing
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(img_rgb)

            img_copy = img.copy()

            # Draw face detection (DNN)
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    # Get face bounding box and scale to original image size
                    box = detections[0, 0, i, 3:7] * np.array([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])  # Scale box to resized image
                    s1, s2, s3, s4 = box.astype(int)

            # If face landmarks are found, draw them on the image
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:

                    ih, iw, _ = img_copy.shape
                                    
                    # Top Of Head (1)
                    landmark = face_landmarks.landmark[10]     
                    px1, py1 = int(landmark.x * iw), (s2 - (int(landmark.y * ih) - s2))
                    cv2.circle(img_copy, (px1, py1), 2, (255, 0, 0), -1)

                    # Chin (2)
                    landmark = face_landmarks.landmark[152]
                    px2, py2 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px2, py2), 2, (255, 0, 0), -1)

                    # Pupil Of Left Eye (3)
                    landmark = face_landmarks.landmark[468]
                    px31, py31 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px31, py31), 2, (255, 0, 0), -1)

                    # Pupil Of Right Eye (4)
                    landmark = face_landmarks.landmark[473]
                    px32, py32 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px32, py32), 2, (255, 0, 0), -1)

                    # Center Of the pupils
                    top, bottom = ((px31, py31), (px32, py32)) if py31 > py32 else ((px32, py32), (px31, py31))
                    l3132 = math.sqrt((bottom[0]-top[0])**2 + (bottom[1]-top[1])**2)
                    pc_x, pc_y = (top[0] + bottom[0]) / 2, (top[1] + bottom[1]) / 2

                    # Bottom of the nose (4)
                    landmark = face_landmarks.landmark[19]
                    px4, py4 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px4, py4), 2, (255, 0, 0), -1)
                    
                    # Center Of The Lip (5)
                    landmark = face_landmarks.landmark[14]
                    px5, py5 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px5, py5), 2, (255, 0, 0), -1)

                    # Left Of Bottom Of Nose (6)
                    landmark = face_landmarks.landmark[48]
                    px6, py6 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px6, py6), 2, (255, 0, 0), -1)
                    
                    # Right Of Bottom Of Nose (7)
                    landmark = face_landmarks.landmark[278]
                    px7, py7 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px7, py7), 2, (255, 0, 0), -1)
                    
                    # Left Of Outside Of Eye (8)
                    landmark = face_landmarks.landmark[33]
                    px8, py8 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px8, py8), 2, (255, 0, 0), -1)
                    
                    # Right Of Outside Of Eye (9)
                    landmark = face_landmarks.landmark[263]
                    px9, py9 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px9, py9), 2, (255, 0, 0), -1)

                    # Left Cheekbone (10)
                    landmark = face_landmarks.landmark[234]
                    px10, py10 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px10, py10), 2, (255, 0, 0), -1)

                    # Right Cheekbone (11)
                    landmark = face_landmarks.landmark[447]
                    px11, py11 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px11, py11), 2, (255, 0, 0), -1)
                    
                    # Hairline (12)
                    px12 , py12 = int(s1+(s3-s1)/2), s2
                    cv2.circle(img_copy, (px12 , py12), 2, (255, 0, 0), -1)

                    # Top Of The Lip (13)
                    landmark = face_landmarks.landmark[0]
                    px13, py13 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px13, py13), 2, (255, 0, 0), -1)

                    # Bottom Of The Lip (14)
                    landmark = face_landmarks.landmark[17]
                    px14, py14 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (px14, py14), 2, (255, 0, 0), -1)

            # Golden Ratio Calculation
            ratio = []
            deviation = []
            normal = []
            score = 0
            
            top, bottom = ((px10, py10), (px11, py11)) if py10 > py11 else ((px11, py11), (px10, py10))
            l1011 = round(math.sqrt((bottom[0] - top[0])**2 + (bottom[1] - top[1])**2), 3)
            top, bottom = ((px6, py6), (px7, py7)) if py6 > py7 else ((px7, py7), (px6, py6))
            l67 = round(math.sqrt((bottom[0] - top[0])**2 + (bottom[1] - top[1])**2), 3)
            l1pc = round(math.sqrt((pc_x - px1)**2 + (pc_y - py1)**2), 3)
            lpc5 = round(math.sqrt((px5 - pc_x)**2 + (py5 - pc_y)**2), 3)
            l12 = round(math.sqrt((px2 - px1)**2 + (py2 - py1)**2), 3)
            l42 = round(math.sqrt((px2 - px4)**2 + (py2 - py4)**2), 3)
            l12pc = round(math.sqrt((pc_x - px12)**2 + (pc_y - py12)**2), 3)
            top, bottom = ((px8, py8), (px9, py9)) if py8 > py9 else ((px9, py9), (px8, py8))
            l89 = round(math.sqrt((bottom[0] - top[0])**2 + (bottom[1] - top[1])**2), 3)
            l1314 = round(math.sqrt((px14 - px13)**2 + (py14 - py13)**2), 3)

            ratio.append(round(abs((l1pc)/(lpc5)), 3))
            ratio.append(round(abs((l12)/(l42)), 3))
            ratio.append(round(abs((l12pc)/(l42)), 3))
            ratio.append(round(abs((l1011)/(l67)), 3))
            ratio.append(round(abs((l89)/(l1314)), 3))

            for i in range(5):
                deviation.append(round(abs(round(ratio[i], 3)-1.618), 3))
                
            for i in range(5):
                normal.append(abs(round(1-(deviation[i]/(sum(deviation)/5)), 3)))
                score = score+normal[i]  
                
            tot_score = (score/5)*10

            # Open and display the image in the GUI
            img_copy_rgb = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_copy_rgb)
            img_pil.thumbnail((height, width))
            img_tk = ImageTk.PhotoImage(img_pil)

            # Update the image label
            image_label.config(image=img_tk)
            image_label.image = img_tk

            # display the score
            score_label.config(text=f"Image Score: {tot_score:.1f}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the image.\n{e}")

# Create the main application window
app = tk.Tk()
app.title("Image Scorer")
app.iconbitmap(resource_path('public\\phiora_logo.ico'))
app.geometry('500x600')  # Set the window size to the screen resolution
app.config(bg="#2a2a2a")  # Dark background color

# Create a label at the top to display the score (initially empty)
score_label = tk.Label(app, text="", font=("Arial", 14), fg="white", bg="#2a2a2a")
score_label.pack(pady=5)

# Add a button to upload the image
upload_button = tk.Button(
    app, 
    text="Upload Image",
    command=upload_image,
    font=("Times New Roman", 14, "bold"),  # Cool font style
    cursor="hand2",  # Hand cursor on hover
    bg="#4CAF50",  # Green background
    fg="white",  # White text color
    activebackground="#45a049",  # Darker green when clicked
    activeforeground="white"  # White text when clicked
)
upload_button.pack(pady=10)

# Add a label to display the image
image_label = tk.Label(app, bg="#2a2a2a")  # Background matches the window's background
image_label.pack(pady=10)

app.mainloop()