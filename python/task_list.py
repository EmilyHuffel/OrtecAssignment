import sys
from typing import Dict, List, TextIO
from task import Task
from task_analytics import TaskAnalytics


class TaskList:
    QUIT = "quit"

    def __init__(self, input_stream: TextIO, output_stream: TextIO):
        self._tasks: Dict[str, List[Task]] = {}
        self._input_stream = input_stream
        self._output_stream = output_stream
        self._last_id = 0
        self._analytics = TaskAnalytics()

    @staticmethod
    def start_console():
        task_list = TaskList(sys.stdin, sys.stdout)
        task_list.run()

    def run(self):
        self._output_stream.write("Welcome to TaskList! Type 'help' for available commands.\n")
        self._output_stream.flush()
        
        while True:
            self._output_stream.write("> ")
            self._output_stream.flush()
            command = self._input_stream.readline().strip()
            
            if command == self.QUIT:
                break
            
            self.execute(command)

    def execute(self, command_line: str):
        parts = command_line.split(" ", 1)
        command = parts[0]
        
        if command == "show":
            self._show()
        elif command == "add":
            self._add(parts[1] if len(parts) > 1 else "")
        elif command == "check":
            self._check(parts[1] if len(parts) > 1 else "")
        elif command == "uncheck":
            self._uncheck(parts[1] if len(parts) > 1 else "")
        # TODO: implement additional commands from TaskAnalytics
        # elif command == "import":
        # elif command == "export":
        # elif command == "summary":
        # etc.
        elif command == "help":
            self._help()
        else:
            self._error(command)

    def _show(self):
        for project_name, tasks in self._tasks.items():
            self._output_stream.write(f"{project_name}\n")
            for task in tasks:
                status = 'x' if task.done else ' '
                self._output_stream.write(f"    [{status}] {task.id}: {task.description}\n")
            self._output_stream.write("\n")
        self._output_stream.flush()

    def _add(self, command_line: str):
        parts = command_line.split(" ", 1)
        subcommand = parts[0]
        
        if subcommand == "project":
            self._add_project(parts[1] if len(parts) > 1 else "")
        elif subcommand == "task":
            task_parts = parts[1].split(" ", 1) if len(parts) > 1 else []
            if len(task_parts) >= 2:
                self._add_task(task_parts[0], task_parts[1])

    def _add_project(self, name: str):
        self._tasks[name] = []

    def _add_task(self, project: str, description: str):
        project_tasks = self._tasks.get(project)
        if project_tasks is None:
            self._output_stream.write(f'Could not find a project with the name "{project}".\n')
            self._output_stream.flush()
            return
        
        project_tasks.append(Task(self._next_id(), description, False))

    def _check(self, id_string: str):
        self._set_done(id_string, True)

    def _uncheck(self, id_string: str):
        self._set_done(id_string, False)

    def _set_done(self, id_string: str, done: bool):
        try:
            task_id = int(id_string)
        except ValueError:
            return
        
        for project_name, tasks in self._tasks.items():
            for task in tasks:
                if task.id == task_id:
                    task.done = done
                    return
        
        self._output_stream.write(f"Could not find a task with an ID of {task_id}.\n")
        self._output_stream.flush()

    def _help(self):
        self._output_stream.write("Commands:\n")
        self._output_stream.write("  show\n")
        self._output_stream.write("  add project <project name>\n")
        self._output_stream.write("  add task <project name> <task description>\n")
        self._output_stream.write("  check <task ID>\n")
        self._output_stream.write("  uncheck <task ID>\n")
        self._output_stream.write("\n")
        self._output_stream.flush()

    def _error(self, command: str):
        self._output_stream.write(f'I don\'t know what the command "{command}" is.\n')
        self._output_stream.flush()

    def _next_id(self) -> int:
        self._last_id += 1
        return self._last_id
