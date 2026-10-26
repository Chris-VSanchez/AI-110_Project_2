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

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
