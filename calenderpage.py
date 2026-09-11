import tkinter as tk
from tkinter import messagebox
import sqlite3


class CalendarPage:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        # Clear previous page
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF8F8")

        # Prepare database
        self.prepare_database()

        # ==========================================
        # TITLE
        # ==========================================
        title = tk.Label(
            self.root,
            text="Outfit Calendar",
            font=("Georgia", 26, "bold"),
            fg="#2F2A67",
            bg="#FFF8F8"
        )
        title.place(x=365, y=30)

        subtitle = tk.Label(
            self.root,
            text="Plan what you want to wear for a special day",
            font=("Arial", 11),
            fg="#726C85",
            bg="#FFF8F8"
        )
        subtitle.place(x=355, y=75)

        # ==========================================
        # BACK BUTTON
        # ==========================================
        back_button = tk.Button(
            self.root,
            text="← Back",
            font=("Arial", 10, "bold"),
            fg="#554C52",
            bg="#E9DDF5",
            activebackground="#DDCDEE",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.go_back
        )
        back_button.place(
            x=40,
            y=35,
            width=100,
            height=35
        )

        # ==========================================
        # LEFT FORM
        # ==========================================
        form_frame = tk.Frame(
            self.root,
            bg="white",
            width=420,
            height=450,
            highlightbackground="#E8DDEA",
            highlightthickness=1
        )
        form_frame.place(
            x=60,
            y=130
        )

        form_title = tk.Label(
            form_frame,
            text="Add Calendar Event",
            font=("Arial", 16, "bold"),
            fg="#39356F",
            bg="white"
        )
        form_title.place(
            x=30,
            y=25
        )

        # ==========================================
        # DATE
        # ==========================================
        date_label = tk.Label(
            form_frame,
            text="Date",
            font=("Arial", 10),
            fg="#554C52",
            bg="white"
        )
        date_label.place(
            x=30,
            y=80
        )

        self.date_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.date_entry.place(
            x=30,
            y=105,
            width=350,
            height=40
        )

        date_hint = tk.Label(
            form_frame,
            text="Example: 2026-09-15",
            font=("Arial", 9),
            fg="#8B8495",
            bg="white"
        )
        date_hint.place(
            x=30,
            y=150
        )

        # ==========================================
        # SAVED OUTFITS
        # ==========================================
        outfit_label = tk.Label(
            form_frame,
            text="Select Saved Outfit",
            font=("Arial", 10),
            fg="#554C52",
            bg="white"
        )
        outfit_label.place(
            x=30,
            y=190
        )

        self.outfit_var = tk.StringVar()
        self.outfit_var.set("Select Outfit")

        self.outfit_menu = tk.OptionMenu(
            form_frame,
            self.outfit_var,
            "Select Outfit"
        )

        self.outfit_menu.config(
            font=("Arial", 10),
            fg="#554C52",
            bg="white",
            activebackground="#F5EAF8",
            relief="solid",
            borderwidth=1
        )

        self.outfit_menu.place(
            x=30,
            y=215,
            width=350,
            height=40
        )

        # ==========================================
        # NOTES
        # ==========================================
        notes_label = tk.Label(
            form_frame,
            text="Notes",
            font=("Arial", 10),
            fg="#554C52",
            bg="white"
        )
        notes_label.place(
            x=30,
            y=280
        )

        self.notes_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.notes_entry.place(
            x=30,
            y=305,
            width=350,
            height=40
        )

        notes_hint = tk.Label(
            form_frame,
            text="Example: Dinner, College, Party, Birthday...",
            font=("Arial", 9),
            fg="#8B8495",
            bg="white"
        )
        notes_hint.place(
            x=30,
            y=350
        )

        # ==========================================
        # SAVE BUTTON
        # ==========================================
        save_button = tk.Button(
            form_frame,
            text="Save Event",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#A467DF",
            activebackground="#9258CC",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.save_event
        )
        save_button.place(
            x=110,
            y=390,
            width=200,
            height=42
        )

        # ==========================================
        # RIGHT EVENTS AREA
        # ==========================================
        events_frame = tk.Frame(
            self.root,
            bg="white",
            width=440,
            height=450,
            highlightbackground="#E8DDEA",
            highlightthickness=1
        )
        events_frame.place(
            x=510,
            y=130
        )

        events_title = tk.Label(
            events_frame,
            text="My Calendar Events",
            font=("Arial", 16, "bold"),
            fg="#39356F",
            bg="white"
        )
        events_title.place(
            x=25,
            y=25
        )

        # Scrollbar
        scrollbar = tk.Scrollbar(
            events_frame
        )
        scrollbar.place(
            x=395,
            y=70,
            height=330
        )

        self.events_text = tk.Text(
            events_frame,
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFFDFD",
            relief="flat",
            wrap="word",
            yscrollcommand=scrollbar.set
        )
        self.events_text.place(
            x=25,
            y=70,
            width=365,
            height=330
        )

        scrollbar.config(
            command=self.events_text.yview
        )

        # Load saved outfits
        self.load_outfits()

        # Load calendar events
        self.load_events()

    # ==========================================
    # PREPARE DATABASE
    # ==========================================
    def prepare_database(self):
        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS calendar_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    event_date TEXT NOT NULL,
                    outfit_id INTEGER NOT NULL,
                    notes TEXT,
                    FOREIGN KEY (user_id)
                    REFERENCES users(id),
                    FOREIGN KEY (outfit_id)
                    REFERENCES outfits(id)
                )
                """
            )

            connection.commit()
            connection.close()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not prepare calendar.\n\n{error}"
            )

    # ==========================================
    # GET USER ID
    # ==========================================
    def get_user_id(self):
        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                """,
                (self.username,)
            )

            user = cursor.fetchone()

            connection.close()

            if user:
                return user[0]

            return None

        except sqlite3.Error:
            return None

    # ==========================================
    # LOAD SAVED OUTFITS
    # ==========================================
    def load_outfits(self):
        user_id = self.get_user_id()

        if user_id is None:
            return

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    outfits.id,
                    top_item.name,
                    bottom_item.name,
                    shoes_item.name

                FROM outfits

                LEFT JOIN clothing AS top_item
                ON outfits.top_id = top_item.id

                LEFT JOIN clothing AS bottom_item
                ON outfits.bottom_id = bottom_item.id

                LEFT JOIN clothing AS shoes_item
                ON outfits.shoes_id = shoes_item.id

                WHERE outfits.user_id = ?

                ORDER BY outfits.id DESC
                """,
                (user_id,)
            )

            outfits = cursor.fetchall()

            connection.close()

            menu = self.outfit_menu["menu"]

            menu.delete(0, "end")

            menu.add_command(
                label="Select Outfit",
                command=lambda:
                self.outfit_var.set("Select Outfit")
            )

            for outfit in outfits:
                outfit_id = outfit[0]

                top_name = outfit[1] or "Top"
                bottom_name = outfit[2] or "Bottom"
                shoes_name = outfit[3] or "Shoes"

                display_text = (
                    f"Outfit {outfit_id}: "
                    f"{top_name} + "
                    f"{bottom_name} + "
                    f"{shoes_name}"
                )

                menu.add_command(
                    label=display_text,
                    command=lambda value=display_text:
                    self.outfit_var.set(value)
                )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load saved outfits.\n\n{error}"
            )

    # ==========================================
    # SAVE CALENDAR EVENT
    # ==========================================
    def save_event(self):
        event_date = self.date_entry.get().strip()

        selected_outfit = self.outfit_var.get()

        notes = self.notes_entry.get().strip()

        # Check date
        if event_date == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter a date."
            )
            return

        # Check basic date format
        date_parts = event_date.split("-")

        if (
            len(date_parts) != 3
            or not date_parts[0].isdigit()
            or not date_parts[1].isdigit()
            or not date_parts[2].isdigit()
        ):
            messagebox.showwarning(
                "Invalid Date",
                "Please enter the date like this:\n\n2026-09-15"
            )
            return

        # Check outfit
        if selected_outfit == "Select Outfit":
            messagebox.showwarning(
                "Missing Outfit",
                "Please select a saved outfit."
            )
            return

        # Extract outfit ID
        try:
            outfit_id = int(
                selected_outfit.split(":")[0]
                .replace("Outfit", "")
                .strip()
            )

        except ValueError:
            messagebox.showerror(
                "Outfit Error",
                "Could not identify the selected outfit."
            )
            return

        user_id = self.get_user_id()

        if user_id is None:
            messagebox.showerror(
                "User Error",
                "Could not find the logged-in user."
            )
            return

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            # Make sure outfit belongs to current user
            cursor.execute(
                """
                SELECT id
                FROM outfits
                WHERE id = ?
                AND user_id = ?
                """,
                (
                    outfit_id,
                    user_id
                )
            )

            outfit = cursor.fetchone()

            if outfit is None:
                connection.close()

                messagebox.showwarning(
                    "Outfit Not Found",
                    "The selected outfit could not be found."
                )

                return

            # Save calendar event
            cursor.execute(
                """
                INSERT INTO calendar_events (
                    user_id,
                    event_date,
                    outfit_id,
                    notes
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    user_id,
                    event_date,
                    outfit_id,
                    notes
                )
            )

            connection.commit()

            connection.close()

            messagebox.showinfo(
                "Gola",
                "Calendar event saved successfully! ♡"
            )

            # Clear form
            self.date_entry.delete(
                0,
                tk.END
            )

            self.outfit_var.set(
                "Select Outfit"
            )

            self.notes_entry.delete(
                0,
                tk.END
            )

            # Reload events
            self.load_events()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not save calendar event.\n\n{error}"
            )

    # ==========================================
    # LOAD CALENDAR EVENTS
    # ==========================================
    def load_events(self):
        self.events_text.config(
            state="normal"
        )

        self.events_text.delete(
            "1.0",
            tk.END
        )

        user_id = self.get_user_id()

        if user_id is None:
            return

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    calendar_events.id,
                    calendar_events.event_date,
                    calendar_events.outfit_id,
                    calendar_events.notes,
                    top_item.name,
                    bottom_item.name,
                    shoes_item.name

                FROM calendar_events

                LEFT JOIN outfits
                ON calendar_events.outfit_id = outfits.id

                LEFT JOIN clothing AS top_item
                ON outfits.top_id = top_item.id

                LEFT JOIN clothing AS bottom_item
                ON outfits.bottom_id = bottom_item.id

                LEFT JOIN clothing AS shoes_item
                ON outfits.shoes_id = shoes_item.id

                WHERE calendar_events.user_id = ?

                ORDER BY calendar_events.event_date ASC
                """,
                (user_id,)
            )

            events = cursor.fetchall()

            connection.close()

            if len(events) == 0:
                self.events_text.insert(
                    tk.END,
                    "\nNo calendar events yet.\n\n"
                    "Save an outfit first, then plan "
                    "what you want to wear ♡"
                )

                self.events_text.config(
                    state="disabled"
                )

                return

            for event in events:
                event_id = event[0]
                event_date = event[1]
                outfit_id = event[2]
                notes = event[3]

                top_name = event[4] or "Top"
                bottom_name = event[5] or "Bottom"
                shoes_name = event[6] or "Shoes"

                self.events_text.insert(
                    tk.END,
                    f"📅 {event_date}\n"
                )

                self.events_text.insert(
                    tk.END,
                    f"Outfit {outfit_id}\n"
                )

                self.events_text.insert(
                    tk.END,
                    f"👕 {top_name}\n"
                )

                self.events_text.insert(
                    tk.END,
                    f"👖 {bottom_name}\n"
                )

                self.events_text.insert(
                    tk.END,
                    f"👟 {shoes_name}\n"
                )

                if notes:
                    self.events_text.insert(
                        tk.END,
                        f"📝 {notes}\n"
                    )

                self.events_text.insert(
                    tk.END,
                    f"Event ID: {event_id}\n"
                    "──────────────────────────\n\n"
                )

            self.events_text.config(
                state="disabled"
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load calendar events.\n\n{error}"
            )

    # ==========================================
    # BACK TO DASHBOARD
    # ==========================================
    def go_back(self):
        from dashboard import DashboardPage

        DashboardPage(
            self.root,
            self.username
        )