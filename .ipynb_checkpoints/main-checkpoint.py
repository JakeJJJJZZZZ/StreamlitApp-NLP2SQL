import streamlit as st
import pandas as pd
import db_manager
import chatbot

# Initialize Streamlit app
st.title("🧠🤖Credit Card Fraud Detection Chatbot ")
# Add a description or instruction below the title
st.markdown("""
Welcome to the Credit Card Fraud Detection Chatbot! This app allows you to upload a credit card transaction dataset and interact with the data through natural language questions.

### Instructions:
1. **Upload your dataset**: Start by uploading your `Credit_Card_Fraud.csv` file using the button below.
2. **Ask questions**: After the dataset is uploaded, you can ask questions about the dataset in natural language. The chatbot will convert your questions into SQL queries and display the results.
3. **Explore the data**: Use the chatbot to explore patterns, detect anomalies, and investigate potential fraudulent activities in your dataset.

example question: 
-What is the distribution of transaction amounts (amt) across different states?
-What are the top 5 cities with the highest number of fraudulent transactions?

Feel free to get started by uploading your dataset!
""")

# Step 1: File upload
uploaded_file = st.file_uploader("Upload your Credit_Card_Fraud.csv file", type=["csv"])

if uploaded_file and "dataset_uploaded" not in st.session_state:
    # Step 2: Load data into DataFrame and SQLite
    df = pd.read_csv(uploaded_file)
    db_manager.create_db_and_load_data(df)

    st.success(f"Data loaded into the SQLite database successfully!")
    
    # Step 3: Display DataFrame preview once after dataset upload
    st.write("Preview of the uploaded data:")
    st.dataframe(df)

    # Mark dataset as uploaded to prevent re-uploading or re-displaying
    st.session_state.dataset_uploaded = True

    # Save the schema description in session state
    st.session_state.schema_description = db_manager.generate_schema_description(df)

# Step 4: Handle chatbot interactions only after dataset is uploaded
if "dataset_uploaded" in st.session_state:
    # Initialize the chatbot for each new query to keep the session active
    chatbot.initialize_chatbot(st.session_state.schema_description)

    # Handle user queries
    if prompt := st.chat_input("Ask a question about the credit card fraud dataset:"):
        # Process the user input and generate SQL query
        sql_query = chatbot.process_user_input(prompt)

        # Open a new connection for each query execution
        conn = db_manager.get_connection()
        
        # Display the query results along with the SQL query
        db_manager.display_query_and_results(conn, sql_query)

        # Close the connection after executing the query
        db_manager.close_connection(conn)









