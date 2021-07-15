FROM python:3.9-slim
WORKDIR /usr
COPY main.py .
RUN pip install fastapi && pip install uvicorn
ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0"  ]


