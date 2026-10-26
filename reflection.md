# PawPal+ Project Reflection

## 1. System Design
- The core actions a user should be able to perform are: adding a pet, creating tasks, and generating a daily schedule.

**a. Initial design**

- Briefly describe your initial UML design.
    Owner: a class that holds the name of the person, a list of all their pets, and availability. Decides what the schedules
        are and when. An owner can have many pets and create many tasks.
    Pet: a class that that holds all the aniimal's data (name, age, species). A pet can only have one owner.
    Task: a class that details an activity the owner will do. It includes a title, an estimated time, a priority, and a
        completion status. An owner can make many tasks and a schedule can display many tasks. A task has only one owner associted
        with it.
    Schedule: a class tht displays all the events created by an owner.

- What classes did you include, and what responsibilities did you assign to each?
    I included owner, pet, task, and schedule classes. An owner is responsible for adding pets, entering / editing their details,
    creating / editing tasks, and displaying a schedule. A schedule is responsible for displaying all the tasks for the day.

**b. Design changes**

- Did your design change during implementation?
    No, I found that my design was an accuate implementation of what the task requires. After using AI to implement my design,
        I got the confirmation that my design was solid and got the assistance I needed to create the UML and Python skeleton 
        code.

- If yes, describe at least one change and why you made it.
    N / A
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    It considers available time, task duration, priority, completion status, due dates, and scheduling conflicts.

- How did you decide which constraints mattered most?
    Priority and available time matter most so important pet-care tasks are scheduled first without exceeding the owner's time limit.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    It detects tasks with identical start times but does not detect overlapping task durations.

- Why is that tradeoff reasonable for this scenario?
    It keeps the scheduler simple and easy to understand, although checking overlapping durations would improve accuracy.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    I used AI to brainstorm features, debug errors, improve my code, and update my UML diagram.

- What kinds of prompts or questions were most helpful?
    Asking AI how to improve my scheduler, connect my classes, and update my Streamlit UI was most helpful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    I checked AI-generated code changes before using them to make sure they matched my existing classes and methods.

- How did you evaluate or verify what the AI suggested?
    I reviewed the code and tested the features to confirm they worked correctly.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested adding pets and tasks, sorting and filtering tasks, detecting conflicts, completing recurring tasks, and generating schedules.

- Why were these tests important?
    They helped me verify that the main features worked correctly and that tasks were scheduled as expected.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    I am fairly confident that my scheduler works correctly for the main scenarios I tested.

- What edge cases would you test next if you had more time?
    I would test empty task lists, zero available time, invalid inputs, and overlapping task durations.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I am most satisfied with combining pet management, task scheduling, and conflict detection into one application.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I would improve the user interface, add permanent data storage, and make conflict detection identify overlapping task durations.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    I learned that good system design, thorough testing, and verifying AI suggestions are important for building reliable software.