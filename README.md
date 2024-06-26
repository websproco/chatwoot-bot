# Chatwoot Bot

This is a FastAPI application that integrates with Chatwoot to provide an assistant API endpoint. It's designed to handle various Chatwoot events and can be easily deployed using Docker or Docker Compose.

## Prerequisites

- Python 3.9
- Docker and Docker Compose (for containerization and easy deployment)

## Setup

1. Clone the repository.
2. Install the dependencies by running `pip install -r requirements.txt`.
3. Set up the required environment variables in the [`.env`] file. You will need to provide values for:
   - `CHATWOOT_BASE_URL`
   - `CHATWOOT_API_KEY`
   - `ACCOUNT_ID`
   - `CELERY_BROKER_URL`
   - `CELERY_RESULT_BACKEND`

## Running the Application Locally

To run the application locally, use the command:

```sh
uvicorn app.main:app --reload
```

## Running with Docker

To build and run the application as a Docker container, execute:

```sh
docker build -t chatwoot-bot .
docker run -p 8000:8000 chatwoot-bot
```

## Running with Docker Compose

For ease of deployment, especially when working with Celery and Redis, you can use Docker Compose:

```sh
docker-compose up --build
```

This command builds the images if they don't exist and starts the services defined in `docker-compose.yml`, including the web application, worker, Redis, and the Flower dashboard for Celery.

## Environment Variables

Ensure the following environment variables are set in your `.env` file or Docker environment:

- `CHATWOOT_BASE_URL`: The base URL of your Chatwoot instance.
- `CHATWOOT_API_KEY`: The API key for your Chatwoot instance.
- `ACCOUNT_ID`: The account ID for your Chatwoot instance.
- `CELERY_BROKER_URL`: The URL for the Celery broker (Redis).
- `CELERY_RESULT_BACKEND`: The URL for the Celery result backend (Redis).

## GitHub Actions for Docker

This project is configured with GitHub Actions to automatically build and publish the Docker image to DockerHub upon pushes to the `main` branch. Ensure you have the following secrets set in your GitHub repository:

- `DOCKERHUB_USERNAME`: Your DockerHub username.
- `DOCKERHUB_TOKEN`: Your DockerHub token.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## Issues

If you encounter any problems with this application, please open an issue on the GitHub repository.