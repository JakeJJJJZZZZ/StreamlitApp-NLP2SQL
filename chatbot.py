datatype_describe= "'trans_date_trans_time': This appears to be a datetime object, storing both the date and time of the transaction. 'merchant': This is a string object, representing the name of the merchant where the transaction took place. 'category': This is a string object, indicating the category of the transaction (e.g., grocery, gas, etc.). 'amt': This is a float64 object, representing the amount of money involved in the transaction. 'city': This is a string object, storing the city where the transaction occurred. 'state': This is a string object, storing the state where the transaction occurred. 'lat': This is a float64 object, representing the latitude of the city where the transaction took place. 'long': This is a float64 object, representing the longitude of the city where the transaction took place. 'city_pop': This is an int64 object, representing the population of the city where the transaction occurred. 'job': This is a string object, representing the occupation of the person involved in the transaction. 'dob': This is a string object, representing the date of birth of the person involved in the transaction. 'trans_num': This is a string object, representing the transaction number, which seems to be a unique identifier for each transaction. 'merch_lat': This is a float64 object, representing the latitude of the merchant location. 'merch_long': This is a float64 object, representing the longitude of the merchant location. 'is_fraud': This is a string object, representing whether the transaction was fraudulent (1 for fraud, 0 for not fraud)."


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
        "First understand the human natural language command, "
        "then construct only the formal SQL query needed to fulfill the command. "
        "Do not include any explanations, comments, or additional text. "
        "Output only the SQL code, and ensure you use the table name 'credit_card_fraud'. "
        "Here is the schema of the dataset:\n" + st.session_state.schema_description + datatype_describe
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








