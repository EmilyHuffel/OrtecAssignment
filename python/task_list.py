import sys
from typing import Dict, List, TextIO
from task import Task
from task_analytics import TaskAnalytics
from datetime import datetime, date

class TaskList_ShowData:
    def __init__(self, output_stream: TextIO):
        self._tasks: Dict[str, List[Task]] = {}
        self._output_stream = output_stream

    def _show(self):
        output = ''
        for project_name, tasks in self._tasks.items():
            output_project = f"{project_name}\n"
            self._output_stream.write(output_project)
            output += output_project
            for task in tasks:
                status = 'x' if task.done else ' '
                deadline = f' (Deadline: {task.deadline})' if len(task.deadline) >= 1 else ''
                output_task = f"    [{status}] {task.id}: {task.description}{deadline}\n"
                self._output_stream.write(output_task)
                output += output_task
            self._output_stream.write("\n")
            output += "\n"
        self._output_stream.flush()
        return output

    def _help(self):
        output =  "Commands:\n"
        output += "  show\n"
        output += "  add project <project name>\n"
        output += "  add task <project name> <task description>\n"
        output += "  check <task ID>\n"
        output += "  uncheck <task ID>\n"
        output += "  deadline <task id> <deadline>\n"
        output += "  view-by-deadline\n"
        output += "  import <filepath>\n"
        output += "  export <filepath>\n"
        output += "  summary\n"
        output += "  top-projects <number of projects>\n"
        output += "  find-tasks-by-keyword <keyword>\n"
        output += "  find-overdue <current date>\n"
        output += "\n"
        self._output_stream.write(output)
        self._output_stream.flush()
        return output

    def _error(self, command: str):
        output = f'I don\'t know what the command "{command}" is.\n'
        self._output_stream.write(output)
        self._output_stream.flush()
        return output

    def _today(self):
        output = ''
        current_date = datetime.today().strftime('%d-%m-%Y')
        for project_name, tasks in self._tasks.items():
            show_project = False
            for task in tasks:
                task_deadline = task.deadline
                if task_deadline == current_date:
                    if not show_project:
                        output_project = f"{project_name}\n"
                        self._output_stream.write(output_project)
                        output += output_project
                        show_project = True
                    status = 'x' if task.done else ' '
                    output_task = f"    [{status}] {task.id}: {task.description}\n"
                    self._output_stream.write(output_task)
                    output += output_task
            self._output_stream.write("\n")
            output += "\n"
            show_project = False
        self._output_stream.flush()
        return output

    def _view_by_deadline(self):
        output = ''
        tasks_organized: Dict[str, Dict[str, List[Task]]] = {}

        # Organize all tasks in a convenient format
        for project_name, tasks_in_project in self._tasks.items():
            for task in tasks_in_project:
                task_deadline = task.deadline if len(task.deadline) else "No deadline"
                if task_deadline not in tasks_organized.keys():
                    tasks_organized[task_deadline] = {project_name: []}
                elif project_name not in tasks_organized[task_deadline].keys():
                    tasks_organized[task_deadline][project_name] = []
                tasks_organized[task_deadline][project_name].append(task)

        # Show all tasks sorted by deadline
        for deadline in sorted(tasks_organized.keys(), key = lambda date: "-".join(date.split("-")[::-1])):
            output_deadline = f"{deadline}:\n"
            self._output_stream.write(output_deadline)
            output += output_deadline
            projects_tasks_at_deadline = tasks_organized[deadline]
            for project_name in sorted(projects_tasks_at_deadline.keys()):
                output_project = f"  {project_name}:\n"
                self._output_stream.write(output_project)
                output += output_project
                tasks_at_deadline = projects_tasks_at_deadline[project_name]
                for task in tasks_at_deadline:
                    output_task = f"    {task.id}: {task.description}\n"
                    self._output_stream.write(output_task)
                    output += output_task
        self._output_stream.flush()
        return output

class TaskList_AddElements:
    def __init__(self, output_stream: TextIO):
        self._tasks: Dict[str, List[Task]] = {}
        self._last_id = 0
        self._output_stream = output_stream

    def _add(self, command_line: str):
        parts = command_line.split(" ", 1)
        subcommand = parts[0]
        
        if subcommand == "project":
            return self._add_project(parts[1] if len(parts) > 1 else "")
        elif subcommand == "task":
            task_parts = parts[1].split(" ", 1) if len(parts) > 1 else []
            if len(task_parts) >= 2:
                return self._add_task(task_parts[0], task_parts[1])
            return "Error: no task description given\n"
        
    def _add_project(self, name: str):
        self._tasks[name] = []
        return f"Added project {name}\n"
    
    def _add_task(self, project: str, description: str):
        project_tasks = self._tasks.get(project)
        if project_tasks is None:
            output = f'Could not find a project with the name "{project}".\n'
            self._output_stream.write(output)
            self._output_stream.flush()
            return output
        
        project_tasks.append(Task(self._next_id(), description, False))
        return f'Added task {description} to project {project}\n'
    
    def _next_id(self) -> int:
        self._last_id += 1
        return self._last_id
    
    def _add_deadline(self, command_line: str):
        parts = command_line.split(" ", 1)
        try:
            task_id = int(parts[0])
        except ValueError:
            self._output_stream.write("No valid Task ID given\n")
            self._output_stream.flush()
            return "No valid Task ID given.\n"
        try:
            day, month, year = parts[1].split("-", 3)
            assert(int(day) <= 31)
            assert(int(month) <= 12)
            assert(0<=int(year)<=9999)
        except ValueError:
            self._output_stream.write("This is not a valid date! Use format DD-MM-YYYY.\n")
            self._output_stream.flush()
            return "This is not a valid date! Use format DD-MM-YYYY.\n"
        for _, tasks in self._tasks.items():
            for task in tasks:
                if task.id == task_id:
                    task.deadline = date(int(year), int(month), int(day)).strftime('%d-%m-%Y')
                    return f"Added deadline to task.\n"
        output = f"Could not find a task with an ID of {task_id}.\n"
        self._output_stream.write(output)
        self._output_stream.flush()
        return output

class TaskList_ModifyElements:
    def __init__(self, output_stream: TextIO):
        self._tasks: Dict[str, List[Task]] = {}
        self._output_stream = output_stream

    def _check(self, id_string: str):
        output = self._set_done(id_string, True)
        return output

    def _uncheck(self, id_string: str):
        output = self._set_done(id_string, False)
        return output
    
    def _set_done(self, id_string: str, done: bool):
        try:
            task_id = int(id_string)
        except ValueError:
            output = f"{task_id} is not a valid ID"
            self._output_stream.write(output)
            self._output_stream.flush()
            return output
        
        for _, tasks in self._tasks.items():
            for task in tasks:
                if task.id == task_id:
                    task.done = done
                    output = f"{'Checked' if done else 'Unchecked'} {task_id}.\n"
                    self._output_stream.write(output)
                    self._output_stream.flush()
                    return output
        
        output = f"Could not find a task with an ID of {task_id}.\n"
        self._output_stream.write(output)
        self._output_stream.flush()
        return output

class TaskList(TaskList_ShowData, TaskList_AddElements, TaskList_ModifyElements):
    QUIT = "quit"
    def __init__(self, input_stream: TextIO, output_stream: TextIO):
        self._tasks: Dict[str, List[Task]] = {}
        self._input_stream = input_stream
        self._output_stream = output_stream
        self._last_id = 0

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
            return self._show()
        elif command == "add":
            return self._add(parts[1] if len(parts) > 1 else "")
        elif command == "check":
            return self._check(parts[1] if len(parts) > 1 else "")
        elif command == "uncheck":
            return self._uncheck(parts[1] if len(parts) > 1 else "")
        elif command == "deadline":
            return self._add_deadline(parts[1] if len(parts) > 1 else "")
        elif command == "today":
            return self._today()
        elif command == "view-by-deadline":
            return self._view_by_deadline()
        # TODO: implement additional commands from TaskAnalytics
        # elif command == "import":
        # elif command == "export":
        # elif command == "summary":
        # etc.
        elif command == "help":
            return self._help()
        else:
            return self._error(command)

if __name__ == "__main__":
    TaskList.start_console()


