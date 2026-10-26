from pawpal_system import Owner, Pet, Task

def main():
    # 1. Create an owner
    owner = Owner(name="Alex", available_minutes=45)

    # 2. Create at least two pets
    buddy = Pet(name="Buddy", age=3, species="Dog")
    whiskers = Pet(name="Whiskers", age=5, species="Cat")

    # 3. Add pets to the owner
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # 4. Create at least three care tasks
    walk_dog = Task(
        title="Walk Buddy",
        duration_minutes=20,
        priority=5,
        frequency="daily",
        pet=buddy,
    )

    feed_cat = Task(
        title="Feed Whiskers",
        duration_minutes=10,
        priority=4,
        frequency="daily",
        pet=whiskers,
    )

    groom_dog = Task(
        title="Brush Buddy",
        duration_minutes=15,
        priority=3,
        frequency="weekly",
        pet=buddy,
    )

    # 5. Register tasks with the owner and their pets
    owner.create_task(walk_dog)
    owner.create_task(feed_cat)
    owner.create_task(groom_dog)

    # 6. Generate today's schedule
    schedule = owner.generate_schedule()

    # 7. Print a readable schedule
    print("\n========== Today's Schedule ==========")
    schedule.display_schedule()

    # 8. Explain the scheduling decisions
    print("\n========== Schedule Explanation ==========")
    print(schedule.explain_plan())


if __name__ == "__main__":
    main()