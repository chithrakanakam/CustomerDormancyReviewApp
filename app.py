import streamlit as st
import pandas as pd
import os
from datetime import datetime


# -----------------------------
# Configuration
# -----------------------------

DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "customer_review.csv")

STATUS_OPTIONS = [
    "Customer Closed",
    "Payment Issue",
    "Legal Dispute",
    "Seasonal Customer",
    "Not Serviced",
    "Other"
]


# Create data folder
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


# -----------------------------
# Page Setup
# -----------------------------

st.set_page_config(
    page_title="Customer Review Tool",
    layout="wide"
)


# -----------------------------
# Helper Functions
# -----------------------------

def load_data():

    if os.path.exists(DATA_FILE):

        df = pd.read_csv(DATA_FILE)

        # Ensure editable columns are text
        if "Customer Status" in df.columns:
            df["Customer Status"] = (
                df["Customer Status"]
                .fillna("")
                .astype(str)
            )

        if "Remarks" in df.columns:
            df["Remarks"] = (
                df["Remarks"]
                .fillna("")
                .astype(str)
            )

        return df

    else:
        return pd.DataFrame()


def save_data(df):

    df.to_csv(
        DATA_FILE,
        index=False
    )


# -----------------------------
# Sidebar Navigation
# -----------------------------

page = st.sidebar.selectbox(
    "Select Page",
    [
        "User Review",
        "Admin Upload"
    ]
)


# ==========================================================
# ADMIN PAGE
# ==========================================================

if page == "Admin Upload":

    st.title("Admin - Upload Customer File")

    uploaded_file = st.file_uploader(
        "Upload Customer CSV",
        type=["csv"]
    )


    if uploaded_file:

        df = pd.read_csv(uploaded_file)


        # Convert editable fields to text
        if "Customer Status" in df.columns:
            df["Customer Status"] = (
                df["Customer Status"]
                .fillna("")
                .astype(str)
            )

        if "Remarks" in df.columns:
            df["Remarks"] = (
                df["Remarks"]
                .fillna("")
                .astype(str)
            )


        # Add required columns

        if "Customer Status" not in df.columns:
            df["Customer Status"] = ""


        if "Remarks" not in df.columns:
            df["Remarks"] = ""


        if "Updated By" not in df.columns:
            df["Updated By"] = ""


        if "Updated Date" not in df.columns:
            df["Updated Date"] = ""


        save_data(df)


        st.success(
            "Customer file uploaded successfully"
        )


        st.dataframe(
            df.head()
        )


# ==========================================================
# USER PAGE
# ==========================================================

elif page == "User Review":

    st.title("Customer Review")


    df = load_data()


    if df.empty:

        st.warning(
            "No customer file available. Please contact Admin."
        )

        st.stop()


    # User name

    user_name = st.text_input(
        "Enter your name"
    )


    st.subheader(
        "Update Customer Status and Remarks"
    )


    edited_df = st.data_editor(

        df,

        height=600,

        column_config={

            "Customer Status":

            st.column_config.SelectboxColumn(

                "Customer Status",

                options=STATUS_OPTIONS

            ),


            "Remarks":

            st.column_config.TextColumn(

                "Remarks"

            )

        },

        disabled=[
            col for col in df.columns
            if col not in [
                "Customer Status",
                "Remarks"
            ]
        ],

        num_rows="fixed"

    )


    if st.button("Save Changes"):


        if user_name.strip() == "":

            st.error(
                "Please enter your name before saving"
            )

        else:

            changed_rows = (
                edited_df[
                    [
                        "Customer Status",
                        "Remarks"
                    ]
                ]
                .ne(
                    df[
                        [
                            "Customer Status",
                            "Remarks"
                        ]
                    ]
                )
                .any(axis=1)
            )


            edited_df.loc[
                changed_rows,
                "Updated By"
            ] = user_name


            edited_df.loc[
                changed_rows,
                "Updated Date"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


            save_data(
                edited_df
            )


            st.success(
                "Changes saved successfully"
            )


    st.download_button(

        label="Download Latest CSV",

        data=edited_df.to_csv(index=False),

        file_name="Customer_Review_Updated.csv",

        mime="text/csv"

    )