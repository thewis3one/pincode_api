FROM python:3.9-slim
WORKDIR /usr
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0"  ]


