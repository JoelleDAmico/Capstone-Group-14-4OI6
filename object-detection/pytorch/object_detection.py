import time

import torch
import numpy as np
from torchvision import models, transforms

import cv2
from PIL import Image

#torch.backends.quantized.engine = 'qnnpack'
torch.backends.quantized.engine = 'fbgemm'

with open("imagenet1000_clsidx_to_labels.txt", "r") as f:
    classes = eval(f.read())

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
# cap.set(cv2.CAP_PROP_FPS, 36)

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

net = models.quantization.mobilenet_v3_large(weights='MobileNet_V3_QuantizedWeights.IMAGENET1K_FBGEMM')
# jit model to take it from ~20fps to ~30fps
net = torch.jit.script(net)

started = time.time()
last_logged = time.time()
frame_count = 0

with torch.no_grad():
    while True:
        # read frame
        ret, image = cap.read()
        if not ret:
            raise RuntimeError("failed to read frame")
        
        cv2.imshow("Original Video", image)
        cv2.waitKey(1) == ord('q')

        # convert opencv output from BGR to RGB
        image = image[:, :, [2, 1, 0]]
        permuted = image

        # preprocess
        input_tensor = preprocess(image)

        # create a mini-batch as expected by the model
        input_batch = input_tensor.unsqueeze(0)

        # run model
        output = net(input_batch)
        # do something with output ...

        top = list(enumerate(output[0].softmax(dim=0)))
        top.sort(key=lambda x: x[1], reverse=True)
        for idx, val in top[:10]:
            print(f"{val.item()*100:.2f}% {classes[idx]}")  