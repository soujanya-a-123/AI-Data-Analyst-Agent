# 📊 AI Data Analyst Agent

## 🚀 Project Overview

**AI Data Analyst Agent** is an AI-powered data analysis application built using **Python, Pandas, Streamlit, Groq, and Plotly**.

The application allows users to upload **CSV or Excel files** and ask questions about their data using natural language.

Instead of manually writing Python or Pandas code, users can ask questions such as:

- Which region has the highest sales?
- Which city has the highest sales?
- What are the top 5 products by sales?
- Which category has the highest profit?
- Which region grew fastest last quarter?

The application uses **Groq LLM** to generate Python/Pandas analysis code and then executes that code on the actual uploaded dataset.

This ensures that numerical answers are calculated from the real data rather than simply being guessed by the AI.

---

# 🎯 Project Objective

The main objective of this project is to build a **Natural Language Data Analysis Agent**.

The system converts:

```text
Natural Language Question
          ↓
       Groq LLM
          ↓
Generated Pandas Code
          ↓
Actual Dataset
          ↓
Pandas Calculation
          ↓
Computed Result
          ↓
AI Explanation + Visualization
