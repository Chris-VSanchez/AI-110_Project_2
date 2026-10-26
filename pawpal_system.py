from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Pet:
    name: str
    age: int
    species: str
    owner: Optional["Owner"] = None

    def update_details(self, name: str, age: int, species: str) -> None:
        """Update the pet's details."""
        pass

    def get_details(self) -> dict:
        """Return the pet's details."""
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int
    is_completed: bool = False
    owner: Optional["Owner"] = None
    pet: Optional[Pet] = None

    def update_task(
        self,
        title: str,
        duration: int,
        priority: int
    ) -> None:
        """Update the task's title, duration, and priority."""
        pass

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        pass

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        pass


@dataclass
class Schedule:
    date: date = field(default_factory=date.today)
    tasks: list[Task] = field(default_factory=list)
    total_duration: int = 0

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule."""
        pass

    def generate_daily_plan(self, available_minutes: int) -> None:
        """Generate a daily plan within the available time."""
        pass

    def display_schedule(self) -> None:
        """Display the scheduled tasks."""
        pass

    def explain_plan(self) -> str:
        """Explain why tasks were selected for the plan."""
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)
    schedules: list[Schedule] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list."""
        pass

    def edit_pet_details(self, pet: Pet) -> None:
        """Edit an existing pet's details."""
        pass

    def create_task(self, task: Task) -> None:
        """Create and store a care task."""
        pass

    def edit_task(self, task: Task) -> None:
        """Edit an existing care task."""
        pass

    def generate_schedule(self) -> Schedule:
        """Generate a schedule for the owner."""
        pass