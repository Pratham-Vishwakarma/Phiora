import os
import time
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from score import calculate_score
from face_shape import face_shape
from PIL import Image

# Paths
CSV_FILE = os.path.join("src", "image_dataset.csv")
CACHE_FILE = os.path.join("src", "processed_results.csv")

def resource_path(relative_path):
    return os.path.join(os.path.abspath("."), relative_path)

net = cv2.dnn.readNetFromCaffe(
    resource_path(os.path.join("models", "deploy.prototxt")),
    resource_path(os.path.join("models", "res10_300x300_ssd_iter_140000.caffemodel"))
)

# Load original image paths
df = pd.read_csv(CSV_FILE)
image_paths = df['path'].tolist()

# Try loading cached results
if os.path.exists(CACHE_FILE):
    print("Loading cached results...")
    result_df = pd.read_csv(CACHE_FILE)
    golden_scores = result_df['score'].tolist()
    all_deviations_np = result_df[[col for col in result_df.columns if col.startswith("R")]].to_numpy()

else:
    print("Processing images and saving results...")
    golden_scores = []
    processing_times = []
    all_face_shapes = []
    all_deviations = []

    for img_path in image_paths:
        if img_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff')):
            try:
                full_img_path = resource_path(img_path)
                if not os.path.exists(full_img_path):
                    print(f"Image not found: {full_img_path}")
                    continue

                start_time = time.time()

                ratios, deviations, score, img_copy = calculate_score(full_img_path, net)
                face_shape_result, hairstyle_recommendation = face_shape(full_img_path)

                end_time = time.time()

                golden_scores.append(score)
                processing_times.append(end_time - start_time)
                all_face_shapes.append(face_shape_result)
                all_deviations.append(deviations)

            except Exception as e:
                print(f"Failed to process {os.path.basename(img_path)}: {e}")

    if len(golden_scores) > 0:
        all_deviations_np = np.array(all_deviations)

        # Save to CSV
        columns = ['path', 'score'] + [f'R{i+1}' for i in range(all_deviations_np.shape[1])]
        data = [[image_paths[i], golden_scores[i]] + list(all_deviations_np[i]) for i in range(len(golden_scores))]
        result_df = pd.DataFrame(data, columns=columns)
        result_df.to_csv(CACHE_FILE, index=False)

# ===================================
# Anlysis Section
# ===================================

if len(golden_scores) > 0:
    # 1. Golden Score Analysis
    average_score = np.mean(golden_scores)
    std_dev_score = np.std(golden_scores)
    min_score = np.min(golden_scores)
    max_score = np.max(golden_scores)

    # print("\nGolden Score Analysis:")
    # print(f"Average Score: {average_score:.2f}")
    # print(f"Standard Deviation: {std_dev_score:.2f}")
    # print(f"Minimum Score: {min_score:.2f}")
    # print(f"Maximum Score: {max_score:.2f}")

    # Top and Bottom 5 Scoring Images
    if len(golden_scores) >= 5:
        # Combine paths and scores
        scored_images = list(zip(image_paths, golden_scores))

        # Sort by score
        sorted_scored_images = sorted(scored_images, key=lambda x: x[1])

        # Get lowest 5
        bottom_5 = sorted_scored_images[:5]
        # Get top 5
        top_5 = sorted_scored_images[-5:]

        print("\nLowest 5 Scoring Images:")
        for path, score in bottom_5:
            print(f"{path} - Score: {score:.2f}")

        print("\nTop 5 Scoring Images:")
        for path, score in reversed(top_5):  # Reverse to show highest first
            print(f"{path} - Score: {score:.2f}")


    # 2. Deviation Analysis
    # all_deviations_np = np.array(all_deviations)
    # mean_deviation_per_ratio = np.mean(all_deviations_np, axis=0)

    # print("\nAverage Deviation from Golden Ratio (1.618) for each measured facial ratio:")
    # ratio_names = [
    #     "Face length to face width",
    #     "Head to pupils vs pupils to lips",
    #     "Nose tip to chin vs lips to chin",
    #     "Nose tip to chin vs pupils to nose tips",
    #     "Nose width to nose tips to lips",
    #     "Outer eye distance to hairline to pupils",
    #     "Lip length to nose width"
    # ]

    # for i, mean_dev in enumerate(mean_deviation_per_ratio):
    #     print(f"{ratio_names[i]}: Average deviation = {mean_dev:.3f}")

    # # 3. Face Shape Distribution
    # face_shape_counter = Counter(all_face_shapes)

    # print("\nFace Shape Distribution:")
    # for shape, count in face_shape_counter.items():
    #     print(f"{shape}: {count} images")

    # # 4. Processing Time
    # average_time = np.mean(processing_times)

    # print("\nProcessing Time:")
    # print(f"Average processing time per image: {average_time:.2f} seconds")

# ===================================
# Visualization Section
# ===================================

# Golden Score Histogram
# plt.figure(figsize=(8, 6))
# plt.hist(golden_scores, bins=20, color='skyblue', edgecolor='black', alpha=0.7, density=True)
# plt.title('Golden Ratio Score Distribution')
# plt.xlabel('Golden Ratio Score')
# plt.ylabel('Density')
# plt.grid(True)

# # Add a smooth density curve on top
# from scipy.stats import gaussian_kde

# kde = gaussian_kde(golden_scores)
# score_range = np.linspace(min(golden_scores), max(golden_scores), 300)
# plt.plot(score_range, kde(score_range), color='blue', linewidth=2)

# plt.show()

# # Face Shape Bar Chart
# plt.figure(figsize=(8, 6))
# plt.bar(face_shape_counter.keys(), face_shape_counter.values(), color='lightcoral', edgecolor='black')
# plt.title('Face Shape Distribution')
# plt.xlabel('Face Shape')
# plt.ylabel('Number of Images')
# plt.xticks(rotation=45)
# plt.grid(axis='y')
# plt.show()

# # Processing Time Histogram
# plt.figure(figsize=(8, 6))
# plt.hist(processing_times, bins=20, color='lightgreen', edgecolor='black')
# plt.title('Processing Time per Image')
# plt.xlabel('Time (seconds)')
# plt.ylabel('Number of Images')
# plt.grid(True)
# plt.show()


# # Define a threshold for R6 outliers
# threshold = 3.5 # You can adjust this

# # Create a mask that keeps only rows where R6 (index 5) is below the threshold
# filtered_deviations_np = all_deviations_np[
#     (all_deviations_np[:, 3] < threshold) &
#     (all_deviations_np[:, 5] < threshold)
# ]

# meow_deviations_np = all_deviations_np[
#     (all_deviations_np[:, 3] >= threshold) &
#     (all_deviations_np[:, 5] >= threshold)
# ]

# # Correct mask for rows where R4 or R6 exceed the threshold
# outlier_mask = (all_deviations_np[:, 3] >= threshold) | (all_deviations_np[:, 5] >= threshold)

# # Get indices of outliers relative to original data
# outlier_indices = np.where(outlier_mask)[0]

# # Print outlier info
# print("Images with R4 or R6 deviation >= threshold:")
# for idx in outlier_indices:
#     print(f" - {image_paths[idx]} (R4 = {all_deviations_np[idx, 3]:.2f}, R6 = {all_deviations_np[idx, 5]:.2f})")


# if len(golden_scores) > 0:
#     plt.figure(figsize=(10, 6))
#     plt.boxplot(filtered_deviations_np, tick_labels=[f'R{i+1}' for i in range(filtered_deviations_np.shape[1])])
#     plt.title('Deviation from Golden Ratio Across Facial Ratios (Filtered)')
#     plt.xlabel('Facial Ratio')
#     plt.ylabel('Deviation from 1.618')
#     plt.grid(True)
#     plt.show()

else:
    print("\nNo images were successfully processed. Please check the image paths or file permissions.")
