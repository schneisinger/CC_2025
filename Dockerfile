FROM python:3.11-slim

WORKDIR /code

# Copy and install dependencies
COPY ./dependencies.txt /code/dependencies.txt
RUN pip install --no-cache-dir --upgrade -r /code/dependencies.txt

# Copy the code 
COPY ./main.py /code/

# Run the Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]