# Deployment - Documentation - Django Event Management

- How to deploy Django  
  <https://docs.djangoproject.com/en/4.2/howto/deployment/>
- Deployment checklist  
  <https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/>
  - Inspect the entire Django project for common problems:  
  `python .\manage.py check --deploy --settings=event_management.settings_prod`

## Backup

- An SQL backup can be created with the following command:  
  `podman exec -t events_postgres_1 pg_dumpall -c -U django > dump.sql`
- Restore a backup:
  - `podman stop events_events_1`
  - `podman exec -it events_postgres_1 psql -U django -d postgres -c "DROP DATABASE events;"`
  - `podman exec -it events_postgres_1 psql -U django -d postgres -c "CREATE DATABASE events;"`
  - `cat dump.sql | podman exec -i events_postgres_1 psql -U django --dbname=events`
  - `podman start events_events_1`
