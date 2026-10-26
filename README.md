# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

# Sample Output
- The following output demonstrates the PawPal+ daily scheduling system with two pets, three care tasks, and a 45-minute time budget:
========== Today's Schedule ==========
PawPal+ Daily Plan — 2026-10-25
----------------------------------------
1. Walk Buddy (Buddy) — 20 min, priority 5/5
2. Feed Whiskers (Whiskers) — 10 min, priority 4/5
3. Brush Buddy (Buddy) — 15 min, priority 3/5

Total: 45 / 45 minutes

========== Schedule Explanation ==========
Plan for 2026-10-25: 45 of 45 minutes used.
Scheduled tasks were ranked by priority (5 is highest), then by shorter duration when priorities tied.
- Selected 'Walk Buddy': priority 5/5, 20 minutes.
- Selected 'Feed Whiskers': priority 4/5, 10 minutes.
- Selected 'Brush Buddy': priority 3/5, 15 minutes.
Completed tasks were excluded from scheduling.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
python -m pytest --cov
```

Sample test output:

```
========================================================== test session starts ===========================================================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.7.0 -- C:\Users\chris\OneDrive\Desktop\AI-110_Project_2\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\chris\OneDrive\Desktop\AI-110_Project_2
plugins: anyio-4.15.1
collected 5 items                                                                                                                                             

tests/test_pawpal.py::test_task_completion PASSED                                                                                                       [ 20%]
tests/test_pawpal.py::test_task_addition PASSED                                                                                                         [ 40%]
tests/test_pawpal.py::test_sorting_correctness PASSED                                                                                                   [ 60%]
tests/test_pawpal.py::test_daily_task_recurrence PASSED                                                                                                 [ 80%]
tests/test_pawpal.py::test_conflict_detection PASSED                                                                                                    [100%]

=========================================================== 5 passed in 0.14s ============================================================
```

⭐ Confidence Level: 4/5
I am highly confident in PawPal+'s reliability based on the core functionality covered by the tests. Additional edge-case and integration testing would help identify potential issues and increase confidence further.

## 📐 Smarter Scheduling
- PawPal+ includes features to make pet-care scheduling easier and more organized.

> Fill in once you've implemented scheduling logic.

+-------------------+----------------------------------+----------------------------------------------+
| Feature           | Method(s)                        | Notes                                        |
+-------------------+----------------------------------+----------------------------------------------+
| Task sorting      | Scheduler.sort_by_time()         | Sorts by start time; unset times appear last.|
| Filtering         | Scheduler.filter_tasks()         | Filters by pet name and completion status.   |
| Conflict handling | Scheduler.detect_time_conflicts()| Detects tasks with identical start times.    |
| Recurring tasks   | Scheduler.mark_task_complete()   | Creates the next daily or weekly occurrence. |
+-------------------+----------------------------------+----------------------------------------------+

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Add pets and configure settings.
    Run streamlit run app.py. Set the owner's name and available care time, then add pets by entering their names, ages, and species.
2. Create care tasks.
    Add tasks such as a morning walk or feeding. Assign each task to a pet, set its duration, priority, frequency, and optional start time.
3. Sort and filter tasks.
    Use the Task Management Dashboard to sort tasks by priority, time, duration, or title. Filter by pet and completion status. The overview displays task totals and completion progress.
4. Detect conflicts and manage recurring tasks.
    PawPal+ warns when pending tasks share the same start time. Completing daily or weekly tasks through the Scheduler automatically creates their next occurrence.
5. Generate today's care plan.
    Click Generate Schedule to create a plan based on available time and task priorities. Review scheduled tasks, time remaining, skipped tasks, and the scheduling explanation.
6. Run the CLI demonstration.
    Run python main.py to test sorting, filtering, conflict detection, recurring tasks, and schedule generation independently of Streamlit.

Output:
========== Conflict Detection ==========
WARNING: 'Walk Buddy' and 'Feed Whiskers' are both scheduled at 08:00 for different pets (Buddy and Whiskers).

========== Recurring Task Automation ==========
Completed: Feed Whiskers
Original due date: 2026-10-25
Next occurrence: Feed Whiskers
Next due date: 2026-10-26
Next occurrence completed: False

========== Tasks Sorted by Time ==========
08:00 | Feed Whiskers | Pet: Whiskers | 10 min | Priority: 4/5 | Completed | Due: 2026-10-25
08:00 | Feed Whiskers | Pet: Whiskers | 10 min | Priority: 4/5 | Pending | Due: 2026-10-26
08:00 | Walk Buddy | Pet: Buddy | 20 min | Priority: 5/5 | Pending | Due: 2026-10-25
17:00 | Brush Buddy | Pet: Buddy | 15 min | Priority: 3/5 | Pending | Due: 2026-10-25

========== Buddy's Tasks ==========
17:00 | Brush Buddy | Pet: Buddy | 15 min | Priority: 3/5 | Pending | Due: 2026-10-25
08:00 | Walk Buddy | Pet: Buddy | 20 min | Priority: 5/5 | Pending | Due: 2026-10-25

========== Pending Tasks ==========
17:00 | Brush Buddy | Pet: Buddy | 15 min | Priority: 3/5 | Pending | Due: 2026-10-25
08:00 | Walk Buddy | Pet: Buddy | 20 min | Priority: 5/5 | Pending | Due: 2026-10-25
08:00 | Feed Whiskers | Pet: Whiskers | 10 min | Priority: 4/5 | Pending | Due: 2026-10-26

========== Completed Tasks ==========
08:00 | Feed Whiskers | Pet: Whiskers | 10 min | Priority: 4/5 | Completed | Due: 2026-10-25

========== Today's Schedule ==========
PawPal+ Daily Plan — 2026-10-25
----------------------------------------
1. 08:00 | Walk Buddy (Buddy) — 20 min, priority 5/5
2. 17:00 | Brush Buddy (Buddy) — 15 min, priority 3/5

Total: 35 / 45 minutes

========== Schedule Explanation ==========
Plan for 2026-10-25: 35 of 45 minutes used.
Scheduled tasks were ranked by priority (5 is highest), then by shorter duration when priorities tied.
- Selected 'Walk Buddy': priority 5/5, 20 minutes.
- Selected 'Brush Buddy': priority 3/5, 15 minutes.
Completed tasks were excluded from scheduling.  

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
