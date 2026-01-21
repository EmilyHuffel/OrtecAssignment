import sys
from task_list import TaskList
from task_controller import app


def main():
    if len(sys.argv) == 1:
        print("Starting console Application")
        TaskList.start_console()
    else:
        app.run(host='localhost', port=8080, debug=True)
        print("localhost:8080/tasks")


if __name__ == "__main__":
    main()
