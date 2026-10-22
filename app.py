import streamlit as st
import asyncio
import pandas as pd
import plotly.express as px
from engine.trajectories import DEFAULT_TRAJECTORIES
from engine.benchmark import BenchmarkRunner

st.set_page_config(
    page_title="AegisTest: Open-Source Jailbreak Resistance Benchmark",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AegisTest: Jailbreak Resistance Benchmark Bot")
st.markdown("Evaluate open-source LLMs against standard adversarial trajectories and analyze success rates in real-time.")

with st.sidebar:
    st.header("Benchmark Configuration")
    target_model = st.selectbox(
        "Select Target Model",
        ["Llama-3-8B-Instruct", "Mistral-7B-Instruct-v0.2", "Vicuna-13B", "Gemma-7B"]
    )
    run_button = st.button("Run Benchmark Suite", type="primary")

if run_button:
    runner = BenchmarkRunner(target_model=target_model)
    
    with st.status("Executing adversarial trajectories...", expanded=True) as status:
        st.write(f"Initializing evaluation against {len(DEFAULT_TRAJECTORIES)} vector trajectories...")
        results = asyncio.run(runner.run_suite())
        status.update(label="Benchmark evaluation complete!", state="complete", expanded=False)

    df_results = pd.DataFrame(results)
    
    total_tests = len(df_results)
    success_count = df_results["success"].sum()
    resistance_rate = ((total_tests - success_count) / total_tests) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Trajectories Tested", total_tests)
    col2.metric("Successful Jailbreaks", int(success_count))
    col3.metric("Resistance Rate", f"{resistance_rate:.1f}%")

    st.divider()

    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Vulnerability by Category")
        category_df = df_results.groupby("category")["success"].mean().reset_index()
        category_df["Failure Rate (%)"] = category_df["success"] * 100
        fig = px.bar(
            category_df, x="category", y="Failure Rate (%)",
            color="Failure Rate (%)", color_continuous_scale="Reds",
            range_y=[0, 100]
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.subheader("Response Trajectory Logs")
        st.dataframe(df_results[["id", "category", "success", "response"]], use_container_width=True)
else:
    st.info("Configure your target model in the sidebar and click **Run Benchmark Suite** to start testing.")

import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if not check_password():
    st.stop()
    