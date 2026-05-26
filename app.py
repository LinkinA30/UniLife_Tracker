import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from habit import Habit
from expense import Expense
from dashboard import Dashboard
from storage import StorageManager


class UniLifeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UniLife Tracker")
        self.root.geometry("1050x720")
        self.root.minsize(950, 650)

        self.storage = StorageManager()
        self.habits, self.expenses, self.monthly_budget = self.storage.load_data()

        self.categories = ("Food", "Transport", "Rent", "Study", "Shopping", "Health", "Other")

        self.heading_font = ("Avenir Next", 30, "bold")
        self.subheading_font = ("Avenir Next", 18, "bold")
        self.normal_font = ("Avenir Next", 14)
        self.small_font = ("Avenir Next", 12)
        self.list_font = ("Menlo", 12)

        self.expense_chart_canvas = None
        self.habit_chart_canvas = None

        self.create_main_layout()

        self.refresh_habit_list()
        self.refresh_expense_list()
        self.update_dashboard()

    def create_main_layout(self):
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#0F172A")
        self.main_frame.pack(fill="both", expand=True)

        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#111827",
            corner_radius=0
        )
        self.header_frame.pack(fill="x")

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="UniLife Tracker",
            font=self.heading_font,
            text_color="#38BDF8"
        )
        self.title_label.pack(pady=(16, 3))

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Student Habit & Budget Manager",
            font=("Avenir Next", 14),
            text_color="#CBD5E1"
        )
        self.subtitle_label.pack(pady=(0, 14))

        self.tab_view = ctk.CTkTabview(
            self.main_frame,
            fg_color="#0F172A",
            segmented_button_fg_color="#1E293B",
            segmented_button_selected_color="#2563EB",
            segmented_button_selected_hover_color="#1D4ED8",
            segmented_button_unselected_color="#1E293B",
            segmented_button_unselected_hover_color="#334155",
            text_color="white",
            corner_radius=18
        )
        self.tab_view.pack(fill="both", expand=True, padx=25, pady=18)

        self.tab_view.add("Habits")
        self.tab_view.add("Budget")
        self.tab_view.add("Dashboard")

        self.habit_tab = self.tab_view.tab("Habits")
        self.budget_tab = self.tab_view.tab("Budget")
        self.dashboard_tab = self.tab_view.tab("Dashboard")

        self.create_habit_tab()
        self.create_budget_tab()
        self.create_dashboard_tab()

    def create_section_title(self, parent, title, subtitle):
        title_label = ctk.CTkLabel(
            parent,
            text=title,
            font=self.subheading_font,
            text_color="#F8FAFC"
        )
        title_label.pack(pady=(12, 3))

        subtitle_label = ctk.CTkLabel(
            parent,
            text=subtitle,
            font=self.small_font,
            text_color="#94A3B8"
        )
        subtitle_label.pack(pady=(0, 10))

    def create_habit_tab(self):
        self.create_section_title(
            self.habit_tab,
            "Habit Tracker",
            "Build better routines by tracking daily habits."
        )

        input_card = ctk.CTkFrame(
            self.habit_tab,
            fg_color="#111827",
            corner_radius=18
        )
        input_card.pack(fill="x", padx=30, pady=12)

        habit_label = ctk.CTkLabel(
            input_card,
            text="Habit Name",
            font=self.small_font,
            text_color="#CBD5E1"
        )
        habit_label.grid(row=0, column=0, padx=20, pady=(16, 4), sticky="w")

        self.habit_entry = ctk.CTkEntry(
            input_card,
            width=430,
            height=42,
            font=self.normal_font,
            placeholder_text="Example: Study Python, Exercise, Meal Prep",
            fg_color="#0F172A",
            border_color="#334155",
            text_color="white"
        )
        self.habit_entry.grid(row=1, column=0, padx=20, pady=(0, 18), sticky="w")

        add_button = ctk.CTkButton(
            input_card,
            text="Add Habit",
            width=150,
            height=42,
            font=("Avenir Next", 14, "bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.add_habit
        )
        add_button.grid(row=1, column=1, padx=20, pady=(0, 18))

        list_card = ctk.CTkFrame(
            self.habit_tab,
            fg_color="#111827",
            corner_radius=18
        )
        list_card.pack(fill="both", expand=True, padx=30, pady=12)

        list_title = ctk.CTkLabel(
            list_card,
            text="Your Habits",
            font=self.subheading_font,
            text_color="#F8FAFC"
        )
        list_title.pack(anchor="w", padx=20, pady=(16, 8))

        self.habit_listbox = tk.Listbox(
            list_card,
            height=10,
            font=self.list_font,
            bg="#020617",
            fg="#E5E7EB",
            selectbackground="#2563EB",
            selectforeground="white",
            highlightthickness=1,
            highlightbackground="#334155",
            relief="flat",
            borderwidth=0,
            activestyle="none"
        )
        self.habit_listbox.pack(fill="both", expand=True, padx=20, pady=8)

        complete_button = ctk.CTkButton(
            list_card,
            text="Mark Selected Habit Complete Today",
            height=42,
            font=("Avenir Next", 13, "bold"),
            fg_color="#14B8A6",
            hover_color="#0F766E",
            command=self.mark_habit_complete
        )
        complete_button.pack(pady=(10, 18))

    def create_budget_tab(self):
        self.create_section_title(
            self.budget_tab,
            "Budget Tracker",
            "Set a monthly budget and record your spending."
        )

        budget_card = ctk.CTkFrame(
            self.budget_tab,
            fg_color="#111827",
            corner_radius=18
        )
        budget_card.pack(fill="x", padx=30, pady=12)

        budget_label = ctk.CTkLabel(
            budget_card,
            text="Monthly Budget",
            font=self.small_font,
            text_color="#CBD5E1"
        )
        budget_label.grid(row=0, column=0, padx=20, pady=(16, 4), sticky="w")

        self.budget_entry = ctk.CTkEntry(
            budget_card,
            width=220,
            height=42,
            font=self.normal_font,
            fg_color="#0F172A",
            border_color="#334155",
            text_color="white"
        )
        self.budget_entry.grid(row=1, column=0, padx=20, pady=(0, 18), sticky="w")
        self.budget_entry.insert(0, str(self.monthly_budget))

        set_budget_button = ctk.CTkButton(
            budget_card,
            text="Set Budget",
            width=150,
            height=42,
            font=("Avenir Next", 14, "bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.set_budget
        )
        set_budget_button.grid(row=1, column=1, padx=20, pady=(0, 18))

        expense_card = ctk.CTkFrame(
            self.budget_tab,
            fg_color="#111827",
            corner_radius=18
        )
        expense_card.pack(fill="x", padx=30, pady=12)

        expense_title = ctk.CTkLabel(
            expense_card,
            text="Add New Expense",
            font=self.subheading_font,
            text_color="#F8FAFC"
        )
        expense_title.grid(row=0, column=0, columnspan=4, padx=20, pady=(16, 10), sticky="w")

        amount_label = ctk.CTkLabel(expense_card, text="Amount", font=self.small_font, text_color="#CBD5E1")
        amount_label.grid(row=1, column=0, padx=20, sticky="w")

        category_label = ctk.CTkLabel(expense_card, text="Category", font=self.small_font, text_color="#CBD5E1")
        category_label.grid(row=1, column=1, padx=20, sticky="w")

        description_label = ctk.CTkLabel(expense_card, text="Description", font=self.small_font, text_color="#CBD5E1")
        description_label.grid(row=1, column=2, padx=20, sticky="w")

        self.amount_entry = ctk.CTkEntry(
            expense_card,
            width=150,
            height=40,
            font=self.normal_font,
            placeholder_text="15.50",
            fg_color="#0F172A",
            border_color="#334155",
            text_color="white"
        )
        self.amount_entry.grid(row=2, column=0, padx=20, pady=(5, 18), sticky="w")

        self.category_box = ctk.CTkComboBox(
            expense_card,
            values=list(self.categories),
            width=170,
            height=40,
            font=self.small_font,
            fg_color="#0F172A",
            border_color="#334155",
            button_color="#2563EB",
            button_hover_color="#1D4ED8",
            dropdown_fg_color="#111827",
            dropdown_hover_color="#1E293B",
            text_color="white"
        )
        self.category_box.grid(row=2, column=1, padx=20, pady=(5, 18), sticky="w")
        self.category_box.set("Food")

        self.description_entry = ctk.CTkEntry(
            expense_card,
            width=330,
            height=40,
            font=self.normal_font,
            placeholder_text="Example: Lunch, train fare, textbook",
            fg_color="#0F172A",
            border_color="#334155",
            text_color="white"
        )
        self.description_entry.grid(row=2, column=2, padx=20, pady=(5, 18), sticky="w")

        add_expense_button = ctk.CTkButton(
            expense_card,
            text="Add Expense",
            width=140,
            height=40,
            font=("Avenir Next", 13, "bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.add_expense
        )
        add_expense_button.grid(row=2, column=3, padx=20, pady=(5, 18))

        list_card = ctk.CTkFrame(
            self.budget_tab,
            fg_color="#111827",
            corner_radius=18
        )
        list_card.pack(fill="both", expand=True, padx=30, pady=12)

        list_title = ctk.CTkLabel(
            list_card,
            text="Expense History",
            font=self.subheading_font,
            text_color="#F8FAFC"
        )
        list_title.pack(anchor="w", padx=20, pady=(16, 8))

        self.expense_listbox = tk.Listbox(
            list_card,
            height=8,
            font=self.list_font,
            bg="#020617",
            fg="#E5E7EB",
            selectbackground="#2563EB",
            selectforeground="white",
            highlightthickness=1,
            highlightbackground="#334155",
            relief="flat",
            borderwidth=0,
            activestyle="none"
        )
        self.expense_listbox.pack(fill="both", expand=True, padx=20, pady=(5, 18))

    def create_dashboard_tab(self):
        dashboard_scroll = ctk.CTkScrollableFrame(
            self.dashboard_tab,
            fg_color="#0F172A"
        )
        dashboard_scroll.pack(fill="both", expand=True)

        self.dashboard_content = dashboard_scroll

        self.create_section_title(
            self.dashboard_content,
            "Summary Dashboard",
            "Visual summary of your habits and student spending."
        )

        self.summary_frame = ctk.CTkFrame(
            self.dashboard_content,
            fg_color="#0F172A"
        )
        self.summary_frame.pack(fill="x", padx=30, pady=(0, 5))

        self.habits_value_label = self.create_summary_card(
            self.summary_frame,
            "Habit Completions",
            "0",
            0,
            "#2563EB"
        )

        self.spending_value_label = self.create_summary_card(
            self.summary_frame,
            "Total Spending",
            "$0.00",
            1,
            "#7C3AED"
        )

        self.budget_value_label = self.create_summary_card(
            self.summary_frame,
            "Remaining Budget",
            "$0.00",
            2,
            "#14B8A6"
        )

        budget_progress_card = ctk.CTkFrame(
            self.dashboard_content,
            fg_color="#111827",
            corner_radius=16,
            border_width=1,
            border_color="#1E293B"
        )
        budget_progress_card.pack(fill="x", padx=40, pady=(4, 8))

        self.budget_progress_label = ctk.CTkLabel(
            budget_progress_card,
            text="Budget Used: 0%",
            font=("Avenir Next", 12, "bold"),
            text_color="#CBD5E1"
        )
        self.budget_progress_label.pack(anchor="w", padx=18, pady=(9, 4))

        self.budget_progress_bar = ctk.CTkProgressBar(
            budget_progress_card,
            height=12,
            progress_color="#38BDF8",
            fg_color="#020617"
        )
        self.budget_progress_bar.pack(fill="x", padx=18, pady=(0, 11))
        self.budget_progress_bar.set(0)

        charts_frame = ctk.CTkFrame(
            self.dashboard_content,
            fg_color="#0F172A"
        )
        charts_frame.pack(fill="x", padx=30, pady=(4, 8))

        charts_frame.columnconfigure(0, weight=1)
        charts_frame.columnconfigure(1, weight=1)

        self.expense_chart_frame = ctk.CTkFrame(
            charts_frame,
            fg_color="#111827",
            corner_radius=18,
            border_width=1,
            border_color="#1E293B",
            height=260
        )
        self.expense_chart_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.expense_chart_frame.grid_propagate(False)

        self.habit_chart_frame = ctk.CTkFrame(
            charts_frame,
            fg_color="#111827",
            corner_radius=18,
            border_width=1,
            border_color="#1E293B",
            height=260
        )
        self.habit_chart_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.habit_chart_frame.grid_propagate(False)

        expense_chart_title = ctk.CTkLabel(
            self.expense_chart_frame,
            text="Spending by Category",
            font=("Avenir Next", 15, "bold"),
            text_color="#F8FAFC"
        )
        expense_chart_title.pack(pady=(10, 0))

        habit_chart_title = ctk.CTkLabel(
            self.habit_chart_frame,
            text="Habit Completion Chart",
            font=("Avenir Next", 15, "bold"),
            text_color="#F8FAFC"
        )
        habit_chart_title.pack(pady=(10, 0))

        button_frame = ctk.CTkFrame(
            self.dashboard_content,
            fg_color="#0F172A"
        )
        button_frame.pack(pady=(8, 18))

        refresh_button = ctk.CTkButton(
            button_frame,
            text="Refresh Dashboard",
            width=180,
            height=40,
            font=("Avenir Next", 13, "bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.update_dashboard
        )
        refresh_button.grid(row=0, column=0, padx=10)

        reset_button = ctk.CTkButton(
            button_frame,
            text="Reset Tracker",
            width=160,
            height=40,
            font=("Avenir Next", 13, "bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.reset_tracker
        )
        reset_button.grid(row=0, column=1, padx=10)

    def create_summary_card(self, parent, title, value, column, color):
        card = ctk.CTkFrame(
            parent,
            fg_color="#111827",
            corner_radius=16,
            border_width=1,
            border_color="#1E293B",
            height=80
        )
        card.grid(row=0, column=column, padx=10, pady=6, sticky="nsew")
        card.grid_propagate(False)

        parent.columnconfigure(column, weight=1)

        accent = ctk.CTkFrame(
            card,
            width=5,
            fg_color=color,
            corner_radius=8
        )
        accent.pack(side="left", fill="y", padx=(0, 8), pady=12)

        text_frame = ctk.CTkFrame(card, fg_color="#111827")
        text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=9)

        title_label = ctk.CTkLabel(
            text_frame,
            text=title,
            font=("Avenir Next", 11),
            text_color="#94A3B8"
        )
        title_label.pack(anchor="w")

        value_label = ctk.CTkLabel(
            text_frame,
            text=value,
            font=("Avenir Next", 20, "bold"),
            text_color="#F8FAFC"
        )
        value_label.pack(anchor="w", pady=(1, 0))

        return value_label

    def draw_expense_pie_chart(self, dashboard):
        if self.expense_chart_canvas is not None:
            self.expense_chart_canvas.get_tk_widget().destroy()

        category_totals = dashboard.get_category_totals()

        figure = Figure(figsize=(4.0, 2.2), dpi=100)
        figure.patch.set_facecolor("#111827")

        plot = figure.add_subplot(111)
        plot.set_facecolor("#111827")

        if len(category_totals) == 0:
            plot.text(
                0.5,
                0.5,
                "No expense data yet",
                ha="center",
                va="center",
                color="#CBD5E1",
                fontsize=12
            )
            plot.axis("off")
        else:
            labels = list(category_totals.keys())
            values = list(category_totals.values())
            colors = ["#38BDF8", "#7C3AED", "#14B8A6", "#F97316", "#EF4444", "#EAB308", "#64748B"]

            plot.pie(
                values,
                labels=labels,
                autopct="%1.0f%%",
                startangle=90,
                colors=colors[:len(values)],
                textprops={"color": "#E5E7EB", "fontsize": 8}
            )
            plot.axis("equal")

        figure.tight_layout()

        self.expense_chart_canvas = FigureCanvasTkAgg(figure, self.expense_chart_frame)
        self.expense_chart_canvas.draw()
        self.expense_chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=5)

    def draw_habit_bar_chart(self, dashboard):
        if self.habit_chart_canvas is not None:
            self.habit_chart_canvas.get_tk_widget().destroy()

        progress_grid = dashboard.get_habit_progress_grid()

        figure = Figure(figsize=(4.0, 2.2), dpi=100)
        figure.patch.set_facecolor("#111827")

        plot = figure.add_subplot(111)
        plot.set_facecolor("#111827")

        if len(progress_grid) == 0:
            plot.text(
                0.5,
                0.5,
                "No habit data yet",
                ha="center",
                va="center",
                color="#CBD5E1",
                fontsize=12
            )
            plot.axis("off")
        else:
            habit_names = []
            counts = []

            for row in progress_grid:
                habit_names.append(row[0])
                counts.append(row[1])

            plot.bar(habit_names, counts, color="#38BDF8")
            plot.tick_params(axis="x", colors="#CBD5E1", labelrotation=20, labelsize=8)
            plot.tick_params(axis="y", colors="#CBD5E1", labelsize=8)
            plot.spines["bottom"].set_color("#334155")
            plot.spines["left"].set_color("#334155")
            plot.spines["top"].set_visible(False)
            plot.spines["right"].set_visible(False)
            plot.set_ylabel("Completions", color="#CBD5E1", fontsize=9)

        figure.tight_layout()

        self.habit_chart_canvas = FigureCanvasTkAgg(figure, self.habit_chart_frame)
        self.habit_chart_canvas.draw()
        self.habit_chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=5)

    def add_habit(self):
        habit_name = self.habit_entry.get().strip().title()

        if habit_name == "":
            messagebox.showerror("Input Error", "Please enter a habit name.")
            return

        for habit in self.habits:
            if habit.name.lower() == habit_name.lower():
                messagebox.showerror("Input Error", "This habit already exists.")
                return

        new_habit = Habit(habit_name)
        self.habits.append(new_habit)

        self.habit_entry.delete(0, tk.END)
        self.refresh_habit_list()
        self.save_and_refresh()

    def mark_habit_complete(self):
        selected_index = self.habit_listbox.curselection()

        if len(selected_index) == 0:
            messagebox.showerror("Selection Error", "Please select a habit first.")
            return

        index = selected_index[0]
        selected_habit = self.habits[index]
        was_marked = selected_habit.mark_complete()

        if was_marked:
            messagebox.showinfo("Success", "Habit marked as complete for today.")
        else:
            messagebox.showinfo("Already Completed", "This habit was already completed today.")

        self.refresh_habit_list()
        self.save_and_refresh()

    def set_budget(self):
        try:
            budget = float(self.budget_entry.get())

            if budget <= 0:
                messagebox.showerror("Input Error", "Budget must be greater than 0.")
                return

            self.monthly_budget = budget
            messagebox.showinfo("Success", "Monthly budget has been set.")
            self.save_and_refresh()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for budget.")

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_box.get().strip()
            description = self.description_entry.get().strip()

            if amount <= 0:
                messagebox.showerror("Input Error", "Expense amount must be greater than 0.")
                return

            if category == "":
                messagebox.showerror("Input Error", "Please select or enter an expense category.")
                return

            if description == "":
                description = "No description"

            new_expense = Expense(amount, category, description)
            self.expenses.append(new_expense)

            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)

            self.refresh_expense_list()
            self.save_and_refresh()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for amount.")

    def refresh_habit_list(self):
        self.habit_listbox.delete(0, tk.END)

        for habit in self.habits:
            self.habit_listbox.insert(tk.END, "  " + habit.get_details())

    def refresh_expense_list(self):
        self.expense_listbox.delete(0, tk.END)

        for expense in self.expenses:
            self.expense_listbox.insert(tk.END, "  " + expense.get_details())

    def save_and_refresh(self):
        self.storage.save_data(self.habits, self.expenses, self.monthly_budget)
        self.update_dashboard()

    def reset_tracker(self):
        answer = messagebox.askyesno(
            "Reset Tracker",
            "Are you sure you want to delete all habits, expenses, and budget data?"
        )

        if answer == False:
            return

        self.habits = []
        self.expenses = []
        self.monthly_budget = 0.0

        self.budget_entry.delete(0, tk.END)
        self.budget_entry.insert(0, "0.0")

        self.refresh_habit_list()
        self.refresh_expense_list()

        self.storage.save_data(self.habits, self.expenses, self.monthly_budget)
        self.update_dashboard()

        messagebox.showinfo("Reset Complete", "All tracker data has been reset.")

    def update_dashboard(self):
        dashboard = Dashboard(self.habits, self.expenses, self.monthly_budget)

        total_completions = dashboard.get_total_completions()
        total_spending = dashboard.get_total_spending()
        remaining_budget = dashboard.get_remaining_budget()

        self.habits_value_label.configure(text=str(total_completions))
        self.spending_value_label.configure(text=f"${total_spending:.2f}")
        self.budget_value_label.configure(text=f"${remaining_budget:.2f}")

        if self.monthly_budget > 0:
            budget_used = total_spending / self.monthly_budget
        else:
            budget_used = 0

        if budget_used > 1:
            budget_used = 1

        self.budget_progress_bar.set(budget_used)

        actual_budget_percent = 0
        if self.monthly_budget > 0:
            actual_budget_percent = (total_spending / self.monthly_budget) * 100

        self.budget_progress_label.configure(
            text=f"Budget Used: {actual_budget_percent:.1f}%"
        )

        self.draw_expense_pie_chart(dashboard)
        self.draw_habit_bar_chart(dashboard)