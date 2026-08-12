import streamlit as st
import pandas as pd

from analyst import (
    generate_analysis_code,
    execute_analysis,
    generate_answer
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="AI Data Analyst",

    page_icon="📊",

    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "📊 AI Data Analyst Agent"
)

st.write(
    """
Upload a CSV or Excel file and ask questions
about your data using natural language.

The application generates Pandas code using
Groq, executes it on your real dataset, and
shows the answer, calculation, and chart.
"""
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "⚙️ Project Information"
    )

    st.write(
        """
### AI Data Analyst

**Technology Stack**

- Python
- Pandas
- Streamlit
- Groq
- Plotly

### Workflow

Dataset
↓
Pandas DataFrame
↓
Natural Language Question
↓
Groq
↓
Pandas Code
↓
Real Calculation
↓
AI Answer
↓
Table + Chart
"""
    )

    st.divider()

    st.info(
        "Numbers are calculated from the uploaded dataset."
    )


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(

    "📁 Upload CSV or Excel file",

    type=[
        "csv",
        "xlsx"
    ]
)


# ============================================================
# AFTER UPLOAD
# ============================================================

if uploaded_file is not None:

    # ========================================================
    # READ DATASET
    # ========================================================

    try:

        if uploaded_file.name.lower().endswith(
            ".csv"
        ):

            df = pd.read_csv(
                uploaded_file
            )

        else:

            df = pd.read_excel(
                uploaded_file
            )

    except Exception as e:

        st.error(
            f"❌ Could not read file: {e}"
        )

        st.stop()


    # ========================================================
    # SUCCESS
    # ========================================================

    st.success(
        f"✅ Dataset uploaded successfully: "
        f"{uploaded_file.name}"
    )


    # ========================================================
    # DATASET METRICS
    # ========================================================

    st.subheader(
        "📊 Dataset Overview"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Rows",
            df.shape[0]
        )

    with col2:

        st.metric(
            "Columns",
            df.shape[1]
        )

    with col3:

        st.metric(
            "Missing Values",
            int(
                df.isnull()
                .sum()
                .sum()
            )
        )

    with col4:

        st.metric(
            "Duplicate Rows",
            int(
                df.duplicated()
                .sum()
            )
        )


    # ========================================================
    # DATA PREVIEW
    # ========================================================

    st.subheader(
        "📋 Dataset Preview"
    )

    st.dataframe(

        df.head(10),

        use_container_width=True
    )


    # ========================================================
    # COLUMN INFORMATION
    # ========================================================

    with st.expander(
        "🔎 View Column Information"
    ):

        column_info = pd.DataFrame(

            {

                "Column": df.columns,

                "Data Type": [

                    str(
                        df[column].dtype
                    )

                    for column in df.columns
                ],

                "Missing Values": [

                    int(
                        df[column]
                        .isnull()
                        .sum()
                    )

                    for column in df.columns
                ],

                "Unique Values": [

                    int(
                        df[column]
                        .nunique()
                    )

                    for column in df.columns
                ]
            }
        )

        st.dataframe(

            column_info,

            use_container_width=True
        )


    # ========================================================
    # AVAILABLE COLUMNS
    # ========================================================

    with st.expander(
        "📌 Available Columns"
    ):

        st.write(
            list(df.columns)
        )


    # ========================================================
    # QUESTION SECTION
    # ========================================================

    st.divider()

    st.subheader(
        "💬 Ask Your Data"
    )


    example_questions = [

        "What is the total sales?",

        "Which region has the highest sales?",

        "Which city has the highest sales?",

        "What are the top 5 products by sales?",

        "Which category has the highest sales?",

        "What is the average sales?",

        "Which salesperson has the highest sales?",

        "Show sales by region.",

        "Which month had the highest sales?",

        "What are the top 3 regions by profit?",

        "Which region grew fastest last quarter?"
    ]


    selected_question = st.selectbox(

        "💡 Example Questions",

        [
            "-- Select an example --"
        ]
        +
        example_questions
    )


    if selected_question != (
        "-- Select an example --"
    ):

        default_question = (
            selected_question
        )

    else:

        default_question = ""


    # ========================================================
    # QUESTION INPUT
    # ========================================================

    question = st.text_input(

        "✏️ Ask a question",

        value=default_question,

        placeholder=(
            "Which region has the highest sales?"
        )
    )


    # ========================================================
    # ANALYZE BUTTON
    # ========================================================

    analyze = st.button(

        "🔍 Analyze Data",

        type="primary",

        use_container_width=True
    )


    # ========================================================
    # ANALYSIS
    # ========================================================

    if analyze:

        # ----------------------------------------------------
        # VALIDATE QUESTION
        # ----------------------------------------------------

        if not question.strip():

            st.warning(
                "⚠️ Please enter a question."
            )

            st.stop()


        # ----------------------------------------------------
        # GENERATE CODE
        # ----------------------------------------------------

        with st.spinner(
            "🤖 Groq is generating analysis code..."
        ):

            try:

                generated_code = (
                    generate_analysis_code(
                        df,
                        question
                    )
                )

            except Exception as e:

                st.error(
                    "❌ Failed to generate "
                    f"analysis code: {e}"
                )

                st.stop()


        # ----------------------------------------------------
        # SHOW CODE
        # ----------------------------------------------------

        with st.expander(
            "🐍 View Generated Python Code"
        ):

            st.code(

                generated_code,

                language="python"
            )


        # ----------------------------------------------------
        # EXECUTE
        # ----------------------------------------------------

        with st.spinner(
            "⚙️ Calculating from your dataset..."
        ):

            result, fig, error = (
                execute_analysis(
                    df,
                    generated_code
                )
            )


        # ----------------------------------------------------
        # ERROR
        # ----------------------------------------------------

        if error:

            st.error(
                f"❌ Analysis failed: {error}"
            )

            st.info(
                "Try using the exact column names "
                "shown under Available Columns."
            )

            st.stop()


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        st.success(
            "✅ Analysis completed successfully."
        )


        # ----------------------------------------------------
        # AI ANSWER
        # ----------------------------------------------------

        st.subheader(
            "🤖 AI Answer"
        )

        try:

            answer = generate_answer(

                question,

                result
            )

            st.write(
                answer
            )

        except Exception as e:

            st.warning(
                f"AI explanation failed: {e}"
            )

            st.write(
                result
            )


        # ----------------------------------------------------
        # COMPUTED RESULT
        # ----------------------------------------------------

        st.subheader(
            "📊 Computed Result"
        )


        if isinstance(
            result,
            pd.DataFrame
        ):

            st.dataframe(

                result,

                use_container_width=True
            )


        elif isinstance(
            result,
            pd.Series
        ):

            st.dataframe(

                result.to_frame(),

                use_container_width=True
            )


        else:

            st.metric(

                "Computed Value",

                str(result)
            )


        # ----------------------------------------------------
        # CHART
        # ----------------------------------------------------

        if fig is not None:

            st.subheader(
                "📈 Visualization"
            )

            st.plotly_chart(

                fig,

                use_container_width=True
            )


        # ----------------------------------------------------
        # COMPUTATION EXPLANATION
        # ----------------------------------------------------

        with st.expander(
            "🧮 How was this answer calculated?"
        ):

            st.write(
                """
The application does not directly guess
the numerical answer.

The calculation happens as follows:

1. The uploaded CSV/Excel file is loaded
   into a Pandas DataFrame.

2. The column names and sample data are
   provided to Groq.

3. Groq generates Pandas code.

4. The generated code is executed on the
   actual uploaded DataFrame.

5. Pandas performs the calculation.

6. The computed result is displayed.

7. Groq explains the computed result.

Therefore, the numerical answer comes from
the actual dataset rather than being guessed
by the language model.
"""
            )


        # ----------------------------------------------------
        # DOWNLOAD RESULT
        # ----------------------------------------------------

        if isinstance(
            result,
            pd.DataFrame
        ):

            result_csv = result.to_csv(
                index=False
            )

            st.download_button(

                label="⬇️ Download Result",

                data=result_csv,

                file_name="analysis_result.csv",

                mime="text/csv"
            )


        elif isinstance(
            result,
            pd.Series
        ):

            result_csv = result.to_csv()

            st.download_button(

                label="⬇️ Download Result",

                data=result_csv,

                file_name="analysis_result.csv",

                mime="text/csv"
            )