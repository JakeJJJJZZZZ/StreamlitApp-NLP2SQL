import sqlite3
import pandas as pd
import streamlit as st

DB_FILE = 'credit_card_fraud.db'

def create_db_and_load_data(df):
    conn = sqlite3.connect(DB_FILE)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df.to_sql('credit_card_fraud', conn, if_exists='replace', index=False)
    conn.close()

def generate_schema_description(df):
    schema_description = "The dataset 'credit_card_fraud' has the following columns:\n"
    for column in df.columns:
        schema_description += f"- {column} ({df[column].dtype})\n"
    return schema_description

def get_connection():
    return sqlite3.connect(DB_FILE)

def display_query_and_results(conn, sql_query):
    # Display the SQL query only here
    st.write("Generated SQL Query:")
    st.code(sql_query, language='sql')

    try:
        result_df = pd.read_sql_query(sql_query, conn)
        st.write("Query Results:")
        st.dataframe(result_df)
    except Exception as e:
        st.error(f"An error occurred: {e}")

def close_connection(conn):
    conn.close()




