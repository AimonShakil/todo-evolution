"""Interactive console interface for Todo Evolution.

This module provides a menu-driven interactive CLI for managing tasks.
"""

import sys
from datetime import datetime

from src.lib.validators import validate_title, validate_user_id
from src.models.task import Task
from src.services.db import get_session, init_db
from src.services.task_service import TaskService


def clear_screen():
    """Clear the console screen."""
    print("\n" * 2)


def print_header():
    """Print the application header."""
    print("=" * 60)
    print("           📝 TODO EVOLUTION - TASK MANAGER")
    print("=" * 60)
    print()


def print_menu():
    """Print the main menu."""
    print("\n" + "─" * 60)
    print("  MAIN MENU")
    print("─" * 60)
    print("  [1] ➕ Add New Task")
    print("  [2] 📋 View All Tasks")
    print("  [3] ✓  Mark Task as Complete")
    print("  [4] 🗑  Delete Task")
    print("  [5] 👤 View Tasks by User")
    print("  [6] 📊 Task Statistics")
    print("  [0] 🚪 Exit")
    print("─" * 60)


def add_task(service: TaskService):
    """Add a new task interactively."""
    print("\n➕ ADD NEW TASK")
    print("─" * 60)

    try:
        user_id = input("👤 Enter your username: ").strip()
        validate_user_id(user_id)

        title = input("📝 Enter task title: ").strip()
        validate_title(title)

        task = service.create_task(user_id=user_id, title=title)

        print("\n✅ SUCCESS!")
        print(f"   Task #{task.id} created: {task.title}")
        print(f"   User: {task.user_id}")
        print(f"   Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    except ValueError as e:
        print(f"\n❌ ERROR: {e}")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")


def view_all_tasks(service: TaskService):
    """View all tasks in the system."""
    print("\n📋 ALL TASKS")
    print("─" * 60)

    try:
        with service.session as session:
            from sqlmodel import select
            tasks = session.exec(select(Task)).all()

        if not tasks:
            print("   No tasks found. Add your first task!")
            return

        # Group by user
        users = {}
        for task in tasks:
            if task.user_id not in users:
                users[task.user_id] = []
            users[task.user_id].append(task)

        for user_id, user_tasks in users.items():
            print(f"\n👤 {user_id.upper()}")
            print("   " + "─" * 56)
            for task in user_tasks:
                status = "✓" if task.completed else "○"
                print(f"   [{task.id:3d}] {status} {task.title}")

        print(f"\n   Total: {len(tasks)} task(s)")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def view_user_tasks(service: TaskService):
    """View tasks for a specific user."""
    print("\n👤 VIEW TASKS BY USER")
    print("─" * 60)

    try:
        user_id = input("Enter username: ").strip()
        validate_user_id(user_id)

        tasks = service.get_tasks_for_user(user_id)

        if not tasks:
            print(f"\n   No tasks found for user '{user_id}'")
            return

        print(f"\n📋 Tasks for {user_id.upper()}")
        print("   " + "─" * 56)

        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"   [{task.id:3d}] {status} {task.title}")

        print(f"\n   Total: {len(tasks)} task(s)")

    except ValueError as e:
        print(f"\n❌ ERROR: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def mark_complete(service: TaskService):
    """Mark a task as complete."""
    print("\n✓ MARK TASK AS COMPLETE")
    print("─" * 60)

    try:
        task_id = int(input("Enter task ID: ").strip())

        with service.session as session:
            from sqlmodel import select
            task = session.exec(select(Task).where(Task.id == task_id)).first()

            if not task:
                print(f"\n❌ Task #{task_id} not found")
                return

            if task.completed:
                print(f"\n⚠️  Task #{task_id} is already completed")
                return

            task.completed = True
            task.updated_at = datetime.utcnow()
            session.add(task)
            session.commit()

            print(f"\n✅ Task #{task_id} marked as complete!")
            print(f"   {task.title}")

    except ValueError:
        print("\n❌ ERROR: Please enter a valid task ID number")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def delete_task(service: TaskService):
    """Delete a task."""
    print("\n🗑 DELETE TASK")
    print("─" * 60)

    try:
        task_id = int(input("Enter task ID to delete: ").strip())

        with service.session as session:
            from sqlmodel import select
            task = session.exec(select(Task).where(Task.id == task_id)).first()

            if not task:
                print(f"\n❌ Task #{task_id} not found")
                return

            confirm = input(f"\n⚠️  Delete task '{task.title}'? (yes/no): ").strip().lower()

            if confirm in ['yes', 'y']:
                session.delete(task)
                session.commit()
                print(f"\n✅ Task #{task_id} deleted successfully")
            else:
                print("\n🚫 Deletion cancelled")

    except ValueError:
        print("\n❌ ERROR: Please enter a valid task ID number")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def show_statistics(service: TaskService):
    """Show task statistics."""
    print("\n📊 TASK STATISTICS")
    print("─" * 60)

    try:
        with service.session as session:
            from sqlmodel import select, func

            # Total tasks
            total = session.exec(select(func.count(Task.id))).one()

            # Completed tasks
            completed = session.exec(
                select(func.count(Task.id)).where(Task.completed == True)
            ).one()

            # Pending tasks
            pending = total - completed

            # Users
            users = session.exec(
                select(Task.user_id, func.count(Task.id))
                .group_by(Task.user_id)
            ).all()

            print(f"\n   Total Tasks:      {total}")
            print(f"   ✓ Completed:      {completed}")
            print(f"   ○ Pending:        {pending}")

            if total > 0:
                completion_rate = (completed / total) * 100
                print(f"   Completion Rate:  {completion_rate:.1f}%")

            if users:
                print("\n   Tasks by User:")
                for user_id, count in users:
                    print(f"      {user_id}: {count} task(s)")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")


def main():
    """Main interactive loop."""
    # Initialize database
    init_db()

    clear_screen()
    print_header()

    print("Welcome! Your task manager is ready.\n")

    # Create session
    with get_session() as session:
        service = TaskService(session)

        while True:
            print_menu()

            try:
                choice = input("\n👉 Enter your choice: ").strip()

                if choice == "1":
                    add_task(service)
                elif choice == "2":
                    view_all_tasks(service)
                elif choice == "3":
                    mark_complete(service)
                elif choice == "4":
                    delete_task(service)
                elif choice == "5":
                    view_user_tasks(service)
                elif choice == "6":
                    show_statistics(service)
                elif choice == "0":
                    print("\n👋 Goodbye! Your tasks are saved.\n")
                    sys.exit(0)
                else:
                    print("\n❌ Invalid choice. Please select 0-6.")

                input("\n⏎  Press Enter to continue...")
                clear_screen()
                print_header()

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Your tasks are saved.\n")
                sys.exit(0)


if __name__ == "__main__":
    main()
