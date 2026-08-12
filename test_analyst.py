import os

import pandas as pd
import pytest
import plotly.graph_objects as go

from analyst import (
    get_groq_client,
    clean_generated_code,
    generate_analysis_code,
    execute_analysis,
    create_visualization,
    generate_answer,
)


# ============================================================
# SAMPLE DATA
# ============================================================

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Order_Date": [
            "2025-01-10",
            "2025-02-15",
            "2025-03-20",
            "2025-04-12",
            "2025-05-08",
            "2025-06-18",
            "2025-07-10",
            "2025-08-22",
        ],
        "Region": [
            "North",
            "South",
            "West",
            "North",
            "South",
            "West",
            "North",
            "South",
        ],
        "City": [
            "Delhi",
            "Bangalore",
            "Mumbai",
            "Delhi",
            "Chennai",
            "Pune",
            "Delhi",
            "Bangalore",
        ],
        "Category": [
            "Electronics",
            "Furniture",
            "Electronics",
            "Furniture",
            "Electronics",
            "Furniture",
            "Electronics",
            "Electronics",
        ],
        "Product": [
            "Laptop",
            "Chair",
            "Phone",
            "Table",
            "Laptop",
            "Chair",
            "Phone",
            "Laptop",
        ],
        "Sales": [
            50000,
            12000,
            30000,
            18000,
            45000,
            15000,
            55000,
            48000,
        ],
        "Profit": [
            8000,
            2500,
            5000,
            3500,
            7000,
            3000,
            9000,
            7500,
        ],
        "Salesperson": [
            "A",
            "B",
            "C",
            "A",
            "B",
            "C",
            "A",
            "B",
        ],
    })


# ============================================================
# BASIC DATA TESTS
# ============================================================

def test_dataframe(sample_df):

    assert isinstance(sample_df, pd.DataFrame)
    assert len(sample_df) == 8
    assert "Sales" in sample_df.columns
    assert "Region" in sample_df.columns
    assert "Order_Date" in sample_df.columns


def test_total_sales(sample_df):

    result = sample_df["Sales"].sum()

    assert result == 273000


def test_average_sales(sample_df):

    result = sample_df["Sales"].mean()

    assert result == 34125


def test_highest_sales_region(sample_df):

    result = (
        sample_df
        .groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    assert result.index[0] == "North"
    assert result.iloc[0] == 123000


def test_highest_sales_city(sample_df):

    result = (
        sample_df
        .groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    assert result.index[0] == "Delhi"


def test_top_product(sample_df):

    result = (
        sample_df
        .groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    assert result.index[0] == "Laptop"


def test_highest_profit_region(sample_df):

    result = (
        sample_df
        .groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    assert result.index[0] == "North"


# ============================================================
# CODE CLEANING TESTS
# ============================================================

def test_clean_generated_code():

    code = "```python\nresult = df['Sales'].sum()\n```"

    cleaned = clean_generated_code(code)

    assert "```" not in cleaned
    assert "result = df['Sales'].sum()" in cleaned


def test_clean_import():

    code = "import pandas as pd\nresult = df['Sales'].sum()"

    cleaned = clean_generated_code(code)

    assert "import pandas" not in cleaned
    assert "result" in cleaned


# ============================================================
# EXECUTION TESTS
# ============================================================

def test_execute_total_sales(sample_df):

    code = "result = df['Sales'].sum()"

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert error is None
    assert result == 273000


def test_execute_average_sales(sample_df):

    code = "result = df['Sales'].mean()"

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert error is None
    assert result == 34125


def test_execute_groupby(sample_df):

    code = (
        "result = df.groupby('Region')['Sales']"
        ".sum().sort_values(ascending=False).head(1)"
    )

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert error is None
    assert isinstance(result, pd.Series)
    assert result.index[0] == "North"
    assert result.iloc[0] == 123000


def test_execute_dataframe(sample_df):

    code = (
        "result = df.groupby('Region')['Sales']"
        ".sum().reset_index()"
    )

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert error is None
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3


# ============================================================
# DATE TESTS
# ============================================================

def test_date_conversion(sample_df):

    code = (
        "df['Order_Date'] = pd.to_datetime(df['Order_Date'])\n"
        "result = df['Order_Date'].dt.year.max()"
    )

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert error is None
    assert result == 2025


def test_quarter_calculation(sample_df):

    code = (
        "df['Order_Date'] = pd.to_datetime(df['Order_Date'])\n"
        "df['Quarter'] = df['Order_Date'].dt.to_period('Q')\n"
        "result = df['Quarter'].max()"
    )

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert error is None
    assert str(result) == "2025Q3"


# ============================================================
# QUARTER GROWTH TEST
# ============================================================

def test_quarter_growth(sample_df):

    code = (
        "df['Order_Date'] = pd.to_datetime(df['Order_Date'])\n"
        "df['Quarter'] = df['Order_Date'].dt.to_period('Q')\n"
        "latest_quarter = df['Quarter'].max()\n"
        "previous_quarter = latest_quarter - 1\n"
        "current_sales = (\n"
        "    df[df['Quarter'] == latest_quarter]\n"
        "    .groupby('Region')['Sales'].sum()\n"
        ")\n"
        "previous_sales = (\n"
        "    df[df['Quarter'] == previous_quarter]\n"
        "    .groupby('Region')['Sales'].sum()\n"
        ")\n"
        "growth = pd.concat(\n"
        "    [previous_sales, current_sales],\n"
        "    axis=1,\n"
        "    keys=['Previous_Sales', 'Current_Sales']\n"
        ")\n"
        "growth = growth.dropna()\n"
        "growth = growth[growth['Previous_Sales'] != 0]\n"
        "growth['Growth_Percentage'] = (\n"
        "    (growth['Current_Sales'] - growth['Previous_Sales'])\n"
        "    / growth['Previous_Sales']\n"
        ") * 100\n"
        "growth = growth.reset_index()\n"
        "result = growth.sort_values(\n"
        "    'Growth_Percentage', ascending=False\n"
        ").head(1)"
    )

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert error is None
    assert isinstance(result, pd.DataFrame)
    assert "Region" in result.columns
    assert "Previous_Sales" in result.columns
    assert "Current_Sales" in result.columns
    assert "Growth_Percentage" in result.columns


# ============================================================
# SECURITY TESTS
# ============================================================

def test_block_import(sample_df):

    # Imports are removed by clean_generated_code().
    # Therefore this test verifies that the cleaned
    # code still executes correctly.

    code = "import os\nresult = df['Sales'].sum()"

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert error is None
    assert result == 273000

def test_block_exec(sample_df):

    code = "exec('result = 100')"

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert result is None
    assert error is not None


def test_block_eval(sample_df):

    code = "result = eval('100')"

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert result is None
    assert error is not None


def test_invalid_column(sample_df):

    code = "result = df['WrongColumn'].sum()"

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert result is None
    assert error is not None


def test_missing_result(sample_df):

    code = "x = df['Sales'].sum()"

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert result is None
    assert error is not None


# ============================================================
# VISUALIZATION TESTS
# ============================================================

def test_visualization_series():

    result = pd.Series({
        "North": 123000,
        "South": 105000,
        "West": 45000,
    })

    fig = create_visualization(result)

    assert fig is not None
    assert isinstance(fig, go.Figure)


def test_visualization_dataframe():

    result = pd.DataFrame({
        "Region": [
            "North",
            "South",
            "West",
        ],
        "Sales": [
            123000,
            105000,
            45000,
        ],
    })

    fig = create_visualization(result)

    assert fig is not None
    assert isinstance(fig, go.Figure)


def test_empty_visualization():

    result = pd.DataFrame()

    fig = create_visualization(result)

    assert fig is None


# ============================================================
# GROQ TESTS
# ============================================================

def test_groq_api_key():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        pytest.skip(
            "GROQ_API_KEY is not available"
        )

    assert len(api_key) > 0


@pytest.mark.integration
def test_groq_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        pytest.skip(
            "GROQ_API_KEY is not available"
        )

    client = get_groq_client()

    assert client is not None


@pytest.mark.integration
def test_generate_analysis_code(sample_df):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        pytest.skip(
            "GROQ_API_KEY is not available"
        )

    code = generate_analysis_code(
        sample_df,
        "What is the total sales?"
    )

    assert code is not None
    assert len(code) > 0
    assert "result" in code


@pytest.mark.integration
def test_generate_code_and_execute(sample_df):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        pytest.skip(
            "GROQ_API_KEY is not available"
        )

    code = generate_analysis_code(
        sample_df,
        "What is the total sales?"
    )

    result, fig, error = execute_analysis(
        sample_df,
        code
    )

    assert error is None
    assert result is not None


@pytest.mark.integration
def test_generate_answer():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        pytest.skip(
            "GROQ_API_KEY is not available"
        )

    answer = generate_answer(
        "What is the total sales?",
        273000
    )

    assert answer is not None
    assert len(answer) > 0