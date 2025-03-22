import torch
import cv2
import os
import glob

# Define paths
input_folder = "images"  # Folder containing input images
output_folder = "images_output"  # Folder to save output images

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load YOLOv5 model (replace 'lacerations.pt' with your actual model)
model = torch.hub.load('yolov5', 'custom', path='new_onion_cut.pt', source='local')

# Set confidence threshold (adjust as needed)
model.conf = 0.01  # Minimum confidence for detections

# Get all image paths from the input folder (supports .jpg, .png, .jpeg)
image_paths = glob.glob(os.path.join(input_folder, "*.*"))

# Process each image
for img_path in image_paths:
    # Load image
    image = cv2.imread(img_path)
    if image is None:
        print(f"Error loading image: {img_path}")
        continue

    # Convert BGR to RGB (YOLOv5 expects RGB images)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Run object detection
    results = model(rgb_image)

    # Print raw detection output
    print(results.pandas().xyxy[0])

    # Run object detection
    results = model(rgb_image)

    # Draw bounding boxes
    for det in results.xyxy[0]:  # Each detection
        x1, y1, x2, y2, conf, cls = det.tolist()  # Convert tensor to list
        label = f"{results.names[int(cls)]} {conf:.2f}"

        # Draw rectangle
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(image, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save processed image to output folder
    output_path = os.path.join(output_folder, os.path.basename(img_path))
    cv2.imwrite(output_path, image)
    print(f"Processed: {output_path}")

print("✅ Object detection complete. Check the 'images_output' folder.")
