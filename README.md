# Investor-Fund Transfer Service

This project provides a solution for transferring money from an investor's account to a fund's account, following specific criteria. It includes services for managing investors, funds, and transactions, with REST APIs exposed for each service.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dependencies](#dependencies)
3. [Installation](#installation)
4. [Running the Server](#running-the-server)
5. [Running Tests](#running-tests)
6. [Environment Variables](#environment-variables)
7. [API Documentation](#api-documentation)
8. [Postman Collection](#postman-collection)
9. [License](#license)

## Getting Started

To run this project locally, follow the instructions below.

## Dependencies

Ensure you have the following dependencies installed:

- **Python 3.8+**: The project is developed using Python, so ensure you have an appropriate version installed.
- **Django 3.2+**: A high-level Python Web framework.
- **PostgreSQL**: The database used for storing investor and fund data.
- **Redis**: For caching and queuing purposes.
- **RabbitMQ**: For handling asynchronous tasks.
- **Virtualenv**: Recommended for creating an isolated Python environment.

# API Documentation

This project includes a Postman collection for testing and interacting with our API.

## Postman Collection

You can find the Postman collection [here]([<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/19779588-a4357600-f859-4daf-8716-3f16a5556418?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D19779588-a4357600-f859-4daf-8716-3f16a5556418%26entityType%3Dcollection%26workspaceId%3D27296c38-f34b-4fd1-8892-8000a4758b24)). It contains all the endpoints with example requests and responses.

### How to Use

1. **Import the Collection:** 
   - Download the JSON file from the link above.
   - In Postman, click on "Import" and select the downloaded file.

2. **Authentication:**
   - The API requires authentication. Please use your API key in the headers for each request.

3. **Available Endpoints:**
   - **GET /api/resource**: Description of the endpoint.
   - **POST /api/resource**: Description of the endpoint.
   - ...

## Postman Public Workspace

If you prefer, you can access our Postman public workspace directly by clicking the badge below:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://www.postman.com/link-to-your-public-workspace)


