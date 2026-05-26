import customtkinter as ctk
from app import UniLifeTrackerApp


def show_splash_then_app():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.withdraw()

    splash = ctk.CTkToplevel(root)
    splash.title("UniLife Tracker")
    splash.geometry("520x320")
    splash.resizable(False, False)

    splash_frame = ctk.CTkFrame(
        splash,
        corner_radius=25,
        fg_color="#111827"
    )
    splash_frame.pack(fill="both", expand=True, padx=20, pady=20)

    title = ctk.CTkLabel(
        splash_frame,
        text="UniLife Tracker",
        font=("Arial", 34, "bold"),
        text_color="#38BDF8"
    )
    title.pack(pady=(55, 10))

    subtitle = ctk.CTkLabel(
        splash_frame,
        text="Student Habit & Budget Manager",
        font=("Arial", 16),
        text_color="#CBD5E1"
    )
    subtitle.pack(pady=5)

    loading = ctk.CTkLabel(
        splash_frame,
        text="Loading your student dashboard...",
        font=("Arial", 13),
        text_color="#94A3B8"
    )
    loading.pack(pady=(35, 10))

    progress = ctk.CTkProgressBar(
        splash_frame,
        width=320,
        progress_color="#38BDF8"
    )
    progress.pack(pady=10)
    progress.set(0.75)

    def open_main_app():
        splash.destroy()
        root.deiconify()
        UniLifeTrackerApp(root)

    root.after(1800, open_main_app)
    root.mainloop()


if __name__ == "__main__":
    show_splash_then_app()