import torch
import cv2
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def run_ml_model(model_type):
    path = model_type + '.pt'
    model = torch.hub.load('yolov5', 'custom', path=path, source='local', verbose=False)
    model.conf = 0.08
    model.eval()
    
    extra_models = {}
    if model_type == "onion_cook":
        extra_models["fire"] = torch.hub.load('yolov5', 'custom', path="fire.pt", source='local', verbose=False)
    elif model_type == "knife_safety":
        extra_models["bloodstain"] = torch.hub.load('yolov5', 'custom', path="bloodstain.pt", source='local', verbose=False)
        extra_models["lacerations"] = torch.hub.load('yolov5', 'custom', path="lacerations.pt", source='local', verbose=False)
    
    for key in extra_models:
        extra_models[key].conf = 0.08
        extra_models[key].eval()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        exit()

    frame_count = 0
    previous_class = None
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(rgb_frame)
            
            extra_results = {}
            for key in extra_models:
                extra_results[key] = extra_models[key](rgb_frame)
            
            for det in results.xyxy[0]:
                x1, y1, x2, y2, conf, cls = det
                label = f"{results.names[int(cls)]} {conf:.2f}"
                class_name = label.split(" ")[0]
                confidence = float(label.split(" ")[1])
                
                if model_type == 'knife_safety':
                    if class_name == "unsafe" and confidence > 0.2:
                        frame_count += 1
                    else:
                        frame_count = 0
                    if frame_count > 5:
                        print("Warning: unsafe knife usage")
                
                if model_type == 'onion_cut':
                    if class_name == previous_class and confidence > 0.15:
                        frame_count += 1
                    else:
                        frame_count = 0
                    previous_class = class_name
                    if frame_count > 5:
                        print(f"Onion cut type: {class_name}")
                        break
                
                if model_type == 'onion_cook':
                    if class_name == previous_class and confidence > 0.15:
                        frame_count += 1
                    else:
                        frame_count = 0
                    previous_class = class_name
                    if frame_count > 5:
                        print(f"Onion cook type: {class_name}")
                        break
                
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            for key in extra_results:
                for det in extra_results[key].xyxy[0]:
                    x1, y1, x2, y2, conf, cls = det
                    label = f"{extra_results[key].names[int(cls)]} {conf:.2f}"
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            cv2.imshow('Ingredient & Safety Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\nChange ML model type")
    
    cap.release()
    cv2.destroyAllWindows()

previous_param = None
while True:
    user_input = input("Enter model type: ")
    if user_input != previous_param:
        print(f"Running {user_input}")
        run_ml_model(user_input)
        previous_param = user_input
    else:
        print("Parameter is the same as the previous one. No action taken.")
