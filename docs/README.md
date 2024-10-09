# Dare Dreamer Job Search Platform

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/daredreamer.git
   cd daredreamer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set the FLASK_APP environment variable:
   On Windows:
   ```bash
   set FLASK_APP=src.wsgi:app
   ```
   On Unix or MacOS:
   ```bash
   export FLASK_APP=src.wsgi:app
   ```

5. Set up the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```bash
   python src/main.py
   ```

## Usage

1. Register as a user or employer
2. Search for jobs or post new job listings
3. Apply for jobs and manage applications
4. Schedule interviews and track your job search progress

## Running Tests

To run the tests, use the following command:
```bash
python -m unittest discover tests
```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
