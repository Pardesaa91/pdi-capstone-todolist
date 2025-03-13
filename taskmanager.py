from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Input
from sqlmodel import SQLModel, Field, Session, create_engine, select
from datetime import date, datetime
from sqlalchemy import asc


engine = create_engine("sqlite:///todolist.db")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

##Define the Class, "Task". 



class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
    completed: bool = Field(default=False)
    due_date: date | None = Field(default=None)


class TaskManager:
    def __init__(self):
        self.engine = engine
    
    def add_task(self, description, due_date):           
        new_task=Task(description=description, due_date=due_date)
        with Session(self.engine) as session:
            session.add(new_task)
            session.commit()
                   
    
    def get_tasks(self):
        with Session(self.engine) as session:
            tasks = session.exec(select(Task).order_by(asc(Task.due_date))).all()
            return tasks

                
    def complete_task(self, task_id):
        with Session(self.engine) as session:
            task = session.get(Task, task_id)
            if task:
                task.completed = True
                session.commit()
           
    def delete_task(self, task_id):
        with Session(self.engine) as session:
            task = session.get(Task, task_id)
            if task:
                session.delete(task)
                session.commit()

class ToDoApp(App):
    Display  = """
    Screen {
        align: center middle;
    }
    Vertical {
        border: solid white;
        padding: 1;
    }
    Button.incomplete {
        background: yellow;
    }
    Button.complete {
        background: green;
    }
    Button.overdue {
        background: red;
    }
    """

    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()

    def compose(self) -> ComposeResult:
        yield Vertical(
            Input(placeholder="New task description"),
            Input(placeholder="Due date (YYYY-MM-DD)"),
            Button("Add Task", id="add"),
            *self.create_task_buttons()
        )

    def create_task_buttons(self):
        tasks = self.task_manager.get_tasks()
        buttons = []
        today = date.today()
        
        for task in tasks:
            if task.completed:
                style = "complete"
            elif task.due_date and task.due_date < today:
                style = "overdue"
            else:
                style = "incomplete"

            buttons.append(Horizontal(
                Button(task.description, id=f"task_{task.id}", classes=style),
                Button("Done", id=f"done_{task.id}")
            ))
        return buttons

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "add":
            self.add_task()
        elif button_id.startswith("done_"):
            task_id = int(button_id.split("_")[1])
            self.task_manager.complete_task(task_id)
            self.update_tasks()
        elif button_id.startswith("task_"):
            pass  # Placeholder for editing tasks

    def add_task(self):
        inputs = self.query(Input)
        description = inputs[0].value.strip()
        due_date_text = inputs[1].value.strip()
        due_date = datetime.strptime(due_date_text, "%Y-%m-%d").date() if due_date_text else None
        
        if description:
            self.task_manager.add_task(description, due_date)
            self.update_tasks()

    def update_tasks(self):
        self.mount(Vertical(*self.create_task_buttons()))

if __name__ == "__main__":
    ToDoApp().run()
            
