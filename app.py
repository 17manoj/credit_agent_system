
import streamlit as st
import pandas as pd
from agents.developer_agent import DeveloperAgent
import os
import io
from contextlib import redirect_stdout
import nbformat
from streamlit.components.v1 import html
import base64
from nbconvert import HTMLExporter

st.set_page_config(page_title="AI ML Pipeline", layout="wide")
st.title("🧠 AI Agent-Powered ML Builder")

# --- File Upload ---
st.sidebar.header("📁 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

st.sidebar.header("📁 Upload Regulations")
uploaded_reg = st.sidebar.file_uploader("Upload a pdf file", type=["pdf"])

if uploaded_reg is not None:
    pdfs_folder = "pdfs"
    os.makedirs(pdfs_folder, exist_ok=True)
    pdf_path = os.path.join(pdfs_folder, uploaded_reg.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_reg.getbuffer())
    st.sidebar.success(f"✅ PDF saved to {pdf_path}")

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state["uploaded_data"] = df
        st.sidebar.success("✅ Data successfully uploaded!")
        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head())
    except Exception as e:
        st.sidebar.error(f"❌ Error reading file: {e}")
        st.stop()
else:
    st.info("Please upload a dataset to begin.")

# --- Ensure data is available ---
if "uploaded_data" not in st.session_state:
    st.warning("Upload data to activate agent tabs.")
    st.stop()

# --- Tabs for each ML stage ---
tabs = st.tabs([
    "📊 Data Cleaning ",
     "📊 Data Preprocessing ",
    "🔧 Feature Engineering",
    "🏋️ Model Training",
    "📈 Evaluation"
])

# --- TAB 1: Data Preprocessing ---
with tabs[0]:
    st.header("Step 1: Data Exploration and Cleaning")
    if st.button("Run Exploration and Cleaning Agent"):
        log_area = st.empty()  # Placeholder for logs
        buffer = io.StringIO()
        with st.spinner("Processing... Please wait."):
            with redirect_stdout(buffer):
                agent = DeveloperAgent("data/credit_data.csv", "guidance/human_guidance.yaml")
                agent.run()
        log_area.expander("Show Logs", expanded=True).text(buffer.getvalue())
        st.success("✅ Preprocessing Complete")
        df = pd.read_csv("data/generated_data/cleaned_credit_data.csv")
        st.dataframe(df.head())
    # Show generated notebook if exists
    notebook_path = "generated_code/data_exploration.ipynb"
    if os.path.exists(notebook_path):
        st.subheader("Generated Python Notebook")
        with open(notebook_path, "r", encoding="utf-8") as nb_file:
            nb = nbformat.read(nb_file, as_version=4)
            html_exporter = HTMLExporter()
            (body, resources) = html_exporter.from_notebook_node(nb)
            # Display notebook as HTML
            st.components.v1.html(body, height=800, scrolling=True)
    else:
        st.info("No generated notebook found in 'generated_code'.")

with tabs[1]:
    st.header("Step 1: Data Preprocessing")
    if st.button("Run Preprocessing Agent"):
        with st.spinner("Preprocessing in progress..."):
            result = DeveloperAgent(st.session_state["uploaded_data"])
        st.success("✅ Preprocessing Complete")
        st.json(result)

# --- TAB 2: Feature Engineering ---
with tabs[2]:
    st.header("Step 2: Feature Engineering")
    if st.button("Run Feature Engineering Agent"):
        with st.spinner("Generating features..."):
            result = DeveloperAgent(st.session_state["uploaded_data"])
        st.success("✅ Feature Engineering Complete")
        st.json(result)

# --- TAB 3: Model Training ---
with tabs[3]:
    st.header("Step 3: Model Training")
    if st.button("Run Training Agent"):
        with st.spinner("Training model..."):
            result = DeveloperAgent(st.session_state["uploaded_data"])
        st.success("✅ Model Training Complete")
        st.write("Model Metrics:")
        st.json(result.get("metrics", {}))

# --- TAB 4: Evaluation ---
with tabs[4]:
    st.header("Step 4: Evaluation")
    if st.button("Run Evaluation Agent"):
        with st.spinner("Evaluating model..."):
            result = DeveloperAgent(st.session_state["uploaded_data"])
        st.success("✅ Evaluation Complete")
        st.write("Evaluation Results:")
        st.json(result.get("evaluation", {}))
