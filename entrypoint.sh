#!/bin/bash

DEV=false # Default value

# Parse the --dev argument
for arg in "$@"; do
    case $arg in
        --dev)
            DEV=true
            shift
            ;;
        --dev=*)
            DEV="${arg#*=}"
            shift
            ;;
        *)
            echo "Unknown argument: $arg"
            exit 1
            ;;
    esac
done

# Check the value of DEV and perform respective actions
if [[ "$DEV" == "true" ]]; then
    echo "Running in development mode..!!"
    python manage.py makemigrations --no-input
    python manage.py migrate
    python manage.py runserver 0.0.0.0:8000

elif [[ "$DEV" == "false" ]]; then
    echo "Running in deployment mode..!!"
    python manage.py makemigrations --no-input
    python manage.py migrate
    python manage.py collectstatic --no-input
    gunicorn --bind 0.0.0.0:8000 core.wsgi

else
    echo "Error: Please specify --dev=true or --dev=false"
    exit 1
fi
