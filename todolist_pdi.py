from sqlmodel import SQLModel, Field, Session, create_engine, select
from datetime import date, datetime
from sqlalchemy import asc
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Header, Footer, Static


engine = create_engine("sqlite:///todolist.db")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

##Define the Class, "Task". 



class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
    completed: bool = Field(default=False)
    due_date: date | None = Field(default=None)
    
    def mark_complete(self):
        self.completed = True
    
    def __str__(self):
        if self.completed:
            status = "[✓]"
            due = f"(Due: {self.due_date})"
            return f"{status} {self.description}{due}\n"
        else:
            status = "[ ]"
            due = f"(Due: {self.due_date})" if self.due_date else ""
            return f"{status} {self.description}{due}\n"



##Define the actual To Do List
class ToDoList:
    def __init__(self):
        self.engine = engine
    
    def add_task(self):
        while True:
            description = input("Please enter task description:")

            due_date_input = input("Enter due date (YYYY-MM-DD) or leave blank: ")
            due_date = None
            if due_date_input:
                try:
                    due_date = datetime.strptime(due_date_input, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date format. Task will be added without a due date.")

            
            new_task=Task(description=description, due_date=due_date)
            
            with Session(self.engine) as session:
                session.add(new_task)
                session.commit()
                print("This task has been added to your list.\n")
            
            while True:
                add_another = input("Would you like to add another task? (y/n): \n").strip().lower()
                if add_another == 'y':
                    break
                elif add_another == 'n':
                    return
                else:
                    print("Invalid choice, please try again.\n")
        

           


    def view_tasks(self):
        while True:
            with Session(self.engine) as session:
                tasks = session.exec(select(Task).order_by(asc(Task.due_date))).all()

                if tasks:
                    for idx, task in enumerate(tasks, start=1):
                        print(f"{idx}. {task}")
                else:
                    print("There are currently no active tasks.\n")
            return_to_menu = input("Would you like to return to the main menu? (y/n)\n").strip().lower()
            if return_to_menu == 'y':
                return
            elif return_to_menu == 'n':
                break
            else:
                print("Invalid choice, please try again.\n")


    
    def complete_task(self):
        while True:
            with Session(self.engine) as session:
                tasks = session.exec(select(Task)).all()
                if not tasks:
                    print("There are no tasks to complete.\n")
                    return

                active_tasks = [task for task in tasks if not task.completed]

                if not active_tasks:
                    print("All active tasks have been completed!\n")
                    break

                for idx, task in enumerate(tasks, start=1):
                    print(f"{idx}. {task}")

                try:
                    index = int(input("Enter task number to complete: ")) - 1
                    if 0 <= index < len(active_tasks):
                        task_to_update = active_tasks[index]
                        task_to_update.mark_complete()
                        session.add(task_to_update)
                        session.commit()
                        print("You have successfully completed this task!\n")
                    else:
                        print("Invalid task number.\n")
                except ValueError:
                    print("Please enter a valid number.\n")
            while True:
                complete_another = input("Would you like to complete any other tasks? (y/n): \n").strip().lower()
                if complete_another == 'y':
                    break
                elif complete_another == 'n':
                    return
                else:
                    print("Invalid Choice, please try again.\n")
           

    def delete_task(self):
        while True:
            with Session(self.engine) as session:
                tasks = session.exec(select(Task)).all()
                if not tasks:
                    print("There are no tasks to delete.\n")
                    return
                for idx, task in enumerate(tasks, start=1):
                    print(f"{idx}. {task}")

                try:
                    index = int(input("Enter task number to delete: ")) - 1
                    if 0 <= index < len(tasks):
                        task_to_delete = tasks[index]
                        session.delete(task_to_delete)
                        session.commit()
                        print(f"Deleted task: {task_to_delete.description}.\n")
                    else:
                        print("Invalid task number.\n")
                except ValueError:
                    print("Please enter a valid number.\n")
            while True:
                delete_another = input("Would you like to delete any other tasks? (y/n): \n").strip().lower()
                if delete_another == 'y':
                    break
                elif delete_another == 'n':
                    return
                else:
                    print("Invalid Choice, please try again.\n")
        
    def run(self):
        create_db_and_tables()

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
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
if __name__ == "__main__":
    todo_list = ToDoList()
    todo_list.run()
        
