# Investor-Fund Transfer Service

This project provides a solution for transferring money from an investor's account to a fund's account, following specific criteria. It includes services for managing investors, funds, and transactions, with REST APIs exposed for each service.


## Getting Started

To run this project locally, follow the instructions below.

## Dependencies

Ensure you have the following dependencies installed:

- **Python 3.8+**: The project is developed using Python, so ensure you have an appropriate version installed.
- **Django 3.2+**: A high-level Python Web framework.
- **Virtualenv**: Recommended for creating an isolated Python environment.

# Within your IDE Terminal
- 1. Run **source myenv/bin activate** - This will ensure that you are within the virtual environment
  2. Once you ensure that you are within the Fintech app, run ** python ./manage.py runserver** - This will start your local development server
  3. Split a 2nd Terminal and Run **python ./manage.py makemigrations** && **python ./manage.py migrate** to validate that the latest migrations have ran
  4. You can simply run the Postman Collections' Endpoints now that you have a local server running and the latest migrations in place to generate dummy data

# API Documentation

This project includes a Postman collection for testing and interacting with our Service-based APIs.

## Postman Collection

Run this Postman collection once your local server is running [<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/19779588-a4357600-f859-4daf-8716-3f16a5556418?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D19779588-a4357600-f859-4daf-8716-3f16a5556418%26entityType%3Dcollection%26workspaceId%3D27296c38-f34b-4fd1-8892-8000a4758b24)
It contains all the endpoints with example requests and responses.

### How to Use

1. **Run the Collection:** 
   - Click the Postman button above.
   - In Postman, add it to your existing Workspace and can immediately run after the four basic commands below.
   - Ensure 

2. **Available Endpoints:**
   - **POST /v1/financing/withdrawal/**: The Investor Service API will sends the withdrawal request, checks the investor's balance and processes the withdrawal. If successful, it triggers a transfer request to the Transaction Service.
   - **POST /v1/financing/transfer/**: The Transaction Service validates the transfer request, ensuring that all of the fund's criteria are met via the Fund Service. Once the Fund service verifies the minimum investment threshold, seat availability, and other criteria, it will process the fund transer and update both the investor and fund balances. Notifications are then sent to relevant parties upon the successful completion.
