import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="wide",
)

st.title("🐾 PawPal+")
st.markdown(
    """
Welcome to **PawPal+**, your pet-care planning assistant!

Manage your pets, organize their care tasks, identify time conflicts,
and generate a daily plan based on task priority and available time.
"""
)

# --------------------------------------------------
# Initialize persistent session state
# --------------------------------------------------

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        available_minutes=60,
    )

owner = st.session_state.owner
scheduler = Scheduler(owner)

# --------------------------------------------------
# Sidebar: Owner settings
# --------------------------------------------------

with st.sidebar:
    st.header("👤 Owner Settings")

    new_owner_name = st.text_input(
        "Owner name",
        value=owner.name,
        key="owner_name_input",
    )

    available_minutes = st.number_input(
        "Available care time (minutes)",
        min_value=0,
        max_value=1440,
        value=owner.available_minutes,
        step=5,
        key="available_minutes_input",
    )

    if st.button("Save settings", use_container_width=True):
        if not new_owner_name.strip():
            st.error("Owner name cannot be empty.")
        else:
            owner.name = new_owner_name.strip()
            owner.available_minutes = int(available_minutes)
            st.success("Settings saved!")

    st.divider()
    st.caption("🐾 Every pet deserves great care!")

# --------------------------------------------------
# Your Pets
# --------------------------------------------------

st.header("🐶 Your Pets")

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")

    pet_age = st.number_input(
        "Pet age (years)",
        min_value=0,
        max_value=100,
        value=1,
        step=1,
    )

    pet_species = st.selectbox(
        "Species",
        ["dog", "cat", "bird", "rabbit", "other"],
    )

    pet_submitted = st.form_submit_button("Add Pet")

    if pet_submitted:
        try:
            pet = Pet(
                name=pet_name,
                age=int(pet_age),
                species=pet_species,
            )
            owner.add_pet(pet)
            st.success(f"{pet.name} was added successfully!")
        except ValueError as error:
            st.error(str(error))

if owner.pets:
    pet_columns = st.columns(3)

    for index, pet in enumerate(owner.pets):
        with pet_columns[index % 3]:
            with st.container(border=True):
                st.subheader(f"🐾 {pet.name}")
                st.write(f"**Species:** {pet.species.title()}")
                st.write(f"**Age:** {pet.age} years")
                st.write(f"**Owner:** {owner.name}")
                st.write(f"**Care tasks:** {len(pet.tasks)}")
else:
    st.info("No pets added yet. Add your first pet above.")

# --------------------------------------------------
# Add a Care Task
# --------------------------------------------------

st.divider()
st.header("📋 Care Tasks")

if not owner.pets:
    st.warning("Add a pet before creating a care task.")

with st.form("add_task_form", clear_on_submit=True):
    task_title = st.text_input(
        "Task title",
        placeholder="e.g. Morning walk",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=240,
            value=20,
            step=5,
        )

    with col2:
        priority_label = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"],
            index=2,
        )

    with col3:
        frequency = st.selectbox(
            "Frequency",
            ["daily", "weekly", "monthly", "as needed"],
        )

    task_time = st.time_input(
        "Scheduled start time (optional)",
        value=None,
    )

    pet_options = {
        f"{pet.name} ({pet.species})": pet
        for pet in owner.pets
    }

    selected_pet_label = st.selectbox(
        "Assign task to pet",
        options=list(pet_options.keys()),
        disabled=not owner.pets,
    )

    priority_map = {
        "Low": 1,
        "Medium": 3,
        "High": 5,
    }

    task_submitted = st.form_submit_button(
        "Add Care Task",
        disabled=not owner.pets,
    )

    if task_submitted:
        try:
            selected_pet = pet_options[selected_pet_label]

            task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority_map[priority_label],
                frequency=frequency,
                time=(
                    task_time.strftime("%H:%M")
                    if task_time is not None
                    else None
                ),
            )

            selected_pet.add_task(task)
            owner.create_task(task)

            st.success(
                f"Added '{task.title}' for {selected_pet.name}!"
            )

        except ValueError as error:
            st.error(str(error))

# --------------------------------------------------
# Task statistics
# --------------------------------------------------

st.divider()
st.header("📈 Task Overview")

scheduler = Scheduler(owner)
all_tasks = scheduler.get_all_tasks()
pending_tasks = scheduler.filter_tasks(is_completed=False)
completed_tasks = scheduler.filter_tasks(is_completed=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric("🐾 Pets", len(owner.pets))
col2.metric("📋 Total Tasks", len(all_tasks))
col3.metric("⏳ Pending", len(pending_tasks))
col4.metric("✅ Completed", len(completed_tasks))

if all_tasks:
    completion_rate = (
        len(completed_tasks) / len(all_tasks)
    )

    st.progress(
        completion_rate,
        text=f"Task completion: {completion_rate:.0%}",
    )

# --------------------------------------------------
# Task management: sorting and filtering
# --------------------------------------------------

st.divider()
st.header("🔎 Task Management Dashboard")

if not all_tasks:
    st.info("Add care tasks to start managing your tasks.")
else:
    st.subheader("📊 Sort Tasks")

    sort_option = st.selectbox(
        "Sort by",
        [
            "Priority (highest first)",
            "Time (earliest first)",
            "Duration (shortest first)",
            "Task title (A–Z)",
        ],
        key="dashboard_sort",
    )

    if sort_option == "Time (earliest first)":
        sorted_tasks = scheduler.sort_by_time(all_tasks)

    elif sort_option == "Priority (highest first)":
        sorted_tasks = sorted(
            all_tasks,
            key=lambda task: (
                -task.priority,
                task.duration_minutes,
                task.title.lower(),
            ),
        )

    elif sort_option == "Duration (shortest first)":
        sorted_tasks = sorted(
            all_tasks,
            key=lambda task: (
                task.duration_minutes,
                -task.priority,
                task.title.lower(),
            ),
        )

    else:
        sorted_tasks = sorted(
            all_tasks,
            key=lambda task: task.title.lower(),
        )

    st.subheader("🎯 Filter Tasks")

    col1, col2 = st.columns(2)

    pet_names = sorted({pet.name for pet in owner.pets})

    with col1:
        pet_filter = st.selectbox(
            "Filter by pet",
            ["All pets"] + pet_names,
            key="dashboard_pet_filter",
        )

    with col2:
        status_filter = st.selectbox(
            "Completion status",
            ["All tasks", "Pending", "Completed"],
            key="dashboard_status_filter",
        )

    completion_filter = {
        "All tasks": None,
        "Pending": False,
        "Completed": True,
    }[status_filter]

    filtered_tasks = scheduler.filter_tasks(
        is_completed=completion_filter,
        pet_name=(
            pet_filter
            if pet_filter != "All pets"
            else None
        ),
    )

    filtered_ids = {id(task) for task in filtered_tasks}

    display_tasks = [
        task for task in sorted_tasks
        if id(task) in filtered_ids
    ]

    st.caption(
        f"Displaying {len(display_tasks)} of {len(all_tasks)} tasks."
    )

    if display_tasks:
        task_rows = []

        for task in display_tasks:
            task_rows.append({
                "Task": task.title,
                "Pet": task.pet.name if task.pet else "Unassigned",
                "Time": task.time or "Not set",
                "Duration (min)": task.duration_minutes,
                "Priority": f"{task.priority}/5",
                "Frequency": task.frequency.title(),
                "Due Date": (
                    task.due_date.isoformat()
                    if task.due_date
                    else "Not set"
                ),
                "Status": (
                    "Completed" if task.is_completed else "Pending"
                ),
            })

        st.dataframe(
            task_rows,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("No tasks match your selected filters.")

# --------------------------------------------------
# Update task status and automate recurring tasks
# --------------------------------------------------

st.divider()
st.header("✅ Update Task Status")

all_tasks = scheduler.get_all_tasks()

if all_tasks:
    task_options = {
        (
            f"{task.title} — "
            f"{task.pet.name if task.pet else 'Unassigned'} "
            f"({'Completed' if task.is_completed else 'Pending'})"
        ): task
        for task in all_tasks
    }

    selected_task_label = st.selectbox(
        "Select a task",
        options=list(task_options.keys()),
        key="status_task_selector",
    )

    selected_task = task_options[selected_task_label]

    if selected_task.is_completed:
        if st.button("Mark as Incomplete"):
            selected_task.mark_incomplete()
            st.success("Task marked as pending.")
            st.rerun()

    else:
        if st.button("Complete Task"):
            try:
                next_task = scheduler.mark_task_complete(selected_task)

                if next_task is not None:
                    st.success(
                        f"'{selected_task.title}' completed! "
                        f"The next occurrence is due "
                        f"{next_task.due_date.isoformat()}."
                    )
                else:
                    st.success(
                        f"'{selected_task.title}' completed!"
                    )

                st.rerun()

            except ValueError as error:
                st.error(str(error))
else:
    st.info("There are no tasks to update.")

# --------------------------------------------------
# Time conflict detection
# --------------------------------------------------

st.divider()
st.header("⏰ Time Conflict Detection")

conflicts = scheduler.detect_time_conflicts()

if conflicts:
    st.warning(
        f"Found {len(conflicts)} potential time conflict(s)."
    )

    for conflict in conflicts:
        st.write(f"⚠️ {conflict}")
else:
    st.success("No time conflicts detected!")

st.caption(
    "Conflict detection checks for identical start times "
    "among pending tasks. It does not yet detect overlapping durations."
)

# --------------------------------------------------
# Generate the daily schedule
# --------------------------------------------------

st.divider()
st.header("🗓️ Daily Care Plan")

st.markdown(
    """
The scheduler prioritizes higher-priority tasks first, then shorter
tasks when priorities are tied. Tasks that do not fit are skipped,
allowing shorter tasks to fit into the remaining time.
"""
)

if st.button(
    "Generate Schedule",
    type="primary",
    use_container_width=True,
):
    try:
        schedule = owner.generate_schedule()
        st.session_state.latest_schedule = schedule
        st.success("Your daily care plan is ready!")
    except ValueError as error:
        st.error(str(error))

# Display the latest schedule after normal reruns
schedule = st.session_state.get("latest_schedule")

if schedule is not None:
    st.subheader(f"Plan for {schedule.date.isoformat()}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Scheduled Tasks", len(schedule.tasks))
    col2.metric("Time Used", f"{schedule.total_duration} min")
    col3.metric(
        "Time Remaining",
        f"{schedule.available_minutes - schedule.total_duration} min",
    )

    if schedule.tasks:
        st.markdown("### ✅ Scheduled Tasks")

        schedule_rows = []

        for index, task in enumerate(schedule.tasks, start=1):
            schedule_rows.append({
                "#": index,
                "Task": task.title,
                "Pet": task.pet.name if task.pet else "Unassigned",
                "Time": task.time or "Not set",
                "Duration (min)": task.duration_minutes,
                "Priority": f"{task.priority}/5",
                "Frequency": task.frequency.title(),
            })

        st.dataframe(
            schedule_rows,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No eligible tasks fit the available time.")

    if schedule.skipped_tasks:
        st.markdown("### ⏭️ Tasks Not Scheduled")

        skipped_rows = [
            {
                "Task": task.title,
                "Pet": task.pet.name if task.pet else "Unassigned",
                "Duration (min)": task.duration_minutes,
                "Priority": f"{task.priority}/5",
                "Reason": "Does not fit in the remaining time",
            }
            for task in schedule.skipped_tasks
        ]

        st.table(skipped_rows)

    st.markdown("### 💡 Plan Explanation")
    st.text(schedule.explain_plan())

    if st.button("Clear Displayed Schedule"):
        del st.session_state.latest_schedule
        st.rerun()

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()
st.caption("🐾 PawPal+ — Helping you care for every pet.")