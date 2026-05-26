UniLife Tracker - Student Habit & Budget Manager

This project is a Python GUI application that helps students track daily habits, manage expenses, set a monthly budget, and view a visual dashboard with charts.

How to Run:
Run only the main.py file.

Command:
python3 main.py

or

python main.py


Extra Libraries Required:
This project uses a few extra libraries for the graphical interface and charts.

Install them using:

pip install tkinter
pip install customtkinter
pip install matplotlib


Files Included:

main.py
- Starts the application.
- Shows the splash screen.
- Opens the main UniLife Tracker window.

app.py
- Contains the main GUI code.
- Creates the Habits, Budget, and Dashboard tabs.
- Handles button actions, input fields, lists, charts, and screen updates.

habit.py
- Contains the Habit class.
- Stores habit name and completed dates.
- Handles marking a habit as complete.

expense.py
- Contains the Expense class.
- Stores expense amount, category, description, and date.

dashboard.py
- Contains the Dashboard class.
- Calculates total habits, total completions, total spending, remaining budget, highest spending category, and chart data.

storage.py
- Handles file input/output.
- Saves and loads user data using the unilife_data.json file.

tests.py
- Contains simple assert-based tests.
- Tests habit completion, expense totals, and dashboard calculations.

unilife_data.json
- Automatically created when the program runs.
- Stores saved habits, expenses, and monthly budget.
- This file allows the application to remember data after closing and reopening.


Important:
To run the project, only run main.py. Do not run the other files directly unless you are testing individual parts of the program.