import json

class BudgetTracker:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        if username in self.users:
            print("Username already exists. Please choose another one.")
        else:
            self.users[username] = {"password": password, "tracker": None}
            print("User registered successfully.")

    def login_user(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            print("Login successful.")
            return True
        else:
            print("Invalid username or password.")
            return False

    def load_user_tracker(self, username):
        if username in self.users and self.users[username]["tracker"]:
            return self.users[username]["tracker"]
        else:
            print("No budget tracker found for this user.")
            return None

    def save_user_tracker(self, username, tracker):
        if username in self.users:
            self.users[username]["tracker"] = tracker
            print("Budget tracker saved successfully.")
        else:
            print("User not found.")

    def add_expense(self, username, category, description, amount):
        if username in self.users:
            if self.users[username]["tracker"] is None:
                self.users[username]["tracker"] = {"expenses": {}}
            if category not in self.users[username]["tracker"]["expenses"]:
                self.users[username]["tracker"]["expenses"][category] = []
            self.users[username]["tracker"]["expenses"][category].append({"description": description, "amount": amount})
            print("Expense added successfully.")
        else:
            print("User not found.")

    def view_expenses(self, username):
        if username in self.users and self.users[username]["tracker"]:
            expenses = self.users[username]["tracker"]["expenses"]
            if not expenses:
                print("No expenses recorded yet.")
            else:
                print("Expenses:")
                for category, category_expenses in expenses.items():
                    print(f"{category}:")
                    for expense in category_expenses:
                        print(f"  - {expense['description']}: ${expense['amount']}")
        else:
            print("No budget tracker found for this user.")

    def total_expenses(self, username):
        if username in self.users and self.users[username]["tracker"]:
            expenses = self.users[username]["tracker"]["expenses"]
            return sum(sum(expense['amount'] for expense in category_expenses) for category_expenses in expenses.values())
        else:
            print("No budget tracker found for this user.")
            return 0

    def remaining_budget(self, username, monthly_budget):
        if username in self.users and self.users[username]["tracker"]:
            total_expenses = self.total_expenses(username)
            return monthly_budget - total_expenses
        else:
            print("No budget tracker found for this user.")
            return monthly_budget

    def save_users_data(self, filename="users.json"):
        with open(filename, "w") as file:
            json.dump(self.users, file)

    def load_users_data(self, filename="users.json"):
        try:
            with open(filename, "r") as file:
                self.users = json.load(file)
        except FileNotFoundError:
            print("No user data found.")

def main():
    tracker = BudgetTracker()
    tracker.load_users_data()

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            tracker.register_user(username, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if tracker.login_user(username, password):
                while True:
                    print("\n1. Add Expense")
                    print("2. View Expenses")
                    print("3. Total Expenses")
                    print("4. Remaining Budget")
                    print("5. Save and Logout")
        
                    user_choice = input("Enter your choice: ")
        
                    if user_choice == "1":
                        category = input("Enter expense category: ")
                        description = input("Enter expense description: ")
                        amount = float(input("Enter expense amount: "))
                        tracker.add_expense(username, category, description, amount)
                    elif user_choice == "2":
                        tracker.view_expenses(username)
                    elif user_choice == "3":
                        print(f"Total expenses: ${tracker.total_expenses(username)}")
                    elif user_choice == "4":
                        monthly_budget = float(input("Enter your monthly budget: "))
                        print(f"Remaining budget: ${tracker.remaining_budget(username, monthly_budget)}")
                    elif user_choice == "5":
                        tracker.save_users_data()
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == "3":
            tracker.save_users_data()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
