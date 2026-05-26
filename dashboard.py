class Dashboard:
    def __init__(self, habits, expenses, monthly_budget):
        self.habits = habits
        self.expenses = expenses
        self.monthly_budget = monthly_budget

    def get_total_habits(self):
        return len(self.habits)

    def get_total_completions(self):
        total = 0

        for habit in self.habits:
            total += habit.get_completed_count()

        return total

    def recursive_total_spending(self, expenses):
        # Small recursion example: total amount from a list of expenses.
        if len(expenses) == 0:
            return 0

        return expenses[0].amount + self.recursive_total_spending(expenses[1:])

    def get_total_spending(self):
        return self.recursive_total_spending(self.expenses)

    def get_remaining_budget(self):
        return self.monthly_budget - self.get_total_spending()

    def get_category_totals(self):
        category_totals = {}

        for expense in self.expenses:
            if expense.category in category_totals:
                category_totals[expense.category] += expense.amount
            else:
                category_totals[expense.category] = expense.amount

        return category_totals

    def get_highest_category(self):
        category_totals = self.get_category_totals()

        if len(category_totals) == 0:
            return "None"

        return max(category_totals, key=category_totals.get)

    def get_best_habit(self):
        if len(self.habits) == 0:
            return "None"

        best_habit = max(self.habits, key=lambda habit: habit.get_completed_count())
        return best_habit.name

    def get_habit_progress_grid(self):
        # This is a simple 2D list: each row has habit name and completion count.
        progress_grid = []

        for habit in self.habits:
            row = [habit.name, habit.get_completed_count()]
            progress_grid.append(row)

        return progress_grid

    def get_feedback(self):
        feedback = []
        total_habits = self.get_total_habits()
        total_completions = self.get_total_completions()
        total_spending = self.get_total_spending()

        if total_habits == 0:
            feedback.append("Add some habits to start tracking your routine.")
        elif total_completions == 0:
            feedback.append("You have added habits. Try marking one as complete.")
        else:
            feedback.append("Good work! You are making progress with your habits.")

        if self.monthly_budget == 0:
            feedback.append("Set a monthly budget to track your spending.")
        elif total_spending > self.monthly_budget:
            feedback.append("Warning: You have gone over your monthly budget.")
        elif total_spending > self.monthly_budget * 0.8:
            feedback.append("Careful: You have used more than 80% of your budget.")
        else:
            feedback.append("Your spending is currently within budget.")

        return feedback