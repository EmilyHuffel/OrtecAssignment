import io
import pytest
from task_list import TaskList
from datetime import datetime
from task_analytics import TaskAnalytics 
from task import Task
import pandas as pd
import os

analytics = TaskAnalytics()

@pytest.fixture
def task_list() -> TaskList:
    input_stream = io.StringIO()
    output_stream = io.StringIO()
    return TaskList(input_stream, output_stream)


@pytest.fixture
def output_stream(task_list: TaskList) -> io.StringIO:
    return task_list._output_stream


def clear_output(output_stream: io.StringIO) -> None:
    output_stream.seek(0)
    output_stream.truncate(0)


def get_output(output_stream: io.StringIO) -> str:
    return output_stream.getvalue()


def test_show_empty_task_list(task_list: TaskList, output_stream: io.StringIO) -> None:
    
    clear_output(output_stream)
    task_list.execute("show")
    
    assert get_output(output_stream) == ""


def test_add_single_project(task_list: TaskList, output_stream: io.StringIO) -> None:

    task_list.execute("add project secrets")
    clear_output(output_stream)
    
    task_list.execute("show")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    expected_lines = [
        "secrets",
    ]
    
    assert lines == expected_lines


def test_add_tasks_to_project(task_list: TaskList, output_stream: io.StringIO) -> None:

    task_list.execute("add project secrets")
    task_list.execute("add task secrets Eat more donuts.")
    task_list.execute("add task secrets Destroy all humans.")
    clear_output(output_stream)
    
    task_list.execute("show")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    expected_lines = [
        "secrets",
        "    [ ] 1: Eat more donuts.",
        "    [ ] 2: Destroy all humans.",
    ]
    
    assert lines == expected_lines


def test_check_task_marks_as_done(task_list: TaskList, output_stream: io.StringIO) -> None:

    task_list.execute("add project secrets")
    task_list.execute("add task secrets Eat more donuts.")
    task_list.execute("check 1")
    clear_output(output_stream)
    
    task_list.execute("show")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    expected_lines = [
        "secrets",
        "    [x] 1: Eat more donuts.",
    ]
    
    assert lines == expected_lines


def test_uncheck_task_marks_as_not_done(task_list: TaskList, output_stream: io.StringIO) -> None:

    task_list.execute("add project secrets")
    task_list.execute("add task secrets Eat more donuts.")
    task_list.execute("check 1")
    task_list.execute("uncheck 1")
    clear_output(output_stream)
    
    task_list.execute("show")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    expected_lines = [
        "secrets",
        "    [ ] 1: Eat more donuts.",
    ]
    
    assert lines == expected_lines


def test_multiple_projects_with_tasks(task_list: TaskList, output_stream: io.StringIO) -> None:

    # Add first project with tasks
    task_list.execute("add project secrets")
    task_list.execute("add task secrets Eat more donuts.")
    task_list.execute("add task secrets Destroy all humans.")
    
    # Add second project with tasks
    task_list.execute("add project training")
    task_list.execute("add task training Four Elements of Simple Design")
    task_list.execute("add task training SOLID")
    task_list.execute("add task training Coupling and Cohesion")
    task_list.execute("add task training Primitive Obsession")
    task_list.execute("add task training Outside-In TDD")
    task_list.execute("add task training Interaction-Driven Design")
    
    clear_output(output_stream)
    task_list.execute("show")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    # Verify output order and content
    expected_lines = [
        "secrets",
        "    [ ] 1: Eat more donuts.",
        "    [ ] 2: Destroy all humans.",
        "",
        "training",
        "    [ ] 3: Four Elements of Simple Design",
        "    [ ] 4: SOLID",
        "    [ ] 5: Coupling and Cohesion",
        "    [ ] 6: Primitive Obsession",
        "    [ ] 7: Outside-In TDD",
        "    [ ] 8: Interaction-Driven Design",
    ]
    
    assert lines == expected_lines


def test_check_multiple_tasks_across_projects(task_list: TaskList, output_stream: io.StringIO) -> None:

    # Setup projects and tasks
    task_list.execute("add project secrets")
    task_list.execute("add task secrets Eat more donuts.")
    task_list.execute("add task secrets Destroy all humans.")
    
    task_list.execute("add project training")
    task_list.execute("add task training Four Elements of Simple Design")
    task_list.execute("add task training SOLID")
    task_list.execute("add task training Coupling and Cohesion")
    task_list.execute("add task training Primitive Obsession")
    task_list.execute("add task training Outside-In TDD")
    task_list.execute("add task training Interaction-Driven Design")
    
    # Check specific tasks
    task_list.execute("check 1")
    task_list.execute("check 3")
    task_list.execute("check 5")
    task_list.execute("check 6")
    
    clear_output(output_stream)
    task_list.execute("show")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    # Verify output order with checked/unchecked status
    expected_lines = [
        "secrets",
        "    [x] 1: Eat more donuts.",
        "    [ ] 2: Destroy all humans.",
        "",
        "training",
        "    [x] 3: Four Elements of Simple Design",
        "    [ ] 4: SOLID",
        "    [x] 5: Coupling and Cohesion",
        "    [x] 6: Primitive Obsession",
        "    [ ] 7: Outside-In TDD",
        "    [ ] 8: Interaction-Driven Design",
    ]
    
    assert lines == expected_lines


def test_add_task_to_nonexistent_project(task_list: TaskList, output_stream: io.StringIO) -> None:

    clear_output(output_stream)
    task_list.execute("add task nonexistent Some task")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    expected_lines = [
        'Could not find a project with the name "nonexistent".',
    ]
    
    assert lines == expected_lines


def test_check_nonexistent_task(task_list: TaskList, output_stream: io.StringIO) -> None:

    task_list.execute("add project secrets")
    task_list.execute("add task secrets Eat more donuts.")
    clear_output(output_stream)
    
    task_list.execute("check 999")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    expected_lines = [
        "Could not find a task with an ID of 999.",
    ]
    
    assert lines == expected_lines


def test_task_id_increments_across_projects(task_list: TaskList, output_stream: io.StringIO) -> None:

    task_list.execute("add project project1")
    task_list.execute("add task project1 Task 1")
    task_list.execute("add project project2")
    task_list.execute("add task project2 Task 2")
    task_list.execute("add task project1 Task 3")
    clear_output(output_stream)
    
    task_list.execute("show")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    # Verify task IDs increment across projects in order
    expected_lines = [
        "project1",
        "    [ ] 1: Task 1",
        "    [ ] 3: Task 3",
        "",
        "project2",
        "    [ ] 2: Task 2",
    ]
    
    assert lines == expected_lines

def test_add_deadline(task_list: TaskList, output_stream: io.StringIO) -> None:

    # Setup projects and tasks
    task_list.execute("add project secrets")
    task_list.execute("add task secrets Eat more donuts.")
    task_list.execute("deadline 1 01-01-2026")
    
    clear_output(output_stream)
    task_list.execute("show")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    # Verify output order with checked/unchecked status
    expected_lines = [
        "secrets",
        "    [ ] 1: Eat more donuts. (Deadline: 01-01-2026)",
    ]
    
    assert lines == expected_lines

def test_add_deadline_invalid_date(task_list: TaskList, output_stream: io.StringIO) -> None:

    # Setup projects and tasks
    task_list.execute("add project secrets")
    task_list.execute("add task secrets Eat more donuts.")
    task_list.execute("deadline 1 not-a-date")
    
    clear_output(output_stream)
    task_list.execute("show")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    # Verify output order with checked/unchecked status
    expected_lines = [
        "secrets",
        "    [ ] 1: Eat more donuts.",
    ]
    
    assert lines == expected_lines

def test_multiple_deadlines_across_projects(task_list: TaskList, output_stream: io.StringIO) -> None:

    # Setup projects and tasks
    task_list.execute("add project secrets")
    task_list.execute("add task secrets Eat more donuts.")
    task_list.execute("add task secrets Destroy all humans.")
    
    task_list.execute("add project training")
    task_list.execute("add task training Four Elements of Simple Design")
    task_list.execute("add task training SOLID")
    task_list.execute("add task training Coupling and Cohesion")
    task_list.execute("add task training Primitive Obsession")
    task_list.execute("add task training Outside-In TDD")
    task_list.execute("add task training Interaction-Driven Design")
    
    # Check specific tasks
    task_list.execute("deadline 1 01-01-2026")
    task_list.execute("deadline 3 31-12-2000")
    task_list.execute("deadline 5 07-09-1903")
    task_list.execute("deadline 6 20-06-9999")
    
    clear_output(output_stream)
    task_list.execute("show")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    # Verify output order with checked/unchecked status
    expected_lines = [
        "secrets",
        "    [ ] 1: Eat more donuts. (Deadline: 01-01-2026)",
        "    [ ] 2: Destroy all humans.",
        "",
        "training",
        "    [ ] 3: Four Elements of Simple Design (Deadline: 31-12-2000)",
        "    [ ] 4: SOLID",
        "    [ ] 5: Coupling and Cohesion (Deadline: 07-09-1903)",
        "    [ ] 6: Primitive Obsession (Deadline: 20-06-9999)",
        "    [ ] 7: Outside-In TDD",
        "    [ ] 8: Interaction-Driven Design",
    ]
    
    assert lines == expected_lines

def test_today(task_list: TaskList, output_stream: io.StringIO) -> None:

    # Setup projects and tasks
    task_list.execute("add project secrets")
    task_list.execute("add task secrets Eat more donuts.")
    task_list.execute("add task secrets Destroy all humans.")
    
    task_list.execute("add project training")
    task_list.execute("add task training Four Elements of Simple Design")
    task_list.execute("add task training SOLID")
    task_list.execute("add task training Coupling and Cohesion")
    task_list.execute("add task training Primitive Obsession")
    task_list.execute("add task training Outside-In TDD")
    task_list.execute("add task training Interaction-Driven Design")
    
    # Check specific tasks
    task_list.execute("deadline 1 01-01-2026")
    task_list.execute(f"deadline 3 {datetime.today().strftime('%d-%m-%Y')}")
    task_list.execute(f"deadline 5 {datetime.today().strftime('%d-%m-%Y')}")
    task_list.execute("deadline 6 20-06-9999")
    
    clear_output(output_stream)
    task_list.execute("today")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    # Verify output order with checked/unchecked status
    expected_lines = [
        "training",
        f"    [ ] 3: Four Elements of Simple Design",
        f"    [ ] 5: Coupling and Cohesion",
    ]
    
    assert lines == expected_lines

def test_deadline(task_list: TaskList, output_stream: io.StringIO) -> None:

    # Setup projects and tasks
    task_list.execute("add project secrets")
    task_list.execute("add task secrets Eat more donuts.")
    task_list.execute("add task secrets Destroy all humans.")
    
    task_list.execute("add project training")
    task_list.execute("add task training Four Elements of Simple Design")
    task_list.execute("add task training SOLID")
    task_list.execute("add task training Coupling and Cohesion")
    task_list.execute("add task training Primitive Obsession")
    task_list.execute("add task training Outside-In TDD")
    task_list.execute("add task training Interaction-Driven Design")
    
    # Check specific tasks
    task_list.execute("deadline 1 01-01-2026")
    task_list.execute("deadline 3 31-12-1999")
    task_list.execute("deadline 5 01-01-2026")
    task_list.execute("deadline 6 20-06-9999")
    
    clear_output(output_stream)
    task_list.execute("view-by-deadline")
    output = get_output(output_stream)
    lines = output.strip().split('\n')
    
    # Verify output order with checked/unchecked status
    expected_lines = [
        "31-12-1999:",
        "  training:",
        "    3: Four Elements of Simple Design",
        "01-01-2026:",
        "  secrets:",
        "    1: Eat more donuts.",
        "  training:",
        "    5: Coupling and Cohesion",
        "20-06-9999:",
        "  training:",
        "    6: Primitive Obsession",
        'No deadline:',
        '  secrets:',
        '    2: Destroy all humans.',
        '  training:',
        '    4: SOLID',
        '    7: Outside-In TDD',
        '    8: Interaction-Driven Design',
    ]
    
    assert lines == expected_lines

def test_import_from_dict():
    task1 = Task(1, 'Eat donuts', False)
    task2 = Task(2, 'Dishes', True)
    task3 = Task(3, 'Dinner', True)
    task4 = Task(4, 'Clean floor', True)
    task5 = Task(5, 'Paint minis', False)

    input_dict = {'Food': [task1, task3], 'Chores': [task2, task4], 'Fun': [task5]}
    input_dict['Food'][1].deadline = '01-01-2027'

    df = analytics.import_from_dict(input_dict)
    target_df = pd.DataFrame([['Food', 1, 'Eat donuts', False, pd.NaT, task1],
                               ['Food', 3, 'Dinner', True, datetime(2027, 1, 1), task3],
                               ['Chores', 2, 'Dishes', True, pd.NaT, task2],
                               ['Chores', 4, 'Clean floor', True, pd.NaT, task4],
                               ['Fun', 5, 'Paint minis', False, pd.NaT, task5]
                               ], columns=['project_name','task_id','description','done','deadline','task'])

    assert df.equals(target_df)

def test_export_to_dict():
    task1 = Task(1, 'Eat donuts', False)
    task2 = Task(2, 'Dishes', True)
    task3 = Task(3, 'Dinner', True)
    task4 = Task(4, 'Clean floor', True)
    task5 = Task(5, 'Paint minis', False)
    input_df = pd.DataFrame([['Food', 1, 'Eat donuts', False, pd.NaT, task1],
                               ['Food', 3, 'Dinner', True, datetime(2027, 1, 1), task3],
                               ['Chores', 2, 'Dishes', True, pd.NaT, task2],
                               ['Chores', 4, 'Clean floor', True, pd.NaT, task4],
                               ['Fun', 5, 'Paint minis', False, pd.NaT, task5]
                               ], columns=['project_name','task_id','description','done','deadline','task'])
    output_dict = analytics.export_to_dict(input_df)
    assert output_dict == {'Food': [task1, task3], 'Chores': [task2, task4], 'Fun': [task5]}

def test_export_to_csv():
    task1 = Task(1, 'Eat donuts', False)
    task2 = Task(2, 'Dishes', True)
    task3 = Task(3, 'Dinner', True)
    task4 = Task(4, 'Clean floor', True)
    task5 = Task(5, 'Paint minis', False)
    input_df = pd.DataFrame([['Food', 1, 'Eat donuts', False, pd.NaT, task1],
                               ['Food', 3, 'Dinner', True, datetime(2027, 1, 1), task3],
                               ['Chores', 2, 'Dishes', True, pd.NaT, task2],
                               ['Chores', 4, 'Clean floor', True, pd.NaT, task4],
                               ['Fun', 5, 'Paint minis', False, pd.NaT, task5]
                               ], columns=['project_name','task_id','description','done','deadline','task'])
    analytics.export_to_csv(input_df, 'temp.csv')
    f = open('temp.csv', 'r')
    assert f.readlines() == ['project_name,task_id,description,done,deadline\n', 'Food,1,Eat donuts,False,\n', 'Food,3,Dinner,True,01-01-2027\n', 'Chores,2,Dishes,True,\n', 'Chores,4,Clean floor,True,\n', 'Fun,5,Paint minis,False,\n']
    f.close()

def test_import_from_csv():
    df = analytics.import_from_csv('temp.csv')
    test_df = pd.DataFrame([['Food', 1, 'Eat donuts', False, pd.NaT],
                               ['Food', 3, 'Dinner', True, datetime(2027, 1, 1)],
                               ['Chores', 2, 'Dishes', True, pd.NaT],
                               ['Chores', 4, 'Clean floor', True, pd.NaT],
                               ['Fun', 5, 'Paint minis', False, pd.NaT]],
                               columns=['project_name','task_id','description','done','deadline'])
    assert df.equals(test_df)
    os.remove('temp.csv')

def test_project_summary():
    task1 = Task(1, 'Eat donuts', False)
    task2 = Task(2, 'Dishes', True)
    task3 = Task(3, 'Dinner', True)
    task4 = Task(4, 'Clean floor', True)
    task5 = Task(5, 'Paint minis', False)
    df = pd.DataFrame([['Food', 1, 'Eat donuts', False, datetime(1999, 9, 3), task1],
                        ['Food', 3, 'Dinner', True, datetime(2027, 1, 1), task3],
                        ['Chores', 2, 'Dishes', True, datetime(3000,5,13), task2],
                        ['Chores', 4, 'Clean floor', True, pd.NaT, task4],
                        ['Fun', 5, 'Paint minis', False, pd.NaT, task5]
                        ], columns=['project_name','task_id','description','done','deadline','task'])
    project_summary = analytics.get_project_summary(df)
    test_df = pd.DataFrame([['Chores', 2, 2, 0, 100.0],
                                            ['Food', 2, 1, 1, 50.0],
                                            ['Fun', 1, 0, 1, 0.0]],
                                            columns=['project_name', 'total_tasks', 'completed_tasks', 'pending_tasks', 'completion_rate'])
    assert project_summary.equals(test_df)

def test_top_projects_by_completion():
    task1 = Task(1, 'Eat donuts', False)
    task2 = Task(2, 'Dishes', True)
    task3 = Task(3, 'Dinner', True)
    task4 = Task(4, 'Clean floor', True)
    task5 = Task(5, 'Paint minis', False)
    df = pd.DataFrame([['Food', 1, 'Eat donuts', False, datetime(1999, 9, 3), task1],
                        ['Food', 3, 'Dinner', True, datetime(2027, 1, 1), task3],
                        ['Chores', 2, 'Dishes', True, datetime(3000,5,13), task2],
                        ['Chores', 4, 'Clean floor', True, pd.NaT, task4],
                        ['Fun', 5, 'Paint minis', False, pd.NaT, task5]
                        ], columns=['project_name','task_id','description','done','deadline','task'])
    top_projects = analytics.get_top_projects_by_completion(df, 2)
    test_df = pd.DataFrame([['Chores', 100.0],['Food', 50.0]], columns=['project_name','completion_rate'])
    assert top_projects.equals(test_df)

def test_find_tasks_by_keyword():
    task1 = Task(1, 'Eat donuts', False)
    task2 = Task(2, 'Dishes', True)
    task3 = Task(3, 'Dinner', True)
    task4 = Task(4, 'Clean floor', True)
    task5 = Task(5, 'Paint minis', False)
    df = pd.DataFrame([['Food', 1, 'Eat donuts', False, datetime(1999, 9, 3), task1],
                        ['Food', 3, 'Dinner', True, datetime(2027, 1, 1), task3],
                        ['Chores', 2, 'Dishes', True, datetime(3000,5,13), task2],
                        ['Chores', 4, 'Clean floor', True, pd.NaT, task4],
                        ['Fun', 5, 'Paint minis', False, pd.NaT, task5]
                        ], columns=['project_name','task_id','description','done','deadline','task'])
    tasks_with_di = analytics.find_tasks_by_keyword(df, 'di')
    test_df = pd.DataFrame([['Food',3,'Dinner',True,datetime(2027,1,1), task3],
                           ['Chores', 2, 'Dishes', True, datetime(3000,5,13), task2]], 
                           columns=['project_name','task_id','description','done','deadline','task'], 
                           index=[1,2])
    assert tasks_with_di.equals(test_df)

def test_find_overdue_tasks():
    task1 = Task(1, 'Eat donuts', False)
    task2 = Task(2, 'Dishes', True)
    task3 = Task(3, 'Dinner', True)
    task4 = Task(4, 'Clean floor', True)
    task5 = Task(5, 'Paint minis', False)
    df = pd.DataFrame([['Food', 1, 'Eat donuts', False, datetime(1999, 9, 3), task1],
                        ['Food', 3, 'Dinner', True, datetime(2027, 1, 1), task3],
                        ['Chores', 2, 'Dishes', True, datetime(3000,5,13), task2],
                        ['Chores', 4, 'Clean floor', True, pd.NaT, task4],
                        ['Fun', 5, 'Paint minis', False, pd.NaT, task5]
                        ], columns=['project_name','task_id','description','done','deadline','task'])
    df_overdue = analytics.find_overdue_tasks(df, '22-01-2040')
    test_df = pd.DataFrame([['Food', 1, 'Eat donuts', False, datetime(1999, 9, 3), task1],
                           ['Food', 3, 'Dinner', True, datetime(2027, 1, 1), task3]], 
                           columns=['project_name','task_id','description','done','deadline','task'], 
                           index=[0,1])
    assert df_overdue.equals(test_df)