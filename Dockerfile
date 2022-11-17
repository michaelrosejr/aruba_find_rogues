FROM python:3.11-slim-bullseye AS python-base
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["/usr/local/bin/python", "./find_rogues/app.py"]
# CMD ["/bin/bash"]