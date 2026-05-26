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
        self.root.geometry("1100x760")
        self.root.minsize(1000, 700)

        self.storage = StorageManager()
        self.habits, self.expenses, self.monthly_budget = self.storage.load_data()

        self.categories = ("Food", "Transport", "Rent", "Study", "Shopping", "Health", "Other")

        self.heading_font = ("Avenir Next", 30, "bold")
        self.subheading_font = ("Avenir Next", 18, "bold")
        self.normal_font = ("Avenir Next", 14)
        self.small_font = ("Avenir Next", 12)
        self.list_font = ("Menlo", 12)

        self.budget_chart_canvas = None
        self.spending_chart_canvas = None

        self.create_main_layout()

        self.refresh_habit_list()
        self.refresh_expense_list()
        self.update_dashboard()

    def create_main_layout(self):
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#061225")
        self.main_frame.pack(fill="both", expand=True)

        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#081528",
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
            fg_color="#061225",
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
            fg_color="#0F1B2E",
            corner_radius=18,
            border_width=1,
            border_color="#1E3A5F"
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
            placeholder_text="Example: Study Python, Exercise, Drink Water",
            fg_color="#061225",
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
            fg_color="#0F1B2E",
            corner_radius=18,
            border_width=1,
            border_color="#1E3A5F"
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
            fg_color="#0F1B2E",
            corner_radius=18,
            border_width=1,
            border_color="#1E3A5F"
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
            fg_color="#061225",
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
            fg_color="#0F1B2E",
            corner_radius=18,
            border_width=1,
            border_color="#1E3A5F"
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
            fg_color="#061225",
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
            fg_color="#061225",
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
            fg_color="#061225",
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
            fg_color="#0F1B2E",
            corner_radius=18,
            border_width=1,
            border_color="#1E3A5F"
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
            fg_color="#061225"
        )
        dashboard_scroll.pack(fill="both", expand=True)

        self.create_section_title(
            dashboard_scroll,
            "Summary Dashboard",
            "Track habits, spending, saving and weekly progress."
        )

        board = ctk.CTkFrame(
            dashboard_scroll,
            fg_color="#071A33",
            corner_radius=24,
            border_width=2,
            border_color="#38BDF8"
        )
        board.pack(fill="both", expand=True, padx=28, pady=12)

        board.grid_columnconfigure(0, weight=1)
        board.grid_columnconfigure(1, weight=1)
        board.grid_rowconfigure(0, weight=1)
        board.grid_rowconfigure(1, weight=1)

        self.habit_panel = self.create_dashboard_panel(board, "🎯  HABIT TRACKER", 0, 0)
        self.budget_panel = self.create_dashboard_panel(board, "💳  BUDGET OVERVIEW", 0, 1)
        self.weekly_panel = self.create_dashboard_panel(board, "📈  WEEKLY PROGRESS", 1, 0)
        self.spending_panel = self.create_dashboard_panel(board, "🧾  SPENDING BREAKDOWN", 1, 1)

        self.habit_rows_frame = ctk.CTkFrame(self.habit_panel, fg_color="#081528")
        self.habit_rows_frame.pack(fill="both", expand=True, padx=12, pady=(4, 12))

        self.budget_info_frame = ctk.CTkFrame(self.budget_panel, fg_color="#081528")
        self.budget_info_frame.pack(fill="x", padx=12, pady=(4, 0))

        self.budget_chart_frame = ctk.CTkFrame(self.budget_panel, fg_color="#081528")
        self.budget_chart_frame.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        self.weekly_message_label = ctk.CTkLabel(
            self.weekly_panel,
            text="You're doing great! Keep it up! 🚀",
            font=("Avenir Next", 13, "bold"),
            text_color="#F8FAFC"
        )
        self.weekly_message_label.pack(anchor="w", padx=16, pady=(8, 4))

        self.weekly_progress_bar = ctk.CTkProgressBar(
            self.weekly_panel,
            height=14,
            progress_color="#22C55E",
            fg_color="#020617"
        )
        self.weekly_progress_bar.pack(fill="x", padx=16, pady=(4, 4))

        self.weekly_percent_label = ctk.CTkLabel(
            self.weekly_panel,
            text="0%",
            font=("Avenir Next", 13, "bold"),
            text_color="#F8FAFC"
        )
        self.weekly_percent_label.pack(anchor="e", padx=16)

        self.weekly_stats_frame = ctk.CTkFrame(self.weekly_panel, fg_color="#081528")
        self.weekly_stats_frame.pack(fill="x", padx=12, pady=10)

        self.streak_label = self.create_small_stat_card(self.weekly_stats_frame, "🔥", "0", "Day Streak", 0)
        self.goals_label = self.create_small_stat_card(self.weekly_stats_frame, "🏆", "0", "Goals Hit", 1)
        self.points_label = self.create_small_stat_card(self.weekly_stats_frame, "⭐", "0", "Points", 2)

        self.spending_chart_frame = ctk.CTkFrame(self.spending_panel, fg_color="#081528")
        self.spending_chart_frame.pack(side="left", fill="both", expand=True, padx=(12, 6), pady=8)

        self.spending_legend_frame = ctk.CTkFrame(self.spending_panel, fg_color="#081528")
        self.spending_legend_frame.pack(side="right", fill="both", expand=True, padx=(6, 12), pady=8)

        button_frame = ctk.CTkFrame(
            dashboard_scroll,
            fg_color="#061225"
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

    def create_dashboard_panel(self, parent, title, row, column):
        panel = ctk.CTkFrame(
            parent,
            fg_color="#081528",
            corner_radius=18,
            border_width=1,
            border_color="#1E3A5F"
        )
        panel.grid(row=row, column=column, padx=12, pady=12, sticky="nsew")

        title_label = ctk.CTkLabel(
            panel,
            text=title,
            font=("Avenir Next", 16, "bold"),
            text_color="#F8FAFC"
        )
        title_label.pack(anchor="w", padx=16, pady=(12, 8))

        line = ctk.CTkFrame(panel, height=1, fg_color="#1E3A5F")
        line.pack(fill="x", padx=12, pady=(0, 4))

        return panel

    def create_small_stat_card(self, parent, icon, value, title, column):
        parent.grid_columnconfigure(column, weight=1)

        card = ctk.CTkFrame(
            parent,
            fg_color="#0F1B2E",
            corner_radius=12,
            border_width=1,
            border_color="#1E3A5F"
        )
        card.grid(row=0, column=column, padx=6, pady=4, sticky="nsew")

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=("Avenir Next", 18),
            text_color="#F8FAFC"
        )
        icon_label.pack(side="left", padx=(10, 6), pady=8)

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Avenir Next", 18, "bold"),
            text_color="#F8FAFC"
        )
        value_label.pack(anchor="w", pady=(5, 0))

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Avenir Next", 9),
            text_color="#CBD5E1"
        )
        title_label.pack(anchor="w", pady=(0, 6))

        return value_label

    def update_habit_panel(self, dashboard):
        for widget in self.habit_rows_frame.winfo_children():
            widget.destroy()

        if len(self.habits) == 0:
            empty_label = ctk.CTkLabel(
                self.habit_rows_frame,
                text="No habits yet. Add Study, Exercise or Drink Water to begin.",
                font=("Avenir Next", 13),
                text_color="#CBD5E1"
            )
            empty_label.pack(pady=35)
            return

        icons = ["📘", "🏃", "💧", "🧘", "🍳", "🚲"]

        for index, habit in enumerate(self.habits[:4]):
            row_frame = ctk.CTkFrame(
                self.habit_rows_frame,
                fg_color="#081528"
            )
            row_frame.pack(fill="x", pady=4)

            icon = icons[index % len(icons)]

            name_label = ctk.CTkLabel(
                row_frame,
                text=f"{icon}  {habit.name}",
                width=150,
                font=("Avenir Next", 13, "bold"),
                text_color="#F8FAFC",
                anchor="w"
            )
            name_label.pack(side="left", padx=6)

            completion_count = habit.get_completed_count()
            checked_days = completion_count

            for day in range(7):
                if day < checked_days:
                    circle_text = "✓"
                    circle_color = "#10B981"
                    text_color = "white"
                else:
                    circle_text = ""
                    circle_color = "#1E293B"
                    text_color = "#1E293B"

                day_label = ctk.CTkLabel(
                    row_frame,
                    text=circle_text,
                    width=26,
                    height=26,
                    corner_radius=13,
                    fg_color=circle_color,
                    text_color=text_color,
                    font=("Avenir Next", 13, "bold")
                )
                day_label.pack(side="left", padx=3)

            count_text = f"{min(completion_count, 7)}/7"
            count_label = ctk.CTkLabel(
                row_frame,
                text=count_text,
                width=42,
                font=("Avenir Next", 14, "bold"),
                text_color="#38BDF8"
            )
            count_label.pack(side="right", padx=8)

    def update_budget_overview_panel(self, dashboard):
        for widget in self.budget_info_frame.winfo_children():
            widget.destroy()

        total_spending = dashboard.get_total_spending()

        if self.monthly_budget > 0:
            saved_amount = self.monthly_budget - total_spending
        else:
            saved_amount = 0

        if saved_amount < 0:
            saved_amount = 0

        spent_label = ctk.CTkLabel(
            self.budget_info_frame,
            text=f"Spent\n${total_spending:.2f}",
            font=("Avenir Next", 16, "bold"),
            text_color="#F87171",
            justify="left"
        )
        spent_label.pack(side="left", padx=16, pady=6)

        saved_label = ctk.CTkLabel(
            self.budget_info_frame,
            text=f"Saved\n${saved_amount:.2f}",
            font=("Avenir Next", 16, "bold"),
            text_color="#4ADE80",
            justify="left"
        )
        saved_label.pack(side="right", padx=16, pady=6)

        self.draw_budget_donut_chart(total_spending, saved_amount)

    def draw_budget_donut_chart(self, spent, saved):
        if self.budget_chart_canvas is not None:
            self.budget_chart_canvas.get_tk_widget().destroy()

        figure = Figure(figsize=(3.4, 2.0), dpi=100)
        figure.patch.set_facecolor("#081528")

        plot = figure.add_subplot(111)
        plot.set_facecolor("#081528")

        total = spent + saved

        if total <= 0:
            plot.text(
                0.5,
                0.5,
                "Set budget\nto view chart",
                ha="center",
                va="center",
                color="#CBD5E1",
                fontsize=10
            )
            plot.axis("off")
        else:
            values = [spent, saved]
            colors = ["#F43F5E", "#22C55E"]

            plot.pie(
                values,
                colors=colors,
                startangle=90,
                wedgeprops={"width": 0.38, "edgecolor": "#081528"}
            )

            plot.text(
                0,
                0,
                f"Total\n${total:.0f}",
                ha="center",
                va="center",
                color="#F8FAFC",
                fontsize=11,
                fontweight="bold"
            )

            plot.axis("equal")

        figure.tight_layout()

        self.budget_chart_canvas = FigureCanvasTkAgg(figure, self.budget_chart_frame)
        self.budget_chart_canvas.draw()
        self.budget_chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_weekly_progress_panel(self, dashboard):
        total_habits = dashboard.get_total_habits()
        total_completions = dashboard.get_total_completions()

        if total_habits > 0:
            progress = total_completions / (total_habits * 7)
        else:
            progress = 0

        if progress > 1:
            progress = 1

        self.weekly_progress_bar.set(progress)
        self.weekly_percent_label.configure(text=f"{progress * 100:.0f}%")

        if progress == 0:
            self.weekly_message_label.configure(text="Add progress by completing your habits this week.")
        elif progress < 0.5:
            self.weekly_message_label.configure(text="Good start! Keep building your routine. ✨")
        else:
            self.weekly_message_label.configure(text="You're doing great! Keep it up! 🚀")

        goals_hit = 0
        for habit in self.habits:
            if habit.get_completed_count() > 0:
                goals_hit += 1

        points = total_completions * 50

        self.streak_label.configure(text=str(total_completions))
        self.goals_label.configure(text=str(goals_hit))
        self.points_label.configure(text=str(points))

    def update_spending_breakdown_panel(self, dashboard):
        for widget in self.spending_legend_frame.winfo_children():
            widget.destroy()

        category_totals = dashboard.get_category_totals()
        self.draw_spending_pie_chart(category_totals)

        if len(category_totals) == 0:
            empty_label = ctk.CTkLabel(
                self.spending_legend_frame,
                text="No spending data yet.",
                font=("Avenir Next", 13),
                text_color="#CBD5E1"
            )
            empty_label.pack(pady=35)
            return

        colors = ["#F59E0B", "#38BDF8", "#A855F7", "#22C55E", "#F43F5E", "#EAB308", "#64748B"]
        icons = {
            "Food": "🍔",
            "Transport": "🚌",
            "Rent": "🏠",
            "Study": "📚",
            "Shopping": "🛍️",
            "Health": "💊",
            "Other": "🎮"
        }

        index = 0
        for category, amount in category_totals.items():
            row = ctk.CTkFrame(self.spending_legend_frame, fg_color="#081528")
            row.pack(fill="x", pady=4)

            icon = icons.get(category, "💸")
            color = colors[index % len(colors)]

            dot = ctk.CTkLabel(
                row,
                text="●",
                font=("Avenir Next", 15, "bold"),
                text_color=color
            )
            dot.pack(side="left", padx=(4, 6))

            category_label = ctk.CTkLabel(
                row,
                text=f"{icon}  {category}",
                font=("Avenir Next", 12, "bold"),
                text_color="#F8FAFC"
            )
            category_label.pack(side="left", padx=4)

            amount_label = ctk.CTkLabel(
                row,
                text=f"${amount:.2f}",
                font=("Avenir Next", 12, "bold"),
                text_color="#CBD5E1"
            )
            amount_label.pack(side="right", padx=8)

            index += 1

    def draw_spending_pie_chart(self, category_totals):
        if self.spending_chart_canvas is not None:
            self.spending_chart_canvas.get_tk_widget().destroy()

        figure = Figure(figsize=(3.0, 2.1), dpi=100)
        figure.patch.set_facecolor("#081528")

        plot = figure.add_subplot(111)
        plot.set_facecolor("#081528")

        if len(category_totals) == 0:
            plot.text(
                0.5,
                0.5,
                "No expenses",
                ha="center",
                va="center",
                color="#CBD5E1",
                fontsize=10
            )
            plot.axis("off")
        else:
            values = list(category_totals.values())
            colors = ["#F59E0B", "#38BDF8", "#A855F7", "#22C55E", "#F43F5E", "#EAB308", "#64748B"]

            plot.pie(
                values,
                startangle=90,
                colors=colors[:len(values)],
                wedgeprops={"edgecolor": "#081528"}
            )
            plot.axis("equal")

        figure.tight_layout()

        self.spending_chart_canvas = FigureCanvasTkAgg(figure, self.spending_chart_frame)
        self.spending_chart_canvas.draw()
        self.spending_chart_canvas.get_tk_widget().pack(fill="both", expand=True)

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

        self.update_habit_panel(dashboard)
        self.update_budget_overview_panel(dashboard)
        self.update_weekly_progress_panel(dashboard)
        self.update_spending_breakdown_panel(dashboard)
