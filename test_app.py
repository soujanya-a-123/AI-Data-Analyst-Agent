import os

import pandas as pd
import pytest

from streamlit.testing.v1 import AppTest


APP_FILE = "app.py"


# ============================================================
# SAMPLE DATA
# ============================================================

def create_test_csv():

    df = pd.DataFrame({
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

    return df


# ============================================================
# HELPER
# ============================================================

def load_app():

    return AppTest.from_file(
        APP_FILE
    )


def upload_sample(at):

    df = create_test_csv()

    csv_data = df.to_csv(
        index=False
    )

    at.run()

    at.file_uploader[0].set_value(
        (
            "sample_data.csv",
            csv_data.encode("utf-8"),
            "text/csv"
        )
    )

    at.run()

    return at


# ============================================================
# TEST 1
# APP STARTS
# ============================================================

def test_app_starts():

    at = load_app()

    at.run()

    assert not at.exception


# ============================================================
# TEST 2
# FILE UPLOADER
# ============================================================

def test_file_uploader():

    at = load_app()

    at.run()

    assert not at.exception

    assert len(
        at.file_uploader
    ) == 1


# ============================================================
# TEST 3
# SIDEBAR
# ============================================================

def test_sidebar():

    at = load_app()

    at.run()

    assert not at.exception

    assert len(
        at.sidebar
    ) > 0


# ============================================================
# TEST 4
# UPLOAD CSV
# ============================================================

def test_csv_upload():

    at = load_app()

    upload_sample(at)

    assert not at.exception


# ============================================================
# TEST 5
# DATASET METRICS
# ============================================================

def test_dataset_metrics():

    at = load_app()

    upload_sample(at)

    assert not at.exception

    assert len(
        at.metric
    ) >= 4


# ============================================================
# TEST 6
# ROW COUNT
# ============================================================

def test_row_count():

    at = load_app()

    upload_sample(at)

    values = [
        metric.value
        for metric in at.metric
    ]

    assert "8" in values


# ============================================================
# TEST 7
# COLUMN COUNT
# ============================================================

def test_column_count():

    at = load_app()

    upload_sample(at)

    values = [
        metric.value
        for metric in at.metric
    ]

    assert "8" in values


# ============================================================
# TEST 8
# DATAFRAME PREVIEW
# ============================================================

def test_dataframe_preview():

    at = load_app()

    upload_sample(at)

    assert not at.exception

    assert len(
        at.dataframe
    ) >= 1


# ============================================================
# TEST 9
# COLUMN INFORMATION
# ============================================================

def test_column_information():

    at = load_app()

    upload_sample(at)

    assert not at.exception

    assert len(
        at.expander
    ) >= 2


# ============================================================
# TEST 10
# AVAILABLE COLUMNS
# ============================================================

def test_available_columns():

    at = load_app()

    upload_sample(at)

    assert not at.exception

    # The uploaded dataset should contain
    # the expected columns.
    df = create_test_csv()

    expected_columns = [
        "Order_Date",
        "Region",
        "City",
        "Category",
        "Product",
        "Sales",
        "Profit",
        "Salesperson"
    ]

    for column in expected_columns:

        assert column in df.columns

# ============================================================
# TEST 11
# EXAMPLE QUESTIONS
# ============================================================

def test_example_questions():

    at = load_app()

    upload_sample(at)

    assert len(
        at.selectbox
    ) >= 1

    options = at.selectbox[0].options

    assert (
        "What is the total sales?"
        in options
    )

    assert (
        "Which region has the highest sales?"
        in options
    )

    assert (
        "Which region grew fastest last quarter?"
        in options
    )


# ============================================================
# TEST 12
# QUESTION INPUT
# ============================================================

def test_question_input():

    at = load_app()

    upload_sample(at)

    assert len(
        at.text_input
    ) >= 1


# ============================================================
# TEST 13
# ANALYZE BUTTON
# ============================================================

def test_analyze_button():

    at = load_app()

    upload_sample(at)

    buttons = [
        button.label
        for button in at.button
    ]

    assert (
        "🔍 Analyze Data"
        in buttons
    )


# ============================================================
# TEST 14
# SELECT QUESTION
# ============================================================

def test_select_question():

    at = load_app()

    upload_sample(at)

    at.selectbox[0].set_value(
        "What is the total sales?"
    )

    at.run()

    assert not at.exception

    assert (
        at.text_input[0].value
        == "What is the total sales?"
    )


# ============================================================
# TEST 15
# SELECT REGION QUESTION
# ============================================================

def test_select_region_question():

    at = load_app()

    upload_sample(at)

    at.selectbox[0].set_value(
        "Which region has the highest sales?"
    )

    at.run()

    assert not at.exception

    assert (
        at.text_input[0].value
        == "Which region has the highest sales?"
    )


# ============================================================
# TEST 16
# SELECT CITY QUESTION
# ============================================================

def test_select_city_question():

    at = load_app()

    upload_sample(at)
