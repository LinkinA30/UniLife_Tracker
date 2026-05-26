from datetime import date


class Habit:
    def __init__(self, name, completed_dates=None):
        self.name = name

        if completed_dates is None:
            self.completed_dates = []
        else:
            self.completed_dates = completed_dates

    def mark_complete(self):
        today = date.today().isoformat()

        if today not in self.completed_dates:
            self.completed_dates.append(today)
            return True

        return False

    def get_completed_count(self):
        return len(self.completed_dates)

    def get_details(self):
        return f"{self.name} | Completed: {self.get_completed_count()} day(s)"

    def to_dictionary(self):
        return {
            "name": self.name,
            "completed_dates": self.completed_dates
        }

    @classmethod
    def from_dictionary(cls, data):
        return cls(
            data["name"],
            data.get("completed_dates", [])
        )