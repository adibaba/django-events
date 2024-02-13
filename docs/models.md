# Models - Documentation - Django Event Management

Contents:

- [Models diagram](#models-diagram)
- [User model](#user-model)

## Models diagram

- Also see: *User roles* and *Event/Registration states* in [Concepts](concepts.md)
- File: [../events/models.py](../events/models.py)

```text
                  +-----------------+     +----------------------+
                  | User            | m:n | Group                |
                  |                 +-----+                      |
                  | first_name      |     | • moderators         |
                  | last_name       |     +----------------------+
                  | email           |
                  |                 |
+-----------+     | ■ is_active     |
| Level     |     | ■ is_staff      |
|           <--+  | ■ is_superuser  |     +----------------------+
| title     |  |  +-+---------------+     | Event                |
| order     |  |    | 1:1                 |                      |
+-----------+  |  +-+---------------+     | title                |
               |  | Person          |     | description          |
+-----------+  +--+                 |     | date                 |
| Country   |     | ■ is_supervisor |     | time_begin           |
|           <-----+                 |     | duration             |
| name      |     |                 |     | maximum_participants |
|           |     |                 |     | project_numbers      |
+-----------+     |                 |     |                      |
                  |                 |     | ■ leisure            |
+-----------+     |                 |     | ■ published          |
| Unit      <-----+                 +-----+ ■ canceled           |
|           |     +-+-^--+-+------^-+ m:n +---------^------------+
| title     |       | |  | |      | presenters      |
| order     |       | |  | |      |                 |
+-----------+       | |  | |      |                 |
                    | |  | |    +-+-----------------+------------+
         supervisor +-+  | |    | Registration                   |
                         | |    |                                |
                     m:n | |    | ■ approvement_state            |
         representatives +-+    | ■ canceled                     |
                                +--------------------------------+
+---> ForeignKey
+---+ ManyToManyField, OneToOneField
    ■ BooleanField
    • Instance
      https://asciiflow.com/legacy/
```

![](images/models-2023-11-08.png)

## User model

Currently, the *Person* model has a One-To-One Link With the *User* model.
This is based on:

- [*simple is better than complex*: How to Extend Django User Model](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone)
  - [*Django documentation - Database transactions*: Controlling transactions explicitly](https://docs.djangoproject.com/en/4.2/topics/db/transactions/#controlling-transactions-explicitly)
  - [*Django documentation - Using the Django authentication system*: The login_required decorator](https://docs.djangoproject.com/en/4.2/topics/auth/default/#the-login-required-decorator)
- [*Django documentation - Customizing authentication in Django*: Extending the existing User model](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#extending-the-existing-user-model)

Another option for changes in the future is a custom user model

- [*/var/*: Use a custom user model](https://spapas.github.io/2022/09/28/django-guidelines/#use-a-custom-user-model)
- [*Django documentation - Customizing authentication in Django*: Using a custom user model when starting a project](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)
