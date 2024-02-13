# Development - Documentation - Django Event Management

Contents:

- [Requirements files](#requirements-files)
- [Releases](#releases)

## Requirements files

- requirements_dev.txt
  - Manually created, contains general modules like Django, Bootstrap, Markdown
  - Additionally: Django debug toolbar
- requirements_dev_all.txt
  - Exported requirements (`pip freeze > requirements_dev_all.txt`)
- requirements_prod.txt
  - Manually created, contains general modules like Django, Bootstrap, Markdown
  - Additionally: SQL
- requirements_test.txt
  - Manually created, contains general modules like Django, Bootstrap, Markdown

## Releases

If possible, exacty one additional migrations file should be added per release. The following approach can be used:

- Delete your local `db.sqlite3` file
- Delete all local migration files after the last release
- Run `python .\manage.py makemigrations` to create a new file for the current release

### Notes about model updates (migrations)

Migrations should be included in the code repository:

> The migration files for each app live in a “migrations” directory inside of that app, and are designed to be committed to, and distributed as part of, its codebase. You should be making them once on your development machine and then running the same migrations on your colleagues’ machines, your staging machines, and eventually your production machines.  
Source: <https://docs.djangoproject.com/en/4.2/topics/migrations/>

> The reason that there are separate commands to make and apply migrations is because you’ll commit migrations to your version control system and ship them with your app; they not only make your development easier, they’re also usable by other developers and in production.  
Source: <https://docs.djangoproject.com/en/4.2/intro/tutorial02/>
