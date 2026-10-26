"""Core classes for the PawPal+ pet-care planner."""

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional

@dataclass
class Pet:
    """Stores pet details and the pet's care tasks."""

    name: str
    age: int
    species: str
    owner: Optional["Owner"] = None
    tasks: list["Task"] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._validate_details(self.name, self.age, self.species)
        self.name = self.name.strip()
        self.species = self.species.strip()

    @staticmethod
    def _validate_details(name: str, age: int, species: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Pet name cannot be empty.")
        if not isinstance(age, int) or isinstance(age, bool) or age < 0:
            raise ValueError("Pet age must be a non-negative integer.")
        if not isinstance(species, str) or not species.strip():
            raise ValueError("Pet species cannot be empty.")

    def update_details(self, name: str, age: int, species: str) -> None:
        self._validate_details(name, age, species)
        self.name = name.strip()
        self.age = age
        self.species = species.strip()

    def get_details(self) -> dict:
        return {
            "name": self.name,
            "age": self.age,
            "species": self.species,
            "owner": self.owner.name if self.owner else None,
        }

    def add_task(self, task: "Task") -> None:
        if task not in self.tasks:
            self.tasks.append(task)
        task.pet = self
        if self.owner is not None:
            task.owner = self.owner

@dataclass(eq=False)
class Task:
    """Represents one pet-care activity."""

    title: str
    duration_minutes: int
    priority: int
    is_completed: bool = False
    owner: Optional["Owner"] = None
    pet: Optional[Pet] = None
    frequency: str = "daily"
    time: Optional[str] = None
    due_date: Optional[date] = None

    def __post_init__(self) -> None:
        self._validate_task(
            self.title,
            self.duration_minutes,
            self.priority,
            self.frequency,
        )
        self.title = self.title.strip()
        self.frequency = self.frequency.strip().lower()
        self._validate_time(self.time)

        if self.due_date is None:
            self.due_date = date.today()
        elif (
            not isinstance(self.due_date, date)
            or isinstance(self.due_date, datetime)
        ):
            raise ValueError("Due date must be a datetime.date.")

        if not isinstance(self.is_completed, bool):
            raise ValueError("Completion status must be a boolean.")

    @staticmethod
    def _validate_task(
        title: str, duration: int, priority: int, frequency: str
    ) -> None:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title cannot be empty.")
        if (
            not isinstance(duration, int)
            or isinstance(duration, bool)
            or duration <= 0
        ):
            raise ValueError("Duration must be a positive integer.")
        if (
            not isinstance(priority, int)
            or isinstance(priority, bool)
            or not 1 <= priority <= 5
        ):
            raise ValueError("Priority must be an integer from 1 to 5.")
        if not isinstance(frequency, str) or not frequency.strip():
            raise ValueError("Frequency cannot be empty.")

    @staticmethod
    def _validate_time(time: Optional[str]) -> None:
        if time is None:
            return
        if not isinstance(time, str):
            raise ValueError("Time must be a string in HH:MM format.")
        try:
            parsed = datetime.strptime(time, "%H:%M")
            if parsed.strftime("%H:%M") != time:
                raise ValueError
        except ValueError:
            raise ValueError(
                "Time must use valid 24-hour HH:MM format, such as 08:30."
            ) from None

    def update_task(
        self, title: str, duration: int, priority: int
    ) -> None:
        self._validate_task(title, duration, priority, self.frequency)
        self.title = title.strip()
        self.duration_minutes = duration
        self.priority = priority

    def mark_complete(self) -> None:
        """Mark this task complete without creating a recurring task."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        self.is_completed = False

@dataclass
class Schedule:
    """Stores and explains a daily care plan."""

    date: date = field(default_factory=date.today)
    tasks: list[Task] = field(default_factory=list)
    total_duration: int = 0
    skipped_tasks: list[Task] = field(default_factory=list)
    available_minutes: int = 0

    def add_task(self, task: Task) -> None:
        if task.is_completed:
            raise ValueError("Completed tasks cannot be added to the plan.")
        if task.due_date is not None and task.due_date > self.date:
            raise ValueError("Future tasks cannot be added to the plan.")
        if task not in self.tasks:
            self.tasks.append(task)
            self.total_duration += task.duration_minutes

    def remove_task(self, task: Task) -> None:
        if task in self.tasks:
            self.tasks.remove(task)
            self.total_duration -= task.duration_minutes

    def generate_daily_plan(self, available_minutes: int) -> None:
        if (
            not isinstance(available_minutes, int)
            or isinstance(available_minutes, bool)
            or available_minutes < 0
        ):
            raise ValueError("Available time must be a non-negative integer.")

        self.tasks.clear()
        self.skipped_tasks.clear()
        self.total_duration = 0
        self.available_minutes = available_minutes

        candidates = getattr(self, "_candidate_tasks", [])
        candidates = [
            task for task in candidates
            if not task.is_completed
            and (task.due_date is None or task.due_date <= self.date)
        ]

        candidates.sort(
            key=lambda task: (
                -task.priority,
                task.duration_minutes,
                task.title.lower(),
            )
        )

        for task in candidates:
            if self.total_duration + task.duration_minutes <= available_minutes:
                self.add_task(task)
            else:
                self.skipped_tasks.append(task)

    def display_schedule(self) -> None:
        print(f"PawPal+ Daily Plan — {self.date.isoformat()}")
        print("-" * 40)

        if not self.tasks:
            print("No tasks fit the available time.")
        else:
            for index, task in enumerate(self.tasks, start=1):
                pet_name = task.pet.name if task.pet else "Unassigned pet"
                time_label = task.time or "Time not set"
                print(
                    f"{index}. {time_label} | {task.title} ({pet_name}) — "
                    f"{task.duration_minutes} min, priority {task.priority}/5"
                )

        print(
            f"\nTotal: {self.total_duration} / "
            f"{self.available_minutes} minutes"
        )

        if self.skipped_tasks:
            print("\nTasks not scheduled:")
            for task in self.skipped_tasks:
                print(f"- {task.title} ({task.duration_minutes} min)")

    def explain_plan(self) -> str:
        if not self.tasks and not self.skipped_tasks:
            return "No eligible care tasks were available to schedule."

        lines = [
            f"Plan for {self.date.isoformat()}: "
            f"{self.total_duration} of {self.available_minutes} minutes used."
        ]

        if self.tasks:
            lines.append(
                "Scheduled tasks were ranked by priority (5 is highest), "
                "then by shorter duration when priorities tied."
            )
            for task in self.tasks:
                lines.append(
                    f"- Selected '{task.title}': priority {task.priority}/5, "
                    f"{task.duration_minutes} minutes."
                )

        if self.skipped_tasks:
            lines.append(
                "The following tasks did not fit in the remaining time "
                "when considered:"
            )
            for task in self.skipped_tasks:
                lines.append(
                    f"- Skipped '{task.title}': requires "
                    f"{task.duration_minutes} minutes."
                )

        lines.append("Completed tasks were excluded from scheduling.")
        return "\n".join(lines)

@dataclass
class Owner:
    """Manages an owner's pets, tasks, and schedules."""

    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)
    schedules: list[Schedule] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Owner name cannot be empty.")
        if (
            not isinstance(self.available_minutes, int)
            or isinstance(self.available_minutes, bool)
            or self.available_minutes < 0
        ):
            raise ValueError("Available time must be a non-negative integer.")
        self.name = self.name.strip()

    def add_pet(self, pet: Pet) -> None:
        if pet.owner is not None and pet.owner is not self:
            raise ValueError("This pet already belongs to another owner.")
        if pet not in self.pets:
            self.pets.append(pet)
        pet.owner = self

        for task in pet.tasks:
            task.owner = self
            if task not in self.tasks:
                self.tasks.append(task)

    def edit_pet_details(self, pet: Pet) -> None:
        if pet not in self.pets:
            raise ValueError(
                "Cannot edit a pet that does not belong to this owner."
            )

    def create_task(self, task: Task) -> None:
        if task.owner is not None and task.owner is not self:
            raise ValueError("This task belongs to another owner.")
        if task.pet is not None and task.pet not in self.pets:
            raise ValueError("Add the task's pet to the owner first.")

        task.owner = self
        if task not in self.tasks:
            self.tasks.append(task)

        if task.pet is not None and task not in task.pet.tasks:
            task.pet.tasks.append(task)

    def edit_task(self, task: Task) -> None:
        if task not in self.tasks:
            raise ValueError(
                "Cannot edit a task that does not belong to this owner."
            )

    def get_all_tasks(self) -> list[Task]:
        result = list(self.tasks)
        for pet in self.pets:
            for task in pet.tasks:
                if task not in result:
                    result.append(task)
        return result

    def generate_schedule(self) -> Schedule:
        scheduler = Scheduler(self)
        schedule = scheduler.generate_schedule(self.available_minutes)
        self.schedules.append(schedule)
        return schedule

@dataclass
class Scheduler:
    """Collects, sorts, filters, and schedules pet-care tasks."""

    owner: Owner

    def get_all_tasks(self) -> list[Task]:
        return self.owner.get_all_tasks()

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """
        Complete a task and create its next occurrence if recurring.

        Returns the new task for daily/weekly tasks, or None for
        non-recurring tasks.
        """
        if task not in self.get_all_tasks():
            raise ValueError("Cannot complete a task not owned by this owner.")

        if task.is_completed:
            raise ValueError("This task has already been completed.")

        task.mark_complete()

        if task.frequency not in ("daily", "weekly"):
            return None

        # timedelta represents a precise calendar-day interval.
        interval = 1 if task.frequency == "daily" else 7
        next_due_date = (task.due_date or date.today()) + timedelta(
            days=interval
        )

        next_task = Task(
            title=task.title,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            owner=self.owner,
            pet=task.pet,
            frequency=task.frequency,
            time=task.time,
            due_date=next_due_date,
        )

        self.owner.create_task(next_task)
        return next_task

    def sort_by_time(
        self, tasks: Optional[list[Task]] = None
    ) -> list[Task]:
        """Return tasks ordered by HH:MM, with unset times at the end."""
        candidates = list(
            self.get_all_tasks() if tasks is None else tasks
        )

        return sorted(
            candidates,
            key=lambda task: (
                task.time is None,
                task.time or "23:59",
                task.title.lower(),
            ),
        )

    def filter_tasks(
        self,
        is_completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> list[Task]:
        """Filter tasks by completion status and/or pet name."""
        if is_completed is not None and not isinstance(is_completed, bool):
            raise ValueError("is_completed must be True, False, or None.")

        if pet_name is not None:
            if not isinstance(pet_name, str) or not pet_name.strip():
                raise ValueError("Pet name must be a non-empty string.")
            pet_name = pet_name.strip().casefold()

        result = self.get_all_tasks()

        if is_completed is not None:
            result = [
                task for task in result
                if task.is_completed == is_completed
            ]

        if pet_name is not None:
            result = [
                task for task in result
                if task.pet is not None
                and task.pet.name.casefold() == pet_name
            ]

        return result

    def generate_schedule(
        self, available_minutes: Optional[int] = None
    ) -> Schedule:
        if available_minutes is None:
            available_minutes = self.owner.available_minutes

        schedule = Schedule(available_minutes=0)
        schedule._candidate_tasks = self.get_all_tasks()
        schedule.generate_daily_plan(available_minutes)
        return schedule

    
    def detect_time_conflicts(self) -> list[str]:
        """Return warnings for tasks sharing the same scheduled start time."""
        tasks = [
            task
            for task in self.get_all_tasks()
            if not task.is_completed and task.time is not None
        ]

        warnings = []

        for index, task_a in enumerate(tasks):
            for task_b in tasks[index + 1:]:
                if task_a.time != task_b.time:
                    continue

                pet_a = task_a.pet.name if task_a.pet else "Unassigned pet"
                pet_b = task_b.pet.name if task_b.pet else "Unassigned pet"

                if task_a.pet is task_b.pet:
                    relationship = (
                        f"the same pet ({pet_a})"
                        if task_a.pet is not None
                        else "unassigned pets"
                    )
                else:
                    relationship = f"different pets ({pet_a} and {pet_b})"

                warnings.append(
                    f"WARNING: '{task_a.title}' and '{task_b.title}' "
                    f"are both scheduled at {task_a.time} for "
                    f"{relationship}."
                )

        return warnings