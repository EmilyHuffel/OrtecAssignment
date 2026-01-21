import io
import pytest
from task_list import TaskList
from datetime import datetime

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