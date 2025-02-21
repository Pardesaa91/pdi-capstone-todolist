
##Define the Class, "Task".
class Task:
    def __init__ (self, description, status):
        self.description = description
        self.completed = False

    def mark_complete(self):
        self.completed = True
    
    def __str__(self):
        if self.completed():
            status = "completed"
            return f"You have {status} the task: {self.description}"
        else:
            status = "not completed"
            return f"You have {status} the task: {self.description}"

##Define the actual To Do List
class ToDoList:
    def __init__(self):
        self.tasks = []
    
    def add_task(self):
        description = input("Please enter task description:")
        self.tasks.append(Task(description))
        print("This task has been added to your list.")

    def view_tasks(self)
        if self.tasks:
            print() ##Print a list of available tasks
        else:
            print("There are currently no active tasks.")
    
    def complete_task(self)
        
    def delete_task(self)
    
    def view_menu(self)
        choice = input("Please choose from the following:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Quit")

    if choice == "1":
        #Add a task
    elif choice == "2":
        #View Tasks
    elif choice == "3":
        #Complete a selected task
    elif choice == "4":
        #Delete a selected task
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please try again.")
    
        
