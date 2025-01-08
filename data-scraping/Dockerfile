# Dockerfile, Image, Container
# Dockerfile: Blueprint for building images
# Image: Template for running Containers
# Container: the actual running process with the package project

FROM python:3.12

ADD main.py .

# urllib is built-in so you don't have to install it here
RUN pip install requests httpx recipe_scrapers 

CMD [ "python", "./recipe_lib_test.py" ]
