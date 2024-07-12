import datetime
import json
from decimal import Decimal
from collections import deque

class BudgetTracker:
    def __init__(self):
        self.categories = {}
        self.transactions = []
        self.budget_type = None
        self.budget_goals = {}
        self.base_currency = "USD"
        self.exchange_rates = {"USD": 1.0, "EUR": 0.85, "GBP": 0.73, "JPY": 110.0}  # Example rates
        self.undo_stack = deque(maxlen=10)
        self.redo_stack = deque(maxlen=10)

    def add_category(self, category_name):
        if category_name not in self.categories:
            self.categories[category_name] = Decimal('0.0')

    def add_income(self, category_name, amount, currency="USD", date=None):
        self.save_state()
        self.add_category(category_name)
        converted_amount = self.convert_currency(amount, currency, self.base_currency)
        self.categories[category_name] += converted_amount
        if date is None:
            date = datetime.datetime.now()
        self.transactions.append((date, category_name, 'Add', converted_amount, currency))
        self.check_budget_goal(category_name)

    def deduct_expense(self, category_name, amount, currency="USD", date=None):
        self.save_state()
        self.add_category(category_name)
        converted_amount = self.convert_currency(amount, currency, self.base_currency)
        self.categories[category_name] -= converted_amount
        if date is None:
            date = datetime.datetime.now()
        self.transactions.append((date, category_name, 'Deduct', converted_amount, currency))
        self.check_budget_goal(category_name)

    def move_money(self, from_category, to_category, amount, currency="USD", date=None):
        self.save_state()
        converted_amount = self.convert_currency(amount, currency, self.base_currency)
        if from_category not in self.categories or self.categories[from_category] < converted_amount:
            print(f"Insufficient funds in {from_category}")
            return
        if date is None:
            date = datetime.datetime.now()
        self.deduct_expense(from_category, converted_amount, self.base_currency, date)
        self.add_income(to_category, converted_amount, self.base_currency, date)

    def view_summary(self, start_date=None, end_date=None):
        print("\nBudget Summary:")
        total_balance = Decimal('0.0')
        for category, amount in self.categories.items():
            category_balance = self.calculate_balance(category, start_date, end_date)
            print(f"Category: {category}, Balance: {self.format_currency(category_balance, self.base_currency)}")
            total_balance += category_balance
        print(f"\nTotal Balance: {self.format_currency(total_balance, self.base_currency)}")

    def view_details(self, start_date=None, end_date=None):
        print("\nDetailed Budget:")
        filtered_transactions = self.filter_transactions(start_date, end_date)
        for transaction in filtered_transactions:
            date, category, trans_type, amount, currency = transaction
            print(f"Date: {date}, Category: {category}, Type: {trans_type}, "
                  f"Amount: {self.format_currency(amount, currency)}")

    def filter_transactions(self, start_date=None, end_date=None):
        if start_date is None and end_date is None:
            return self.transactions
        return [t for t in self.transactions if self.is_within_date_range(t[0], start_date, end_date)]

    def is_within_date_range(self, date, start_date, end_date):
        if start_date and date < start_date:
            return False
        if end_date and date > end_date:
            return False
        return True

    def calculate_balance(self, category, start_date=None, end_date=None):
        balance = Decimal('0.0')
        for transaction in self.filter_transactions(start_date, end_date):
            if transaction[1] == category:
                if transaction[2] == 'Add':
                    balance += transaction[3]
                else:
                    balance -= transaction[3]
        return balance

    def setup_budget(self):
        print("Choose Budget Type:")
        print("1. Real Budget")
        print("2. Projected Budget")
        budget_choice = input("Enter your choice (1 or 2): ")

        if budget_choice == '1':
            self.budget_type = "Real"
            self.handle_real_budget()
        elif budget_choice == '2':
            self.budget_type = "Projected"
            self.handle_projected_budget()
        else:
            print("Invalid choice, please try again.")
            self.setup_budget()

    def handle_real_budget(self):
        print("Setting up Real Budget")
        self.collect_income()

    def handle_projected_budget(self):
        print("Setting up Projected Budget")
        self.collect_income()

    def collect_income(self):
        print("\nPlease enter your income details:")
        categories = [
            "Salary/Wages", "Full time work", "Bonuses", "Commissions", "Tips", "Part time work",
            "Freelance/Side Gigs", "Passive money", "Investment income", "Rental Income", "Commercial Income",
            "Government Benefits", "Gifts/Inheritance", "Miscellaneous Income"
        ]

        for category in categories:
            while True:
                amount_str = input(f"Enter amount for {category} (or press Enter to skip): ")
                if amount_str == "":
                    break
                try:
                    amount = Decimal(amount_str.replace(',', ''))
                    currency = self.get_currency()
                    date = self.get_date()
                    self.add_income(category, amount, currency, date)
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

    def run(self):
        self.load_from_file()
        if not self.budget_type:
            self.setup_budget()
        
        while True:
            print("\nWhat would you like to do?")
            print("1. Add Income")
            print("2. Deduct Expense")
            print("3. Move Money")
            print("4. View Summary")
            print("5. View Details")
            print("6. Set Budget Goal")
            print("7. Change Base Currency")
            print("8. Filter by Date Range")
            print("9. Undo")
            print("10. Redo")
            print("11. Save and Exit")

            choice = input("Enter your choice (1-11): ")

            if choice == '1':
                category = input("Enter the category for income: ")
                amount = self.get_valid_amount("Enter the amount: ")
                currency = self.get_currency()
                date = self.get_date()
                self.add_income(category, amount, currency, date)
            elif choice == '2':
                category = input("Enter the category for expense: ")
                amount = self.get_valid_amount("Enter the amount: ")
                currency = self.get_currency()
                date = self.get_date()
                self.deduct_expense(category, amount, currency, date)
            elif choice == '3':
                from_category = input("Enter the category to move money from: ")
                to_category = input("Enter the category to move money to: ")
                amount = self.get_valid_amount("Enter the amount: ")
                currency = self.get_currency()
                date = self.get_date()
                self.move_money(from_category, to_category, amount, currency, date)
            elif choice == '4':
                start_date, end_date = self.get_date_range()
                self.view_summary(start_date, end_date)
            elif choice == '5':
                start_date, end_date = self.get_date_range()
                self.view_details(start_date, end_date)
            elif choice == '6':
                self.set_budget_goal()
            elif choice == '7':
                self.change_base_currency()
            elif choice == '8':
                self.filter_by_date_range()
            elif choice == '9':
                self.undo()
            elif choice == '10':
                self.redo()
            elif choice == '11':
                self.save_to_file()
                print("Budget saved. Thank you for using the Budget Tracker. Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")

    def get_valid_amount(self, prompt):
        while True:
            amount_str = input(prompt)
            try:
                return Decimal(amount_str.replace(',', ''))
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def get_currency(self):
        while True:
            currency = input(f"Enter currency ({', '.join(self.exchange_rates.keys())}): ").upper()
            if currency in self.exchange_rates:
                return currency
            print("Invalid currency. Please try again.")

    def get_date(self):
        while True:
            date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
            if date_str == "":
                return datetime.datetime.now()
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    def get_date_range(self):
        print("Enter date range (leave blank for no limit)")
        start_date = self.get_date_or_none("Start date: ")
        end_date = self.get_date_or_none("End date: ")
        return start_date, end_date

    def get_date_or_none(self, prompt):
        date_str = input(prompt)
        if date_str == "":
            return None
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return self.get_date_or_none(prompt)

    def filter_by_date_range(self):
        start_date, end_date = self.get_date_range()
        self.view_summary(start_date, end_date)
        self.view_details(start_date, end_date)

    def convert_currency(self, amount, from_currency, to_currency):
        if from_currency == to_currency:
            return amount
        return amount * (self.exchange_rates[to_currency] / self.exchange_rates[from_currency])

    def format_currency(self, amount, currency):
        return f"{currency} {amount:.2f}"

    def set_budget_goal(self):
        category = input("Enter the category for the budget goal: ")
        goal_amount = self.get_valid_amount("Enter the goal amount: ")
        currency = self.get_currency()
        converted_goal = self.convert_currency(goal_amount, currency, self.base_currency)
        self.budget_goals[category] = converted_goal
        print(f"Budget goal set for {category}: {self.format_currency(converted_goal, self.base_currency)}")

    def check_budget_goal(self, category):
        if category in self.budget_goals:
            current_amount = self.categories[category]
            goal_amount = self.budget_goals[category]
            if current_amount > goal_amount:
                print(f"Alert: Budget goal exceeded for {category}!")
                print(f"Current: {self.format_currency(current_amount, self.base_currency)}")
                print(f"Goal: {self.format_currency(goal_amount, self.base_currency)}")

    def change_base_currency(self):
        print(f"Current base currency: {self.base_currency}")
        new_base = self.get_currency()
        if new_base != self.base_currency:
            # Convert all category balances to the new base currency
            for category in self.categories:
                self.categories[category] = self.convert_currency(self.categories[category], 
                                                                  self.base_currency, new_base)
            # Convert all budget goals to the new base currency
            for category in self.budget_goals:
                self.budget_goals[category] = self.convert_currency(self.budget_goals[category], 
                                                                    self.base_currency, new_base)
            self.base_currency = new_base
            print(f"Base currency changed to {self.base_currency}")

    def save_to_file(self, filename='budget_data.json'):
        data = {
            'categories': {k: str(v) for k, v in self.categories.items()},
            'transactions': self.transactions,
            'budget_type': self.budget_type,
            'budget_goals': {k: str(v) for k, v in self.budget_goals.items()},
            'base_currency': self.base_currency
        }
        with open(filename, 'w') as f:
            json.dump(data, f, default=str)
        print(f"Budget data saved to {filename}")

    def load_from_file(self, filename='budget_data.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.categories = {k: Decimal(v) for k, v in data['categories'].items()}
            self.transactions = [tuple(t) for t in data['transactions']]
            self.budget_type = data['budget_type']
            self.budget_goals = {k: Decimal(v) for k, v in data['budget_goals'].items()}
            self.base_currency = data['base_currency']
            print(f"Budget data loaded from {filename}")
        except FileNotFoundError:
            print("No saved budget data found.")

    def save_state(self):
        state = {
            'categories': self.categories.copy(),
            'transactions': self.transactions.copy(),
            'budget_goals': self.budget_goals.copy()
        }
        self.undo_stack.append(state)
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            print("Nothing to undo.")
            return
        current_state = {
            'categories': self.categories.copy(),
            'transactions': self.transactions.copy(),
            'budget_goals': self.budget_goals.copy()
        }
        self.redo_stack.append(current_state)
        previous_state = self.undo_stack.pop()
        self.categories = previous_state['categories']
        self.transactions = previous_state['transactions']
        self.budget_goals = previous_state['budget_goals']
        print("Undo successful.")

    def redo(self):
        if not self.redo_stack:
            print("Nothing to redo.")
            return
        current_state = {
            'categories': self.categories.copy(),
            'transactions': self.transactions.copy(),
            'budget_goals': self.budget_goals.copy()
        }
        self.undo_stack.append(current_state)
        next_state = self.redo_stack.pop()
        self.categories = next_state['categories']
        self.transactions = next_state['transactions']
        self.budget_goals = next_state['budget_goals']
        print("Redo successful.")

if __name__ == "__main__":
    budget_tracker = BudgetTracker()
    budget_tracker.run()