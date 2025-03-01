# Text-to-SQL AI Agent: Complete Setup and Execution Guide

This guide explains how to set up PostgreSQL, create a project directory, build the database tables and import data, and run a LangGraph-based text-to-SQL AI agent. The agent uses a Tavily-based language model client to convert natural language queries into SQL queries, executes them on a PostgreSQL database, and returns the results. You can use any LLM of your choice.

## 1. Setting Up PostgreSQL

### a. Install PostgreSQL (macOS Example with Homebrew)
Install Homebrew (if not installed):
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Install PostgreSQL:
brew install postgresql@14

Start PostgreSQL as a service:
brew services start postgresql@14

Verify PostgreSQL is running:
pg_ctl -D /usr/local/var/postgresql@14 status

### b. Create a New Database
Create a database (e.g., text_to_sql_gen):
createdb text_to_sql_gen

Verify the database is created:
psql -l

## 2. Setting Up Your Project Directory

Create a New Directory:
mkdir SQL_QUERY_GENERATOR
cd SQL_QUERY_GENERATOR

### Directory Structure:
Create a folder named data to store your CSV files.
In the root directory, create the following files:
create_tables.py – Creates tables and imports CSV data.
my_llm_module.py – Implements your Tavily-based language model client.
my_db_module.py – Sets up database connectivity and query execution.
agent.py – Contains the LangGraph-based AI agent workflow.
.env – Contains your environment variables (e.g., TAVILY_API_KEY).
.env File Example:
TAVILY_API_KEY=<YOUR_TAVILY_API_KEY>

## 3. Creating Tables and Importing Data

### a. create_tables.py
Create this file to connect to PostgreSQL, create your tables, and import CSV data.

### create_tables.py
import psycopg2
import os

### Connect to PostgreSQL (update with your own credentials)
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="text_to_sql_gen",
    user="<YOUR_DB_USER>",
    password="<YOUR_DB_PASSWORD>"
)
cursor = conn.cursor()

### Directory containing CSV files
csv_dir = "data/"

### Create 'titles' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS titles (
        title_id VARCHAR PRIMARY KEY,
        title VARCHAR NOT NULL
    );
""")
### Create 'employees' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        emp_no INT PRIMARY KEY,
        emp_title_id VARCHAR NOT NULL,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL
    );
""")
### Create 'salaries' table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS salaries (
        emp_no INT PRIMARY KEY,
        salary INT NOT NULL,
        FOREIGN KEY (emp_no) REFERENCES employees(emp_no)
    );
""")

### Import data from CSV files
with open(os.path.join(csv_dir, "titles.csv"), "r") as f:
    cursor.copy_expert("COPY titles FROM STDIN WITH CSV HEADER DELIMITER ',';", f)

with open(os.path.join(csv_dir, "employees.csv"), "r") as f:
    cursor.copy_expert("COPY employees FROM STDIN WITH CSV HEADER DELIMITER ',';", f)

with open(os.path.join(csv_dir, "salaries.csv"), "r") as f:
    cursor.copy_expert("COPY salaries FROM STDIN WITH CSV HEADER DELIMITER ',';", f)

conn.commit()
cursor.close()
conn.close()

print("Tables created and data imported successfully!")
b. Run the Script:
python3 create_tables.py

## 4. Building the AI Agent with LangGraph

The agent uses a Tavily-based LLM to generate SQL queries from natural language, executes them on your PostgreSQL database, and returns the results.

### a. my_llm_module.py
This file implements the Tavily client.

### b. my_db_module.py
This file handles database connectivity and query execution.

### c. agent.py
This file ties everything together into a LangGraph workflow.

## 5. Running the Agent

Ensure All Files Are in the Project Directory:

create_tables.py
my_llm_module.py
my_db_module.py
agent.py
data/ folder with your CSV files
.env file with your API key

Import Data (if not already done):
python3 create_tables.py

Run the Agent:
python3 agent.py

The workflow will:

Accept your natural language query.
Generate a SQL query using the Tavily client.
Execute the query on your PostgreSQL database.
Output the final answer with both the generated SQL query and the query result.
Additional Notes

Prompt Refinement:
If the generated SQL query isn’t correct, adjust the prompt in agent.py (initial_state["user_query"]) until it produces the desired result.
Post-Processing:
Additional post-processing in query_gen_node can help fix common mistakes.
Security:
Use environment variables or secure methods to store confidential information (API keys, database credentials).
Enhancements:
As your project evolves, consider adding nodes for query validation, error handling, and logging within the LangGraph workflow.
