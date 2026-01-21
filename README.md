# Task List

You have been handed over an existing (fictional) codebase of a task list application. This application allows you to create projects, add tasks to those projects, check and uncheck them, and view tasks by project.
Your job is to add extra features to the application, and to refactor the codebase to make it more maintainable and testable (since the code base is not in the best shape right now).

There are some unit tests present in the codebase, which should give you some understanding on how to application works.
- For each change you make, think about adding tests.
- Feel free to refactor the code base to make it easier to test.
- Do not break existing functionality.
- Add properly sized commits with meaningful commit messages.

The application is available in multiple programming languages. Pick the language you are most comfortable with.
However, the `Python` language should only be chosen if this specifically fits the job profile that you are applying for.

The assignment can take between 3-8 hours, but you can spend about 2-4 hours on it. It doesn't matter if you don't finish all tasks. If you are short on time focus on the non-optional parts first.
We will discuss the assignment during the interview.

There are 3 ways to submit the solution:

1. Download as zip. Extract the zip to a folder. Create your own public repository (on for example GitHub) and add the files to it. Start making commits. Send the link to the public repository back. This is the preferred way
2. Download as zip. Extract the zip to a folder. Type `git init` in the folder and start making commits. Zip the folder again and send that back.
3. Clone the repo. Start making commits. Zip the folder again and send it back. 

## The assignment

### 1. Adding deadlines to tasks

1. Add a new command `deadline <ID> <date>`. With this command you are able to add a deadline to a task. By default, a task has no deadline.
    - Example: `deadline 1 25-11-2024`  
2. _Optional_: Add a new command `today`. This command shows the same data as the `show` command, but it will only contain the tasks (and project it belongs to) that have a deadline for today. Make sure to not print any projects for tasks that don't have a deadline today.

### 2. Deadline view
1. Add a `view-by-deadline` command. This command will show all tasks grouped by deadline. Make sure the list is ordered chronologically, and the `no deadline` block is at the end. An example output could be:
   ```
   11-11-2021:
          1: Eat more donuts.
          4: Four Elements of Simple Design
   13-11-2021:
          3: Interaction-Driven Design
   No deadline:
          2: Refactor the codebase
   ```
2. _Optional_: Also group by project after grouping by date. Example:
   ```
   11-11-2021:
        Secrets:
          	1: Eat more donuts.
        Training:
          	4: Four Elements of Simple Design
   13-11-2021:
        Training:
          	3: Interaction-Driven Design
   No deadline:
        Training: 
          	2: Refactor the codebase
   ```


### 3. Refactor the code base for multiple interfaces

At the moment, all interaction of the program happens via `TaskList.run` and `TaskList.execute`, since this is a command line program. However, in the future, we might want to add a GUI or a REST API that interacts with the same code. 
- Refactor the codebase to make it easier to add new interfaces in the future. Start with extracting the core logic away from the command line logic.
- Refactor the core logic further, taking the following criteria into account:
  - The core logic should be easy to test and have good test coverage
  - The classes should be small and have a single responsibility
  - If possible, split up the refactorings in small steps that can be committed separately

### 4. Create REST APIs for the application 
Currently the application is only controllable via the console. Now that the core logic is extracted, we also want interaction via REST APIs.
It's okay to keep storing the tasks in memory such as is happening now (instead of a database).

In the file `TaskListApplication` there is some logic to either start the console application or the web application. You could use the provided IDE run configurations to run either application, or modify this code manually to run either the one or the other.

Note that the console application should also keep fully working. In theory you should be able to run both the console application and the REST APIs at the same time.

You should create at least the following REST endpoints:
- `POST /projects`: Create a new project
- `GET /projects`: Returns all projects and underlying tasks

_Optional_:
- `POST /projects/{project_id}/tasks`: Create a new task for a project
- `PUT /projects/{project_id}/tasks/{task_id}?deadline`: Update the deadline for a task
- `GET /projects/view_by_deadline`: Get all tasks grouped by deadline (or also by project if you did the optional part)


