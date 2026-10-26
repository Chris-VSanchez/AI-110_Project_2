from pawpal_system import Pet, Task

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
    pet = Pet(
        name="Buddy",
        age=3,
        species="Dog",
    )

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