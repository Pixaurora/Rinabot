FROM python:3
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY run.py .
COPY config.yaml .
CMD ["python", "run.py"]
