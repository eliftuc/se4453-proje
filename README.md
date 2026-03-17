# SE4453 Midterm Project - Group 11 

This project is a secure web application deployment developed for the SE4453 Midterm Project. The application runs on Azure App Service, manages secrets via Azure Key Vault, and establishes a secure database connection to PostgreSQL over a private network.

## 👥 Group Members
23070006117 - Elif Tuç - 18070006030 - Sıla Barışık

## ⚙️ Project Configuration (Configuration 8)
Our project is deployed strictly following Configuration 8 as specified in the guidelines:
**Git Workflow:** Feature Based
**App Service:** App Service - CLI - Private
**PostgreSQL:** PostgreSQL - Portal - Private (Over VM SSH)
**Secret Management:** KeyVault - Portal - Service Endpoint

## 🛠️ Technologies Used
* **Backend:** Python 3, Flask
* **Database:** PostgreSQL
* **Cloud Provider:** Microsoft Azure
* **Security:** Azure Identity, Azure Key Vault SDK

## 🔗 Endpoints
* `/` : Welcome page.
* `/hello` : The mandatory endpoint required by the guidelines. When triggered, the application fetches database credentials from Key Vault and successfully connects to the PostgreSQL database.