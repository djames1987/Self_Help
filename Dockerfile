FROM python:3
ENV DockerHOME=/home/app/
RUN mkdir -p $DockerHOME
WORKDIR $DockerHOME
COPY ./requirements.txt .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PWMUSER="pwm"
ENV PWMPASS="xKFvqz3FWZPHTl65253s"
RUN pip install --upgrade pip
COPY . $DockerHOME
RUN pip install -r requirements.txt
EXPOSE 8001
COPY . .