# Import libraries
import torch
import cv2
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def run_ml_model(model_type):
    # Load a custom model trained on ingredients (e.g., vegetables, fruits, herbs, meats)
    # Replace 'custom_model_path' with the path to your trained model
    path = model_type + '.pt'
    model = torch.hub.load('yolov5', 'custom', path=path, source='local', verbose = False)
    model.conf = 0.08
    model.eval()

    # Initialize the video capture (webcam)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        exit()

    frame_count = 0
    previous_class = None
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the image from BGR (OpenCV format) to RGB (for PyTorch model)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform detection
            results = model(rgb_frame)

            if model_type == "onion_cook":
                model2 = torch.hub.load('yolov5', 'custom', path="fire.pt", source='local', verbose = False)
                model2.conf = 0.08
                model2.eval()
                results2 = model2(rgb_frame)
            
            if model_type == "knife_safety":
                model2 = torch.hub.load('yolov5', 'custom', path="bloodstain.pt", source='local', verbose = False)
                model2.conf = 0.08
                model2.eval()
                results2 = model2(rgb_frame)
                model3 = torch.hub.load('yolov5', 'custom', path="lacerations.pt", source='local', verbose = False)
                model3.conf = 0.08
                model3.eval()
                results3 = model3(rgb_frame)

            # Draw bounding boxes and labels on the original frame
            for det in results.xyxy[0]:  # each detection
                x1, y1, x2, y2, conf, cls = det  # Unpack detection values
                label = f"{results.names[int(cls)]} {conf:.2f}"
                #print(label)

                class_name = label.split(" ")[0]
                confidence = float(label.split(" ")[1])
                #print(f'frame count{frame_count}')


                if model_type == 'knife_safety':
                    if class_name == "unsafe" and confidence > 0.2:
                        frame_count+=1 
                    else:
                        frame_count = 0
                    if frame_count > 5:
                        print("warning: unsafe knife usage")


                if model_type == 'onion_cut':
                    if class_name == previous_class and confidence > 0.15: # finely_dice #slice
                        frame_count+=1 
                    else:
                        frame_count = 0
                    previous_class = class_name
                    if frame_count > 5:
                        print(f"onion cut type: {class_name}")
                        break
                

                
                if model_type == 'onion_cook':

                    if class_name == previous_class and confidence > 0.15:
                        frame_count+=1 
                    else:
                        frame_count = 0
                    previous_class = class_name
                    if frame_count > 5:
                        print(f"onion cook type: {class_name}")
                        break

                # Draw rectangle and label
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display the frame with detections
            cv2.imshow('Ingredient Detection', frame)

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    except KeyboardInterrupt:
        print("\nChange ML model type")
    
    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# model_type ["onion_cook", "onion_cut", "knife_safety"]

previous_param = None
while True:
    # Prompt the user for input
    user_input = input("Enter model type: ")

    if user_input != previous_param:
        # Run the function with the new parameter
        print(f"Running {user_input}")
        run_ml_model(user_input)
        previous_param = user_input  # Update the previous parameter
    else:
        print("Parameter is the same as the previous one. No action taken.")