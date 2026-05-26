import json
from habit import Habit
from expense import Expense


class StorageManager:
    def __init__(self, filename="unilife_data.json"):
        self.filename = filename

    def save_data(self, habits, expenses, monthly_budget):
        data = {
            "monthly_budget": monthly_budget,
            "habits": [],
            "expenses": []
        }

        for habit in habits:
            data["habits"].append(habit.to_dictionary())

        for expense in expenses:
            data["expenses"].append(expense.to_dictionary())

        try:
            file = open(self.filename, "w")
            json.dump(data, file, indent=4)
        except OSError:
            print("The data file could not be saved.")
        finally:
            try:
                file.close()
            except UnboundLocalError:
                pass

    def load_data(self):
        habits = []
        expenses = []
        monthly_budget = 0.0

        try:
            file = open(self.filename, "r")
            data = json.load(file)

            monthly_budget = float(data.get("monthly_budget", 0.0))

            for habit_data in data.get("habits", []):
                habits.append(Habit.from_dictionary(habit_data))

            for expense_data in data.get("expenses", []):
                expenses.append(Expense.from_dictionary(expense_data))

        except FileNotFoundError:
            # First run: no saved file exists yet.
            pass
        except json.JSONDecodeError:
            print("The data file is not in the correct format.")
        finally:
            try:
                file.close()
            except UnboundLocalError:
                pass

        return habits, expenses, monthly_budget