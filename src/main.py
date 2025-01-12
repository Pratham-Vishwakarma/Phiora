# Final Project - Phiora.
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import numpy as np
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def safe_divide(numerator, denominator):
    if denominator != 0:
        return numerator / denominator
    else:
        return 0  # or float('inf'), or any value you prefer for division by zero

def upload_image():
    # Open a file dialog for the user to select an image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.webp;*.tiff;*.jfif;*.svg;*.ppm;*.pgm;*.heic;*.bpg;*.ico;*.jpe;*.jp2;*.jps;*.pbm;*.pcx;*.pic;*.pict;*.pnm;*.psd;*.rgb;*.rgba;*.tga;*.tif")]
    )
    if file_path:
        try:
            # Load DNN Face Detection model
            net = cv2.dnn.readNetFromCaffe(resource_path("models\\deploy.prototxt"), 
                               resource_path("models\\res10_300x300_ssd_iter_140000.caffemodel"))

            # Initialize Mediapipe Face Mesh
            mp_face_mesh = mp.solutions.face_mesh
            # Example for setting image dimensions
            face_mesh = mp.solutions.face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )


            # Initialize MediaPipe drawing utils
            mp_drawing = mp.solutions.drawing_utils

            # Load the image
            img = cv2.imread(file_path)
            height = 400
            width = int((img.shape[0] * height) / img.shape[1])
            img = cv2.resize(img, (height, width))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # DNN Face Detection
            blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            net.setInput(blob)
            detections = net.forward()

            # Convert the image to RGB for Mediapipe processing
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(img_rgb)

            # while True:
            img_copy = img.copy()

            # Draw face detection (DNN)
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    # Get face bounding box and scale to original image size
                    box = detections[0, 0, i, 3:7] * np.array([img.shape[1], img.shape[0], img.shape[1], img.shape[0]])  # Scale box to resized image
                    s1, s2, s3, s4 = box.astype(int)
                    (x, y, w, h) = box.astype(int)

            # If face landmarks are found, draw them on the image
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:

                    # Extract extreme points for facial features
                    leftmost_point = min(face_landmarks.landmark, key=lambda landmark: landmark.x)
                    rightmost_point = max(face_landmarks.landmark, key=lambda landmark: landmark.x)
                    bottommost_point = max(face_landmarks.landmark, key=lambda landmark: landmark.y)

                    ih, iw, _ = img_copy.shape

                    # Draw Leftmost Point (Separate Landmark)
                    p10, y = int(leftmost_point.x * iw), int(leftmost_point.y * ih)
                    cv2.circle(img_copy, (p10, y), 2, (255, 0, 0), -1)

                    # Draw Rightmost Point (Separate Landmark)
                    p11, y = int(rightmost_point.x * iw), int(rightmost_point.y * ih)
                    cv2.circle(img_copy, (p11, y), 2, (255, 0, 0), -1)

                    # Chin (2)
                    x, p2 = int(bottommost_point.x * iw), int(bottommost_point.y * ih)
                    cv2.circle(img_copy, (x, p2), 2, (255, 0, 0), -1)
                
                    # Bottom of the nose (4)
                    landmark = face_landmarks.landmark[19]
                    x, p4 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (x, p4), 2, (255, 0, 0), -1)

                    # Left Of Outside Of Eye (8)
                    landmark = face_landmarks.landmark[33]
                    p8, y = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (p8, y), 2, (255, 0, 0), -1)
                    
                    # Right Of Outside Of Eye (9)
                    landmark = face_landmarks.landmark[263]
                    p9, y = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (p9, y), 2, (255, 0, 0), -1)
                                
                    # Top Of The Lip (13)
                    landmark = face_landmarks.landmark[0]
                    x, p13 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (x, p13), 2, (255, 0, 0), -1)

                    # Bottom Of The Lip (14)
                    landmark = face_landmarks.landmark[17]
                    x, p14 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (x, p14), 2, (255, 0, 0), -1)
                    
                    # Center Of The Lip (5)
                    landmark = face_landmarks.landmark[14]
                    x, p5 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (x, p5), 2, (255, 0, 0), -1)

                    # Pupil Of Left Eye (3)
                    landmark = face_landmarks.landmark[468]
                    x, p3 = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (x, p3), 2, (255, 0, 0), -1)

                    # Left Of Bottom Of Nose (6)
                    landmark = face_landmarks.landmark[48]
                    p6, y = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (p6, y), 2, (255, 0, 0), -1)
                    
                    # Right Of Bottom Of Nose (7)
                    landmark = face_landmarks.landmark[278]
                    p7, y = int(landmark.x * iw), int(landmark.y * ih)
                    cv2.circle(img_copy, (p7, y), 2, (255, 0, 0), -1)
                                                    
                    # Top Of Head (1)
                    landmark = face_landmarks.landmark[10]     
                    x, p1 = int(landmark.x * iw), (s2 - (int(landmark.y * ih) - s2))
                    cv2.circle(img_copy, (x, p1), 2, (255, 0, 0), -1)

                    # Hairline (12)
                    x , p12 = int(s1+(s3-s1)/2), s2
                    cv2.circle(img_copy, (x, p12), 2, (255, 0, 0), -1)

            cv2.destroyAllWindows()            

            # Calculating the ratios
            ratio = []
            deviation = []
            normal_score = []
            avg_score = 0

            # Append each ratio while checking for zero denominators
            ratio.append(safe_divide((p3 - p1), (p5 - p3)))
            ratio.append(safe_divide((p2 - p1), (p2 - p4)))
            ratio.append(safe_divide((p3 - p12), (p2 - p4)))
            ratio.append(safe_divide((p11 - p10), (p7 - p6)))
            ratio.append(safe_divide((p9 - p8), (p14 - p13)))

            # Print the ratios
            for i in range(5):
                if(ratio[i]<0):
                    ratio[i]=-ratio[i]
                deviation.append(ratio[i]-1.618)
                # print("Ratio", i + 1, ":", ratio[i])
                if(deviation[i]<0):
                    deviation[i]=-deviation[i]
                normal_score.append(1-(deviation[i]/5.0))
                # print("Deviation:", deviation[i])
                avg_score = avg_score+normal_score[i]
                # print("Normal Score:", normal_score[i])

            avg_score = (avg_score/5)*10

            # Open and display the image in the GUI
            # Convert img_copy to RGB (from BGR used by OpenCV)
            img_copy_rgb = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)

            # Convert to a PIL image
            img_pil = Image.fromarray(img_copy_rgb)

            # Resize for display
            img_pil.thumbnail((height, width))

            # Convert to ImageTk for Tkinter
            img_tk = ImageTk.PhotoImage(img_pil)

            # Update the image label
            image_label.config(image=img_tk)
            image_label.image = img_tk

            # display the score
            score_label.config(text=f"Image Score: {round(avg_score, 1)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the image.\n{e}")

# Create the main application window
app = tk.Tk()
app.title("Image Scorer")
app.iconbitmap(resource_path('public\\phiora_logo.ico'))
app.geometry('500x600')  # Set the window size to the screen resolution

# Set the background color of the window
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

# Run the application
app.mainloop()