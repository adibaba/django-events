# Example data - Documentation - Django Event Management

Contents:

- [Import data](#import-data)
- [Generate data](#generate-data)

## Import data

Execute the following command:  
`python manage.py loaddata events/fixtures/examples/0001_user.xml events/fixtures/examples/0002_person.xml events/fixtures/examples/0003_event.xml events/fixtures/examples/0004_registration.xml`

This creates the following data:

- 7 users / persons  
  (The default password for example users is `django`)
  - `aadmin`: superuser
  - `cconsultant`: created 5 events
  - `ddigital`: registered to all events, all open
  - `ffrance`: registered to all events, all approved
  - `ggcloud`: registered to all events, all rejected
  - `mmoderator`: moderator
  - `nnplatform`:  registered to all events, all approved, all canceled
  - `ssupervisor`: supervisor of all other persons, representatives: aadmin and cconsultant
- 5 events
  - *Lisp is leisure*: published, not canceled, **leisure**
  - *Web works*: published, not canceled, **not leisure**
  - *C++ Canceled*: published, **canceled**, not leisure
  - *Prolog in the past*: published, not canceled, not leisure, **date in past**
  - *Python Publishing*: **not published**, not canceled, not leisure

## Generate data

Execute the following command:  
`python manage.py populate`  
This creates User, Person, Event and Registration objects.

You can also specify some parameters:

```text
python manage.py help populate

Populates data: Creates User, Person, Event and Registration objects

options:
  --users USERS         Number of users/persons to create, default: 20
  --events EVENTS       Number of events to create, default: 40
  --password PASSWORD   Password for users, default: django
```

For example:  
`python manage.py populate --users=20 --events=40 --password=django`
