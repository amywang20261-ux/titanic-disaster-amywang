FROM python:3.10-slim
WORKDIR /app

# install deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy your source
COPY src/ ./src/

# run your script
CMD ["python", "src/app/main.py"]
