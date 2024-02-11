# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /flaskr

# Copy the rest of the application code to the container
COPY . .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables
# ENV FLASK_APP=""
# ENV FLASK_DEBUG=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose port 5000 for the Flask development server to listen on
# EXPOSE 5000
EXPOSE 8000

# Define the command to run the Flask development server
# CMD ["flask", "run", "--host=0.0.0.0"]
# ENTRYPOINT FLASK_APP=/opt/flaskr/app.py flask run -h 0.0.0.0
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "app.app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
CMD uvicorn flask:create_app --host 0.0.0.0 --port 8000