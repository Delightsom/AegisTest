# 🛡️ AegisTest: LLM Jailbreak Resistance Benchmark

An open-source evaluation suite designed to assess open-source large language models against adversarial prompt vectors, token smuggling, persona hijacking, and safety guardrail bypass attempts.

## Project Structure
- `app.py`: Streamlit-powered analytical dashboard and execution interface.
- `engine/benchmark.py`: Core synchronous evaluation runner.
- `engine/trajectories.py`: Pydantic data schemas and default adversarial test cases.
- `custom_trajectories.json`: User-defined test vector imports.

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Run the application:
   ```bash
   streamlit run app.py
