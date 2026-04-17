import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
import datetime

# ─── Data Storage ───────────────────────────────────────────────────────────
DATA_FILE = "attendance_data.json"

COURSES = ["CSE", "CSD", "AIML", "MECH", "CIVIL", "EC", "EEE"]
SEMESTERS = [f"Sem {i}" for i in range(1, 9)]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
PERIODS = ["Period 1\n08:00-09:00", "Period 2\n09:00-10:00", "Period 3\n10:00-11:00",
           "Period 4\n11:00-12:00", "Period 5\n01:00-02:00", "Period 6\n02:00-03:00",
           "Period 7\n03:00-04:00"]

# Colors
BG_DARK    = "#0f1923"
BG_CARD    = "#1a2535"
BG_CARD2   = "#1e2d42"
ACCENT     = "#00c8ff"
ACCENT2    = "#0077aa"
SUCCESS    = "#00e676"
DANGER     = "#ff4444"
WARNING    = "#ffaa00"
TEXT_WHITE = "#e8f4fd"
TEXT_GRAY  = "#7a9bb5"
BORDER     = "#2a3f5a"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "users": {"admin": "admin123", "teacher1": "pass123"},
        "students": {},
        "attendance": {},
        "timetable": {}
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ─── Styled Widgets ──────────────────────────────────────────────────────────
def styled_button(parent, text, command, color=ACCENT, fg=BG_DARK, width=None, font_size=10):
    kw = dict(text=text, command=command, bg=color, fg=fg,
              font=("Segoe UI", font_size, "bold"), relief="flat",
              cursor="hand2", activebackground=ACCENT2, activeforeground=TEXT_WHITE,
              padx=14, pady=6, bd=0)
    if width:
        kw["width"] = width
    btn = tk.Button(parent, **kw)
    return btn

def styled_label(parent, text, size=10, color=TEXT_WHITE, bold=False, anchor="w"):
    w = "bold" if bold else "normal"
    return tk.Label(parent, text=text, bg=BG_DARK, fg=color,
                    font=("Segoe UI", size, w), anchor=anchor)

def styled_entry(parent, width=20, show=None):
    e = tk.Entry(parent, width=width, bg=BG_CARD2, fg=TEXT_WHITE,
                 insertbackground=ACCENT, font=("Segoe UI", 10),
                 relief="flat", bd=0, highlightthickness=1,
                 highlightbackground=BORDER, highlightcolor=ACCENT)
    if show:
        e.config(show=show)
    return e

def styled_combo(parent, values, width=18):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Dark.TCombobox",
                    fieldbackground=BG_CARD2, background=BG_CARD2,
                    foreground=TEXT_WHITE, bordercolor=BORDER,
                    arrowcolor=ACCENT, selectbackground=ACCENT2)
    cb = ttk.Combobox(parent, values=values, width=width,
                      style="Dark.TCombobox", font=("Segoe UI", 10),
                      state="readonly")
    return cb

def card_frame(parent, padx=16, pady=12, bg=BG_CARD):
    f = tk.Frame(parent, bg=bg, highlightthickness=1,
                 highlightbackground=BORDER)
    f.pack(fill="x", padx=padx, pady=pady)
    return f

# ─── Main Application ────────────────────────────────────────────────────────
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EduTrack — Student Attendance System")
        self.root.geometry("1200x750")
        self.root.minsize(900, 650)
        self.root.configure(bg=BG_DARK)
        self.data = load_data()
        self.current_user = None
        self.show_login()

    # ═══ LOGIN ═══════════════════════════════════════════════════════════════
    def show_login(self):
        self.clear_root()
        root = self.root

        # Background gradient simulation
        bg_frame = tk.Frame(root, bg=BG_DARK)
        bg_frame.place(relwidth=1, relheight=1)

        # Decorative left panel
        left = tk.Frame(bg_frame, bg="#0a1520", width=400)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="🎓", bg="#0a1520", fg=ACCENT,
                 font=("Segoe UI", 64)).pack(pady=(120, 10))
        tk.Label(left, text="EduTrack", bg="#0a1520", fg=TEXT_WHITE,
                 font=("Georgia", 36, "bold")).pack()
        tk.Label(left, text="Student Attendance\nManagement System",
                 bg="#0a1520", fg=TEXT_GRAY,
                 font=("Segoe UI", 13), justify="center").pack(pady=8)

        # Decorative dots
        dot_frame = tk.Frame(left, bg="#0a1520")
        dot_frame.pack(pady=30)
        for i, c in enumerate([ACCENT, ACCENT2, BORDER, BORDER]):
            tk.Label(dot_frame, text="●", bg="#0a1520", fg=c,
                     font=("Segoe UI", 8)).pack(side="left", padx=3)

        tk.Label(left, text="BE Engineering • All Branches\n8 Semesters • Full Attendance Suite",
                 bg="#0a1520", fg=TEXT_GRAY, font=("Segoe UI", 10),
                 justify="center").pack(pady=8)

        # Right login panel
        right = tk.Frame(bg_frame, bg=BG_DARK)
        right.pack(side="right", fill="both", expand=True)

        inner = tk.Frame(right, bg=BG_DARK)
        inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner, text="Welcome Back", bg=BG_DARK, fg=TEXT_WHITE,
                 font=("Georgia", 26, "bold")).pack(pady=(0, 4))
        tk.Label(inner, text="Sign in to your teacher account",
                 bg=BG_DARK, fg=TEXT_GRAY, font=("Segoe UI", 11)).pack(pady=(0, 30))

        # Card
        card = tk.Frame(inner, bg=BG_CARD, highlightthickness=1,
                        highlightbackground=BORDER)
        card.pack(ipadx=30, ipady=28)

        tk.Label(card, text="Username", bg=BG_CARD, fg=TEXT_GRAY,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(20, 2))
        self.login_user = styled_entry(card, width=28)
        self.login_user.pack(padx=20, pady=(0, 14), ipady=6)

        tk.Label(card, text="Password", bg=BG_CARD, fg=TEXT_GRAY,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=20, pady=(0, 2))
        self.login_pass = styled_entry(card, width=28, show="●")
        self.login_pass.pack(padx=20, pady=(0, 20), ipady=6)

        btn = styled_button(card, "  Sign In  →", self.do_login,
                            color=ACCENT, width=28, font_size=11)
        btn.pack(padx=20, pady=(0, 20), ipady=4)

        self.login_msg = tk.Label(card, text="", bg=BG_CARD, fg=DANGER,
                                  font=("Segoe UI", 9))
        self.login_msg.pack()

        # Default credentials hint
        tk.Label(inner, text="Default: admin / admin123",
                 bg=BG_DARK, fg=TEXT_GRAY, font=("Segoe UI", 9)).pack(pady=10)

        self.login_pass.bind("<Return>", lambda e: self.do_login())
        self.login_user.bind("<Return>", lambda e: self.login_pass.focus())
        self.login_user.focus()

    def do_login(self):
        u = self.login_user.get().strip()
        p = self.login_pass.get().strip()
        if u in self.data["users"] and self.data["users"][u] == p:
            self.current_user = u
            self.show_main()
        else:
            self.login_msg.config(text="✗  Invalid username or password")
            self.login_pass.delete(0, "end")

    # ═══ MAIN WINDOW ══════════════════════════════════════════════════════════
    def show_main(self):
        self.clear_root()
        root = self.root

        # Top header
        header = tk.Frame(root, bg="#0a1520", height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🎓 EduTrack", bg="#0a1520", fg=ACCENT,
                 font=("Georgia", 16, "bold")).pack(side="left", padx=20, pady=14)
        tk.Label(header, text="Student Attendance Management System",
                 bg="#0a1520", fg=TEXT_GRAY, font=("Segoe UI", 10)).pack(side="left", pady=14)

        now = datetime.datetime.now().strftime("%A, %d %B %Y")
        tk.Label(header, text=f"📅 {now}  👤 {self.current_user}",
                 bg="#0a1520", fg=TEXT_GRAY, font=("Segoe UI", 9)).pack(side="right", padx=16)

        styled_button(header, "Logout", self.show_login,
                      color="#1e2d42", fg=TEXT_WHITE).pack(side="right", padx=4, pady=12)

        # Sidebar + Content
        body = tk.Frame(root, bg=BG_DARK)
        body.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(body, bg="#0d1b2a", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(body, bg=BG_DARK)
        self.content.pack(side="right", fill="both", expand=True)

        self.current_page = None
        nav_items = [
            ("🏠", "Dashboard", self.page_dashboard),
            ("👥", "Student Details", self.page_students),
            ("✅", "E-Attendance", self.page_attendance),
            ("📋", "Saved Records", self.page_saved),
            ("📅", "Timetable", self.page_timetable),
        ]

        tk.Label(self.sidebar, text="NAVIGATION", bg="#0d1b2a", fg=TEXT_GRAY,
                 font=("Segoe UI", 8, "bold")).pack(pady=(20, 8), padx=14, anchor="w")

        self.nav_btns = []
        for icon, label, cmd in nav_items:
            btn = tk.Button(self.sidebar, text=f"  {icon}  {label}",
                            command=lambda c=cmd, l=label: self.nav_click(c, l),
                            bg="#0d1b2a", fg=TEXT_GRAY,
                            font=("Segoe UI", 10), relief="flat",
                            cursor="hand2", anchor="w", padx=10, pady=10, bd=0,
                            activebackground=BG_CARD2, activeforeground=ACCENT)
            btn.pack(fill="x", padx=6, pady=1)
            self.nav_btns.append((label, btn))

        self.nav_click(self.page_dashboard, "Dashboard")

    def nav_click(self, cmd, label):
        for lbl, btn in self.nav_btns:
            if lbl == label:
                btn.config(bg=BG_CARD2, fg=ACCENT)
            else:
                btn.config(bg="#0d1b2a", fg=TEXT_GRAY)
        self.clear_content()
        cmd()

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

    def scroll_frame(self, parent):
        """Create a scrollable frame."""
        container = tk.Frame(parent, bg=BG_DARK)
        container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container, bg=BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        inner = tk.Frame(canvas, bg=BG_DARK)
        win = canvas.create_window((0, 0), window=inner, anchor="nw")

        def on_resize(e):
            canvas.itemconfig(win, width=canvas.winfo_width())

        def on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", on_resize)
        inner.bind("<Configure>", on_configure)

        def on_mousewheel(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)
        return inner

    # ═══ DASHBOARD ════════════════════════════════════════════════════════════
    def page_dashboard(self):
        outer = self.scroll_frame(self.content)

        tk.Label(outer, text="Dashboard", bg=BG_DARK, fg=TEXT_WHITE,
                 font=("Georgia", 22, "bold")).pack(anchor="w", padx=24, pady=(20, 4))
        tk.Label(outer, text="Overview of your attendance system",
                 bg=BG_DARK, fg=TEXT_GRAY, font=("Segoe UI", 10)).pack(anchor="w", padx=24, pady=(0, 16))

        # Stats
        stats_row = tk.Frame(outer, bg=BG_DARK)
        stats_row.pack(fill="x", padx=20, pady=4)

        total_students = sum(len(v) for v in self.data["students"].values())
        total_records = len(self.data["attendance"])
        total_courses = len(COURSES)

        for val, lbl, clr in [
            (total_students, "Total Students", ACCENT),
            (total_records, "Attendance Records", SUCCESS),
            (total_courses, "Courses", WARNING),
            (8, "Semesters", "#cc88ff"),
        ]:
            card = tk.Frame(stats_row, bg=BG_CARD, highlightthickness=1,
                            highlightbackground=BORDER)
            card.pack(side="left", fill="both", expand=True, padx=6, pady=4, ipadx=12, ipady=14)
            tk.Label(card, text=str(val), bg=BG_CARD, fg=clr,
                     font=("Segoe UI", 32, "bold")).pack(pady=(8, 0))
            tk.Label(card, text=lbl, bg=BG_CARD, fg=TEXT_GRAY,
                     font=("Segoe UI", 9)).pack(pady=(2, 8))

        # Recent Activity
        tk.Label(outer, text="Courses Overview", bg=BG_DARK, fg=TEXT_WHITE,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=24, pady=(20, 8))

        grid = tk.Frame(outer, bg=BG_DARK)
        grid.pack(fill="x", padx=20)
        for i, course in enumerate(COURSES):
            card = tk.Frame(grid, bg=BG_CARD, highlightthickness=1,
                            highlightbackground=BORDER)
            card.grid(row=i // 4, column=i % 4, padx=6, pady=6,
                      sticky="nsew", ipadx=8, ipady=8)
            grid.columnconfigure(i % 4, weight=1)
            count = sum(
                len(v) for k, v in self.data["students"].items()
                if k.startswith(course + "|")
            )
            tk.Label(card, text=course, bg=BG_CARD, fg=ACCENT,
                     font=("Segoe UI", 14, "bold")).pack(pady=(8, 2))
            tk.Label(card, text=f"{count} students", bg=BG_CARD, fg=TEXT_GRAY,
                     font=("Segoe UI", 9)).pack()
            tk.Label(card, text="8 Semesters", bg=BG_CARD, fg=TEXT_GRAY,
                     font=("Segoe UI", 8)).pack(pady=(2, 8))

    # ═══ STUDENT DETAILS ══════════════════════════════════════════════════════
    def page_students(self):
        outer = self.content
        tk.Label(outer, text="Student Details", bg=BG_DARK, fg=TEXT_WHITE,
                 font=("Georgia", 22, "bold")).pack(anchor="w", padx=24, pady=(20, 4))

        top = tk.Frame(outer, bg=BG_DARK)
        top.pack(fill="x", padx=20, pady=8)

        # Filter row
        filter_card = tk.Frame(top, bg=BG_CARD, highlightthickness=1,
                               highlightbackground=BORDER)
        filter_card.pack(fill="x", pady=4, ipadx=10, ipady=10)

        tk.Label(filter_card, text="Course:", bg=BG_CARD, fg=TEXT_GRAY,
                 font=("Segoe UI", 10)).pack(side="left", padx=(14, 4))
        self.std_course = styled_combo(filter_card, COURSES)
        self.std_course.pack(side="left", padx=4)
        self.std_course.set(COURSES[0])

        tk.Label(filter_card, text="Semester:", bg=BG_CARD, fg=TEXT_GRAY,
                 font=("Segoe UI", 10)).pack(side="left", padx=(14, 4))
        self.std_sem = styled_combo(filter_card, SEMESTERS)
        self.std_sem.pack(side="left", padx=4)
        self.std_sem.set(SEMESTERS[0])

        styled_button(filter_card, "🔍 Load", self.load_students,
                      color=ACCENT2).pack(side="left", padx=10)
        styled_button(filter_card, "➕ Add Student", self.add_student_dialog,
                      color=SUCCESS, fg=BG_DARK).pack(side="right", padx=10)

        # Table
        self.std_frame = tk.Frame(outer, bg=BG_DARK)
        self.std_frame.pack(fill="both", expand=True, padx=20, pady=8)
        self.load_students()

    def get_key(self, course=None, sem=None):
        c = course or self.std_course.get()
        s = sem or self.std_sem.get()
        return f"{c}|{s}"

    def load_students(self):
        for w in self.std_frame.winfo_children():
            w.destroy()

        key = self.get_key()
        students = self.data["students"].get(key, [])

        # Header
        header = tk.Frame(self.std_frame, bg=BG_CARD2)
        header.pack(fill="x")
        for col, w in [("Roll No", 8), ("Name", 22), ("Register No", 14), ("Actions", 18)]:
            tk.Label(header, text=col, bg=BG_CARD2, fg=ACCENT,
                     font=("Segoe UI", 10, "bold"), width=w, anchor="w").pack(side="left", padx=8, pady=8)

        if not students:
            tk.Label(self.std_frame, text="No students found. Click '+ Add Student' to begin.",
                     bg=BG_DARK, fg=TEXT_GRAY, font=("Segoe UI", 11)).pack(pady=40)
            return

        container = tk.Frame(self.std_frame, bg=BG_DARK)
        container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container, bg=BG_DARK, highlightthickness=0)
        sb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        sb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        canvas.configure(yscrollcommand=sb.set)
        inner = tk.Frame(canvas, bg=BG_DARK)
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for i, s in enumerate(students):
            bg = BG_CARD if i % 2 == 0 else BG_CARD2
            row = tk.Frame(inner, bg=bg, highlightthickness=1, highlightbackground=BORDER)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=s.get("roll", ""), bg=bg, fg=TEXT_WHITE,
                     font=("Segoe UI", 10), width=8, anchor="w").pack(side="left", padx=8, pady=7)
            tk.Label(row, text=s.get("name", ""), bg=bg, fg=TEXT_WHITE,
                     font=("Segoe UI", 10), width=22, anchor="w").pack(side="left", padx=8)
            tk.Label(row, text=s.get("reg", ""), bg=bg, fg=TEXT_GRAY,
                     font=("Segoe UI", 9), width=14, anchor="w").pack(side="left", padx=8)

            actions = tk.Frame(row, bg=bg)
            actions.pack(side="left", padx=8)
            styled_button(actions, "✏ Edit",
                          lambda idx=i: self.edit_student_dialog(idx),
                          color="#1e3a5f", fg=ACCENT, font_size=9).pack(side="left", padx=2)
            styled_button(actions, "🗑 Del",
                          lambda idx=i: self.delete_student(idx),
                          color="#3a1e1e", fg=DANGER, font_size=9).pack(side="left", padx=2)

    def add_student_dialog(self):
        self._student_dialog("Add Student", None)

    def edit_student_dialog(self, idx):
        self._student_dialog("Edit Student", idx)

    def _student_dialog(self, title, idx):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("400x320")
        win.configure(bg=BG_DARK)
        win.grab_set()

        key = self.get_key()
        student = self.data["students"].get(key, [])[idx] if idx is not None else {}

        tk.Label(win, text=title, bg=BG_DARK, fg=TEXT_WHITE,
                 font=("Georgia", 16, "bold")).pack(pady=(20, 8))

        card = tk.Frame(win, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
        card.pack(padx=30, fill="x", ipady=10)

        entries = {}
        for lbl, key_name, default in [
            ("Roll Number", "roll", student.get("roll", "")),
            ("Full Name", "name", student.get("name", "")),
            ("Register Number", "reg", student.get("reg", "")),
        ]:
            tk.Label(card, text=lbl, bg=BG_CARD, fg=TEXT_GRAY,
                     font=("Segoe UI", 9)).pack(anchor="w", padx=16, pady=(10, 2))
            e = styled_entry(card, width=36)
            e.pack(padx=16, ipady=5)
            e.insert(0, default)
            entries[key_name] = e

        def save():
            roll = entries["roll"].get().strip()
            name = entries["name"].get().strip()
            reg = entries["reg"].get().strip()
            if not roll or not name:
                messagebox.showerror("Error", "Roll and Name required", parent=win)
                return
            k = self.get_key()
            if k not in self.data["students"]:
                self.data["students"][k] = []
            if idx is None:
                self.data["students"][k].append({"roll": roll, "name": name, "reg": reg})
            else:
                self.data["students"][k][idx] = {"roll": roll, "name": name, "reg": reg}
            save_data(self.data)
            win.destroy()
            self.load_students()

        styled_button(win, "💾 Save", save, color=SUCCESS, fg=BG_DARK).pack(pady=16)

    def delete_student(self, idx):
        key = self.get_key()
        s = self.data["students"][key][idx]
        if messagebox.askyesno("Delete", f"Delete student '{s['name']}'?"):
            self.data["students"][key].pop(idx)
            save_data(self.data)
            self.load_students()

    # ═══ E-ATTENDANCE ══════════════════════════════════════════════════════════
    def page_attendance(self):
        outer = self.content
        tk.Label(outer, text="E-Attendance", bg=BG_DARK, fg=TEXT_WHITE,
                 font=("Georgia", 22, "bold")).pack(anchor="w", padx=24, pady=(20, 4))
        tk.Label(outer, text="Mark attendance — double-click circle to toggle absent",
                 bg=BG_DARK, fg=TEXT_GRAY, font=("Segoe UI", 10)).pack(anchor="w", padx=24, pady=(0, 10))

        # Selection card
        sel = tk.Frame(outer, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
        sel.pack(fill="x", padx=20, pady=4, ipadx=10, ipady=10)

        # Row 1
        row1 = tk.Frame(sel, bg=BG_CARD)
        row1.pack(fill="x", padx=10, pady=4)

        for lbl, attr, values in [
            ("Course", "att_course", COURSES),
            ("Semester", "att_sem", SEMESTERS),
        ]:
            tk.Label(row1, text=lbl + ":", bg=BG_CARD, fg=TEXT_GRAY,
                     font=("Segoe UI", 10)).pack(side="left", padx=(10, 4))
            cb = styled_combo(row1, values, width=14)
            cb.set(values[0])
            cb.pack(side="left", padx=4)
            setattr(self, attr, cb)

        tk.Label(row1, text="Subject:", bg=BG_CARD, fg=TEXT_GRAY,
                 font=("Segoe UI", 10)).pack(side="left", padx=(10, 4))
        self.att_subject = styled_entry(row1, width=18)
        self.att_subject.pack(side="left", padx=4, ipady=4)

        # Row 2 - Date/Time
        row2 = tk.Frame(sel, bg=BG_CARD)
        row2.pack(fill="x", padx=10, pady=4)

        tk.Label(row2, text="Date:", bg=BG_CARD, fg=TEXT_GRAY,
                 font=("Segoe UI", 10)).pack(side="left", padx=(10, 4))
        self.att_date = styled_entry(row2, width=14)
        self.att_date.pack(side="left", padx=4, ipady=4)
        self.att_date.insert(0, datetime.date.today().strftime("%d/%m/%Y"))

        tk.Label(row2, text="Time:", bg=BG_CARD, fg=TEXT_GRAY,
                 font=("Segoe UI", 10)).pack(side="left", padx=(10, 4))
        self.att_time = styled_entry(row2, width=12)
        self.att_time.pack(side="left", padx=4, ipady=4)
        self.att_time.insert(0, datetime.datetime.now().strftime("%H:%M"))

        styled_button(row2, "📋 Load Students", self.load_attendance_sheet,
                      color=ACCENT).pack(side="left", padx=14)

        # Attendance table area
        self.att_scroll_area = tk.Frame(outer, bg=BG_DARK)
        self.att_scroll_area.pack(fill="both", expand=True, padx=20, pady=8)

    def load_attendance_sheet(self):
        for w in self.att_scroll_area.winfo_children():
            w.destroy()

        course = self.att_course.get()
        sem = self.att_sem.get()
        subject = self.att_subject.get().strip()
        date = self.att_date.get().strip()
        time_ = self.att_time.get().strip()

        if not subject:
            messagebox.showerror("Error", "Please enter a subject name")
            return
        if not date:
            messagebox.showerror("Error", "Please enter date")
            return

        key = f"{course}|{sem}"
        students = self.data["students"].get(key, [])

        if not students:
            tk.Label(self.att_scroll_area,
                     text=f"No students found for {course} {sem}.\nPlease add students first.",
                     bg=BG_DARK, fg=TEXT_GRAY, font=("Segoe UI", 12)).pack(pady=40)
            return

        # Info bar
        info = tk.Frame(self.att_scroll_area, bg=BG_CARD2, highlightthickness=1,
                        highlightbackground=BORDER)
        info.pack(fill="x", pady=(0, 8), ipady=6)
        tk.Label(info, text=f"📚 {course}  •  {sem}  •  {subject}  •  📅 {date}  •  🕐 {time_}",
                 bg=BG_CARD2, fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(side="left", padx=14)
        count_var = tk.StringVar(value=f"Present: {len(students)} / {len(students)}")
        tk.Label(info, textvariable=count_var, bg=BG_CARD2, fg=SUCCESS,
                 font=("Segoe UI", 10)).pack(side="right", padx=14)

        self.att_status = {}  # roll -> bool (True=present)
        self.att_notes = {}   # roll -> StringVar

        # Scroll
        container = tk.Frame(self.att_scroll_area, bg=BG_DARK)
        container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container, bg=BG_DARK, highlightthickness=0)
        sb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        sb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        canvas.configure(yscrollcommand=sb.set)
        inner = tk.Frame(canvas, bg=BG_DARK)
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Table header
        hdr = tk.Frame(inner, bg=BG_CARD2)
        hdr.pack(fill="x")
        for col, w in [("#", 4), ("Roll", 8), ("Name", 22), ("Reg No", 14),
                       ("Status", 12), ("Note", 28)]:
            tk.Label(hdr, text=col, bg=BG_CARD2, fg=ACCENT,
                     font=("Segoe UI", 9, "bold"), width=w, anchor="w").pack(side="left", padx=6, pady=7)

        def update_count():
            p = sum(1 for v in self.att_status.values() if v)
            count_var.set(f"Present: {p} / {len(students)}")

        for i, s in enumerate(students):
            roll = s["roll"]
            self.att_status[roll] = True
            note_var = tk.StringVar()
            self.att_notes[roll] = note_var

            bg = BG_CARD if i % 2 == 0 else BG_CARD2
            row = tk.Frame(inner, bg=bg, highlightthickness=1, highlightbackground=BORDER)
            row.pack(fill="x", pady=1)

            tk.Label(row, text=str(i + 1), bg=bg, fg=TEXT_GRAY,
                     font=("Segoe UI", 9), width=4, anchor="w").pack(side="left", padx=6, pady=6)
            tk.Label(row, text=roll, bg=bg, fg=TEXT_WHITE,
                     font=("Segoe UI", 10), width=8, anchor="w").pack(side="left", padx=6)
            tk.Label(row, text=s["name"], bg=bg, fg=TEXT_WHITE,
                     font=("Segoe UI", 10), width=22, anchor="w").pack(side="left", padx=6)
            tk.Label(row, text=s.get("reg", ""), bg=bg, fg=TEXT_GRAY,
                     font=("Segoe UI", 9), width=14, anchor="w").pack(side="left", padx=6)

            # Status circle
            status_frame = tk.Frame(row, bg=bg, width=12)
            status_frame.pack(side="left", padx=10)
            circle = tk.Label(status_frame, text="●", bg=bg, fg=SUCCESS,
                              font=("Segoe UI", 18), cursor="hand2")
            circle.pack()
            status_lbl = tk.Label(status_frame, text="Present", bg=bg, fg=SUCCESS,
                                  font=("Segoe UI", 7))
            status_lbl.pack()

            def toggle(r=roll, c=circle, sl=status_lbl, bg_=bg):
                self.att_status[r] = not self.att_status[r]
                if self.att_status[r]:
                    c.config(fg=SUCCESS)
                    sl.config(text="Present", fg=SUCCESS)
                else:
                    c.config(fg=DANGER)
                    sl.config(text="Absent", fg=DANGER)
                update_count()

            circle.bind("<Double-Button-1>", lambda e, r=roll, c=circle, sl=status_lbl, bg_=bg:
                        toggle(r, c, sl, bg_))

            # Note
            note_entry = styled_entry(row, width=26)
            note_entry.pack(side="left", padx=6, pady=4, ipady=3)
            self.att_notes[roll] = note_entry

        # Save button
        def save_attendance():
            date_ = self.att_date.get().strip()
            time__ = self.att_time.get().strip()
            subj = self.att_subject.get().strip()
            course_ = self.att_course.get()
            sem_ = self.att_sem.get()
            k = f"{course_}|{sem_}|{subj}|{date_}|{time__}"
            record = {
                "course": course_, "sem": sem_, "subject": subj,
                "date": date_, "time": time__, "records": []
            }
            key_ = f"{course_}|{sem_}"
            for st in self.data["students"].get(key_, []):
                r = st["roll"]
                record["records"].append({
                    "roll": r, "name": st["name"],
                    "status": "Present" if self.att_status.get(r, True) else "Absent",
                    "note": self.att_notes[r].get().strip()
                })
            self.data["attendance"][k] = record
            save_data(self.data)

            # Summary popup
            present = sum(1 for v in self.att_status.values() if v)
            absent = len(self.att_status) - present
            messagebox.showinfo("Attendance Saved",
                                f"✅ Attendance Saved!\n\n"
                                f"📚 {course_} | {sem_} | {subj}\n"
                                f"📅 {date_} at {time__}\n\n"
                                f"✅ Present: {present}\n"
                                f"❌ Absent:  {absent}\n"
                                f"📊 Total:   {len(self.att_status)}")

        btn_row = tk.Frame(self.att_scroll_area, bg=BG_DARK)
        btn_row.pack(fill="x", pady=8)
        styled_button(btn_row, "💾  Save Attendance", save_attendance,
                      color=SUCCESS, fg=BG_DARK, font_size=12).pack(side="right", padx=4)

    # ═══ SAVED RECORDS ═════════════════════════════════════════════════════════
    def page_saved(self):
        outer = self.content
        tk.Label(outer, text="Saved Records", bg=BG_DARK, fg=TEXT_WHITE,
                 font=("Georgia", 22, "bold")).pack(anchor="w", padx=24, pady=(20, 4))

        sel = tk.Frame(outer, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
        sel.pack(fill="x", padx=20, pady=4, ipadx=10, ipady=10)

        row = tk.Frame(sel, bg=BG_CARD)
        row.pack(fill="x", padx=10, pady=4)

        for lbl, attr, values in [
            ("Course", "rec_course", COURSES),
            ("Semester", "rec_sem", SEMESTERS),
        ]:
            tk.Label(row, text=lbl + ":", bg=BG_CARD, fg=TEXT_GRAY,
                     font=("Segoe UI", 10)).pack(side="left", padx=(10, 4))
            cb = styled_combo(row, values, width=14)
            cb.set(values[0])
            cb.pack(side="left", padx=4)
            setattr(self, attr, cb)

        tk.Label(row, text="Subject:", bg=BG_CARD, fg=TEXT_GRAY,
                 font=("Segoe UI", 10)).pack(side="left", padx=(10, 4))
        self.rec_subject = styled_entry(row, width=18)
        self.rec_subject.pack(side="left", padx=4, ipady=4)

        styled_button(row, "🔍 Search", self.load_saved_records, color=ACCENT).pack(side="left", padx=14)

        self.rec_area = tk.Frame(outer, bg=BG_DARK)
        self.rec_area.pack(fill="both", expand=True, padx=20, pady=8)

        tk.Label(self.rec_area, text="Select course, semester and subject then click Search.",
                 bg=BG_DARK, fg=TEXT_GRAY, font=("Segoe UI", 11)).pack(pady=40)

    def load_saved_records(self):
        for w in self.rec_area.winfo_children():
            w.destroy()

        course = self.rec_course.get()
        sem = self.rec_sem.get()
        subj = self.rec_subject.get().strip()

        matches = {k: v for k, v in self.data["attendance"].items()
                   if v["course"] == course and v["sem"] == sem
                   and (not subj or v["subject"].lower() == subj.lower())}

        if not matches:
            tk.Label(self.rec_area, text="No records found for the selected filters.",
                     bg=BG_DARK, fg=TEXT_GRAY, font=("Segoe UI", 11)).pack(pady=40)
            return

        # Session list on left, detail on right
        paned = tk.Frame(self.rec_area, bg=BG_DARK)
        paned.pack(fill="both", expand=True)

        list_frame = tk.Frame(paned, bg=BG_CARD, width=280,
                              highlightthickness=1, highlightbackground=BORDER)
        list_frame.pack(side="left", fill="y", padx=(0, 8))
        list_frame.pack_propagate(False)

        tk.Label(list_frame, text="Sessions", bg=BG_CARD, fg=ACCENT,
                 font=("Segoe UI", 11, "bold")).pack(pady=10)

        detail_frame = tk.Frame(paned, bg=BG_DARK)
        detail_frame.pack(side="right", fill="both", expand=True)

        def show_record(key, record):
            for w in detail_frame.winfo_children():
                w.destroy()

            info = tk.Frame(detail_frame, bg=BG_CARD2, highlightthickness=1,
                            highlightbackground=BORDER)
            info.pack(fill="x", pady=(0, 8), ipadx=10, ipady=8)
            tk.Label(info, text=f"📚 {record['course']} | {record['sem']} | {record['subject']}  "
                                f"•  📅 {record['date']}  🕐 {record['time']}",
                     bg=BG_CARD2, fg=ACCENT, font=("Segoe UI", 10, "bold")).pack(side="left", padx=10)

            styled_button(info, "🗑 Delete Session",
                          lambda k=key: self.delete_record(k),
                          color="#3a1e1e", fg=DANGER, font_size=9).pack(side="right", padx=10)

            # Editable student rows
            self.edit_records = {}  # roll -> {status_var, note_var}

            # Table header
            hdr = tk.Frame(detail_frame, bg=BG_CARD2)
            hdr.pack(fill="x")
            for col, w in [("#", 4), ("Roll", 8), ("Name", 20), ("Status", 12), ("Note", 24)]:
                tk.Label(hdr, text=col, bg=BG_CARD2, fg=ACCENT,
                         font=("Segoe UI", 9, "bold"), width=w, anchor="w").pack(side="left", padx=6, pady=6)

            scroll_c = tk.Frame(detail_frame, bg=BG_DARK)
            scroll_c.pack(fill="both", expand=True)
            canvas = tk.Canvas(scroll_c, bg=BG_DARK, highlightthickness=0)
            sb = ttk.Scrollbar(scroll_c, orient="vertical", command=canvas.yview)
            sb.pack(side="right", fill="y")
            canvas.pack(fill="both", expand=True)
            canvas.configure(yscrollcommand=sb.set)
            inner = tk.Frame(canvas, bg=BG_DARK)
            canvas.create_window((0, 0), window=inner, anchor="nw")
            inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            for i, rec in enumerate(record.get("records", [])):
                bg = BG_CARD if i % 2 == 0 else BG_CARD2
                row = tk.Frame(inner, bg=bg, highlightthickness=1, highlightbackground=BORDER)
                row.pack(fill="x", pady=1)

                tk.Label(row, text=str(i + 1), bg=bg, fg=TEXT_GRAY,
                         width=4, anchor="w", font=("Segoe UI", 9)).pack(side="left", padx=6, pady=6)
                tk.Label(row, text=rec["roll"], bg=bg, fg=TEXT_WHITE,
                         width=8, anchor="w", font=("Segoe UI", 10)).pack(side="left", padx=6)
                tk.Label(row, text=rec["name"], bg=bg, fg=TEXT_WHITE,
                         width=20, anchor="w", font=("Segoe UI", 10)).pack(side="left", padx=6)

                status_var = tk.StringVar(value=rec.get("status", "Present"))
                clr = SUCCESS if status_var.get() == "Present" else DANGER
                status_menu = tk.OptionMenu(row, status_var, "Present", "Absent")
                status_menu.config(bg=bg, fg=clr, font=("Segoe UI", 9),
                                   relief="flat", bd=0, width=8,
                                   highlightthickness=0, activebackground=BG_CARD2)
                status_menu.pack(side="left", padx=6)

                note_entry = styled_entry(row, width=22)
                note_entry.pack(side="left", padx=6, pady=3, ipady=3)
                note_entry.insert(0, rec.get("note", ""))

                self.edit_records[rec["roll"]] = {
                    "status": status_var, "note": note_entry
                }

            # Save changes
            def save_changes(k=key, r=record):
                for roll_, widgets in self.edit_records.items():
                    for rec_ in r["records"]:
                        if rec_["roll"] == roll_:
                            rec_["status"] = widgets["status"].get()
                            rec_["note"] = widgets["note"].get().strip()
                self.data["attendance"][k] = r
                save_data(self.data)
                messagebox.showinfo("Saved", "✅ Changes saved successfully!")

            styled_button(detail_frame, "💾 Save Changes", save_changes,
                          color=SUCCESS, fg=BG_DARK).pack(side="bottom", pady=8, anchor="e", padx=10)

        # Session list buttons
        list_scroll = tk.Frame(list_frame, bg=BG_CARD)
        list_scroll.pack(fill="both", expand=True)

        for k, v in sorted(matches.items(), key=lambda x: x[1].get("date", ""), reverse=True):
            btn = tk.Button(list_scroll,
                            text=f"📅 {v['date']}\n🕐 {v['time']}\n📖 {v['subject']}",
                            command=lambda key=k, rec=v: show_record(key, rec),
                            bg=BG_CARD, fg=TEXT_WHITE, font=("Segoe UI", 9),
                            relief="flat", cursor="hand2", anchor="w",
                            padx=10, pady=6, justify="left",
                            activebackground=BG_CARD2, activeforeground=ACCENT)
            btn.pack(fill="x", padx=4, pady=2)

    def delete_record(self, key):
        if messagebox.askyesno("Delete", "Delete this attendance session?"):
            del self.data["attendance"][key]
            save_data(self.data)
            self.load_saved_records()

    # ═══ TIMETABLE ════════════════════════════════════════════════════════════
    def page_timetable(self):
        outer = self.content
        tk.Label(outer, text="Timetable", bg=BG_DARK, fg=TEXT_WHITE,
                 font=("Georgia", 22, "bold")).pack(anchor="w", padx=24, pady=(20, 4))
        tk.Label(outer, text="Click any cell to view or assign subjects — 7 periods per day",
                 bg=BG_DARK, fg=TEXT_GRAY, font=("Segoe UI", 10)).pack(anchor="w", padx=24, pady=(0, 10))

        # Course/Sem selector
        sel = tk.Frame(outer, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
        sel.pack(fill="x", padx=20, pady=4, ipadx=10, ipady=8)

        row = tk.Frame(sel, bg=BG_CARD)
        row.pack(fill="x", padx=10)

        for lbl, attr, values in [
            ("Course", "tt_course", COURSES),
            ("Semester", "tt_sem", SEMESTERS),
        ]:
            tk.Label(row, text=lbl + ":", bg=BG_CARD, fg=TEXT_GRAY,
                     font=("Segoe UI", 10)).pack(side="left", padx=(10, 4))
            cb = styled_combo(row, values, width=14)
            cb.set(values[0])
            cb.pack(side="left", padx=4)
            setattr(self, attr, cb)
            cb.bind("<<ComboboxSelected>>", lambda e: self.render_timetable())

        self.tt_grid_frame = tk.Frame(outer, bg=BG_DARK)
        self.tt_grid_frame.pack(fill="both", expand=True, padx=20, pady=8)
        self.render_timetable()

    def render_timetable(self):
        for w in self.tt_grid_frame.winfo_children():
            w.destroy()

        course = self.tt_course.get()
        sem = self.tt_sem.get()
        tt_key = f"{course}|{sem}"

        if tt_key not in self.data["timetable"]:
            self.data["timetable"][tt_key] = {}

        tt = self.data["timetable"][tt_key]

        canvas = tk.Canvas(self.tt_grid_frame, bg=BG_DARK, highlightthickness=0)
        sb_x = ttk.Scrollbar(self.tt_grid_frame, orient="horizontal", command=canvas.xview)
        sb_y = ttk.Scrollbar(self.tt_grid_frame, orient="vertical", command=canvas.yview)
        sb_x.pack(side="bottom", fill="x")
        sb_y.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        canvas.configure(xscrollcommand=sb_x.set, yscrollcommand=sb_y.set)

        inner = tk.Frame(canvas, bg=BG_DARK)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Period header
        tk.Label(inner, text="Day / Period", bg=BG_CARD2, fg=ACCENT,
                 font=("Segoe UI", 9, "bold"), width=12, relief="flat",
                 bd=0, pady=12).grid(row=0, column=0, padx=1, pady=1, sticky="nsew")

        period_labels = ["08:00-09:00", "09:00-10:00", "10:00-11:00",
                         "11:00-12:00", "01:00-02:00", "02:00-03:00", "03:00-04:00"]

        for j, plbl in enumerate(period_labels):
            tk.Label(inner, text=f"P{j+1}\n{plbl}", bg=BG_CARD2, fg=ACCENT,
                     font=("Segoe UI", 8, "bold"), width=13, relief="flat",
                     bd=0, pady=8, justify="center").grid(row=0, column=j + 1, padx=1, pady=1, sticky="nsew")

        for i, day in enumerate(DAYS):
            tk.Label(inner, text=day, bg=BG_CARD, fg=TEXT_WHITE,
                     font=("Segoe UI", 10, "bold"), width=12, relief="flat",
                     bd=0, pady=12).grid(row=i + 1, column=0, padx=1, pady=1, sticky="nsew")

            for j in range(7):
                cell_key = f"{day}|P{j+1}"
                cell_data = tt.get(cell_key, {})
                subj = cell_data.get("subject", "")
                has_data = bool(subj)

                bg = BG_CARD if (i + j) % 2 == 0 else BG_CARD2
                cell_bg = "#1a3a2a" if has_data else bg

                cell = tk.Frame(inner, bg=cell_bg, highlightthickness=1,
                                highlightbackground=BORDER if not has_data else SUCCESS,
                                cursor="hand2", width=110, height=60)
                cell.grid(row=i + 1, column=j + 1, padx=1, pady=1, sticky="nsew")
                cell.pack_propagate(False)

                if has_data:
                    tk.Label(cell, text=subj, bg=cell_bg, fg=SUCCESS,
                             font=("Segoe UI", 9, "bold"), wraplength=100).pack(expand=True)
                    info_text = cell_data.get("info", "")
                    if info_text:
                        tk.Label(cell, text=info_text, bg=cell_bg, fg=TEXT_GRAY,
                                 font=("Segoe UI", 7), wraplength=100).pack()
                else:
                    tk.Label(cell, text="＋\nClick to add", bg=cell_bg, fg=BORDER,
                             font=("Segoe UI", 8), justify="center").pack(expand=True)

                cell.bind("<Button-1>",
                          lambda e, dk=day, pj=j + 1, ck=cell_key:
                          self.edit_cell(tt_key, dk, pj, ck, period_labels[pj - 1]))
                for child in cell.winfo_children():
                    child.bind("<Button-1>",
                               lambda e, dk=day, pj=j + 1, ck=cell_key:
                               self.edit_cell(tt_key, dk, pj, ck, period_labels[pj - 1]))

    def edit_cell(self, tt_key, day, period_num, cell_key, period_time):
        cell_data = self.data["timetable"][tt_key].get(cell_key, {})

        win = tk.Toplevel(self.root)
        win.title(f"{day} — Period {period_num}")
        win.geometry("420x380")
        win.configure(bg=BG_DARK)
        win.grab_set()

        course, sem = tt_key.split("|")
        tk.Label(win, text=f"📅 {day}  •  Period {period_num}  •  🕐 {period_time}",
                 bg=BG_DARK, fg=ACCENT, font=("Segoe UI", 11, "bold")).pack(pady=(16, 4))
        tk.Label(win, text=f"{course}  •  {sem}",
                 bg=BG_DARK, fg=TEXT_GRAY, font=("Segoe UI", 10)).pack(pady=(0, 12))

        card = tk.Frame(win, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
        card.pack(padx=24, fill="x", ipady=10)

        tk.Label(card, text="Subject / Paper:", bg=BG_CARD, fg=TEXT_GRAY,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=16, pady=(12, 2))
        subj_e = styled_entry(card, width=38)
        subj_e.pack(padx=16, ipady=5)
        subj_e.insert(0, cell_data.get("subject", ""))

        tk.Label(card, text="Additional Info (e.g. Lab / Elective):", bg=BG_CARD, fg=TEXT_GRAY,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=16, pady=(10, 2))
        info_e = styled_entry(card, width=38)
        info_e.pack(padx=16, ipady=5)
        info_e.insert(0, cell_data.get("info", ""))

        # Show current cell summary if filled
        if cell_data.get("subject"):
            tk.Label(win, text=f"Current: {cell_data['subject']}  {cell_data.get('info', '')}",
                     bg=BG_DARK, fg=SUCCESS, font=("Segoe UI", 9)).pack(pady=6)

        def save():
            subj = subj_e.get().strip()
            info = info_e.get().strip()
            if subj:
                self.data["timetable"][tt_key][cell_key] = {
                    "subject": subj, "info": info,
                    "day": day, "period": period_num,
                    "time": period_time, "course": course, "sem": sem
                }
            else:
                self.data["timetable"][tt_key].pop(cell_key, None)
            save_data(self.data)
            win.destroy()
            self.render_timetable()

        def clear():
            self.data["timetable"][tt_key].pop(cell_key, None)
            save_data(self.data)
            win.destroy()
            self.render_timetable()

        btn_row = tk.Frame(win, bg=BG_DARK)
        btn_row.pack(pady=16)
        styled_button(btn_row, "💾 Save", save, color=SUCCESS, fg=BG_DARK).pack(side="left", padx=6)
        styled_button(btn_row, "🗑 Clear", clear, color="#3a1e1e", fg=DANGER).pack(side="left", padx=6)
        styled_button(btn_row, "Cancel", win.destroy, color=BG_CARD, fg=TEXT_GRAY).pack(side="left", padx=6)


# ─── Entry Point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()