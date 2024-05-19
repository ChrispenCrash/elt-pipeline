FROM python:3.11-slim

# Install PostgreSQL command-line tools
RUN apt-get update && apt-get install -y postgresql-client-15 cron

COPY start.sh /app/start.sh
COPY elt_script.py .

WORKDIR /app

RUN echo "* * * * * python /app/elt_script.py" | crontab -
# RUN echo "* * * * * python /app/elt_script.py >> /var/log/cron.log 2>&1" > /etc/cron.d/elt_script && \
#     chmod 0644 /etc/cron.d/elt_script && \
#     crontab /etc/cron.d/elt_script && \
#     touch /var/log/cron.log

# Set the default command to run the ELT script
CMD ["python", "elt_script.py"]