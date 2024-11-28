# Weather-API

A weather API that fetches and returns weather data.

project exersice url = `https://roadmap.sh/projects/weather-api-wrapper-service`

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)

## Introduction

Weather-API is a simple Flask-based API that fetches weather data from the Visual Crossing Weather API and caches it using Redis. It provides endpoints to retrieve weather information for different cities.

## Features

- Fetches weather data from the Visual Crossing Weather API.
- Caches weather data in Redis to improve performance.
- Provides a simple RESTful API to access weather data.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/roxxe3/weather-api.git
    cd weather-api
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    Create a `.env` file in the root directory and add your Visual Crossing Weather API key:
    ```env
    api_key=YOUR_API_KEY
    ```

## Usage

1. Run the Flask application:
    ```sh
    python weather_api.py
    ```

2. The API will be available at `http://127.0.0.1:5000`.

## Endpoints

- `GET /weather/<city>`: Fetches and returns weather data for the specified city.

## Environment Variables

- `api_key`: Your Visual Crossing Weather API key.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
