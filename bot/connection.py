import os
from dotenv import load_dotenv, find_dotenv
from web3 import Web3

def http_connection():
    # Load environment variables from .env file
    dotenv_path = find_dotenv()
    if dotenv_path:
        load_dotenv(dotenv_path)
    else:
        print(".env file not found. Ensure environment variables are set.")

    # Get the Ethereum node URL from environment variables
    NODE_URL = os.getenv("NODE_URL")
    if not NODE_URL:
        print("NODE_URL environment variable is not set.")
        return None

    # Initialize Web3 instance
    w3 = Web3(Web3.HTTPProvider(NODE_URL))

    # Check connection
    if w3.is_connected():
        print("✅ Connected to Ethereum HTTPS")
        return w3
    else:
        print("❌ Connection failure HTTPS")
        return None
