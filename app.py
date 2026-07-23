import streamlit as st
import pandas as pd
import os


# ==========================================================
# CONFIGURATION
# ==========================================================

DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "customer_review.csv")

ADMIN_PASSWORD = "Admin@123"


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



# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Customer Review Tool",
    layout="wide"
)



# ==========================================================
# FUNCTIONS
# ==========================================================

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


    return pd.DataFrame()



def save_data(df):

    df.to_csv(
        DATA_FILE,
        index=False
    )



# ==========================================================
# ADMIN MODE
# ==========================================================

params = st.query_params


admin_mode = (
    "admin" in params
    and params["admin"] == "true"
)



# ==========================================================
# ADMIN UPLOAD
# ==========================================================

if admin_mode:


    st.title("Admin - Upload Customer File")


    password = st.text_input(
        "Admin Password",
        type="password"
    )


    if password == ADMIN_PASSWORD:


        st.success(
            "Admin Access Granted"
        )


        uploaded_file = st.file_uploader(
            "Upload New Customer CSV",
            type=["csv"]
        )


        if uploaded_file:


            df = pd.read_csv(
                uploaded_file
            )


            # Add editable columns only

            if "Customer Status" not in df.columns:
                df["Customer Status"] = ""


            if "Remarks" not in df.columns:
                df["Remarks"] = ""



            df["Customer Status"] = (
                df["Customer Status"]
                .fillna("")
                .astype(str)
            )


            df["Remarks"] = (
                df["Remarks"]
                .fillna("")
                .astype(str)
            )


            save_data(
                df
            )


            st.success(
                "Customer file uploaded successfully"
            )


            st.subheader(
                "File Preview"
            )


            st.dataframe(
                df.head(10)
            )



# ==========================================================
# USER REVIEW
# ==========================================================

else:


    st.title(
        "Customer Review"
    )


    df = load_data()



    if df.empty:


        st.warning(
            "No customer file available. Please contact Admin."
        )

        st.stop()



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

                options=STATUS_OPTIONS,

                required=False

            ),



            "Remarks":
            st.column_config.TextColumn(

                "Remarks"

            )

        },


        # Only allow editing these columns

        disabled=[

            col for col in df.columns

            if col not in [

                "Customer Status",

                "Remarks"

            ]

        ],


        num_rows="fixed"

    )



    if st.button(
        "Save Changes"
    ):


        save_data(
            edited_df
        )


        st.success(
            "Changes saved successfully"
        )



    st.download_button(

        label="Download Updated CSV",

        data=edited_df.to_csv(index=False),

        file_name="Customer_Review_Updated.csv",

        mime="text/csv"

    )