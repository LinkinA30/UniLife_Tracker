from datetime import date


class Expense:
    def __init__(self, amount, category, description, expense_date=None):
        self.amount = amount
        self.category = category
        self.description = description

        if expense_date is None:
            self.expense_date = date.today().isoformat()
        else:
            self.expense_date = expense_date

    def get_details(self):
        return f"{self.expense_date} | ${self.amount:.2f} | {self.category} | {self.description}"

    def to_dictionary(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "expense_date": self.expense_date
        }

    @classmethod
    def from_dictionary(cls, data):
        return cls(
            float(data["amount"]),
            data["category"],
            data["description"],
            data.get("expense_date")
        )