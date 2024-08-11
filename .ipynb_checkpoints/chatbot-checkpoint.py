import os
import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def initialize_chatbot(schema_description):
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "system", "content": schema_description},
        ]

def process_user_input(prompt):
    hidden_instruction = (
        "First understand the following command, "
        "then construct only the formal SQL query needed to fulfill the command. "
        "Do not include any explanations, comments, or additional text. "
        "Output only the SQL code, and ensure you use the table name 'credit_card_fraud'. "
        "Here is the schema of the dataset:\n" + st.session_state.schema_description
    )

    # Combine the hidden instruction, schema description, and user prompt internally
    full_prompt = hidden_instruction + "\nUser's question: " + prompt

    # Generate SQL query using OpenAI
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": full_prompt}],
        model="gpt-3.5-turbo",
    ).choices[0].message.content

    # Clean the response
    sql_query = response.replace("dataset_name", "credit_card_fraud").strip("```sql").strip("```")
    
    return sql_query








