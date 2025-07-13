ARG PYTHON_VERSION=3.13.5

FROM python:${PYTHON_VERSION}-slim

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache --upgrade pip setuptools \
    && pip install -r requirements.txt

# Copying the source code into the container
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application
ENTRYPOINT [ "./entrypoint.sh", "--dev" ]
