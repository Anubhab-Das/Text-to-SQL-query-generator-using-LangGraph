import psycopg2
import os

# Update connection parameters as needed:
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="text_to_sql_gen",  # Use the database you just created
    user="postgres",             # Adjust the username if needed
    password="postgres"          # Adjust the password if necessary
)
cursor = conn.cursor()

# Directory containing CSV files
csv_dir = "data/"

# Loop through each CSV file and import
for file in ['titles.csv', 'employees.csv', 'departments.csv', 'dept_emp.csv', 'dept_manager.csv', 'salaries.csv']:
    print(f"Processing {file}")
    if file.endswith(".csv"):
        table_name = os.path.splitext(file)[0]  # Table name based on file name
        file_path = os.path.join(csv_dir, file)
        print(f"Creating table: {table_name}")

        # Create table based on file name. Adjust schema as needed:
        if table_name == "employees":
            cursor.execute("""
                CREATE TABLE employees (
                    emp_no INT NOT NULL,
                    emp_title_id VARCHAR NOT NULL,
                    birth_date DATE NOT NULL,
                    first_name VARCHAR NOT NULL,
                    last_name VARCHAR NOT NULL,
                    sex VARCHAR NOT NULL,
                    hire_date DATE NOT NULL,
                    PRIMARY KEY (emp_no),
                    FOREIGN KEY (emp_title_id) REFERENCES titles (title_id)
                );
            """)
        elif table_name == "departments":
            cursor.execute("""
                CREATE TABLE departments (
                    dept_no VARCHAR NOT NULL,
                    dept_name VARCHAR NOT NULL,
                    PRIMARY KEY (dept_no)
                );
            """)
        elif table_name == "titles":
            cursor.execute("""
                CREATE TABLE titles (
                    title_id VARCHAR NOT NULL,
                    title VARCHAR NOT NULL,
                    PRIMARY KEY (title_id)
                );
            """)
        elif table_name == "dept_emp":
            cursor.execute("""
                CREATE TABLE dept_emp (
                    emp_no INT NOT NULL,
                    dept_no VARCHAR NOT NULL,
                    PRIMARY KEY (emp_no, dept_no),
                    FOREIGN KEY (emp_no) REFERENCES employees (emp_no),
                    FOREIGN KEY (dept_no) REFERENCES departments (dept_no)
                );
            """)
        elif table_name == "salaries":
            cursor.execute("""
                CREATE TABLE salaries (
                    emp_no INT NOT NULL,
                    salary INT NOT NULL,
                    PRIMARY KEY (emp_no),
                    FOREIGN KEY (emp_no) REFERENCES employees (emp_no)
                );
            """)
        elif table_name == "dept_manager":
            cursor.execute("""
                CREATE TABLE dept_manager (
                    dept_no VARCHAR NOT NULL,
                    emp_no INT NOT NULL,
                    PRIMARY KEY (dept_no, emp_no),
                    FOREIGN KEY (emp_no) REFERENCES employees (emp_no),
                    FOREIGN KEY (dept_no) REFERENCES departments (dept_no)
                );
            """)

        # Import CSV into table
        with open(file_path, "r") as f:
            cursor.copy_expert(f"""
                COPY {table_name} FROM STDIN WITH DELIMITER ',' CSV HEADER;
            """, f)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
