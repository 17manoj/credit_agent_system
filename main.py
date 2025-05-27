from agents.developer_agent import DeveloperAgent
from agents.governance_agent import GovernanceAgent
from dotenv import load_dotenv


load_dotenv(".env",override=True)

import os
api_key = os.getenv("OPENAI_API_KEY")

# print("API key ---- >  ",api_key)
def main():
    # Step 1: Governance reads PDF
    governance = GovernanceAgent("pdfs/ifrs9_excerpt.pdf")
    gov_summary = governance.read_regulation()

    # Step 2: Developer interprets YAML + governance and generates code
    agent = DeveloperAgent("data/credit_data.csv", "guidance/human_guidance.yaml")
    agent.run()

if __name__ == "__main__":
    main()
