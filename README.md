# Asynchronous Crypto Monitor

## Overview

This service monitors cryptocurrency prices asynchronously and exposes a REST API built with **FastAPI**. It fetches price data from the CoinGecko API via **aiohttp**, caches it in memory and serves it through HTTP endpoints. The application is structured into modules using a clean architecture approach and uses **Pydantic** for data validation.

## Features

- Asynchronous HTTP requests using `aiohttp` to avoid blocking operations.
- Background task that periodically fetches prices for configured coins.
- REST API to retrieve all cached prices or a specific coin's price.
- Strong typing and validation with Pydantic models.
- Configurable polling interval and coin list (see `app/main.py`).
- Logging configured with Python's `logging` module.
- Ready for deployment with a provided `Dockerfile`.

## Architecture Overview

The project uses a modular structure for clarity and maintainability:

```
auto-generated-crypto-monitor/
├── app/
│   ├── main.py      # FastAPI application and route definitions
│   ├── models.py    # Pydantic models for API responses
│   └── services.py  # CryptoMonitor class handling background tasks
├── requirements.txt # Python dependencies
├── Dockerfile       # Container build instructions
└── README.md        # Project documentation
```

### Modules

* **app/main.py** – Creates the FastAPI instance, configures logging and defines the `/prices` and `/prices/{coin_id}` routes. On startup it launches a background task that periodically updates price data.
* **app/services.py** – Defines the `CryptoMonitor` class which fetches price data from the CoinGecko API using aiohttp and caches it. It provides methods to retrieve the latest cached prices.
* **app/models.py** – Contains the `PriceData` Pydantic model used for API responses.

## Installation & Usage

1. Clone the repository:

```bash
git clone https://github.com/okaloopen/auto-generated-crypto-monitor.git
cd auto-generated-crypto-monitor
```

2. (Optional) Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive documentation is served at `/docs` (Swagger UI) and `/redoc`.

## API Documentation

| Method | Path               | Description                                                |
|------:|--------------------|------------------------------------------------------------|
| GET   | `/prices`          | Returns a list of latest price data for all monitored coins |
| GET   | `/prices/{coin_id}`| Returns the latest price for a specific coin               |

## Docker Deployment

To build and run the service in a container:

```bash
docker build -t crypto-monitor:latest .
docker run --rm -p 8000:8000 crypto-monitor:latest
```

## License

This project is released under the MIT License.
