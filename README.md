# MS_Hackathon

This is our offical repo for the Microsoft Ai Agent Hackathon Project.


## Requirements

- Github Account
- Python 3.12+
- Azure Subscription
- Azure AI Foundry Account

## Initial Setup

1. Create a virtual environment in the specified directory by running the following command in your terminal:
```bash
python -m venv venv
```
2. Activate the virtual environment by running the following command in your terminal:
```bash
venv/scripts/activate
```
3. Create a `.env` file from the `.env.example` file by running the following command in your terminal:
```bash
cp .env.example .env
```
4. Install the Required Packages
Make sure the virtual environment is activated and then run the followning command in your terminal:
```bash
pip install -r requirements.txt
```
## Sign in to Azure using Keyless Authentication

Download **Azure CLI** 

Next, open a terminal and run `az login` or `az login --use-device-code` to sign into your Azure account.

Once you have logged in, select your subscription in the terminal.

## Running the Project
```bash
python main.py
```



