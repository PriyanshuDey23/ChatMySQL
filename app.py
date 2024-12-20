from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os


# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API key is missing! Please set it in the .env file.")
    st.stop()

# Initialize database connection
def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    try:
        db_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        return SQLDatabase.from_uri(db_uri)
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        st.stop()

# SQL Chain
def get_sql_chain(db):
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    <SCHEMA>{schema}</SCHEMA>
    Conversation History: {chat_history}
    Write only the SQL query and nothing else.
    Question: {question}
    SQL Query:
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    def get_schema(_):
        return db.get_table_info()

    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

# Generate response from SQL query
def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    try:
        sql_chain = get_sql_chain(db)
        sql_query = sql_chain.invoke({
            "question": user_query,
            "chat_history": chat_history,
        })

        if not sql_query.strip():
            return "Sorry, I couldn't generate a SQL query for that question."

        # Wrap the table name in backticks to handle reserved keywords
        sql_query = sql_query.replace("FROM rank", "FROM `rank`")

        sql_result = db.run(sql_query)

        template = """
        You are a data analyst. Based on the question, SQL query, and its result, provide a natural language explanation.
        <SCHEMA>{schema}</SCHEMA>
        Question: {question}
        SQL Query: {query}
        SQL Response: {response}
        """
        prompt = ChatPromptTemplate.from_template(template)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

        explanation_chain = (
            RunnablePassthrough.assign(
                query=lambda _: sql_query,
                response=lambda _: sql_result,
                schema=lambda _: db.get_table_info(),
            )
            | prompt
            | llm
            | StrOutputParser()
        )
        return explanation_chain.invoke({
            "question": user_query,
        })
    except Exception as e:
        return f"Error processing your query: {e}"

# Streamlit app setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
    ]

st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_balloon:")
st.title("Chat with MySQL")

# Sidebar for database connection
with st.sidebar:
    st.subheader("Settings")
    st.write("Connect to your MySQL database.")

    # Sidebar input fields for database connection
    host = st.text_input("Host", value="localhost", key="Host")
    port = st.text_input("Port", value="3306", key="Port")
    user = st.text_input("User", value="root", key="User")
    password = st.text_input("Password", type="password", key="Password")
    database = st.text_input("Database Name", placeholder="Database Name", key="DataBase")

    if st.button("Connect"):
        if not all([host, port, user, password, database]):
            st.error("All fields are required to connect to the database.")
        else:
            with st.spinner("Connecting to database..."):
                st.session_state.db = init_database(user, password, host, port, database)
                st.success("Connected to database!")

# Display chat messages
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

# Handle user input
user_query = st.chat_input("Type a message...")
if user_query and user_query.strip():
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        if "db" not in st.session_state:
            st.error("Please connect to the database first!")
        else:
            response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
            st.markdown(response)
            st.session_state.chat_history.append(AIMessage(content=response))
