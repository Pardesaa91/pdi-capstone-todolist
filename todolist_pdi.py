
##Define the Class, "Task".
class Task:
    def __init__ (self, description):
        self.description = description
        self.completed = False

    def mark_complete(self):
        self.completed = True
    
    def __str__(self):
        if self.completed:
            status = "[✓]"
            return f"{status} {self.description}\n"
        else:
            status = "[ ]"
            return f"{status} {self.description}\n"

##Define the actual To Do List
class ToDoList:
    def __init__(self):
        self.tasks = []
    
    def add_task(self):
        description = input("Please enter task description:")
        self.tasks.append(Task(description))
        print("This task has been added to your list.\n")

    def view_tasks(self):
        if self.tasks:
            for idx, task in enumerate(self.tasks, start=1):
                print(f"{idx}. {task}")
        else:
            print("There are currently no active tasks.\n")
        print()
    
    def complete_task(self):
        self.view_tasks()
        try:
            index = int(input("Enter task number to complete: \n")) - 1
            if 0 <= index < len(self.tasks):
                self.tasks[index].mark_complete()
                print("You have successfully completed this task!\n")
            else:
                print("Invalid task number.\n")
        except ValueError:
            print("Please enter a valid number.\n")

    def delete_task(self):
        self.view_tasks()
        try:
            index = int(input("Enter task number to delete: \n")) - 1
            if 0 <= index <len(self.tasks):
                removed_task = self.tasks.pop(index)
                print(f"Deleted task: {removed_task.description}\n")
            else:
                print("Invalid task number.\n")
        except ValueError:
            print("Please enter a valid number.")
    
    def run(self):
        while True:
            print("Please choose an option from below:\n")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Complete Task")
            print("4. Delete Task")
            print("5. Quit")
            choice = input()
            print()

            if choice == "1":
                #Add a task
                self.add_task()
            elif choice == "2":
                #View Tasks
                self.view_tasks()
            elif choice == "3":
                #Complete a selected task
                self.complete_task()
            elif choice == "4":
                #Delete a selected task
                self.delete_task()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
if __name__ == "__main__":
    todo_list = ToDoList()
    todo_list.run()
        
