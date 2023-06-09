# Variables
IMAGE_NAME = my-scraping-app
CONTAINER_NAME = my-scraping-container
APP_PORT = 8000

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -d --name $(CONTAINER_NAME) -p $(APP_PORT):$(APP_PORT) $(IMAGE_NAME)

# Stop the Docker container
stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

# Remove the Docker image
clean:
	docker rmi $(IMAGE_NAME)

# Run the application
app:
	uvicorn app:app --host 0.0.0.0 --port $(APP_PORT)

# Shortcut for building the image, running the container, and starting the application
start: build run app

# Help command to display available targets
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  build      Build the Docker image"
	@echo "  run        Run the Docker container"
	@echo "  stop       Stop the Docker container"
	@echo "  clean      Remove the Docker image"
	@echo "  app        Run the application locally"
	@echo "  start      Build, run, and start the application"
	@echo "  help       Display this help message"