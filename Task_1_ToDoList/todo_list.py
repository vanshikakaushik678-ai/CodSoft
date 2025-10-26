import json
import os
from datetime import datetime

# --- Configuration & Global State ---

# File where the task dictionary will be stored for persistence
TASK_DATA_FILE = "my_task_records.json" 
# Simple counter for assigning unique task IDs
next_task_id = 1 

# --- Data Persistence Handlers ---

def load_task_dictionary():
    """
    Loads tasks from the JSON file. Tasks are stored in a dictionary 
    for fast lookup, where the key is the task ID.
    
    Returns:
        tuple: (dict_of_tasks, next_available_id)
    """
    global next_task_id
    if os.path.exists(TASK_DATA_FILE):
        try:
            with open(TASK_DATA_FILE, 'r') as file:
                data = json.load(file)
                tasks = data.get('tasks', {})
                # Ensure the next ID is higher than any existing ID
                if tasks:
                    max_id = max(int(k) for k in tasks.keys())
                    next_task_id = max_id + 1
                return tasks
        except (json.JSONDecodeError, FileNotFoundError):
            # Handle empty or corrupt files gracefully
            print("\n[INFO] Task file not found or corrupted. Starting fresh.")
            return {}
    return {}

def save_task_dictionary(tasks):
    """Saves the current dictionary of tasks and the next ID to the JSON file."""
    data = {
        'tasks': tasks,
        'last_assigned_id': next_task_id - 1 # Store the last ID used
    }
    try:
        with open(TASK_DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"[ERROR] Could not save task data: {e}")

# --- Task Management Logic ---

def create_new_task(tasks):
    """Prompts for task details and adds a new task dictionary to the main collection."""
    global next_task_id
    
    description = input("Enter new task description: ").strip()
    if not description:
        print("\n[ALERT] Task description cannot be empty.")
        return

    due_date = input("Enter due date (Optional, e.g., YYYY-MM-DD): ").strip()
    
    # Create the detailed task object
    task_id = str(next_task_id)
    new_task = {
        'id': task_id,
        'description': description,
        'completed': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'due_date': due_date if due_date else "N/A"
    }

    tasks[task_id] = new_task
    next_task_id += 1
    save_task_dictionary(tasks)
    print(f"\n[SUCCESS] Task ID {task_id} added.")


def display_tasks(tasks, filter_status=None):
    """
    Displays tasks, optionally filtering by completion status, 
    and sorts them by ID for a consistent view.
    """
    if not tasks:
        print("\n*** The To-Do Manager is empty! ***")
        return

    # Sort tasks by integer ID for consistent ordering
    sorted_keys = sorted(tasks.keys(), key=lambda x: int(x))
    
    print("\n" + "="*60)
    print("                 CURRENT TASK LIST")
    print("="*60)
    
    found_tasks = False
    
    for task_id in sorted_keys:
        task = tasks[task_id]
        
        # Apply filter if requested
        if filter_status is None or task['completed'] == filter_status:
            status = " [DONE] " if task['completed'] else " [TODO] "
            due = f"Due: {task['due_date']}" if task['due_date'] != "N/A" else ""
            
            print(f"| {task_id:<3} {status} | {task['description']:<35} | {due:<15}")
            found_tasks = True

    if not found_tasks and filter_status is not None:
        status_text = "COMPLETED" if filter_status else "INCOMPLETE"
        print(f"\nNo {status_text} tasks found.")
        
    print("="*60 + "\n")


def toggle_task_completion(tasks):
    """Allows the user to mark a task as complete or incomplete."""
    task_id = input("Enter the Task ID to toggle status (e.g., 2): ").strip()
    task = tasks.get(task_id)

    if task:
        task['completed'] = not task['completed']
        status = "COMPLETE" if task['completed'] else "INCOMPLETE"
        save_task_dictionary(tasks)
        print(f"\n[SUCCESS] Task ID {task_id} ('{task['description']}') marked as {status}.")
    else:
        print(f"\n[ERROR] Task with ID {task_id} not found.")


def search_tasks(tasks):
    """Allows searching tasks by keyword in the description."""
    keyword = input("Enter keyword to search for: ").strip().lower()
    if not keyword:
        print("\n[ALERT] Search keyword cannot be empty.")
        return

    found_tasks = []
    for task_id, task in tasks.items():
        if keyword in task['description'].lower():
            found_tasks.append(task)

    if found_tasks:
        print("\n--- SEARCH RESULTS ---")
        for task in found_tasks:
            status = " [DONE] " if task['completed'] else " [TODO] "
            print(f"ID {task['id']} {status} - {task['description']}")
        print("----------------------")
    else:
        print(f"\nNo tasks found containing '{keyword}'.")


def delete_task_by_id(tasks):
    """Deletes a task using its unique ID."""
    task_id = input("Enter the Task ID to DELETE: ").strip()
    
    if task_id in tasks:
        deleted_task = tasks.pop(task_id)
        save_task_dictionary(tasks)
        print(f"\n[SUCCESS] Task ID {task_id} ('{deleted_task['description']}') permanently deleted.")
    else:
        print(f"\n[ERROR] Task with ID {task_id} not found. Cannot delete.")


# --- Main Application Loop ---

def run_task_manager():
    """The entry point for the Command-Line Task Manager application."""
    tasks = load_task_dictionary() # Load existing tasks on startup

    while True:
        display_tasks(tasks)
        
        print("\n--- Task Manager Menu ---")
        print("1. Add Task (A)")
        print("2. Toggle Status (C for Complete/I for Incomplete)")
        print("3. Delete Task (D)")
        print("4. Search Tasks (S)")
        print("5. View Completed/Incomplete Tasks (V)")
        print("6. Exit and Save (E)")
        
        choice = input("Enter your choice (1-6 or letter code): ").strip().upper()
        
        if choice in ('1', 'A'):
            create_new_task(tasks)
        
        elif choice in ('2', 'C', 'I'):
            toggle_task_completion(tasks)

        elif choice in ('3', 'D'):
            delete_task_by_id(tasks)
            
        elif choice in ('4', 'S'):
            search_tasks(tasks)
            
        elif choice in ('5', 'V'):
            print("\nView Options:")
            print("  - Type 'D' to see only DONE tasks.")
            print("  - Type 'T' to see only TO-DO (incomplete) tasks.")
            view_choice = input("Enter view option (D/T): ").strip().upper()
            if view_choice == 'D':
                display_tasks(tasks, filter_status=True)
            elif view_choice == 'T':
                display_tasks(tasks, filter_status=False)
            else:
                print("\n[ALERT] Invalid view option.")
        
        elif choice in ('6', 'E'):
            save_task_dictionary(tasks)
            print("\n*** Tasks saved. Shutting down Task Manager. Goodbye! ***")
            break
            
        else:
            print(f"\n[ERROR] Invalid command: '{choice}'. Please select from the menu.")
            
        # Pause before redrawing the menu to prevent screen flicker
        if choice not in ('4', 'V'): 
            input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    run_task_manager()