# Import libraries
import torch
import cv2

# Load a pre-trained YOLOv5 model
# You can replace 'yolov5s' with other YOLOv5 models like 'yolov5m', 'yolov5l', etc.
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.eval()

# Initialize the video capture (webcam)
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image from BGR (OpenCV format) to RGB (for PyTorch model)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform detection
    results = model(rgb_frame)

    # Draw bounding boxes and labels on the original frame
    for det in results.xyxy[0]:  # each detection
        x1, y1, x2, y2, conf, cls = det  # Unpack detection values
        label = f"{results.names[int(cls)]} {conf:.2f}"

        # Draw rectangle and label
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
        cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Display the frame with detections
    cv2.imshow('Object Detection', frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
