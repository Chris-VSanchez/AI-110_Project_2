
import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule, Scheduler

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="centered",
)

st.title("🐾 PawPal+")
st.markdown(
    """
Welcome to **PawPal+**, your pet-care planning assistant!

Add your pets and their care tasks, then generate a daily plan
based on task priority and the time you have available.
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

# --------------------------------------------------
# Add a Pet
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
    for pet in owner.pets:
        with st.expander(f"🐾 {pet.name} ({pet.species})"):
            st.write(f"**Age:** {pet.age} years")
            st.write(f"**Owner:** {owner.name}")
            st.write(f"**Care tasks:** {len(pet.tasks)}")
else:
    st.info("No pets added yet. Use the form above to add your first pet.")

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

    col1, col2 = st.columns(2)

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

    priority_map = {
        "Low": 1,
        "Medium": 3,
        "High": 5,
    }

    pet_options = {
        f"{pet.name} ({pet.species})": pet
        for pet in owner.pets
    }

    selected_pet_label = st.selectbox(
        "Assign task to pet",
        options=list(pet_options.keys()),
        disabled=not owner.pets,
    )

    frequency = st.selectbox(
        "Frequency",
        ["daily", "weekly", "monthly", "as needed"],
    )

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
            )

            # Connect the task to the selected pet and owner.
            selected_pet.add_task(task)
            owner.create_task(task)

            st.success(
                f"Added '{task.title}' for {selected_pet.name}!"
            )

        except ValueError as error:
            st.error(str(error))

# --------------------------------------------------
# Display all care tasks
# --------------------------------------------------

all_tasks = owner.get_all_tasks()

if all_tasks:
    st.subheader("Your Current Tasks")

    task_rows = []

    for task in all_tasks:
        task_rows.append(
            {
                "Task": task.title,
                "Pet": task.pet.name if task.pet else "Unassigned",
                "Duration (min)": task.duration_minutes,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Completed": "Yes" if task.is_completed else "No",
            }
        )

    st.dataframe(
        task_rows,
        use_container_width=True,
        hide_index=True,
    )

    # Allow users to mark tasks complete or incomplete.
    st.subheader("Update Task Status")

    task_options = {
        f"{task.title} — "
        f"{task.pet.name if task.pet else 'Unassigned'}": task
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
            st.rerun()
    else:
        if st.button("Mark as Complete"):
            selected_task.mark_complete()
            st.rerun()

else:
    st.info("No care tasks yet. Add a task above.")

# --------------------------------------------------
# Generate the daily schedule
# --------------------------------------------------

st.divider()
st.header("🗓️ Daily Care Plan")

st.caption(
    "The scheduler prioritizes higher-priority tasks first, "
    "then shorter tasks when priorities are tied. Tasks that "
    "do not fit are skipped so shorter tasks can still fit."
)

if st.button("Generate Schedule", type="primary", use_container_width=True):
    try:
        schedule = owner.generate_schedule()
        st.session_state.latest_schedule = schedule
        st.success("Your daily care plan is ready!")
    except ValueError as error:
        st.error(str(error))

# Display the latest schedule after any normal rerun.
schedule = st.session_state.get("latest_schedule")

if schedule is not None:
    st.subheader(f"Plan for {schedule.date.isoformat()}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Scheduled tasks", len(schedule.tasks))
    col2.metric("Time used", f"{schedule.total_duration} min")
    col3.metric(
        "Time remaining",
        f"{schedule.available_minutes - schedule.total_duration} min",
    )

    if schedule.tasks:
        st.markdown("### ✅ Scheduled Tasks")

        for index, task in enumerate(schedule.tasks, start=1):
            pet_name = task.pet.name if task.pet else "Unassigned pet"

            st.write(
                f"**{index}. {task.title}** — {pet_name}"
            )
            st.caption(
                f"{task.duration_minutes} minutes · "
                f"Priority {task.priority}/5 · "
                f"{task.frequency}"
            )
    else:
        st.info("No eligible tasks fit the available time.")

    if schedule.skipped_tasks:
        st.markdown("### ⏭️ Tasks Not Scheduled")

        for task in schedule.skipped_tasks:
            st.write(
                f"- **{task.title}** — "
                f"{task.duration_minutes} minutes "
                f"(Priority {task.priority}/5)"
            )

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