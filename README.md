# Dagster on Heroku: Deployment Guide

This guide provides the steps to deploy your generated Dagster application to Heroku.

## Prerequisites

1. A Heroku account.
2. The Heroku CLI installed and authenticated (`heroku login`).
3. A Git repository initialized in this project directory.

## Quick Deploy

This project includes an `app.json` file for streamlined deployment. The manifest will automatically provision:
- PostgreSQL database (heroku-postgresql:essential-0)
- S3-compatible storage via HDrive (hdrive:developer-s3)
- Web and worker dynos (standard-1x)

<a href="https://deploy.herokuapps.ai?template=https://github.com/aagnone-sfhk/heroku-dagster">
    <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku">
</a>

The HDrive addon automatically provides S3-compatible storage and sets the required environment variables. Alternatively, follow the manual steps below if you want to use your own AWS S3 bucket.

## Manual Deployment Steps

### 1. Create the Heroku Application

From your terminal, run the following command to create a new Heroku app. Replace `your-unique-dagster-app-name` with a name of your choice.

```sh
heroku create your-unique-dagster-app-name
```

### 2. Provision Add-ons

Dagster requires a PostgreSQL database for state storage and S3-compatible storage for compute logs (due to Heroku's ephemeral filesystem).

```sh
# PostgreSQL database - automatically sets DATABASE_URL
heroku addons:create heroku-postgresql:essential-0 --app your-unique-dagster-app-name

# HDrive provides S3-compatible storage - automatically sets HDRIVE_S3_* variables
heroku addons:create hdrive:developer-s3 --app your-unique-dagster-app-name
```

The Procfile converts `DATABASE_URL` (from Postgres) to `DAGSTER_DATABASE_URL`, updating the scheme from `postgres://` to `postgresql://` for SQLAlchemy 2.0 compatibility.

### 3. Set Environment Variables (Config Vars)

Set the required environment variable:

```sh
# Set DAGSTER_HOME to the directory where Dagster looks for dagster.yaml configuration file
heroku config:set DAGSTER_HOME=/app --app your-unique-dagster-app-name
```

**Note**: If you prefer to use your own AWS S3 bucket instead of HDrive, skip the HDrive addon and manually set `HDRIVE_S3_BUCKET`, `HDRIVE_S3_ACCESS_KEY`, and `HDRIVE_S3_SECRET_KEY`.

### 4. Deploy the Application

Commit your files to Git and push the `main` branch to Heroku. This will trigger the build and deployment process.

```sh
git add .
git commit -m "Initial Dagster application setup"
git push heroku main
```

### 5. Scale the Dynos

Scale up both processes. The `worker` process runs the Dagster daemon for schedules, sensors, and run coordination.

```sh
heroku ps:scale web=1:standard-1x worker=1:standard-1x --app your-unique-dagster-app-name
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
├── app.json               # Heroku app manifest for deployment
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

- **PostgreSQL Storage**: Uses Heroku Postgres via `DAGSTER_DATABASE_URL` for persistent state storage. The Procfile automatically converts Heroku's `DATABASE_URL` (which uses `postgres://`) to `DAGSTER_DATABASE_URL` (using `postgresql://`) for SQLAlchemy 2.0 compatibility.
- **S3 Compute Logs**: Uses HDrive (S3-compatible storage) for compute logs, required due to Heroku's ephemeral filesystem. HDrive automatically provides and configures the necessary environment variables.
- **Two Process Types**: 
  - `web`: Runs the Dagster UI (dagster-webserver) on standard-1x dyno
  - `worker`: Runs the Dagster daemon for schedules, sensors, and run coordination on standard-1x dyno

## Troubleshooting

- **Check logs**: `heroku logs --tail --app your-unique-dagster-app-name`
- **Check dyno status**: `heroku ps --app your-unique-dagster-app-name`
- **Check addons**: `heroku addons --app your-unique-dagster-app-name`
- **Database connection**: Ensure `DATABASE_URL` is set automatically by the Postgres addon. The Procfile converts this to `DAGSTER_DATABASE_URL` with the correct `postgresql://` scheme.
- **S3 storage**: HDrive automatically provides S3-compatible storage and sets the required environment variables. Check with `heroku config --app your-unique-dagster-app-name` to verify `HDRIVE_S3_*` variables are present.
- **Code server heartbeat warnings**: On standard-1x dynos, you may occasionally see "No heartbeat received" warnings due to resource constraints. This doesn't prevent the app from working, though responses may be slower during heavy processing.

