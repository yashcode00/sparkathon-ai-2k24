FROM python:3.9

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./AI_hackathon /app
COPY ./AI_hackathon/packages.txt /

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    build-essential \
    curl \
    software-properties-common \
    git \ 
    && rm -rf /var/lib/apt/lists/* 


RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]