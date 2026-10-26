from datetime import date, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler

def test_task_completion():
    """Verify that a task can be marked as complete."""
    task = Task(
        title="Feed Buddy",
        duration_minutes=10,
        priority=3,
    )

    assert task.is_completed is False

    task.mark_complete()

    assert task.is_completed is True

def test_task_addition():
    """Verify that adding a task increases the pet's task count."""
    pet = Pet(name="Buddy", age=3, species="Dog")
    task = Task(
        title="Walk Buddy",
        duration_minutes=20,
        priority=5,
    )

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert task in pet.tasks
    assert task.pet is pet

def test_sorting_correctness():
    """Verify that tasks are sorted chronologically."""
    owner = Owner(name="Alex", available_minutes=60)
    scheduler = Scheduler(owner)

    task_evening = Task(
        title="Evening Walk",
        duration_minutes=20,
        priority=3,
        time="18:00",
    )
    task_morning = Task(
        title="Breakfast",
        duration_minutes=10,
        priority=4,
        time="08:00",
    )
    task_noon = Task(
        title="Lunch",
        duration_minutes=10,
        priority=3,
        time="12:00",
    )

    owner.create_task(task_evening)
    owner.create_task(task_morning)
    owner.create_task(task_noon)

    sorted_tasks = scheduler.sort_by_time()

    assert [task.title for task in sorted_tasks] == [
        "Breakfast",
        "Lunch",
        "Evening Walk",
    ]

def test_daily_task_recurrence():
    """Completing a daily task creates the next day's occurrence."""
    owner = Owner(name="Alex", available_minutes=60)
    pet = Pet(name="Buddy", age=3, species="Dog")
    owner.add_pet(pet)

    today = date.today()
    task = Task(
        title="Feed Buddy",
        duration_minutes=10,
        priority=3,
        frequency="daily",
        due_date=today,
        time="08:00",
        pet=pet,
    )
    owner.create_task(task)

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete(task)

    assert task.is_completed is True
    assert next_task is not None
    assert next_task is not task
    assert next_task.title == task.title
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.frequency == "daily"
    assert next_task.pet is pet
    assert next_task in owner.tasks

def test_conflict_detection():
    """Verify that tasks with identical times produce a warning."""
    owner = Owner(name="Alex", available_minutes=60)
    pet = Pet(name="Buddy", age=3, species="Dog")
    owner.add_pet(pet)

    task_one = Task(
        title="Morning Walk",
        duration_minutes=20,
        priority=4,
        time="09:00",
        pet=pet,
    )
    task_two = Task(
        title="Morning Feeding",
        duration_minutes=10,
        priority=3,
        time="09:00",
        pet=pet,
    )

    owner.create_task(task_one)
    owner.create_task(task_two)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_time_conflicts()

    assert len(warnings) == 1
    assert "Morning Walk" in warnings[0]
    assert "Morning Feeding" in warnings[0]
    assert "09:00" in warnings[0]
    assert "same pet (Buddy)" in warnings[0]