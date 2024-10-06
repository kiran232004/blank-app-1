import streamlit as st
import time


@st.cache_resource
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

if 'show_alert' not in st.session_state:
    st.session_state['show_alert'] = False

if 'alert_timeout' not in st.session_state:
    st.session_state['alert_timeout'] = 0

if 'editing_index' not in st.session_state:
    st.session_state['editing_index'] = None


def add_task():
    task = st.session_state.task_input
    if task:
        st.session_state.tasks.append(task)
        st.session_state.task_input = ""  
        show_alert("Task added successfully!")


def show_alert(message):
    st.session_state['show_alert'] = message
    st.session_state['alert_timeout'] = time.time() + 5  


def delete_task(index):
    st.session_state.tasks.pop(index)
    show_alert("Task deleted successfully!")


def edit_task(index):
    edited_task = st.session_state.tasks[index]
    new_task = st.text_input("Edit Task", edited_task, key=f"edit_task_{index}")
    if st.button("Save", key=f"save_{index}"):
        st.session_state.tasks[index] = new_task
        st.session_state.editing_index = None 
        show_alert("Task updated successfully!")


st.title("📝 To-Do List")


load_css()


st.text_input("New Task", key='task_input')
st.button("Add Task", on_click=add_task)

# Display alert for 5 seconds
if st.session_state['show_alert']:
    st.success(st.session_state['show_alert'])
    
   
    if time.time() > st.session_state['alert_timeout']:
        st.session_state['show_alert'] = False


if st.session_state.tasks:
    st.subheader("Your Tasks:")
    for index, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([1, 1])  
        with col1:
            if st.button("✏️", key=f"edit_{index}"):
                st.session_state.editing_index = index  

        with col2:
            if st.button("🗑️", key=f"delete_{index}"):
                delete_task(index)

    
        if st.session_state.editing_index == index:
            edit_task(index)
        else:
            st.markdown(f"<div class='task-card'><strong>{index + 1}. {task}</strong></div>", unsafe_allow_html=True)
else:
    st.write("No tasks added yet.")
