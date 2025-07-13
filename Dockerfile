# Based on https://www.docker.com/blog/how-to-dockerize-django-app/

# Use the official Python runtime image
FROM python:3.13-slim
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip 

# Set the working directory inside the container
WORKDIR /app
 
# Copy the Django project and install dependencies
COPY requirements.txt .
 
# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the Django project to the container
COPY . .
 
# # Run Django’s development server
# CMD ["python", "generate-fake-ldif.py", "10"]

ENTRYPOINT ["python", "generate-fake-ldif.py"]
CMD ["1", "example.com", "br"]
