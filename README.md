# LRS Connector

LRS Connector is a lightweight FastAPI application designed to act as a proxy for querying Learning Record Stores (LRS) such as Learning Locker or Ralph, from the DataSpace. It handles pagination to retrieve all statements that match a query, providing a seamless interface for interacting with your LRS.

## Features

- **Proxy Requests**: Forward GET requests to your LRS.
- **Pagination Handling**: Automatically manage paginated responses to retrieve all statements.

## Getting Started

### Prerequisites

- Docker
- Docker Compose (optional, for multi-container setups)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/inokufu/lrs-connector.git
   cd lrs-connector
   ```
2. **Using Docker**

   Using docker, <ENV> variable can take the `dev` or `prod` values.

   - **Build the Docker image**:
      ```bash
      docker compose -f docker-compose.yml -f docker-compose.<ENV>.yml build
      ```

   - **Run the Docker container**:
      ```bash
      docker compose -f docker-compose.yml -f docker-compose.<ENV>.yml up -d
      ```

3. **Locally**
   - **Using pip**: `pip install -r requirements.lock`
   - **Using rye**: `rye sync`

### Usage

- **Endpoint**: `/statements`
  - Method: `GET`
  - Description: Proxy requests to the LRS and handle pagination.
  - Headers:
    - `X-Experience-API-Endpoint`: Base URL of your LRS.
    - `X-Experience-API-LRS`: Type of LRS (`learninglocker` or `ralph`), `learninglocker` is the default value.
    - All other headers will be passed to the query sent by this application, except for the `host`.

### Example Request

```bash
curl -H "X-Experience-API-Endpoint: https://lrs.example.com" \
     -H "X-Experience-API-LRS: learninglocker" \
     "http://localhost/statements?param1=value1"
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please contact [guillaume.lefebvre@inokufu.com](mailto:guillaume.lefebvre@inokufu.com).
