# 📊 AI Data Analyst Agent

## 🚀 Project Overview

**AI Data Analyst Agent** is an AI-powered data analysis application that allows users to upload **CSV or Excel files** and ask questions about their data using natural language.

Instead of manually writing Python or Pandas code, users can ask questions such as:

```text
Which region has the highest sales?
```

```text
Which city has the highest sales?
```

```text
What are the top 5 products by sales?
```

```text
Which region grew fastest last quarter?
```

The application uses **Groq LLM** to generate Python/Pandas analysis code and then executes that code on the actual uploaded dataset.

The final result is displayed together with supporting calculations and visualizations.

---

# 🎯 Project Objective

The objective of this project is to build a **Natural Language Data Analysis Agent** that can:

- Load CSV files
- Load Excel files
- Understand dataset columns
- Accept natural-language questions
- Generate Pandas analysis code
- Execute calculations on real data
- Display computed results
- Generate supporting visualizations
- Explain the result
- Reduce numerical hallucination by performing calculations on the actual dataset

---

# ✨ Features

- 📁 CSV upload
- 📊 Excel `.xlsx` upload
- 📋 Dataset preview
- 📈 Dataset information
- 🔍 Column information
- ❗ Missing-value detection
- 🔄 Duplicate-row detection
- 💬 Natural-language data questions
- 🤖 Groq LLM integration
- 🐍 Automatic Pandas code generation
- 🧮 Real computation using Pandas
- 📊 Computed result display
- 📈 Interactive Plotly visualizations
- 💡 AI-generated explanations
- 🐍 Generated analysis code display
- 📅 Date-based analysis
- 📅 Quarterly growth analysis
- 📥 Result display/download
- 🛡️ Basic generated-code validation

---

# 🧠 Core Concept

The project follows a computation-first approach.

```text
User Question
      ↓
Groq LLM
      ↓
Generate Pandas Code
      ↓
Execute Code on Actual DataFrame
      ↓
Real Computation
      ↓
Computed Result
      ↓
AI Explanation
      ↓
Visualization
```

The LLM does **not** directly invent the numerical answer.

Instead, the LLM generates analysis logic and **Pandas performs the actual calculation** using the uploaded dataset.

---

# 🏗️ System Architecture

```text
                         USER
                           │
                           ▼
                ┌────────────────────┐
                │     Streamlit      │
                │       app.py       │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   Uploaded File    │
                │    CSV / Excel     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │      Pandas        │
                │    DataFrame       │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │     analyst.py     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │      Groq LLM      │
                │   Llama 3.3 70B    │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │  Generated Pandas  │
                │       Code         │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Execute on Actual  │
                │       Data         │
                └─────────┬──────────┘
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
        ┌────────────────┐  ┌────────────────┐
        │ Computed Result│  │    Plotly      │
        │                │  │ Visualization  │
        └────────┬───────┘  └───────┬────────┘
                 │                  │
                 └────────┬─────────┘
                          ▼
                  ┌───────────────┐
                  │ AI Explanation│
                  └───────────────┘
```

---

# 📂 VS Code Project Structure

```text
AI_Data_Analyst/
│
├── 📄 app.py
├── 📄 analyst.py
├── 📄 requirements.txt
├── 📄 README.md
├── 📄 .gitignore
├── 📄 sample_data.csv
├── 📄 .env
│
└── 📁 venv/
    ├── Include/
    ├── Lib/
    ├── Scripts/
    └── pyvenv.cfg
```

### GitHub Structure

The following files should be committed:

```text
app.py
analyst.py
requirements.txt
README.md
.gitignore
sample_data.csv
```

The following files should **not** be committed:

```text
.env
venv/
__pycache__/
*.pyc
```

---

# 📄 File Descriptions

## `app.py`

Main Streamlit application.

Responsibilities:

- Create user interface
- Upload CSV
- Upload Excel
- Display dataset preview
- Display dataset statistics
- Accept natural-language questions
- Call analysis functions
- Display computed results
- Display AI answers
- Display visualizations
- Display generated code

---

## `analyst.py`

Backend AI/data-analysis module.

Responsibilities:

- Connect to Groq
- Create prompts
- Generate Pandas code
- Clean generated code
- Validate generated code
- Execute generated code
- Calculate results
- Generate charts
- Generate AI explanations

---

## `requirements.txt`

Contains Python dependencies.

Example:

```text
streamlit
pandas
openpyxl
groq
python-dotenv
plotly
```

---

## `.env`

Stores the Groq API key.

```text
GROQ_API_KEY=your_groq_api_key_here
```

⚠️ Never commit this file to GitHub.

---

## `.gitignore`

Recommended contents:

```text
.env
venv/
__pycache__/
*.pyc
.streamlit/
```

---

## `sample_data.csv`

Sample dataset used to demonstrate the project.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data processing |
| Streamlit | Web application |
| Groq | LLM API |
| Llama 3.3 70B | AI/code generation |
| Plotly | Interactive visualization |
| OpenPyXL | Excel processing |
| python-dotenv | API key management |

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/soujanya-a-123/AI-Data-Analyst-Agent.git
```

Move into the project:

```bash
cd AI-Data-Analyst-Agent
```

---

# 2. Create Virtual Environment

Windows:

```powershell
python -m venv venv
```

---

# 3. Activate Virtual Environment

```powershell
.\venv\Scripts\activate
```

You should see:

```text
(venv) PS C:\...\AI_Data_Analyst>
```

---

# 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

Or:

```powershell
pip install streamlit pandas openpyxl groq python-dotenv plotly
```

---

# 🔑 Groq API Configuration

Create a file called:

```text
.env
```

in the root project folder.

Add:

```text
GROQ_API_KEY=your_groq_api_key_here
```

The project reads the key from the environment.

Do not place the API key directly in:

```text
app.py
```

or:

```text
analyst.py
```

---

# ▶️ Run the Application

Activate the virtual environment:

```powershell
.\venv\Scripts\activate
```

Then:

```powershell
streamlit run app.py
```

The Streamlit application will open in the browser.

---

# 🔄 End-to-End Workflow

```text
1. Start application
        ↓
2. Upload CSV / Excel
        ↓
3. Pandas loads dataset
        ↓
4. Dataset preview is displayed
        ↓
5. User asks a question
        ↓
6. Columns and sample data are sent to Groq
        ↓
7. Groq generates Pandas code
        ↓
8. Generated code is validated
        ↓
9. Code executes on the actual DataFrame
        ↓
10. Pandas calculates the result
        ↓
11. Result is displayed
        ↓
12. AI generates explanation
        ↓
13. Plotly visualization is displayed
```

---

# 🧮 How Real Computation Works

Suppose the user asks:

```text
Which region has the highest sales?
```

The LLM may generate:

```python
result = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(1)
)
```

The application executes this code against the uploaded DataFrame.

Therefore:

```text
Groq
  ↓
Generates analysis code
  ↓
Pandas
  ↓
Processes actual dataset
  ↓
Actual numerical result
```

This reduces the chance of the LLM simply guessing a numerical answer.

---

# 📅 Quarterly Growth Analysis

The agent also supports:

```text
Which region grew fastest last quarter?
```

The analysis concept is:

```text
Date Column
      ↓
Convert to Datetime
      ↓
Create Quarter
      ↓
Identify Latest Quarter
      ↓
Identify Previous Quarter
      ↓
Calculate Regional Sales
      ↓
Calculate Growth Percentage
      ↓
Sort Regions
      ↓
Return Fastest Growing Region
```

Growth is calculated using:

```text
Growth % =
((Current Quarter Sales - Previous Quarter Sales)
 / Previous Quarter Sales) × 100
```

Example result:

| Region | Previous Sales | Current Sales | Growth % |
|---|---:|---:|---:|
| North | 100000 | 125000 | 25% |
| South | 90000 | 99000 | 10% |
| West | 80000 | 96000 | 20% |

In this example:

```text
North
```

grew the fastest.

---

# 📊 Sample Dataset

A sample sales dataset can contain:

```text
Order_Date
Region
City
Category
Product
Sales
Profit
Salesperson
```

Example:

| Order_Date | Region | City | Category | Product | Sales | Profit |
|---|---|---|---|---|---:|---:|
| 2026-01-10 | North | Delhi | Electronics | Laptop | 50000 | 8000 |
| 2026-02-15 | South | Bangalore | Furniture | Chair | 12000 | 2500 |
| 2026-03-20 | West | Mumbai | Electronics | Phone | 30000 | 5000 |
| 2026-04-12 | North | Delhi | Furniture | Table | 18000 | 3500 |
| 2026-05-08 | South | Chennai | Electronics | Laptop | 45000 | 7000 |

---

# 💬 Sample Questions

## Basic
