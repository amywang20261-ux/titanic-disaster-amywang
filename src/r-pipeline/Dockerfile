FROM rocker/r-base:4.3.2

WORKDIR /app

# install R packages first (better layer caching)
COPY src/r-pipeline/install_packages.R /app/install_packages.R
RUN Rscript /app/install_packages.R

# bring in source tree so paths exist; data will be bind-mounted at runtime
COPY src /app/src

# run the R script
CMD ["Rscript", "/app/src/r-pipeline/main.R"]
