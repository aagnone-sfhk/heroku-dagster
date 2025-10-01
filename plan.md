Of course. Here is a detailed instruction set designed for an LLM app generator to create a complete, production-ready Dagster application using the Procfile-based deployment approach for Heroku.

-----

### **Instruction for LLM App Generator: Create a Heroku-Deployable Dagster Application (Procfile Method)**

**Objective:** Generate a complete Dagster application project, configured for a Procfile-based deployment on Heroku. The application should be structured with best practices for a Platform-as-a-Service (PaaS) environment, including externalized state management and proper process definitions.

**1. Project Structure**

Generate the following directory and file structure. This structure separates the application source code from the root-level configuration files required by Heroku.

```
dagster-heroku-project/
├── Procfile
├── requirements.txt
├── runtime.txt
├── dagster.yaml
├── workspace.yaml
└── src/
    └── dagster_heroku_project/
        ├── __init__.py
        └── definitions.py
```

**2. File Contents**

Populate each file with the exact contents specified below. Include all comments, as they provide critical context.

-----

**File: `Procfile`**

This file is the entry point for Heroku, defining the commands to run for each process type.[5, 6]

```procfile
# Procfile for a Dagster OSS deployment on Heroku

# The 'web' process is special: it's the only process that receives external HTTP traffic.
# It must bind to the host '0.0.0.0' and the port specified in the '$PORT' env var.
web: dagster-webserver -h 0.0.0.0 -p $PORT

# The 'worker' process is for background tasks. Here, it runs the Dagster daemon,
# which is responsible for schedules, sensors, and the run queue.
worker: dagster-daemon run
```

-----

**File: `runtime.txt`**

This file specifies the exact Python version for the Heroku buildpack to install.

```
python-3.10.13
```

-----

**File: `requirements.txt`**

This file lists all Python dependencies. In the Procfile model, dependencies for the core Dagster services and all user code are consolidated into this single file.

```
# Core Dagster libraries
dagster
dagster-webserver

# Library for PostgreSQL storage backend
dagster-postgres

# Library for using AWS S3 for compute log storage
# This is critical for Heroku's ephemeral filesystem
dagster-aws

# A production-grade web server, recommended for Heroku
gunicorn

# Example dependency for user code
pandas
```

-----

**File: `dagster.yaml`**

This is the central instance configuration file. It is configured to use external, persistent services, reading connection details and secrets from environment variables, which will be set as Heroku Config Vars.[7]

```yaml
# dagster.yaml: Production instance configuration for Heroku

# Configures the storage backend for run history, event logs, and schedule/sensor state.
# It uses PostgreSQL, which is provisioned as a Heroku add-on.
storage:
  postgres:
    # This directly consumes the DATABASE_URL provided by the Heroku Postgres add-on.
    # Using 'postgres_url' is the recommended approach for Heroku.
    postgres_url:
      env: DATABASE_URL

# Configures where stdout/stderr from computations are stored.
# Using a cloud-based manager like S3 is mandatory on Heroku due to its
# ephemeral filesystem, which would otherwise cause logs to be lost on dyno restarts.
compute_logs:
  module: dagster_aws.s3.compute_log_manager
  class: S3ComputeLogManager
  config:
    # The S3 bucket name is sourced from an environment variable.
    bucket:
      env: S3_BUCKET_NAME
    # A prefix to organize logs within the bucket.
    prefix: "dagster-compute-logs/"
    # Note: AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # should also be set as environment variables.

# Configures the run coordinator to queue runs, preventing the system from being
# overwhelmed by too many concurrent executions. This is a best practice for production.
run_coordinator:
  module: dagster.core.run_coordinator
  class: QueuedRunCoordinator
  config:
    max_concurrent_runs: 10
```

-----

**File: `workspace.yaml`**

This file tells the Dagster webserver and daemon where to find and load your user-defined code (your assets, jobs, etc.).[8]

```yaml
load_from:
  - python_module:
      # The name of the Python module containing your Dagster definitions.
      module_name: dagster_heroku_project.definitions
      # The directory to add to the Python path to find the module.
      working_directory: src
```

-----

**File: `src/dagster_heroku_project/__init__.py`**

This file marks the directory as a Python package. It can be left empty.

```python
# This file can be left empty.
```

-----

**File: `src/dagster_heroku_project/definitions.py`**

This file contains the core logic of your Dagster project. It defines the assets and jobs that will be visible in the UI. This example includes a simple asset that uses the `pandas` library.

```python
import pandas as pd
from dagster import Definitions, asset

@asset
def hello_asset():
    """An example asset that creates and returns a pandas DataFrame."""
    data = {'col1': [1, 2], 'col2': [3, 4]}
    return pd.DataFrame(data=data)

# The Definitions object is the entry point for Dagster to find all your definitions.
defs = Definitions(
    assets=[hello_asset],
)
```

-----

**3. Deployment and Operational Instructions**

Generate a `README.md` file that includes the following step-by-step instructions for the user to deploy and run the generated application on Heroku.

# Dagster on Heroku: Deployment Guide

This guide provides the steps to deploy your generated Dagster application to Heroku.

### Prerequisites

1.  A Heroku account.
2.  The Heroku CLI installed and authenticated (`heroku login`).
3.  A Git repository initialized in this project directory.
4.  An AWS S3 bucket and corresponding AWS credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`).

### Deployment Steps

1.  **Create the Heroku Application**
    From your terminal, run the following command to create a new Heroku app. Replace `your-unique-dagster-app-name` with a name of your choice.sh
    heroku create your-unique-dagster-app-name

    ```
    
    ```

2.  **Provision the PostgreSQL Database**
    Dagster requires a PostgreSQL database for storing its state. Provision the free "hobby-dev" tier add-on. Heroku will automatically configure the `DATABASE_URL` environment variable.

    ```sh
    heroku addons:create heroku-postgresql:hobby-dev --app your-unique-dagster-app-name
    ```

3.  **Set Environment Variables (Config Vars)**
    Configure the necessary environment variables for your Dagster instance.

      - `DAGSTER_HOME`: Tells Dagster services where to find the `dagster.yaml` file.
      - `S3_BUCKET_NAME`: The name of your S3 bucket for compute logs.
      - `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY`: Your AWS credentials.

    <!-- end list -->

    ```sh
    # Set DAGSTER_HOME to the root directory
    heroku config:set DAGSTER_HOME=. --app your-unique-dagster-app-name

    # Set AWS credentials for S3 log storage
    heroku config:set S3_BUCKET_NAME="your-s3-bucket-name" --app your-unique-dagster-app-name
    heroku config:set AWS_ACCESS_KEY_ID="your-aws-access-key" --app your-unique-dagster-app-name
    heroku config:set AWS_SECRET_ACCESS_KEY="your-aws-secret-key" --app your-unique-dagster-app-name
    ```

4.  **Deploy the Application**
    Commit your files to Git and push the `main` branch to Heroku. This will trigger the build and deployment process.

    ```sh
    git add.
    git commit -m "Initial Dagster application setup"
    git push heroku main
    ```

5.  **Scale the Dynos**
    By default, Heroku only starts the `web` process. You must manually scale up the `worker` process to run the Dagster daemon.[5]

    ```sh
    heroku ps:scale web=1 worker=1 --app your-unique-dagster-app-name
    ```

6.  **Open Your Dagster UI**
    Your Dagster instance is now live. Open it in your browser to view your assets.

    ```sh
    heroku open --app your-unique-dagster-app-name
    ```

<!-- end list -->

```
```