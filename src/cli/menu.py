"""Menu display and user input handling for the CLI."""


def display_header():
    """Display the application header and branding."""
    print("\n" + "=" * 50)
    print("         TODO APP - Phase I")
    print("=" * 50)
    print("⚠️  Warning: All data is stored in memory only.")
    print("   All todos will be lost when you exit.")
    print("=" * 50 + "\n")


def display_main_menu():
    """Display the main menu options."""
    print("\nMain Menu:")
    print("1. Add todo")
    print("2. View all todos")
    print("3. Mark todo as complete")
    print("4. Update todo")
    print("5. Delete todo")
    print("6. Exit")


def get_menu_choice() -> str:
    """Get and validate menu choice from user.

    Returns:
        User's menu choice as a string (1-6)
    """
    while True:
        choice = input("\nEnter your choice (1-6): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6"]:
            return choice
        print("❌ Error: Invalid choice")
        print("💡 Suggestion: Please enter a number between 1 and 6")


def display_goodbye():
    """Display goodbye message when exiting."""
    print("\n" + "=" * 50)
    print("Thank you for using TODO APP!")
    print("⚠️  Reminder: All todos have been cleared from memory.")
    print("=" * 50 + "\n")
