from sqlmodel import SQLModel, Field, Session, create_engine, select

engine = create_engine("sqlite:///todolist.db")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

##Define the Class, "Task".



class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
    completed: bool = Field(default=False)
    
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
        self.engine = engine
    
    def add_task(self):
        description = input("Please enter task description:")
        
        new_task=Task(description=description)
        
        with Session(self.engine) as session:
            session.add(new_task)
            session.commit()
            print("This task has been added to your list.\n")


    def view_tasks(self):
        with Session(self.engine) as session:
            tasks = session.exec(select(Task)).all()

            if tasks:
                for idx, task in enumerate(tasks, start=1):
                    print(f"{idx}. {task}")
                else:
                    print("There are currently no active tasks.\n")

    
    def complete_task(self):
        with Session(self.engine) as session:
            tasks = session.exec(select(Task)).all()
            if not tasks:
                print("There are no tasks to complete.\n")
                return

            for idx, task in enumerate(tasks, start=1):
                print(f"{idx}. {task}")

            try:
                index = int(input("Enter task number to complete: ")) - 1
                if 0 <= index < len(tasks):
                    task_to_update = tasks[index]
                    task_to_update.mark_complete()
                    session.add(task_to_update)
                    session.commit()
                    print("You have successfully completed this task!\n")
                else:
                    print("Invalid task number.\n")
            except ValueError:
                print("Please enter a valid number.\n")

    def delete_task(self):
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
        
