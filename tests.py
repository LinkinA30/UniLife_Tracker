from habit import Habit
from expense import Expense
from dashboard import Dashboard


def test_habit_completion():
    habit = Habit("Study")
    result = habit.mark_complete()

    assert result == True
    assert habit.get_completed_count() == 1


def test_expense_total():
    expenses = [
        Expense(10.0, "Food", "Lunch"),
        Expense(5.5, "Transport", "Train")
    ]

    dashboard = Dashboard([], expenses, 100.0)
    assert dashboard.get_total_spending() == 15.5
    assert dashboard.get_remaining_budget() == 84.5


def test_highest_category():
    expenses = [
        Expense(10.0, "Food", "Lunch"),
        Expense(20.0, "Food", "Dinner"),
        Expense(5.0, "Transport", "Bus")
    ]

    dashboard = Dashboard([], expenses, 100.0)
    assert dashboard.get_highest_category() == "Food"


def run_tests():
    tests = [test_habit_completion, test_expense_total, test_highest_category]

    for test in tests:
        test()
        print(test.__name__, "passed")

    print("All tests passed.")


if __name__ == "__main__":
    run_tests()