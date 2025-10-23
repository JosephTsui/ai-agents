import os
from dotenv import load_dotenv

# Add references



# Clear the console
os.system('cls' if os.name=='nt' else 'clear')

# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")


# Connect to the agents client


with agents_client:


    # Create an agent to prioritize support tickets



    # Create an agent to assign tickets to the appropriate team



    # Create an agent to estimate effort for a support ticket



    # Create connected agent tools for the support agents

    

    # Create an agent to triage support ticket processing by using connected agents
    
    

    # Use the agents to triage a support issue



    # Clean up

