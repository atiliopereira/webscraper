# Web Scraper

Web Scraper is a Django application that allows you to get all the information of a given page and gets a list of all of the links in that page.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/atiliopereira/webscraper.git
    ```

2. [Install pipenv](https://docs.pipenv.org/) system-wide or locally but outside a virtualenv. Alternatively, follow these commands:
    ```bash
    pip install -U pip
    pip install pipenv
    ```

3. Navigate to the project directory:
    ```bash
    cd webscraper
    ```

4. Install the project dependencies using pipenv:
    ```bash
    pipenv install
    ```

5. Activate the pipenv shell:
    ```bash
    pipenv shell
    ```

6. Run the migrations:
    ```bash
    python manage.py migrate
    ```

7. Start the server:
    ```bash
    python manage.py runserver
    ```

The application will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

To access the user registration and login pages, navigate to [http://127.0.0.1:8000/accounts/](http://127.0.0.1:8000/accounts/).

[Optional]:
You can create a superuser that will allow you additional functions like:

- Create, Update and Delete Pages, Links and Users.
- See all the Pages scraped by all the users.
    ```bash
        python manage.py createsuperuser
    ```

## Testing

This project uses pytest for testing.

To run the tests, use the following command:

```bash
pytest
```

### Dependencies

- pytest: Testing
- beautifulsoup4: Scraping
- allauth: Additional authentication functionality
- pipenv: Dependencies management
