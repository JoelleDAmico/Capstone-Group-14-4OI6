
from roboflow import Roboflow
rf = Roboflow(api_key="NJEg6gKJblyK6o9Lcshg")
project = rf.workspace("katei").project("comida3.0")
version = project.version(1)
dataset = version.download("yolov5")
                