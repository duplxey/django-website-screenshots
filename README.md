# Taking Website Screenshots with Django, Celery, and Playwright

A simple website screenshot application written in Django, with Celery for background tasks and Playwright for taking screenshots.

## Want to learn how to build this?

Read the [article](#).

## Want to use this project?

1. Fork/Clone

2. Build and start the containers:

    ```sh
    $ docker compose up --build -d
    ```

3. Apply the migrations:

    ```sh
    $ docker compose exec web python manage.py migrate
    ```

4. Navigate to [http://localhost:8000/](http://localhost:8000/) in your favorite web browser.
