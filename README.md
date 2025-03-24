# ZenithSolve Backend

## Project Overview
ZenithSolve Backend is a robust and scalable backend solution designed to handle complex business logic and data processing. It provides a set of APIs for various functionalities and ensures high performance and security.

## Features
- **User Authentication**: Secure user authentication and authorization.
- **Data Management**: Efficient data handling and storage.
- **API Endpoints**: Well-documented API endpoints for various operations.
- **Error Handling**: Comprehensive error handling mechanisms.
- **Logging**: Detailed logging for monitoring and debugging.
- **Testing**: Unit and integration testing using pytest.

## Project Structure
```
ZenithSolve-Backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── crud/
│   ├── db/
│   ├── routers/
│   ├── schemas/
├── config/
├── env/
├── htmlcov/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
```

## Tech Stack
- **Python**: Programming language
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for database interactions
- **Pytest**: Testing framework
- **Docker**: Containerization
- **Swagger**: API documentation
- **Uvicorn**: ASGI server

## Prerequisites
- **Python 3.8+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/).
- **PostgreSQL**: Ensure you have PostgreSQL installed and running. You can download it from [postgresql.org](https://www.postgresql.org/).
- **.env file**: Create a `.env` file in the root directory to store database variables. Use the provided `.env.example` as a reference.

## Setup Instructions
1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ZenithSolve-Backend.git
    cd ZenithSolve-Backend
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set environment variables**:
    Provide a `.env.example` file and set the necessary environment variables.

5. **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```

## Makefile Usage
The Makefile provides various commands for local testing, running code, linting, and pytest checks.

- **Run the application**:
    ```bash
    make start-local
    ```

- **Run ruff linting and pytest checks**:
    ```bash
    make precommit-check
    ```

## Docker Instructions
1. **Build the Docker image**:
    ```bash
    docker build -t zenithsolve-backend .
    ```

2. **Run the Docker container**:
    ```bash
    docker-compose up --build
    ```

## Swagger UI
Swagger UI is available for API testing. Once the application is running, navigate to `http://localhost:8000/docs` to access the Swagger UI.

## Unit Testing
Unit tests are written using pytest. To run the tests in VSCode:
1. Open the command palette (`Ctrl+Shift+P`).
2. Select `Python: Discover Tests`.
3. Run the tests using the test explorer.

## License Information
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
