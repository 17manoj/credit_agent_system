import os
import pandas as pd
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from agents.governance_agent import GovernanceAgent
from utils.utils import read_yaml_config, save_code_to_file, extract_code
from dotenv import load_dotenv
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import ast

load_dotenv()

class DeveloperAgent:
    def __init__(self, data_path, guidance_path, llm_model="gpt-4"): 
        self.data_path = data_path
        self.guidance_path = guidance_path
        self.llm = ChatOpenAI(model=llm_model, temperature=0)
        self.data = None
        self.generated_code = ""
        self.governance_agent = GovernanceAgent("pdfs/ifrs9_excerpt.pdf")

    def load_data(self):
        self.data = pd.read_csv(self.data_path)
        print("✅ Data loaded successfully.")

    def read_human_guidance(self):
        return read_yaml_config(self.guidance_path)
        print("✅ Human guidance read successfully.")

    def generate_cleaning_code(self):
        guidance = self.read_human_guidance()
        user_instructions = guidance['step_2']['human_guidance']
        # regulatory_guidance = self.governance_agent.extract_relevant_guidance("data cleaning")

        sample_columns = ", ".join(self.data.columns[:5])
        prompt = f"""
        You are a data engineer. Clean the dataset based on the following guidance.

        Human Guidance:
        {user_instructions}

        Regulatory Guidance:
        

        Sample Columns: {sample_columns}

        Generate Python pandas code that performs the above cleaning on a DataFrame named `df`.
        Make sure the response generated can be directly copied in py file and executed. There should be no syntax error and initial comment, double check for syntax errors.  Only give python code in response, nothing else , no english text before the code.     """

        response = self.llm([HumanMessage(content=prompt)]).content.strip()
        self.generated_code = extract_code(response)
        save_code_to_file(self.generated_code, "generated_code/step1_data_cleaning.py")
        print("✅ Code generation complete. Saved to generated_code/step1_data_cleaning.py")
        return self.generated_code

    def self_review_and_fix_generated_code(self, max_retries=5):
        """
        Check if generated code has syntax errors and attempt to regenerate if needed.
        """
        for attempt in range(max_retries + 1):
            try:
                ast.parse(self.generated_code)
                print("✅ Code passed syntax check.")
                return True
            except SyntaxError as e:
                print(f"❌ Syntax error in generated code: {e}")
                if attempt < max_retries:
                    print("🔁 Attempting to regenerate code...")
                    self.generate_cleaning_code()
                else:
                    print("🚫 Maximum retries reached. Fix the code manually.")
                    return False

    def execute_generated_code(self):
        if not self.generated_code:
            print("⚠️ No code to execute.")
            return

        if not self.self_review_and_fix_generated_code():
            print("⚠️ Execution aborted due to persistent syntax issues.")
            return

        try:
            exec_env = {'df': self.data}
            exec(self.generated_code, exec_env)
            self.data = exec_env['df']
            self.data.to_csv("data/cleaned_credit_data.csv", index=False)
            print("✅ Code executed , data cleaned and saved successfully.")
        except Exception as e:
            print(f"❌ Error during execution: {e}")

    def explore_data_and_generate_notebook(self, notebook_path="generated_code/data_exploration.ipynb"):
        self.load_data()
        guidance = self.read_human_guidance()
        user_instructions = guidance['step_2']['human_guidance']

        preview = self.data.head(3).to_markdown()

        prompt = f"""
            You are a credit risk modeling expert and data scientist.

            Your task is to explore a credit dataset and generate a visually rich exploratory data analysis (EDA) notebook based on the following human guidance:

            {user_instructions}

            Here is a preview of the dataset:

            {preview}

            Generate well-structured Jupyter notebook cells including:
            - Markdown with explanations and titles
            - Code for basic statistics, null counts, distributions
            - Visuals: histograms, box plots, correlation matrix, category distributions

            The notebook should be insightful, readable, and professionally formatted.
            Only return valid Python or Markdown content in cell-ready format.
            """

        response = self.llm([HumanMessage(content=prompt)]).content.strip()

        # Parse response into notebook cells (naively by Markdown/code separators)
        lines = response.splitlines()
        cells = []
        current_block = []
        is_code = False

        for line in lines:
            if line.strip().startswith("```python"):
                if current_block:
                    cells.append(new_markdown_cell("\n".join(current_block)))
                    current_block = []
                is_code = True
            elif line.strip().startswith("```"):
                if is_code:
                    cells.append(new_code_cell("\n".join(current_block)))
                    current_block = []
                    is_code = False
            else:
                current_block.append(line)

        if current_block:
            cells.append(new_code_cell("\n".join(current_block)) if is_code else new_markdown_cell("\n".join(current_block)))

        notebook = new_notebook(cells=cells)
        os.makedirs(os.path.dirname(notebook_path), exist_ok=True)

        with open(notebook_path, "w", encoding="utf-8") as f:
            nbformat.write(notebook, f)

        print(f"📒 Notebook saved to: {notebook_path}")





    def run(self):
        self.load_data()
        self.explore_data_and_generate_notebook()
        self.generate_cleaning_code()
        self.execute_generated_code()
