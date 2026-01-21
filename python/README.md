# Python Task List Application

This project is based on `Python 3.12`.

**Important:**
This `Python` example contains additional exercises for demonstrating your ability to work with `numpy` and `pandas`.
Also give some focus to material found in `task_analytics.py` and integrating the functionality with the application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Console Mode (Default)
To run the console application:
```bash
python task_list_application.py
```

### Web API Mode
To run the Flask web server:
```bash
python task_list_application.py --web
```

The API will be available at `http://localhost:8080/tasks`

## Running Tests

Run the test suite with pytest:
```bash
pytest test_application.py
```

## Project Structure

- `task.py` - Task model class
- `task_list.py` - Core task list logic and console interface
- `task_controller.py` - Flask REST API endpoints
- `task_list_application.py` - Main application entry point
- `test_application.py` - Unit tests
- `requirements.txt` - Python dependencies
- `task_analytics.py` - Additional analytics to implement.