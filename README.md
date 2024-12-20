# Chat with MySQL

## Overview
**Chat with MySQL** is a Streamlit-based application that enables users to interact with their MySQL database using natural language queries. This tool leverages advanced language models to translate user questions into SQL queries, execute them on the connected database, and provide clear, natural language responses based on the query results.

## Features
- **Natural Language SQL Generation**: Automatically generate SQL queries from user questions.
- **Dynamic Schema Validation**: Ensures queries match the database schema.
- **Error Handling**: Robust handling of SQL syntax and connection errors.
- **Interactive Chat Interface**: A user-friendly chat interface for seamless interaction.

## Prerequisites
- Python 3.9+
- MySQL server
- A Google API Key for accessing the language model (e.g., Gemini 1.5 Pro).

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/PriyanshuDey23/ChatMySQL.git
   cd chat-with-mysql
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory with the following content:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   ```

## Usage

1. **Run the Application**
   ```bash
   streamlit run app.py
   ```

2. **Connect to Your Database**
   - Use the sidebar to input your MySQL database credentials (host, port, username, password, and database name).
   - Click the "Connect" button to establish a connection.

3. **Ask Questions**
   - Type a question about your database in the chat input field (e.g., "What are the top 5 customers by revenue?").
   - The app will generate a SQL query, execute it on the connected database, and provide a response.

## Example

### User Input
> "What is the total revenue for each product category?"

### Generated SQL Query
```sql
SELECT `category_name`, SUM(`revenue`) AS `total_revenue`
FROM `products`
GROUP BY `category_name`
ORDER BY `total_revenue` DESC;
```

### Response
> "The total revenue for each product category is displayed below, sorted in descending order."

## Error Handling
- **Connection Errors**: Displays a user-friendly error message if the database connection fails.
- **SQL Errors**: Catches and explains SQL syntax errors or issues with reserved keywords.

## Technologies Used
- **Streamlit**: Interactive web interface
- **LangChain Core**: Message handling and prompt management
- **Google Generative AI**: Natural language to SQL conversion
- **PyMySQL**: MySQL database connection
- **SQLAlchemy**: Database utility wrapper

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Streamlit](https://streamlit.io)
- [LangChain](https://langchain.com)
- [Google Generative AI](https://aistudio.google.com/prompts/new_chat)



