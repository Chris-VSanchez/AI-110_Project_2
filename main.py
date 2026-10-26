"""Demonstration of the PawPal+ pet-care planner."""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_tasks(title, tasks):
    """Print task details in a readable format."""
    print(f"\n========== {title} ==========")

    if not tasks:
        print("No matching tasks found.")
        return

    for task in tasks:
        pet_name = (
            task.pet.name if task.pet else "Unassigned pet"
        )
        status = "Completed" if task.is_completed else "Pending"
        time_label = task.time or "Time not set"
        due_date = (
            task.due_date.isoformat()
            if task.due_date
            else "Not set"
        )

        print(
            f"{time_label} | {task.title} | Pet: {pet_name} | "
            f"{task.duration_minutes} min | "
            f"Priority: {task.priority}/5 | {status} | "
            f"Due: {due_date}"
        )

def main():
    # 1. Create an owner.
    owner = Owner(name="Alex", available_minutes=45)

    # 2. Create pets.
    buddy = Pet(name="Buddy", age=3, species="Dog")
    whiskers = Pet(name="Whiskers", age=5, species="Cat")

    # 3. Register pets with the owner.
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # 4. Create tasks.
    groom_dog = Task(
        title="Brush Buddy",
        duration_minutes=15,
        priority=3,
        frequency="weekly",
        pet=buddy,
        time="17:00",
    )

    walk_dog = Task(
        title="Walk Buddy",
        duration_minutes=20,
        priority=5,
        frequency="daily",
        pet=buddy,
        time="08:00",
    )

    # Deliberate conflict: both tasks start at 08:00.
    feed_cat = Task(
        title="Feed Whiskers",
        duration_minutes=10,
        priority=4,
        frequency="daily",
        pet=whiskers,
        time="08:00",
    )

    # 5. Register tasks.
    owner.create_task(groom_dog)
    owner.create_task(walk_dog)
    owner.create_task(feed_cat)

    # 6. Initialize the scheduler.
    scheduler = Scheduler(owner)

    # 7. Detect time conflicts.
    print("\n========== Conflict Detection ==========")

    warnings = scheduler.detect_time_conflicts()

    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("No scheduling conflicts detected.")

    # 8. Complete a recurring task.
    # The original becomes completed, and a new pending task is created.
    next_feed = scheduler.mark_task_complete(feed_cat)

    print("\n========== Recurring Task Automation ==========")
    print(f"Completed: {feed_cat.title}")
    print(f"Original due date: {feed_cat.due_date}")

    if next_feed is not None:
        print(f"Next occurrence: {next_feed.title}")
        print(f"Next due date: {next_feed.due_date}")
        print(
            f"Next occurrence completed: "
            f"{next_feed.is_completed}"
        )

    # 9. Sort tasks by time.
    print_tasks(
        "Tasks Sorted by Time",
        scheduler.sort_by_time(),
    )

    # 10. Filter Buddy's tasks.
    print_tasks(
        "Buddy's Tasks",
        scheduler.filter_tasks(pet_name="Buddy"),
    )

    # 11. Display pending tasks.
    print_tasks(
        "Pending Tasks",
        scheduler.filter_tasks(is_completed=False),
    )

    # 12. Display completed tasks.
    print_tasks(
        "Completed Tasks",
        scheduler.filter_tasks(is_completed=True),
    )

    # 13. Generate today's schedule.
    # Completed tasks and future-due tasks are excluded.
    schedule = owner.generate_schedule()

    print("\n========== Today's Schedule ==========")
    schedule.display_schedule()

    # 14. Explain the scheduling decisions.
    print("\n========== Schedule Explanation ==========")
    print(schedule.explain_plan())


if __name__ == "__main__":
    main()