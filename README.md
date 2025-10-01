# Dagster on Heroku: Deployment Guide

This guide provides the steps to deploy your generated Dagster application to Heroku.

## Prerequisites

1. A Heroku account.
2. The Heroku CLI installed and authenticated (`heroku login`).
3. A Git repository initialized in this project directory.
4. An AWS S3 bucket and corresponding AWS credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`).

## Deployment Steps

### 1. Create the Heroku Application

From your terminal, run the following command to create a new Heroku app. Replace `your-unique-dagster-app-name` with a name of your choice.

```sh
heroku create your-unique-dagster-app-name
```

### 2. Provision the PostgreSQL Database

Dagster requires a PostgreSQL database for storing its state. Provision the free "essential-0" tier add-on. Heroku will automatically configure the `DATABASE_URL` environment variable.

```sh
heroku addons:create heroku-postgresql:essential-0 --app your-unique-dagster-app-name
```

### 3. Set Environment Variables (Config Vars)

Configure the necessary environment variables for your Dagster instance.

- `DAGSTER_HOME`: Tells Dagster services where to find the `dagster.yaml` file.
- `S3_BUCKET_NAME`: The name of your S3 bucket for compute logs.
- `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY`: Your AWS credentials.

```sh
# Set DAGSTER_HOME to the root directory
heroku config:set DAGSTER_HOME=. --app your-unique-dagster-app-name

# Set AWS credentials for S3 log storage
heroku config:set S3_BUCKET_NAME="your-s3-bucket-name" --app your-unique-dagster-app-name
heroku config:set AWS_ACCESS_KEY_ID="your-aws-access-key" --app your-unique-dagster-app-name
heroku config:set AWS_SECRET_ACCESS_KEY="your-aws-secret-key" --app your-unique-dagster-app-name
```

### 4. Deploy the Application

Commit your files to Git and push the `main` branch to Heroku. This will trigger the build and deployment process.

```sh
git add .
git commit -m "Initial Dagster application setup"
git push heroku main
```

### 5. Scale the Dynos

By default, Heroku only starts the `web` process. You must manually scale up the `worker` process to run the Dagster daemon.

```sh
heroku ps:scale web=1 worker=1 --app your-unique-dagster-app-name
```

### 6. Open Your Dagster UI

Your Dagster instance is now live. Open it in your browser to view your assets.

```sh
heroku open --app your-unique-dagster-app-name
```

## Project Structure

```
dagster-heroku-project/
├── Procfile                # Defines process types for Heroku
├── requirements.txt        # Python dependencies
├── runtime.txt            # Python version
├── dagster.yaml           # Dagster instance configuration
├── workspace.yaml         # Dagster workspace definition
└── src/
    └── dagster_heroku_project/
        ├── __init__.py
        └── definitions.py  # Your Dagster assets and jobs
```

## Key Configuration Points

- **PostgreSQL Storage**: Uses Heroku Postgres via `DATABASE_URL` for persistent state storage
- **S3 Compute Logs**: Required due to Heroku's ephemeral filesystem
- **Two Process Types**: 
  - `web`: Runs the Dagster UI (dagster-webserver)
  - `worker`: Runs the Dagster daemon for schedules, sensors, and run coordination

## Troubleshooting

- **Check logs**: `heroku logs --tail --app your-unique-dagster-app-name`
- **Check dyno status**: `heroku ps --app your-unique-dagster-app-name`
- **Database connection**: Ensure `DATABASE_URL` is set automatically by the Postgres addon
- **S3 access**: Verify your AWS credentials have proper S3 bucket permissions

