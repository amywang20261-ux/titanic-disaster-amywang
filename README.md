# Titanic — Survival Prediction (MLDS 400)

This project trains a **logistic-regression** baseline to predict Titanic survival. It includes a **Python** pipeline (primary) and a matching **R** pipeline, each runnable in Docker.  
**Datasets are NOT committed**—you will download them yourself and place them locally.


**Step 1 — Repository layout**


.
├─ src/

│ ├─ pipeline/ # Python app (Dockerfile, main.py, helpers)

│ ├─ r-pipeline/ # R app (Dockerfile, install_packages.R, script.R)

│ └─ data/ # place train/test here (kept by .gitkeep)

├─ requirements.txt

├─ .gitignore

└─ README.md

`src/data/` exists but actual files are ignored by Git to keep the repo clean.



**Step 2 — Get the data (not included)**

Download the Kaggle Titanic files and place them here:

src/data/

├─ train.csv

└─ test.csv

If your files are named differently, pass the names via env vars or CLI args when running (see “Run the Python container”).


**Step 3 — Build the Python container**

From the repo root:

(A) Build the Python image

docker build -f src/pipeline/Dockerfile -t titanic-app .

(B) Confirm the image exists

docker images | grep titanic-app

What the image does

-Installs dependencies from requirements.txt

-Copies the Python pipeline

-Sets the default command to run the training & prediction script



**Step 4 — Run the Python container (with local data)**

Mount your local src/data into the container and write predictions back to it:

Default file names (train.csv, test.csv) in src/data/

docker run --rm \

  -v "$(pwd)/src/data:/app/data" \
  
  titanic-app

Custom file names (optional):

docker run --rm \

  -v "$(pwd)/src/data:/app/data" \
  
  -e TRAIN_FILE=train.csv \
  
  -e TEST_FILE=test.csv  \
  
  -e PREDICTIONS_FILE=predictions.csv \
  
  titanic-app

Expected outputs

Console prints: data load confirmation, fit summary, accuracy/metrics

File: src/data/predictions.csv with PassengerId,Survived


**Step 5 — Build & run the R container (Part 4)**

(A) Build R image (Dockerfile is in src/r-pipeline)

docker build -f src/r-pipeline/Dockerfile -t titanic-r .

(B) Run R pipeline, mounting the same data folder

docker run --rm \

  -v "$(pwd)/src/data:/app/data" \
  
  titanic-r

The R container should read the same train.csv/test.csv and write predictions.csv to src/data/.


**Step 6 — Reproducibility notes**

No data in repo: .gitignore excludes src/data/* while keeping a placeholder .gitkeep.

Determinism: set seeds inside the scripts if your instructor requires exact reproducibility.

Python versions: base image is pinned in src/pipeline/Dockerfile (e.g., python:3.10-slim).

R packages: installed from install_packages.R inside the R image.



**Appendix — Helpful commands (bash)**

Clean old images/containers

docker ps -a

docker rm -f <container_id>

docker rmi <image_id>

Rebuild without cache

docker build --no-cache -f src/pipeline/Dockerfile -t titanic-app .

Compose (both services)

docker compose up --build

docker compose down
