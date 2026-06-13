import argparse
from rich.console import Console
from rich.table import Table

from utils.data_manager import load_data, save_data
from models.user import User
from models.project import Project
from models.task import Task

console = Console()

def sync_id_counters(data):
    if data["users"]:
        User._id_counter = max(u["id"] for u in data["users"])
    if data["projects"]: 
        Project._id_counter = max(p["id"] for p in data["projects"])
    if data["tasks"]:    
        Task._id_counter = max(t["id"] for t in data["tasks"])

def handle_add_user(args):
    data = load_data()
    sync_id_counters(data)
    try:
        new_user = User(name=args.name, email=args.email)
        data["users"].append(new_user.to_dict())
        save_data(data)
        console.print(f"[green]Successfully created user: {new_user}[/green]")
    except ValueError as e:
        console.print(f"[red]Error setting up profile fields: {e}[/red]")

def handle_list_users(args):
    data = load_data()
    table = Table(title="Registered Users System Graph")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Email Source", style="green")
    
    for u in data["users"]:
        table.add_row(str(u["id"]), u["name"], u["email"])
    console.print(table)

def handle_add_project(args):
    data = load_data()
    sync_id_counters(data)
    
    if not any(u["id"] == args.user_id for u in data["users"]):
        console.print(f"[red]User with ID {args.user_id} does not exist.[/red]")
        return

    new_project = Project(title=args.title, description=args.desc, due_date=args.due, user_id=args.user_id)
    data["projects"].append(new_project.to_dict())
    save_data(data)
    console.print(f"[green]Added project: '{new_project.title}' assigned to User ID {args.user_id}[/green]")

def handle_list_projects(args):
    data = load_data()
    table = Table(title="System Operational Projects")
    table.add_column("Proj ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Owner User ID", style="yellow")
    table.add_column("Due Date", style="green")

    for p in data["projects"]:
        if args.user_id and p["user_id"] != args.user_id:
            continue
        table.add_row(str(p["id"]), p["title"], str(p["user_id"]), p["due_date"])
    console.print(table)

def handle_add_task(args):
    data = load_data()
    sync_id_counters(data)
    
    if not any(p["id"] == args.project_id for p in data["projects"]):
        console.print(f"[red]Project with ID {args.project_id} does not exist.[/red]")
        return

    new_task = Task(title=args.title, project_id=args.project_id)
    data["tasks"].append(new_task.to_dict())
    save_data(data)
    console.print(f"[green]Added task '{new_task.title}' to Project ID {args.project_id}[/green]")

def handle_complete_task(args):
    data = load_data()
    for t in data["tasks"]:
        if t["id"] == args.task_id:
            t["status"] = "Completed"
            save_data(data)
            console.print(f"[green]Task ID {args.task_id} status updated to 'Completed'[/green]")
            return
    console.print(f"[red]Task ID {args.task_id} not found.[/red]")

def handle_list_tasks(args):
    """Renders out tracked tasks inside a formatted UI table."""
    data = load_data()
    table = Table(title="Project Task Milestones")
    table.add_column("Task ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Proj ID", style="yellow")
    table.add_column("Status", style="green")

    for t in data["tasks"]:
        if args.project_id and t["project_id"] != args.project_id:
            continue
            
        status_style = "[green]Completed[/green]" if t["status"] == "Completed" else "[yellow]Pending[/yellow]"
        table.add_row(str(t["id"]), t["title"], str(t["project_id"]), status_style)
        
    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Multi-User Production Tracker CLI Platform Interface Engine")
    subparsers = parser.add_subparsers(dest="command", help="System Commands")

    # Add User
    u_add = subparsers.add_parser("add-user", help="Register a profile item record.")
    u_add.add_argument("--name", required=True, help="User name.")
    u_add.add_argument("--email", required=True, help="User email profile handle.")
    u_add.set_defaults(func=handle_add_user)

    # List Users
    u_lst = subparsers.add_parser("list-users", help="Render out database global profiles.")
    u_lst.set_defaults(func=handle_list_users)
    
    # Add Project
    p_add = subparsers.add_parser("add-project", help="Create an assignment canvas node.")
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--desc", default="No description given.")
    p_add.add_argument("--due", default="N/A")
    p_add.add_argument("--user-id", type=int, required=True)
    p_add.set_defaults(func=handle_add_project)

    # List Projects
    p_lst = subparsers.add_parser("list-projects", help="Render all tracking modules.")
    p_lst.add_argument("--user-id", type=int, help="Filter down to target user.")
    p_lst.set_defaults(func=handle_list_projects)

    # Add Task
    t_add = subparsers.add_parser("add-task", help="Append milestone tracker item node.")
    t_add.add_argument("--title", required=True)
    t_add.add_argument("--project-id", type=int, required=True)
    t_add.set_defaults(func=handle_add_task)

    # Complete Task
    t_cmp = subparsers.add_parser("complete-task", help="Flag objective state tracker tracking line.")
    t_cmp.add_argument("--task-id", type=int, required=True)
    t_cmp.set_defaults(func=handle_complete_task)

    # List Tasks
    t_lst = subparsers.add_parser("list-tasks", help="Render task tracking items.")
    t_lst.add_argument("--project-id", type=int, help="Filter down to a target project.")
    t_lst.set_defaults(func=handle_list_tasks)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()