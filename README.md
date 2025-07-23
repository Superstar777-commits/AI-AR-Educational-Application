# AI-AR-Educational-Application

## Architecture:

This is a mono repo (monolithic repository), which means it contains both client and server codebases

### Pre-requisites (NB):

- For the frontend:
    - Node.js from [nodejs.org](https://nodejs.org/en)
    - npm (comes with Node.js)
- For the backend:
    - Python 3 from [python.org](https://www.python.org/)
    - pip (comes with your Python installation)

### Client (Frontend)

- React
- TypeScript
- React Router
- Shadcn

### Server (Backend)

- Python (with virtual environment)
- FastAPI
- SQLAlchemy

### To Run This Application

1. Clone this repo into a directory
2. From the root folder (quiz)
    1. Run ```npm install``` to install [concurrently](https://www.npmjs.com/package/concurrently) to the monorepo
    2. Run ```npm run install:all``` which will install all packages for both client and server
        - For the Python virtual environment, there is ```install:server:windows``` and ```install:server:unix``` based on your OS
        - It will run the Windows one and if it doesn't work, it'll run the Unix one
    3. Then run ```npm run dev:all``` (similar logic as ```install:all```)
3. App is now running with both client and server running on different ports!

## NB!!!

If the npm scripts don't work, you may have to manually go into each folder and run specific commands
- For client, this would be ```npm install```
- For server, this would be having to start the virtual environment (which is different based on your OS, ask ChatGPT, Gemini, or Google search), then using pip to install from the requirements.txt file

If having problems with Uvicorn not reloading after saving changes to a file
- run this command in CMD: ```tasklist /FI "IMAGENAME eq python.exe"```, then run this command ```taskkill /PID <PROCESS_ID>  /F``` using the process IDs listed out
- Make sure you're running the server on Command Prompt and not Git Bash
- Otherwise use ```npm run dev:server_alt``` which will use FastAPI directly (still make sure you're using Command Prompt)

### For API Testing

FastAPI provides a Swagger and a ReDoc UI to test the Python API with, read more about it [here](https://fastapi.tiangolo.com/#interactive-api-docs)