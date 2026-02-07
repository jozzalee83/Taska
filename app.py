import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Glenn's 50th Planner", page_icon="🎂", layout="wide")

# --- THE "AI" BRAIN (Simple Keyword Matching) ---
def magic_categorise(task_text):
    task_lower = task_text.lower()
    if any(x in task_lower for x in ['pay', 'cost', 'deposit', 'money', 'owed']):
        return "💰 Finance"
    elif any(x in task_lower for x in ['eat', 'food', 'dinner', 'lunch', 'bbq', 'cake', 'ice', 'beer']):
        return "🍔 Food & Drink"
    elif any(x in task_lower for x in ['drive', 'car', 'fuel', 'map', 'bonnie', 'road']):
        return "🚗 Travel"
    elif any(x in task_lower for x in ['bnb', 'sleep', 'bed', 'room', 'house']):
        return "🏠 Accommodation"
    return "📝 General"

# --- SIDEBAR (The Control Centre) ---
st.sidebar.title("🎂 Glenn's 50th")
st.sidebar.write("Shepparton ➡️ Bonnie Doon")
category_filter = st.sidebar.radio("View Category:", 
    ["All", "🏠 Accommodation", "🍔 Food & Drink", "🚗 Travel", "💰 Finance", "📝 General"])

# --- MAIN APP ---
st.title("The Birthday Mission Control 🚀")

# 1. THE INPUT SECTION
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Add New Task")
    new_task = st.text_input("What needs doing?", placeholder="e.g. Order the keg for Saturday")
    
    # Advanced Options (Sub-categories)
    with st.expander("More Options (Sub-categories & Files)"):
        sub_cat = st.selectbox("Sub-Category", ["To-Do", "Shopping List", "Urgent", "Idea"])
        uploaded_file = st.file_uploader("Attach Document (PDF/Image)", type=['png', 'jpg', 'pdf'])

    if st.button("Add Task ✨"):
        if new_task:
            # Auto-detect category using our "AI" function
            auto_cat = magic_categorise(new_task)
            
            # Creating a neat dictionary for the task
            task_entry = {
                "Task": new_task,
                "Category": auto_cat,
                "Sub-Category": sub_cat,
                "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "File": uploaded_file.name if uploaded_file else "No File"
            }
            
            # In a real app, we would save this to a database here
            if 'tasks' not in st.session_state:
                st.session_state['tasks'] = []
            st.session_state['tasks'].append(task_entry)
            st.success(f"Added to {auto_cat}!")

# 2. THE LIST (Displaying the messy family inputs neatly)
st.divider()
st.subheader(f"📋 The List: {category_filter}")

# Initialize session state if empty
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = [
        {"Task": "Book the BnB", "Category": "🏠 Accommodation", "Sub-Category": "Urgent", "File": "booking_conf.pdf"},
        {"Task": "Buy Glenn's Cake", "Category": "🍔 Food & Drink", "Sub-Category": "Shopping List", "File": "No File"},
    ]

# Convert to DataFrame for easy filtering
df = pd.DataFrame(st.session_state['tasks'])

# Filter logic
if category_filter != "All":
    df = df[df['Category'] == category_filter]

# Show the data table
st.dataframe(
    df, 
    column_config={
        "File": st.column_config.TextColumn("Attachments", help="Files uploaded"),
        "Category": st.column_config.TextColumn("Category", width="medium"),
    },
    use_container_width=True,
    hide_index=True
)

# 3. STATS (For the organiser)
st.divider()
st.metric("Total Tasks", len(st.session_state['tasks']), delta="Get cracking!")
