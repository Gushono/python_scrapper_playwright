# Use the official Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the poetry.lock and pyproject.toml files
COPY poetry.lock pyproject.toml ./

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Install Playwright and its dependencies
RUN pip install playwright \
    && playwright install \
    && playwright install-deps


# Copy the rest of the application code
COPY . .

# Expose the port that FastAPI will be running on
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]