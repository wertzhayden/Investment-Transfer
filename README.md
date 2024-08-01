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
1. **Create and Activate Virtual Environment:**
```bash
virtualenv myenv
source myenv/bin/activate
```
2. **Apply Migrations (Within FinTech App):**
```bash
python ./manage.py makemigrations
python ./manage.py migrate
```
3. **Start Local Development Server**
```bash
   python ./manage.py runserver
```

# API Documentation

This project includes a Postman collection for testing and interacting with our Service-based APIs.

## Postman Collection

Run this Postman collection once you have the latest migrations and local server running.

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/19779588-a4357600-f859-4daf-8716-3f16a5556418?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D19779588-a4357600-f859-4daf-8716-3f16a5556418%26entityType%3Dcollection%26workspaceId%3D27296c38-f34b-4fd1-8892-8000a4758b24)

It contains all the endpoints with example requests and responses.

### How to Use

1. **Run the Collection:** 
   - Click the Postman button above.
   - In Postman, add it to your existing Workspace and can immediately run after the commands above.
  
### Key Endpoints

#### Investor Withdrawal
- **Endpoint:** `POST /v1/financing/withdrawal/`
- **Description:** Sends a withdrawal request, checks the investor's balance, and processes the withdrawal. If successful, it triggers a transfer request to the Transaction Service.

#### Fund Transfer
- **Endpoint:** `POST /v1/financing/transfer/`
- **Description:** The Transaction Service validates the transfer request, ensuring all fund criteria are met via the Fund Service. Upon verification, it processes the fund transfer and updates both the investor and fund balances. Notifications are sent to relevant parties upon successful completion.

This README provides an overview and setup instructions for the Investor-Fund Transfer Service. For detailed API specifications and usage, refer to the Postman collection linked above.
