import torch
import cv2
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def run_ml_model(model_type):
    '''
    DANGER_CODES = {
    1: "FIRE",
    2: "CHOPPING TECHNIQUE",
    3: "LACERATION",
    4: "BURNS"
    }
    '''
    # conf_required = 0.08
    path = model_type + '.pt'
    print(f"Loading {model_type} model")
    model = torch.hub.load('yolov5', 'custom', path=path, source='local', verbose=False)
    model.conf = 0.4
    model.eval()
    
    extra_models = {}
    if model_type == "onion_cook":
        print("Loading Fire Model\n")
        extra_models["fire"] = torch.hub.load('yolov5', 'custom', path="fire.pt", source='local', verbose=False)
    elif model_type == "knife_safety":
        print("Loading Blood Model\n")
        extra_models["bloodstain"] = torch.hub.load('yolov5', 'custom', path="bloodstain.pt", source='local', verbose=False)
        print("Loading Cut Model\n")
        extra_models["lacerations"] = torch.hub.load('yolov5', 'custom', path="lacerations.pt", source='local', verbose=False)
    
    for key in extra_models:
        extra_models[key].conf = 0.60
        extra_models[key].eval()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        exit()

    frame_count = 0
    previous_class = None
    
    
    try:
        while True:
            # globally watched variables
            interrupt_active = False
            interrupt_code = None
            current_result = None
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
                        interrupt_active = True
                        interrupt_code = 2
                        print("WARNING: unsafe knife handling")
                
                if model_type == 'onion_cut':
                    if class_name == previous_class and confidence > 0.15:
                        frame_count += 1
                    else:
                        frame_count = 0
                    previous_class = class_name
                    if frame_count > 5:
                        current_result = class_name
                        print(f"Onion cut type: {class_name}")
                        break
                
                if model_type == 'onion_cook':
                    if class_name == previous_class and confidence > 0.15:
                        frame_count += 1
                    else:
                        frame_count = 0
                    previous_class = class_name
                    if frame_count > 5:
                        current_result = class_name
                        print(f"Onion cook type: {class_name}")
                        break
                
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            for key in extra_results:
                for det in extra_results[key].xyxy[0]:
                    x1, y1, x2, y2, conf, cls = det
                    label = f"{extra_results[key].names[int(cls)]} {conf:.2f}"
                    class_name = label.split(" ")[0]
                    if class_name == "fire":
                        interrupt_active = True
                        interrupt_code = 1
                        print("WARNING: fire!")

                    if class_name == "lacerations" or class_name == "bloodstains":
                        interrupt_active = True
                        interrupt_code = 3
                        print("WARNING: injury!")
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            cv2.imshow('Ingredient & Safety Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\nChange ML model type")
    
    cap.release()
    cv2.destroyAllWindows()

def keyword_checker(sentence: str):
    """
    Checks if a sentence contains specific keywords and returns a number based on the keyword found.
    """
    keywords = {
        "finely": "finely_dice",
        "roughly": "roughly_slice",
        "slice": "slice",
        "blonde": "blonde",
        "golden": "golden",
        "caramelize": "caramelized"
    }
    
    for word, value in keywords.items():
        if word in sentence.lower():  # Case insensitive match
            return value
    
    return 0  # Return 0 if no keyword is found

'''

# yahya's variable: global variable user_input
user_input = None
current_result = None
interrupt_active = False
interrupt_code = None

# TODO: interrupt handling
# INSTRUCTION #1
sentence = "finely dice onions"
result = keyword_checker(sentence)
if result == "finely_dice" or result == "roughly_slice" or result == "slice": # onion cutting instruction
    model_type = "knife_safety"
    while True:
        run_ml_model(model_type)
        user_input = input("User input: ").strip().lower()
        if user_input == "next":
            break 
    print("Checking onion cut...")
    model_type = "onion_cut"
    while True:
        run_ml_model(model_type)
        if current_result == result: # user correctly diced onions
            break 

# INSTRUCTION #2
sentence = "cook onions until golden"
result = keyword_checker(sentence)
if result == "blonde" or result == "golden" or result == "caramelized": # onion cooking instruction
    model_type = "onion_cook"
    while True:
        run_ml_model(model_type)
        if current_result == result: # onions are done cooking
            # TODO: add opinion to keep cooking (ensure they don't burn) ACTUALLY no we shouldn't, lets discuss
            break 
        if user_input == "next":
            # "onions are not fully cooked yet, are you sure you want to process"
            if user_input == "yes":
                break
            
'''



previous_param = None
while True:
    user_input = input("Enter model type: ")
    if user_input != previous_param:
        print(f"Running {user_input}")
        run_ml_model(user_input)
        previous_param = user_input
    else:
        print("Parameter is the same as the previous one. No action taken.")
