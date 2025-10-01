# Procfile for a Dagster OSS deployment on Heroku

# The 'web' process is special: it's the only process that receives external HTTP traffic.
# It must bind to the host '0.0.0.0' and the port specified in the '$PORT' env var.
web: dagster-webserver -h 0.0.0.0 -p $PORT

# The 'worker' process is for background tasks. Here, it runs the Dagster daemon,
# which is responsible for schedules, sensors, and the run queue.
worker: dagster-daemon run

