# CC_2025 - Animal Picture App 

## Description 

A simple microservice, that fetches a random picture of a fox, a dog, or a bear, and saves it to a database. The last picture can be shown on a simple UI.  
The App is using the follwing external APIs: 
*Fox: https://randomfox.ca/floof/ 
*Dogs: https://place.dog/300/200 
*Bear: https://placebear.com/200/300 

## How to run it
- Using Docker 
    1. Open the project directory. 
    2. Build and run the container: 
        docker compose up --build 

- Running locally 
    1. Create a virtual environment in the project directory: 
        python3 -m venv env
    2. Activate the venv: 
        source env/bin/activate
    3. Install dependencies: 
        pip install -r dependencies.txt
    4. Start the uvicorn server: 
        uvicorn main:app --reload

## Access the application
- A simple frontend will be available at: 
    http://localhost:8000/ 
- The automatic API documentation from FastAPI will be available at: 
    http://localhost:8000/docs 

## Roadmap 
- Use environment variables for configuration. 
- Add automated testing. 
- Use async functions. 
- Style the frontend. 
- Add some authentification and logging. 
- Different databse for production. 

