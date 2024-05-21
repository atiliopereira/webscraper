# # Web Scraper

Web Scraper is a Django application that allows you to get all the information of a given page and gets a list of all of the links in that page.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/atiliopereira/webscraper.git
    ```

2. Navigate to the project directory:
    ```bash
    cd webscraper
    ```

3. Install the project dependencies using pipenv:
    ```bash
    pipenv install
    ```

4. Activate the pipenv shell:
    ```bash
    pipenv shell
    ```

5. Run the migrations:
    ```bash
    python manage.py migrate
    ```

6. Start the server:
    ```bash
    python manage.py runserver
    ```

The application will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

To access the user registration and login pages, navigate to [http://127.0.0.1:8000/accounts/](http://127.0.0.1:8000/accounts/).

## Testing

This project uses pytest for testing.

To run the tests, use the following command:

```bash
pytest
```
