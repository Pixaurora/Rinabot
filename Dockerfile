FROM python:3
WORKDIR /src/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
