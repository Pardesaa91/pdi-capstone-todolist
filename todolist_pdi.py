
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

    def view_tasks(self):
        if self.tasks:
            for idx, task in enumerate(self.tasks, start=1):
                print(f"{idx}. {task}")
        else:
            print("There are currently no active tasks.")
        print()
    
    def complete_task(self):
        self.view_tasks()
        try:
            index = int(input("Enter task number to complete: ")) - 1
            if 0 <= index < len(self.tasks):
                self.tasks[index].mark_complete()
                print("You have successfully completed this task!")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")

    def delete_task(self):
        self.view_tasks()
        try:
            index = int(input("Enter task number to delete: ")) - 1
            if 0 <= index <len(self.tasks):
                removed_task = self.tasks.pop(index)
                print(f"Deleted task: {removed_task.description}")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")
    
def view_menu():
    while True:
        print("Please choose an option from below:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Quit")
        choice = input()

        if choice == "1":
            #Add a task
            ToDoList.add_task
        elif choice == "2":
            #View Tasks
            ToDoList.view_tasks
        elif choice == "3":
            #Complete a selected task
            ToDoList.complete_task
        elif choice == "4":
            #Delete a selected task
            ToDoList.delete_task
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")
view_menu()
        
