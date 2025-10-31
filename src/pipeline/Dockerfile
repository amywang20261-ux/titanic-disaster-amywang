FROM python:3.10-slim
WORKDIR /app

# install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy your code and data into the image
COPY src/pipeline/ /app/pipeline/
COPY src/data/ /app/data/

# run your script from the pipeline folder
CMD ["python", "/app/pipeline/main.py"]