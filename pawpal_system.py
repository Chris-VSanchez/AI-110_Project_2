"""Core classes for the PawPal+ pet-care planner."""

from dataclasses import dataclass, field
from datetime import date
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
        """Validate pet details after initialization."""
        self._validate_details(self.name, self.age, self.species)

    @staticmethod
    def _validate_details(name: str, age: int, species: str) -> None:
        """Validate the pet's name, age, and species."""
        if not name.strip():
            raise ValueError("Pet name cannot be empty.")
        if not isinstance(age, int) or isinstance(age, bool) or age < 0:
            raise ValueError("Pet age must be a non-negative integer.")
        if not species.strip():
            raise ValueError("Pet species cannot be empty.")

    def update_details(self, name: str, age: int, species: str) -> None:
        """Update the pet's details."""
        self._validate_details(name, age, species)
        self.name = name.strip()
        self.age = age
        self.species = species.strip()

    def get_details(self) -> dict:
        """Return the pet's details."""
        return {
            "name": self.name,
            "age": self.age,
            "species": self.species,
            "owner": self.owner.name if self.owner else None,
        }

    def add_task(self, task: "Task") -> None:
        """Associate a task with this pet without duplicating it."""
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

    def __post_init__(self) -> None:
        """Validate task details after initialization."""
        self._validate_task(
            self.title, self.duration_minutes, self.priority, self.frequency
        )

    @staticmethod
    def _validate_task(
        title: str, duration: int, priority: int, frequency: str
    ) -> None:
        """Validate the task's title, duration, priority, and frequency."""
        if not title.strip():
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

    def update_task(
        self,
        title: str,
        duration: int,
        priority: int
    ) -> None:
        """Update a task's title, duration, and priority."""
        self._validate_task(title, duration, priority, self.frequency)
        self.title = title.strip()
        self.duration_minutes = duration
        self.priority = priority

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
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
        """Add a task if it is not already scheduled."""
        if task.is_completed:
            raise ValueError("Completed tasks cannot be added to the plan.")
        if task not in self.tasks:
            self.tasks.append(task)
            self.total_duration += task.duration_minutes

    def remove_task(self, task: Task) -> None:
        """Remove a task and update the total duration."""
        if task in self.tasks:
            self.tasks.remove(task)
            self.total_duration -= task.duration_minutes

    def generate_daily_plan(self, available_minutes: int) -> None:
        """
        Select tasks by descending priority, then shorter duration.
        Tasks that do not fit are skipped so shorter tasks can still fit.
        """
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
            task for task in candidates if not task.is_completed
        ]
        candidates.sort(
            key=lambda task: (-task.priority, task.duration_minutes, task.title.lower())
        )

        for task in candidates:
            if self.total_duration + task.duration_minutes <= available_minutes:
                self.add_task(task)
            else:
                self.skipped_tasks.append(task)

    def display_schedule(self) -> None:
        """Print the scheduled tasks and total time."""
        print(f"PawPal+ Daily Plan — {self.date.isoformat()}")
        print("-" * 40)

        if not self.tasks:
            print("No tasks fit the available time.")
        else:
            for index, task in enumerate(self.tasks, start=1):
                pet_name = task.pet.name if task.pet else "Unassigned pet"
                print(
                    f"{index}. {task.title} ({pet_name}) — "
                    f"{task.duration_minutes} min, priority {task.priority}/5"
                )

        print(f"\nTotal: {self.total_duration} / {self.available_minutes} minutes")

        if self.skipped_tasks:
            print("\nTasks not scheduled:")
            for task in self.skipped_tasks:
                print(f"- {task.title} ({task.duration_minutes} min)")

    def explain_plan(self) -> str:
        """Explain why tasks were selected or skipped."""
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
        """Validate the owner's name and available time."""
        if not self.name.strip():
            raise ValueError("Owner name cannot be empty.")
        if (
            not isinstance(self.available_minutes, int)
            or isinstance(self.available_minutes, bool)
            or self.available_minutes < 0
        ):
            raise ValueError("Available time must be a non-negative integer.")

    def add_pet(self, pet: Pet) -> None:
        """Add a pet and connect it to this owner."""
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
        """Confirm the pet belongs to this owner."""
        if pet not in self.pets:
            raise ValueError("Cannot edit a pet that does not belong to this owner.")
        # Use pet.update_details(name, age, species) to change its details.

    def create_task(self, task: Task) -> None:
        """Create/store a task and connect it to its owner and pet."""
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
        """Confirm a task belongs to this owner before editing."""
        if task not in self.tasks:
            raise ValueError("Cannot edit a task that does not belong to this owner.")
        # Use task.update_task(title, duration, priority) to change its details.

    def get_all_tasks(self) -> list[Task]:
        """Return unique tasks belonging to the owner or their pets."""
        result = list(self.tasks)
        for pet in self.pets:
            for task in pet.tasks:
                if task not in result:
                    result.append(task)
        return result

    def generate_schedule(self) -> Schedule:
        """Generate, store, and return today's schedule."""
        scheduler = Scheduler(self)
        schedule = scheduler.generate_schedule(self.available_minutes)
        self.schedules.append(schedule)
        return schedule

@dataclass
class Scheduler:
    """Collects tasks across pets and builds an explainable daily plan."""

    owner: Owner

    def get_all_tasks(self) -> list[Task]:
        """Retrieve unique tasks across the owner and all their pets."""
        return self.owner.get_all_tasks()

    def generate_schedule(
        self, available_minutes: Optional[int] = None
    ) -> Schedule:
        """Generate a schedule using the given or owner's time budget."""
        if available_minutes is None:
            available_minutes = self.owner.available_minutes

        schedule = Schedule(available_minutes=available_minutes)
        schedule._candidate_tasks = self.get_all_tasks()
        schedule.generate_daily_plan(available_minutes)
        return schedule