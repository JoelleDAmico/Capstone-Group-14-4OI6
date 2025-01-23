# Dockerfile, Image, Container
# Dockerfile: Blueprint for building images
# Image: Template for running Containers
# Container: the actual running process with the package project

FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt ${LAMBDA_TASK_ROOT}

# urllib is built-in so you don't have to install it here
RUN pip install -r requirements.txt

COPY main.py ${LAMBDA_TASK_ROOT}
# Set the command to handler
CMD [ "main.handler" ]
