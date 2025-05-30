import os
from typing import List
from task_manager import TaskManager, Task

class UserInterface:
    """Command-line user interface with category support"""
    
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 40)
        print("       TASK MANAGER MENU v2.0")
        print("=" * 40)
        print("1. Add New Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View Completed Tasks")
        print("5. View Tasks by Category")
        print("6. View Tasks by Tag")
        print("7. Mark Task Complete")
        print("8. Mark Task Incomplete")
        print("9. Edit Task")
        print("10. Delete Task")
        print("11. Manage Categories")
        print("12. Manage Tags")
        print("13. View Statistics")
        print("14. Search Tasks")
        print("0. Exit")
        print("=" * 40)
    
    def get_user_input(self, prompt: str) -> str:
        """Get user input with prompt"""
        return input(f"{prompt}: ").strip()
    
    def get_user_choice(self) -> str:
        """Get user menu choice"""
        return self.get_user_input("Enter your choice")
    
    def display_tasks(self, tasks: List[Task], title: str = "Tasks"):
        """Display a list of tasks with enhanced formatting"""
        print(f"\n{title.upper()}")
        print("-" * len(title))
        
        if not tasks:
            print("No tasks found.")
            return
        
        # Group tasks by category for better display
        categories = {}
        for task in tasks:
            if task.category not in categories:
                categories[task.category] = []
            categories[task.category].append(task)
        
        # Sort tasks within each category
        priority_order = {"high": 0, "medium": 1, "low": 2}
        
        for category in sorted(categories.keys()):
            print(f"\n📁 {category}:")
            category_tasks = sorted(categories[category], 
                                  key=lambda t: (t.completed, priority_order.get(t.priority, 3)))
            
            for i, task in enumerate(category_tasks, 1):
                print(f"   {i}. {task}")
                if task.description:
                    print(f"      Description: {task.description}")
                print(f"      Created: {task.created_at}")
                if task.completed_at:
                    print(f"      Completed: {task.completed_at}")
                print()
    
    def add_task(self):
        """Add a new task with category selection"""
        print("\n" + "=" * 30)
        print("        ADD NEW TASK")
        print("=" * 30)
        
        title = self.get_user_input("Task title")
        if not title:
            print("Error: Task title cannot be empty!")
            return
        
        description = self.get_user_input("Description (optional)")
        
        print("\nPriority levels: low, medium, high")
        priority = self.get_user_input("Priority (default: medium)")
        if not priority:
            priority = "medium"
        
        # Category selection
        categories = self.task_manager.get_all_categories()
        if categories:
            print(f"\nAvailable categories: {', '.join(categories)}")
        category = self.get_user_input("Category (default: General)")
        if not category:
            category = "General"
        
        # Tags
        tags_input = self.get_user_input("Tags (comma-separated, optional)")
        
        try:
            task = self.task_manager.add_task(title, description, priority, category)
            
            # Add tags
            if tags_input:
                for tag in tags_input.split(','):
                    task.add_tag(tag.strip())
            
            print(f"\nTask '{task.title}' added successfully to category '{category}'!")
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_tasks_by_category(self):
        """View tasks filtered by category"""
        categories = self.task_manager.get_all_categories()
        if not categories:
            print("\nNo categories found!")
            return
        
        print("\nAvailable categories:")
        for i, category in enumerate(categories, 1):
            count = len(self.task_manager.get_tasks_by_category(category))
            print(f"{i}. {category} ({count} tasks)")
        
        try:
            choice = int(self.get_user_input("Select category number"))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                tasks = self.task_manager.get_tasks_by_category(selected_category)
                self.display_tasks(tasks, f"Tasks in '{selected_category}'")
            else:
                print("Invalid category number!")
        except ValueError:
            print("Please enter a valid number!")
    
    def view_tasks_by_tag(self):
        """View tasks filtered by tag"""
        all_tags = set()
        for task in self.task_manager.get_all_tasks():
            all_tags.update(task.tags)
        
        if not all_tags:
            print("\nNo tags found!")
            return
        
        print(f"\nAvailable tags: {', '.join(sorted(all_tags))}")
        tag = self.get_user_input("Enter tag to filter by")
        
        if tag:
            tasks = self.task_manager.get_tasks_by_tag(tag.lower())
            self.display_tasks(tasks, f"Tasks tagged with '{tag}'")
    
    def manage_categories(self):
        """Manage categories"""
        while True:
            print("\n" + "=" * 30)
            print("     CATEGORY MANAGEMENT")
            print("=" * 30)
            print("1. View all categories")
            print("2. Add new category")
            print("3. Remove category")
            print("0. Back to main menu")
            
            choice = self.get_user_choice()
            
            if choice == "1":
                categories = self.task_manager.get_all_categories()
                if categories:
                    print("\nAll categories:")
                    for i, category in enumerate(categories, 1):
                        count = len(self.task_manager.get_tasks_by_category(category))
                        print(f"{i}. {category} ({count} tasks)")
                else:
                    print("\nNo categories found!")
            
            elif choice == "2":
                new_category = self.get_user_input("Enter new category name")
                if self.task_manager.add_category(new_category):
                    print(f"Category '{new_category}' added successfully!")
                else:
                    print("Category already exists or invalid name!")
            
            elif choice == "3":
                categories = self.task_manager.get_all_categories()
                if categories:
                    print("\nCategories:")
                    for i, category in enumerate(categories, 1):
                        count = len(self.task_manager.get_tasks_by_category(category))
                        print(f"{i}. {category} ({count} tasks)")
                    
                    try:
                        choice_num = int(self.get_user_input("Select category to remove"))
                        if 1 <= choice_num <= len(categories):
                            category_to_remove = categories[choice_num - 1]
                            if self.task_manager.remove_category(category_to_remove):
                                print(f"Category '{category_to_remove}' removed!")
                            else:
                                print("Cannot remove category - it contains tasks!")
                        else:
                            print("Invalid category number!")
                    except ValueError:
                        print("Please enter a valid number!")
                else:
                    print("\nNo categories to remove!")
            
            elif choice == "0":
                break
            else:
                print("Invalid choice!")
    
    def manage_tags(self):
        """Manage task tags"""
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("\nNo tasks available!")
            return
        
        self.display_tasks(tasks, "All Tasks")
        
        task_id = self.select_task_by_number(tasks)
        if not task_id:
            return
        
        task = self.task_manager.get_task(task_id)
        
        while True:
            print(f"\nManaging tags for: {task.title}")
            print(f"Current tags: {', '.join(task.tags) if task.tags else 'None'}")
            print("\n1. Add tag")
            print("2. Remove tag")
            print("0. Done")
            
            choice = self.get_user_choice()
            
            if choice == "1":
                tag = self.get_user_input("Enter tag to add")
                task.add_tag(tag)
                print(f"Tag '{tag}' added!")
            
            elif choice == "2":
                if task.tags:
                    print(f"Current tags: {', '.join(task.tags)}")
                    tag = self.get_user_input("Enter tag to remove")
                    task.remove_tag(tag)
                    print(f"Tag '{tag}' removed!")
                else:
                    print("No tags to remove!")
            
            elif choice == "0":
                break
            else:
                print("Invalid choice!")
    
    def mark_task_complete(self):
        """Mark a task as complete"""
        pending_tasks = self.task_manager.get_pending_tasks()
        if not pending_tasks:
            print("\nNo pending tasks to complete!")
            return
        
        self.display_tasks(pending_tasks, "Pending Tasks")
        
        task_id = self.select_task_by_number(pending_tasks)
        if task_id:
            task = self.task_manager.get_task(task_id)
            task.mark_complete()
            print(f"\nTask '{task.title}' marked as complete!")
    
    def mark_task_incomplete(self):
        """Mark a task as incomplete"""
        completed_tasks = self.task_manager.get_completed_tasks()
        if not completed_tasks:
            print("\nNo completed tasks to mark incomplete!")
            return
        
        self.display_tasks(completed_tasks, "Completed Tasks")
        
        task_id = self.select_task_by_number(completed_tasks)
        if task_id:
            task = self.task_manager.get_task(task_id)
            task.mark_incomplete()
            print(f"\nTask '{task.title}' marked as incomplete!")
    
    def edit_task(self):
        """Edit an existing task"""
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("\nNo tasks available to edit!")
            return
        
        self.display_tasks(tasks, "All Tasks")
        
        task_id = self.select_task_by_number(tasks)
        if not task_id:
            return
        
        task = self.task_manager.get_task(task_id)
        
        print(f"\nEditing task: {task.title}")
        print("Leave empty to keep current value")
        
        new_title = self.get_user_input(f"New title (current: {task.title})")
        new_description = self.get_user_input(f"New description (current: {task.description})")
        new_priority = self.get_user_input(f"New priority (current: {task.priority})")
        
        categories = self.task_manager.get_all_categories()
        print(f"Available categories: {',
