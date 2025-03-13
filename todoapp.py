from datetime import date, datetime

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Input, Label

from taskmanager import TaskManager




class ToDoApp(App):
    CSS  = """
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
    .due-date {
    width: 15;
    align: center middle;
    color: cyan;
    }
    """

    def compose(self):
        self.task_manager = TaskManager()  
        self.task_list = Vertical()
         

        yield Input(placeholder="New task description", id="desc")
        yield Input(placeholder="Due date (YYYY-MM-DD)", id="due_date")
        yield Button("Add Task", id="add")
        yield self.task_list  

    def on_mount(self):
        self.update_tasks()

    # def create_task_buttons(self):
    #     tasks = self.task_manager.get_tasks()
    #     buttons = []
    #     today = date.today()
        
    #     # for task in tasks:
    #     #     if task.completed:
    #     #         style = "complete"
    #     #     elif task.due_date and task.due_date < today:
    #     #         style = "overdue"
    #     #     else:
    #     #         style = "incomplete"

    #         # buttons.append(Horizontal(
    #         #     Button(task.description, id=f"task_{task.id}", classes=style),
    #         #     Button("Done", id=f"done_{task.id}")
    #         # ))
    #     return buttons

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
        elif button_id.startswith("delete_"):
            task_id = int(button_id.split("_")[1])
            self.task_manager.delete_task(task_id)
            self.update_tasks()


    def add_task(self):
        inputs = self.query(Input)
        description = inputs[0].value.strip()
        due_date_text = inputs[1].value.strip()
        due_date = datetime.strptime(due_date_text, "%Y-%m-%d").date() if due_date_text else None
        
        if description:
            self.task_manager.add_task(description, due_date)
            self.update_tasks()


    def update_tasks(self):
        self.task_list.remove_children()
        today = date.today()

        for task in self.task_manager.get_tasks():
            if task.completed:
                style = "complete"
            elif task.due_date and task.due_date < today:
                style = "overdue"
            else:
                style = "incomplete"
            
            due_date_text = task.due_date.strftime("%Y-%m-%d") if task.due_date else "No Due Date"
            
            self.task_list.mount(
                Horizontal(
                    Label(due_date_text, classes="due-date"),
                    Button(task.description, id=f"task_{task.id}", classes=style),
                    Button("Done", id=f"done_{task.id}"),
                    Button("Delete Task", id=f"delete_{task.id}"),))
            

if __name__ == "__main__":
    ToDoApp().run()
            