# Multi-Container Database Application

## Purpose

This project is designed for educational purposes. It aims to help you learn how to:

- Set up and configure Docker containers.
- Create and manage a MariaDB database.
- Perform CRUD (Create, Read, Update, Delete) operations using SQL and Python from within the `localhost`
- Connect a simple Python application in one container to a MariaDB database in another

## Citation Instructions

If you use this repository in your work, please cite it as follows:

**GitHub Repository**: [multi-container-crud-app](https://github.com/francisco-camargo/multi-container-crud-app)

**Suggested Citation**:

- Author: Francisco Camargo
- Title: Multi-Container CRUD Application
- Source: [https://github.com/francisco-camargo/multi-container-crud-app](https://github.com/francisco-camargo/multi-container-crud-app)
- Date Accessed:

Please ensure proper attribution when using or modifying this work.

## Project Roadmap

### 1. Define the Database Schema

📌 **Milestone:** Create a SQL script to define the database structure (tables, relationships, constraints).

📄 **File:** `schema.sql`

🔹 This file will contain `CREATE TABLE` statements for your **three tables**.

### 2. Set Up Sample Data

📌 **Milestone:** Create a SQL script to insert test data into the tables.

📄 **File:** `seed.sql`

🔹 This file will contain `INSERT INTO` statements with **dummy data** to test queries.

### 3. Configure Docker for MariaDB

📌 **Milestone:** Create a Docker environment to run MariaDB.

📄 **Files:**

- `docker-compose.yaml` (to manage services like MariaDB).
- `.env` (to store environment variables). Use `.env-template` as a reference. Don't use quotes or spaces.

🔹 This ensures **MariaDB runs in a container** and is easy to start/stop.

🔹 **Data persistence** is achieved using a named Docker volume (`mariadb_data_volume`).

See section "How to Instantiate the MariaDB Container" to run the project at this stage.

Note, when running `docker compose up`:

- If you get a `unable to get image` error, it may be that docker engine is not running
- If port 3306 is unexpectedly already in use, it may be mysql. If so kill the process in task manager.

### 4. Connect Python to MariaDB

📌 **Milestone:** Write a Python script to run on the host machine to connect to the database, run queries, and retrieve data.

📄 **File:** `src/db_connect.py`

🔹 This script will use a MariaDB library (`mariadb`) to interact with the database. I chose `mariadb` over `sqlalchemy` because I will use SQL scripts instead of using ORM functionality so `mariadb` will suffice.

🔹 **Running the Script:**

1. **Install Dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

2. **Run the Script**:

    Ensure that the MariaDB container is running before executing the script.

    ```sh
    python src/db_connect.py
    ```

    This will connect to the MariaDB instance running in the Docker container and print a success message if the connection is established.

### 5. Explicit Database Creation (Optional)

📌 **Milestone:** Automate database setup with Python.

So far, `docker-compose.yaml` configuration already ensures that `init.sql` runs when the MariaDB container is started. Recall, that this was achieved by mounting the `/sql` directory to `/docker-entrypoint-initdb.d` in the container, which is a special directory that MariaDB uses to initialize the database.

Now we will create a script, `setup_db.py`, that handles the database creation directly.

While `docker-compose.yaml` handles the initial setup of the database, there are some scenarios where having a `setup_db.py` script can be beneficial:

- Reinitialization: If you need to reinitialize the database without restarting the container, a Python script can be run independently to reset the database state
- Environment Flexibility: The script can be used in environments where Docker is not available or not preferred, such as local development without containers
- Additional Logic: The script can include additional logic, such as conditional checks, logging, or more complex initialization steps that are not easily handled by SQL scripts alone
- CI/CD Integration: The script can be integrated into CI/CD pipelines to ensure the database is correctly set up before running tests or deploying the application

📄 **File:** `setup_db.py`

🔹 This script will:

✅ Create the database (if it doesn’t exist).

### **6. Initialize Database Schema and Data**

📌 **Milestone:** Create tables and populate with initial data.

📄 **File:** `initialize_db.py`

🔹 This script will:

✅ Connect to the database created by `setup_db.py`

✅ Execute `schema.sql` to create the tables

✅ Execute `seed.sql` to populate tables with test data

🔹 **Running the Script:**

```sh
python src/initialize_db.py
```

### 7. Implement CRUD Operations

📌 **Milestone:** Create a comprehensive CRUD interface that can be used from `localhost`.

📄 **File:** `crud_operations.py`

🔹 This script will implement:

- Create: Insert new records
- Read: Retrieve existing records
- Update: Modify existing records
- Delete: Remove records

### 8. Containerize the Python App

📌 **Milestone:** Run your Python scripts inside a Docker container.

📄 **File:** `Dockerfile` (for Python container).

🔹 This allows your **Python app** to run in a container alongside MariaDB.

- Added `python-app` service to `docker-compose.yaml`
- Created dedicated `python-app` directory for application files
  - `Dockerfile` - Container configuration for Python app
  - `requirements.txt` - Python dependencies
  - `run.sh` - Application startup script
  - Python source files (*.py)

### 9. Return logging back to the host machine

📌 **Milestone:** Add logging to the `python-app` that saves logs to a file. A Docker volume will persist the logs into the localhost.

The logs will show:

- Timestamp for each log entry
- Log level (DEBUG, INFO, ERROR, etc.)
- Component name
- Detailed message

The logs will be available within the `logs` directory in the `localhost` and will be overwritten each time the container runs.

This setup will help you:

- Debug database connection issues
- Track SQL query execution
- Monitor application state
- Troubleshoot errors in real-time

## How to Instantiate the MariaDB Container

1. **Clone the Repository**:

    ```sh
    git clone https://github.com/francisco-camargo/multi-container-crud-app.git
    cd multi-container-crud-app
    ```

2. **Create the `.env` File**:
    Copy the `.env-template` file to `.env` and fill in the required environment variables.

    ```sh
    cp .env-template .env
    ```

3. **Build and Start the MariaDB Container**:
    Use Docker Compose to build and start the MariaDB container.

    ```sh
    docker compose up --build -d
    ```

4. **Initialize the Database**:
    Run the setup script to create and initialize the database:

    ```sh
    python src/setup_db.py
    ```

5. **Stop the MariaDB Container**:
    To stop the MariaDB container and clean up, use one of the following approaches:

    ```sh
    # Just stop the container but keep the database volume
    docker compose down

    # Stop the container and remove the declared volume
    docker compose down -v

    # To delete just the database but keep the container running:
    python src/delete_db.py
    ```

6. **Access the MariaDB Container**:
    To access the MariaDB container, use the following command:

    ```sh
    docker exec -it mariadb_container bash
    ```

    To enter MariaDB run

    ```sh
    mariadb -u user -puserpassword
    ```

    Or, alternatively, run

    ```sh
    docker exec -it mariadb_container mariadb -u user -puserpassword
    ```

    Either way, once you are in the MariaDB program, you can verify that the database is up by running

    ```sh
    SHOW DATABASES;

    >>>
    +--------------------+
    | Database           |
    +--------------------+
    | crud_db            |
    | information_schema |
    +--------------------+
    ```

- `information_schema`: A system database that contains metadata about the database server and its objects. It is automatically created and managed by MariaDB.
- `crud_db`: A user-defined database created for your application to store your application's data. The name is defined in `.env`
