import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import random
import pickle
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict

class TimetableGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("School Timetable Generator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#FFFFFF")  # Light green background
        
        # Data storage
        self.school_data = {}
        self.classes_data = []
        self.teachers_data = []
        self.subjects_data = {}
        self.timetables = {}
        self.stream_data = {}  # Store stream information for classes 11-12
        
        # Board curricula with stream-based subjects for 11-12
        self.board_subjects = {
            "CBSE": {
                1: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                2: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                3: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                4: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                5: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                6: ["English", "Hindi", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                7: ["English", "Hindi", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                8: ["English", "Hindi", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                9: ["English", "Hindi", "Mathematics", "Science", "Social Science", "Physical Education", "Computer Science", "REGIONAL_LANGUAGE"],
                10: ["English", "Hindi", "Mathematics", "Science", "Social Science", "Physical Education", "Computer Science", "REGIONAL_LANGUAGE"],
            },
            "ICSE": {
                1: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                2: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                3: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                4: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                5: ["English", "Hindi", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                6: ["English", "Hindi", "Mathematics", "Science", "History", "Geography", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                7: ["English", "Hindi", "Mathematics", "Science", "History", "Geography", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                8: ["English", "Hindi", "Mathematics", "Science", "History", "Geography", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                9: ["English", "Hindi", "Mathematics", "Physics", "Chemistry", "Biology", "History", "Geography", "Computer Applications", "REGIONAL_LANGUAGE"],
                10: ["English", "Hindi", "Mathematics", "Physics", "Chemistry", "Biology", "History", "Geography", "Computer Applications", "REGIONAL_LANGUAGE"],
            },
            "State Board": {
                1: ["English", "Regional Language", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                2: ["English", "Regional Language", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                3: ["English", "Regional Language", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                4: ["English", "Regional Language", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                5: ["English", "Regional Language", "Mathematics", "EVS", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                6: ["English", "Regional Language", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                7: ["English", "Regional Language", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                8: ["English", "Regional Language", "Mathematics", "Science", "Social Science", "Art", "Physical Education", "REGIONAL_LANGUAGE"],
                9: ["English", "Regional Language", "Mathematics", "Science", "Social Science", "Physical Education", "REGIONAL_LANGUAGE"],
                10: ["English", "Regional Language", "Mathematics", "Science", "Social Science", "Physical Education", "REGIONAL_LANGUAGE"],
            }
        }

        # Stream-based subjects for classes 11-12
        self.stream_subjects = {
            "Science": {
                "core": ["English", "Physics", "Chemistry", "Mathematics", "REGIONAL_LANGUAGE"],
                "optional": ["Biology", "Computer Science", "Physical Education"],
                "labs": ["Physics Lab", "Chemistry Lab", "Biology Lab", "Computer Lab"]
            },
            "Commerce": {
                "core": ["English", "Accountancy", "Business Studies", "Economics", "REGIONAL_LANGUAGE"],
                "optional": ["Mathematics", "Computer Science", "Physical Education", "Entrepreneurship"],
                "labs": ["Computer Lab", "Business Lab"]
            },
            "Arts/Humanities": {
                "core": ["English", "History", "Political Science", "Geography", "REGIONAL_LANGUAGE"],
                "optional": ["Psychology", "Sociology", "Economics", "Philosophy", "Physical Education"],
                "labs": ["Computer Lab", "Geography Lab"]
            }
        }

        # Add ECA and lab data storage
        self.eca_data = {}
        self.lab_data = {}
        self.extra_class_data = {}
        
        # Initialize field variables
        self.primary_fields = {}
        self.secondary_fields = {}
        self.senior_secondary_fields = {}
        
        self.current_frame = None
        self.create_main_menu()
        
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
    
    def create_home_button(self, parent_frame):
        """Create a HOME button that appears on all pages except main menu"""
        home_btn = tk.Button(parent_frame, text="🏠 HOME", command=self.create_main_menu,
                           font=('Arial', 10, 'bold'), bg='#FFB6C1', fg='black',
                           relief='raised', bd=2, width=10)
        home_btn.pack(side='top', anchor='ne', padx=10, pady=5)
        return home_btn
    
    def create_styled_button(self, parent, text, command, width=20, height=2, bg_color='#87CEEB'):
        """Create a styled button matching the design"""
        btn = tk.Button(parent, text=text, command=command,
                       font=('Arial', 12, 'bold'), width=width, height=height,
                       bg=bg_color, fg='black', relief='raised', bd=3,
                       cursor='hand2')
        return btn

    def create_scrollable_frame(self, parent):
        """Create a scrollable frame with both vertical and horizontal scrollbars"""
        # Create canvas and scrollbars
        canvas = tk.Canvas(parent, bg='white')
        v_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        return scrollable_frame
            
    def create_main_menu(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#FFFFFF")  # Light green
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Main container with rounded appearance
        main_container = tk.Frame(self.current_frame, bg="#FFFFFF", relief='solid', bd=3)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header section with pink background
        header_frame = tk.Frame(main_container, bg='#FFB6C1', height=120, relief='solid', bd=2)  # Pink background
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="SCHOOL TIMETABLE GENERATOR", 
                        font=('Arial', 24, 'bold'), bg='#FFB6C1', fg='black')
        title.pack(expand=True)
        
        # Buttons section
        buttons_container = tk.Frame(main_container, bg="#FFFFFF")
        buttons_container.pack(expand=True, pady=20)
        
        # Top row buttons
        top_buttons_frame = tk.Frame(buttons_container, bg="#FFFFFF")
        top_buttons_frame.pack(pady=20)
        
        # Create styled buttons matching the design
        school_btn = self.create_styled_button(top_buttons_frame, "SCHOOL DETAILS", self.school_details_screen)
        school_btn.pack(side='left', padx=15)
        
        class_btn = self.create_styled_button(top_buttons_frame, "CLASS DETAILS", self.class_details_screen)
        class_btn.pack(side='left', padx=15)
        
        subject_btn = self.create_styled_button(top_buttons_frame, "SUBJECT DETAILS", self.subject_details_screen)
        subject_btn.pack(side='left', padx=15)
        
        teacher_btn = self.create_styled_button(top_buttons_frame, "TEACHER DETAILS", self.teacher_details_screen)
        teacher_btn.pack(side='left', padx=15)
        
        # Middle row buttons - NEW FEATURES
        middle_buttons_frame = tk.Frame(buttons_container, bg="#FFFFFF")
        middle_buttons_frame.pack(pady=10)
        
        teachers_list_btn = self.create_styled_button(middle_buttons_frame, "TEACHER'S LIST", self.teachers_details_view_screen)
        teachers_list_btn.pack(side='left', padx=15)
        
        # NEW: Teacher's Timetable button
        teacher_timetable_btn = self.create_styled_button(middle_buttons_frame, "TEACHER'S TIMETABLE", self.teacher_timetable_screen, bg_color='#FFD700')
        teacher_timetable_btn.pack(side='left', padx=15)
        
        # NEW: Substitution button
        substitution_btn = self.create_styled_button(middle_buttons_frame, "SUBSTITUTION", self.substitution_screen, bg_color='#FFA500')
        substitution_btn.pack(side='left', padx=15)
        
        # Bottom row button
        bottom_buttons_frame = tk.Frame(buttons_container, bg="#FFFFFF")
        bottom_buttons_frame.pack(pady=20)
        
        generate_btn = self.create_styled_button(bottom_buttons_frame, "GENERATE TIME TABLE", 
                                                self.generate_timetable_screen, width=25)
        generate_btn.pack()
        
        # Export button
        export_btn = self.create_styled_button(bottom_buttons_frame, "EXPORT TIMETABLE", 
                                             self.export_timetable_screen, width=25)
        export_btn.pack(pady=10)
        
        # File operations
        file_frame = tk.Frame(buttons_container, bg="#FFFFFF")
        file_frame.pack(pady=20)
        
        save_btn = self.create_styled_button(file_frame, "SAVE PROJECT", self.save_project, width=15, bg_color="#FFFFFF")
        save_btn.pack(side='left', padx=10)
        
        load_btn = self.create_styled_button(file_frame, "LOAD PROJECT", self.load_project, width=15, bg_color="#FFFFFF")
        load_btn.pack(side='left', padx=10)

    # NEW FEATURE 1: Teacher's Timetable Screen
    def teacher_timetable_screen(self):
        """NEW FEATURE: Display individual teacher's timetable by Employee ID"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add HOME button
        self.create_home_button(self.current_frame)
        
        # Title
        title_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=3)
        title_frame.pack(fill='x', pady=10)
        
        title_label = tk.Label(title_frame, text="TEACHER'S TIMETABLE", 
                              font=('Arial', 18, 'bold'), bg='white', fg='black')
        title_label.pack(pady=15)
        
        # Check if timetables exist
        if not self.timetables or not self.teachers_data:
            message_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
            message_frame.pack(expand=True, padx=50, pady=50)
            
            if not self.teachers_data:
                tk.Label(message_frame, text="No Teachers Added Yet!", 
                        font=('Arial', 16, 'bold'), bg='white', fg='red').pack(pady=20)
                tk.Label(message_frame, text="Please add teachers first.", 
                        font=('Arial', 12), bg='white').pack(pady=10)
                
                add_teachers_btn = self.create_styled_button(message_frame, "Add Teachers", 
                                                           self.teacher_details_screen, width=15, bg_color='lightgreen')
                add_teachers_btn.pack(pady=10)
            else:
                tk.Label(message_frame, text="No Timetables Generated Yet!", 
                        font=('Arial', 16, 'bold'), bg='white', fg='red').pack(pady=20)
                tk.Label(message_frame, text="Please generate timetables first.", 
                        font=('Arial', 12), bg='white').pack(pady=10)
                
                generate_btn = self.create_styled_button(message_frame, "Generate Timetables", 
                                                        self.generate_timetable_screen, width=15, bg_color='lightgreen')
                generate_btn.pack(pady=10)
            
            back_btn = self.create_styled_button(message_frame, "Back to Home", 
                                               self.create_main_menu, width=15, bg_color='lightcoral')
            back_btn.pack(pady=10)
            return
        
        # Main content frame with scrollable area
        content_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        content_frame.pack(fill='both', expand=True, pady=10)
        
        scrollable_frame = self.create_scrollable_frame(content_frame)
        
        # Employee ID input section
        input_frame = tk.Frame(scrollable_frame, bg='white')
        input_frame.pack(fill='x', padx=20, pady=20)
        
        # Employee ID label and input
        tk.Label(input_frame, text="Employee ID:", font=('Arial', 14, 'bold'), 
                bg='white').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        self.teacher_id_entry = tk.Entry(input_frame, font=('Arial', 12), width=20, relief='solid', bd=2)
        self.teacher_id_entry.grid(row=0, column=1, padx=10, pady=10)
        self.teacher_id_entry.bind('<Return>', self.search_teacher_timetable)
        
        # Search button
        search_btn = self.create_styled_button(input_frame, "SEARCH", self.search_teacher_timetable, 
                                             width=12, height=1, bg_color='#87CEEB')
        search_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Teacher selection dropdown (alternative method)
        tk.Label(input_frame, text="Or Select Teacher:", font=('Arial', 12, 'bold'), 
                bg='white').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        
        self.selected_teacher_var = tk.StringVar()
        teacher_options = [f"{teacher['name']} (ID: {teacher['employee_id']})" 
                          for teacher in sorted(self.teachers_data, key=lambda x: x['name'].lower())]
        
        teacher_combo = ttk.Combobox(input_frame, textvariable=self.selected_teacher_var,
                                   values=teacher_options, width=35, font=('Arial', 10))
        teacher_combo.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky='w')
        teacher_combo.bind('<<ComboboxSelected>>', self.load_selected_teacher_timetable)
        
        # Teacher info display area
        self.teacher_info_frame = tk.Frame(scrollable_frame, bg='white')
        self.teacher_info_frame.pack(fill='x', padx=20, pady=10)
        
        # Timetable display area
        self.teacher_timetable_container = tk.Frame(scrollable_frame, bg='white')
        self.teacher_timetable_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Instructions
        instruction_label = tk.Label(scrollable_frame, 
                                    text="Enter Employee ID or select from dropdown to display teacher's timetable and workload status",
                                    font=('Arial', 10), bg='white', fg='gray')
        instruction_label.pack(pady=10)
        
        # Back button
        btn_frame = tk.Frame(self.current_frame, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        back_btn = self.create_styled_button(btn_frame, "Back to Home", self.create_main_menu, 
                                           width=15, bg_color='lightcoral')
        back_btn.pack()

    def search_teacher_timetable(self, event=None):
        """Search and display teacher timetable by Employee ID"""
        emp_id = self.teacher_id_entry.get().strip()
        if not emp_id:
            messagebox.showerror("Error", "Please enter Employee ID")
            return
        
        # Find teacher by employee ID
        teacher = None
        for t in self.teachers_data:
            if t['employee_id'].lower() == emp_id.lower():
                teacher = t
                break
        
        if not teacher:
            messagebox.showerror("Error", f"Teacher with Employee ID '{emp_id}' not found")
            return
        
        self.display_teacher_timetable(teacher)

    def load_selected_teacher_timetable(self, event=None):
        """Load teacher timetable from dropdown selection"""
        selected = self.selected_teacher_var.get()
        if not selected:
            return
        
        # Extract employee ID from selection
        emp_id = selected.split("ID: ")[1].rstrip(")")
        
        # Find teacher
        teacher = None
        for t in self.teachers_data:
            if t['employee_id'] == emp_id:
                teacher = t
                break
        
        if teacher:
            self.teacher_id_entry.delete(0, tk.END)
            self.teacher_id_entry.insert(0, teacher['employee_id'])
            self.display_teacher_timetable(teacher)

    def display_teacher_timetable(self, teacher):
        """Display the selected teacher's timetable and workload status"""
        # Clear previous displays
        for widget in self.teacher_info_frame.winfo_children():
            widget.destroy()
        for widget in self.teacher_timetable_container.winfo_children():
            widget.destroy()
        
        # Display teacher information
        info_header = tk.Label(self.teacher_info_frame, text="TEACHER INFORMATION", 
                              font=('Arial', 12, 'bold'), bg='white', fg='navy')
        info_header.pack(anchor='w', pady=5)
        
        teacher_name_label = tk.Label(self.teacher_info_frame, text=f"Name: {teacher['name']}", 
                                     font=('Arial', 14, 'bold'), bg='white', fg='black')
        teacher_name_label.pack(anchor='w', pady=2)
        
        teacher_id_label = tk.Label(self.teacher_info_frame, text=f"Employee ID: {teacher['employee_id']}", 
                                   font=('Arial', 12), bg='white', fg='black')
        teacher_id_label.pack(anchor='w', pady=2)
        
        subjects_label = tk.Label(self.teacher_info_frame, text=f"Subjects: {', '.join(teacher['subjects'])}", 
                                 font=('Arial', 12), bg='white', fg='black')
        subjects_label.pack(anchor='w', pady=2)
        
        classes_label = tk.Label(self.teacher_info_frame, text=f"Classes: {', '.join(teacher['classes'])}", 
                                font=('Arial', 12), bg='white', fg='black')
        classes_label.pack(anchor='w', pady=2)
        
        # Calculate and display workload status
        workload = self.calculate_teacher_workload(teacher)
        
        workload_frame = tk.LabelFrame(self.teacher_info_frame, text="WORKLOAD STATUS", 
                                      bg='white', font=('Arial', 12, 'bold'))
        workload_frame.pack(fill='x', pady=10)
        
        workload_info = tk.Frame(workload_frame, bg='white')
        workload_info.pack(fill='x', padx=10, pady=5)
        
        tk.Label(workload_info, text=f"Total Weekly Periods: {workload['total_periods']}", 
                font=('Arial', 11), bg='white').pack(anchor='w')
        tk.Label(workload_info, text=f"Average Periods/Day: {workload['avg_periods']:.1f}", 
                font=('Arial', 11), bg='white').pack(anchor='w')
        
        status_color = 'red' if workload['status'] == 'Heavy' else 'orange' if workload['status'] == 'Moderate' else 'green'
        tk.Label(workload_info, text=f"Workload Status: {workload['status']}", 
                font=('Arial', 11, 'bold'), bg='white', fg=status_color).pack(anchor='w')
        
        # Create timetable display
        timetable_label = tk.Label(self.teacher_timetable_container, text="PERSONAL TIMETABLE", 
                                  font=('Arial', 12, 'bold'), bg='white', fg='navy')
        timetable_label.pack(pady=10)
        
        # Generate teacher's consolidated timetable
        teacher_schedule = self.generate_teacher_schedule(teacher)
        
        if not teacher_schedule or not any(teacher_schedule.values()):
            tk.Label(self.teacher_timetable_container, text="No schedule found for this teacher", 
                    font=('Arial', 14), bg='white', fg='red').pack(pady=50)
            return
        
        # Create timetable grid
        table_frame = tk.Frame(self.teacher_timetable_container, bg='white', relief='solid', bd=2)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        working_days = self.school_data.get('working_days', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        
        # Headers
        tk.Label(table_frame, text="Time", font=('Arial', 11, 'bold'), 
                relief='solid', bd=1, bg='lightgray', width=12).grid(row=0, column=0, sticky='nsew')
        
        for col, day in enumerate(working_days, 1):
            tk.Label(table_frame, text=day, font=('Arial', 11, 'bold'), 
                    relief='solid', bd=1, bg='lightgray', width=15).grid(row=0, column=col, sticky='nsew')
        
        # Get all unique time slots
        all_times = set()
        for day_schedule in teacher_schedule.values():
            for slot in day_schedule:
                all_times.add(slot['time'])
        
        sorted_times = sorted(list(all_times))
        
        # Display schedule
        for row, time_slot in enumerate(sorted_times, 1):
            tk.Label(table_frame, text=time_slot, font=('Arial', 10), 
                    relief='solid', bd=1, bg='white', width=12).grid(row=row, column=0, sticky='nsew')
            
            for col, day in enumerate(working_days, 1):
                cell_text = ""
                cell_color = 'white'
                
                if day in teacher_schedule:
                    for slot in teacher_schedule[day]:
                        if slot['time'] == time_slot:
                            cell_text = f"{slot['subject']}\n{slot['class']}"
                            cell_color = 'lightblue'
                            break
                
                if not cell_text:
                    cell_text = "Free"
                    cell_color = 'lightgreen'
                
                tk.Label(table_frame, text=cell_text, font=('Arial', 9), 
                        relief='solid', bd=1, bg=cell_color, width=15, 
                        wraplength=100, justify='center').grid(row=row, column=col, sticky='nsew')
        
        # Configure grid weights for proper resizing
        for i in range(len(working_days) + 1):
            table_frame.columnconfigure(i, weight=1)
        for i in range(len(sorted_times) + 1):
            table_frame.rowconfigure(i, weight=1)

    def generate_teacher_schedule(self, teacher):
        """Generate consolidated schedule for a specific teacher"""
        teacher_schedule = {}
        working_days = self.school_data.get('working_days', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        
        for day in working_days:
            teacher_schedule[day] = []
        
        # Go through all class timetables and extract teacher's periods
        for class_key, timetable in self.timetables.items():
            if class_key in teacher['classes']:
                for day, slots in timetable.items():
                    if day in working_days:
                        for slot in slots:
                            if (slot.get('type') == 'period' and 
                                slot.get('teacher') == teacher['name'] and
                                slot.get('subject') in teacher['subjects']):
                                
                                teacher_schedule[day].append({
                                    'time': slot['time'],
                                    'subject': slot['subject'],
                                    'class': class_key,
                                    'type': 'teaching'
                                })
        
        return teacher_schedule

    # NEW FEATURE 2: Substitution Screen
    def substitution_screen(self):
        """NEW FEATURE: Find substitute teachers based on availability and workload"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add HOME button
        self.create_home_button(self.current_frame)
        
        # Title
        title_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=3)
        title_frame.pack(fill='x', pady=10)
        
        title_label = tk.Label(title_frame, text="SUBSTITUTION SYSTEM", 
                              font=('Arial', 18, 'bold'), bg='white', fg='black')
        title_label.pack(pady=15)
        
        # Check if required data exists
        if not self.timetables or not self.teachers_data:
            message_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
            message_frame.pack(expand=True, padx=50, pady=50)
            
            tk.Label(message_frame, text="Prerequisites Not Met!", 
                    font=('Arial', 16, 'bold'), bg='white', fg='red').pack(pady=20)
            
            if not self.teachers_data:
                tk.Label(message_frame, text="Please add teachers first.", 
                        font=('Arial', 12), bg='white').pack(pady=5)
            if not self.timetables:
                tk.Label(message_frame, text="Please generate timetables first.", 
                        font=('Arial', 12), bg='white').pack(pady=5)
            
            btn_frame = tk.Frame(message_frame, bg='white')
            btn_frame.pack(pady=20)
            
            if not self.teachers_data:
                add_teachers_btn = self.create_styled_button(btn_frame, "Add Teachers", 
                                                           self.teacher_details_screen, width=15, bg_color='lightgreen')
                add_teachers_btn.pack(side='left', padx=10)
            
            if not self.timetables:
                generate_btn = self.create_styled_button(btn_frame, "Generate Timetables", 
                                                        self.generate_timetable_screen, width=15, bg_color='lightblue')
                generate_btn.pack(side='left', padx=10)
            
            back_btn = self.create_styled_button(btn_frame, "Back to Home", 
                                               self.create_main_menu, width=15, bg_color='lightcoral')
            back_btn.pack(side='left', padx=10)
            return
        
        # Main content with scrollable area
        content_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        content_frame.pack(fill='both', expand=True, pady=10)
        
        scrollable_frame = self.create_scrollable_frame(content_frame)
        
        # Selection section
        selection_frame = tk.LabelFrame(scrollable_frame, text="Find Substitute Teacher", 
                                       bg='white', font=('Arial', 12, 'bold'))
        selection_frame.pack(fill='x', padx=20, pady=20)
        
        # Absent teacher Employee ID input
        tk.Label(selection_frame, text="Absent Teacher Employee ID:", 
                font=('Arial', 11, 'bold'), bg='white').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        self.absent_teacher_id_entry = tk.Entry(selection_frame, font=('Arial', 12), width=20, relief='solid', bd=2)
        self.absent_teacher_id_entry.grid(row=0, column=1, padx=10, pady=10)
        self.absent_teacher_id_entry.bind('<Return>', self.find_substitute_teachers)
        
        # Or dropdown selection
        tk.Label(selection_frame, text="Or Select Teacher:", 
                font=('Arial', 11, 'bold'), bg='white').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        
        self.absent_teacher_var = tk.StringVar()
        teacher_options = [f"{teacher['name']} (ID: {teacher['employee_id']})" 
                          for teacher in sorted(self.teachers_data, key=lambda x: x['name'].lower())]
        
        teacher_combo = ttk.Combobox(selection_frame, textvariable=self.absent_teacher_var,
                                   values=teacher_options, width=40, font=('Arial', 10))
        teacher_combo.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        teacher_combo.bind('<<ComboboxSelected>>', self.load_absent_teacher_id)
        
        # Day selection
        tk.Label(selection_frame, text="Select Day:", font=('Arial', 11, 'bold'), 
                bg='white').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        
        self.substitute_day_var = tk.StringVar()
        working_days = self.school_data.get('working_days', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        day_combo = ttk.Combobox(selection_frame, textvariable=self.substitute_day_var,
                               values=working_days, width=15, font=('Arial', 10))
        day_combo.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        
        # Find substitutes button
        find_btn = self.create_styled_button(selection_frame, "FIND SUBSTITUTES", 
                                           self.find_substitute_teachers, width=20, height=1, bg_color='#FFA500')
        find_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Results display area
        self.results_frame = tk.LabelFrame(scrollable_frame, text="Available Substitute Teachers", 
                                          bg='white', font=('Arial', 12, 'bold'))
        self.results_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = tk.Label(self.results_frame, 
                               text="Enter absent teacher's Employee ID and select day to find available substitutes.\nSubstitutes are ranked by workload (lighter workload = better substitute).",
                               font=('Arial', 10), bg='white', fg='gray', justify='center')
        instructions.pack(pady=20)
        
        # Back button
        btn_frame = tk.Frame(self.current_frame, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        back_btn = self.create_styled_button(btn_frame, "Back to Home", self.create_main_menu, 
                                           width=15, bg_color='lightcoral')
        back_btn.pack()

    def load_absent_teacher_id(self, event=None):
        """Load absent teacher ID from dropdown selection"""
        selected = self.absent_teacher_var.get()
        if not selected:
            return
        
        # Extract employee ID from selection
        emp_id = selected.split("ID: ")[1].rstrip(")")
        self.absent_teacher_id_entry.delete(0, tk.END)
        self.absent_teacher_id_entry.insert(0, emp_id)

    def find_substitute_teachers(self, event=None):
        """Find and display available substitute teachers"""
        emp_id = self.absent_teacher_id_entry.get().strip()
        selected_day = self.substitute_day_var.get()
        
        if not emp_id:
            messagebox.showerror("Error", "Please enter absent teacher's Employee ID")
            return
        
        if not selected_day:
            messagebox.showerror("Error", "Please select a day")
            return
        
        # Find absent teacher
        absent_teacher = None
        for t in self.teachers_data:
            if t['employee_id'].lower() == emp_id.lower():
                absent_teacher = t
                break
        
        if not absent_teacher:
            messagebox.showerror("Error", f"Teacher with Employee ID '{emp_id}' not found")
            return
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Get absent teacher's schedule for the selected day
        absent_teacher_schedule = self.generate_teacher_schedule(absent_teacher)
        
        if selected_day not in absent_teacher_schedule or not absent_teacher_schedule[selected_day]:
            tk.Label(self.results_frame, text=f"{absent_teacher['name']} has no classes on {selected_day}", 
                    font=('Arial', 14), bg='white', fg='orange').pack(pady=20)
            return
        
        # Find available substitute teachers for each period
        day_periods = absent_teacher_schedule[selected_day]
        
        # Header
        header_text = f"Substitute Teachers for {absent_teacher['name']} on {selected_day}"
        tk.Label(self.results_frame, text=header_text, 
                font=('Arial', 14, 'bold'), bg='white', fg='navy').pack(pady=10)
        
        # Create scrollable results area
        results_scroll_frame = self.create_scrollable_frame(self.results_frame)
        
        for period_info in day_periods:
            period_frame = tk.LabelFrame(results_scroll_frame, 
                                       text=f"Period: {period_info['time']} - {period_info['subject']} ({period_info['class']})", 
                                       bg='white', font=('Arial', 11, 'bold'))
            period_frame.pack(fill='x', padx=10, pady=10)
            
            # Find available substitutes for this specific period
            available_substitutes = []
            
            for teacher in self.teachers_data:
                if teacher['employee_id'] == absent_teacher['employee_id']:
                    continue  # Skip the absent teacher
                
                # Check if teacher can teach the subject
                if period_info['subject'] not in teacher['subjects']:
                    continue
                
                # Check if teacher is free at this time
                teacher_schedule = self.generate_teacher_schedule(teacher)
                is_free = True
                
                if selected_day in teacher_schedule:
                    for slot in teacher_schedule[selected_day]:
                        if slot['time'] == period_info['time']:
                            is_free = False
                            break
                
                if is_free:
                    # Calculate teacher's workload
                    workload = self.calculate_teacher_workload(teacher)
                    available_substitutes.append({
                        'teacher': teacher,
                        'workload': workload
                    })
            
            # Sort by workload (lighter workload first)
            available_substitutes.sort(key=lambda x: x['workload']['avg_periods'])
            
            # Display results for this period
            if not available_substitutes:
                tk.Label(period_frame, text="No available substitute teachers", 
                        font=('Arial', 12), bg='white', fg='red').pack(pady=10)
            else:
                # Create table for results
                table_frame = tk.Frame(period_frame, bg='white')
                table_frame.pack(fill='both', expand=True, padx=10, pady=10)
                
                # Table headers
                headers = ["Rank", "Teacher Name", "Employee ID", "Avg Periods/Day", "Workload Status"]
                for col, header in enumerate(headers):
                    tk.Label(table_frame, text=header, font=('Arial', 10, 'bold'), 
                            relief='solid', bd=1, bg='lightgray', width=15).grid(row=0, column=col, sticky='nsew')
                
                # Display substitute teachers (top 5 for each period)
                for row, substitute_info in enumerate(available_substitutes[:5], 1):
                    teacher = substitute_info['teacher']
                    workload = substitute_info['workload']
                    
                    # Rank
                    tk.Label(table_frame, text=str(row), font=('Arial', 10), 
                            relief='solid', bd=1, bg='white').grid(row=row, column=0, sticky='nsew')
                    
                    # Teacher name
                    tk.Label(table_frame, text=teacher['name'], font=('Arial', 10), 
                            relief='solid', bd=1, bg='white').grid(row=row, column=1, sticky='nsew')
                    
                    # Employee ID
                    tk.Label(table_frame, text=teacher['employee_id'], font=('Arial', 10), 
                            relief='solid', bd=1, bg='white').grid(row=row, column=2, sticky='nsew')
                    
                    # Average periods
                    tk.Label(table_frame, text=f"{workload['avg_periods']:.1f}", font=('Arial', 10), 
                            relief='solid', bd=1, bg='white').grid(row=row, column=3, sticky='nsew')
                    
                    # Workload status with color coding
                    status_color = 'red' if workload['status'] == 'Heavy' else 'orange' if workload['status'] == 'Moderate' else 'green'
                    tk.Label(table_frame, text=workload['status'], font=('Arial', 10), 
                            relief='solid', bd=1, bg='white', fg=status_color).grid(row=row, column=4, sticky='nsew')
                
                # Configure grid weights
                for i in range(len(headers)):
                    table_frame.columnconfigure(i, weight=1)

    def calculate_teacher_workload(self, teacher):
        """Calculate workload analysis for a teacher"""
        if not self.timetables:
            return {
                'avg_periods': 0,
                'total_periods': 0,
                'status': 'No Data',
                'daily_breakdown': {}
            }
        
        teacher_periods = {}
        total_periods = 0
        
        # Count periods for each day
        working_days = self.school_data.get('working_days', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        
        for day in working_days:
            teacher_periods[day] = 0
        
        # Go through all timetables and count teacher's periods
        for class_key, timetable in self.timetables.items():
            if class_key in teacher.get('classes', []):
                for day, slots in timetable.items():
                    if day in working_days:
                        for slot in slots:
                            if slot.get('type') == 'period' and slot.get('teacher') == teacher['name']:
                                teacher_periods[day] += 1
                                total_periods += 1
        
        # Calculate average
        avg_periods = total_periods / len(working_days) if working_days else 0
        
        # Determine workload status
        if avg_periods >= 6:
            status = 'Heavy'
        elif avg_periods >= 4:
            status = 'Moderate'
        else:
            status = 'Light'
        
        return {
            'avg_periods': avg_periods,
            'total_periods': total_periods,
            'status': status,
            'daily_breakdown': teacher_periods
        }

    # Enhanced existing methods with scroll bars
    def school_details_screen(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add HOME button
        self.create_home_button(self.current_frame)
        
        # Title
        title = tk.Label(self.current_frame, text="SCHOOL DETAILS", 
                        font=('Arial', 16, 'bold'), bg="#FFFFFF", fg='black')
        title.pack(pady=10)
        
        # Main form frame with scrollbars
        form_container = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        form_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        form_frame = self.create_scrollable_frame(form_container)
        
        # School name and board
        top_frame = tk.Frame(form_frame, bg='white')
        top_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(top_frame, text="ENTER SCHOOL NAME:", bg='white', font=('Arial', 10)).grid(row=0, column=0, sticky='w', padx=5)
        tk.Label(top_frame, text="(Enter the full name of your school)", bg='white', font=('Arial', 8), fg='gray').grid(row=0, column=2, sticky='w', padx=5)
        self.school_name_entry = tk.Entry(top_frame, width=30, font=('Arial', 10))
        self.school_name_entry.grid(row=0, column=1, padx=10)
        
        tk.Label(top_frame, text="SELECT BOARD:", bg='white', font=('Arial', 10)).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        tk.Label(top_frame, text="(Choose your school's curriculum board)", bg='white', font=('Arial', 8), fg='gray').grid(row=1, column=2, sticky='w', padx=5)
        self.board_var = tk.StringVar()
        board_combo = ttk.Combobox(top_frame, textvariable=self.board_var, values=list(self.board_subjects.keys()), 
                                  width=27, font=('Arial', 10))
        board_combo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(top_frame, text="SELECT REGION:", bg='white', font=('Arial', 10)).grid(row=2, column=0, sticky='w', padx=5, pady=5)
        tk.Label(top_frame, text="(Select your state/region for regional language)", bg='white', font=('Arial', 8), fg='gray').grid(row=2, column=2, sticky='w', padx=5)
        self.region_var = tk.StringVar()
        region_combo = ttk.Combobox(top_frame, textvariable=self.region_var, 
                                   values=["Tamil Nadu", "Karnataka", "Kerala", "Andhra Pradesh", "Telangana", "Maharashtra", "Gujarat", "Rajasthan", "Punjab", "Haryana", "Uttar Pradesh", "Bihar", "West Bengal", "Odisha", "Jharkhand", "Chhattisgarh", "Madhya Pradesh", "Assam", "Other"], 
                                   width=27, font=('Arial', 10))
        region_combo.grid(row=2, column=1, padx=10, pady=5)
        
        # Load existing data if available
        if self.school_data:
            self.school_name_entry.insert(0, self.school_data.get('name', ''))
            self.board_var.set(self.school_data.get('board', ''))
            self.region_var.set(self.school_data.get('region', ''))
        
        # Update timings frame to include senior secondary
        timings_frame = tk.Frame(form_frame, bg='white')
        timings_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Primary, Secondary, and Senior Secondary columns
        primary_frame = tk.LabelFrame(timings_frame, text="PRIMARY CLASS TIMINGS:", bg='white', font=('Arial', 10, 'bold'))
        primary_frame.pack(side='left', fill='both', expand=True, padx=5)

        secondary_frame = tk.LabelFrame(timings_frame, text="SECONDARY CLASS TIMINGS:", bg='white', font=('Arial', 10, 'bold'))
        secondary_frame.pack(side='left', fill='both', expand=True, padx=5)

        senior_secondary_frame = tk.LabelFrame(timings_frame, text="SENIOR SECONDARY CLASS TIMINGS:", bg='white', font=('Arial', 10, 'bold'))
        senior_secondary_frame.pack(side='left', fill='both', expand=True, padx=5)

        # Create timing fields for all three sections
        self.create_timing_fields(primary_frame, 'primary')
        self.create_timing_fields(secondary_frame, 'secondary')
        self.create_timing_fields(senior_secondary_frame, 'senior_secondary')
        
        # Working days
        days_frame = tk.LabelFrame(form_frame, text="SELECT WORKING DAYS:", bg='white', font=('Arial', 10, 'bold'))
        days_frame.pack(fill='x', padx=20, pady=10)
        
        days_inner = tk.Frame(days_frame, bg='white')
        days_inner.pack(pady=10)
        
        tk.Label(days_inner, text="(Select the days your school operates)", bg='white', font=('Arial', 8), fg='gray').pack()
        
        self.working_days = {}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        days_checkboxes = tk.Frame(days_inner, bg='white')
        days_checkboxes.pack(pady=5)
        
        for i, day in enumerate(days):
            var = tk.BooleanVar()
            self.working_days[day] = var
            # Load existing data
            if self.school_data and day in self.school_data.get('working_days', []):
                var.set(True)
            cb = tk.Checkbutton(days_checkboxes, text=day, variable=var, bg='white', font=('Arial', 10))
            cb.grid(row=0, column=i, padx=10)
        
        # Buttons
        btn_frame = tk.Frame(self.current_frame, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        save_btn = self.create_styled_button(btn_frame, "Save & Continue", self.save_school_details, width=15, bg_color='lightgreen')
        save_btn.pack(side='left', padx=10)

    def create_timing_fields(self, parent, level):
        fields = {}
        
        # School start timing
        tk.Label(parent, text="School start timing:", bg='white', font=('Arial', 9)).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        tk.Label(parent, text="(e.g., 9:00)", bg='white', font=('Arial', 7), fg='gray').grid(row=0, column=2, sticky='w', padx=2)
        fields['start_time'] = tk.Entry(parent, width=15, font=('Arial', 9))
        fields['start_time'].grid(row=0, column=1, padx=5, pady=2)
        
        # Prayer timing
        tk.Label(parent, text="Prayer timing:", bg='white', font=('Arial', 9)).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        tk.Label(parent, text="(e.g., 8:45)", bg='white', font=('Arial', 7), fg='gray').grid(row=1, column=2, sticky='w', padx=2)
        fields['prayer_time'] = tk.Entry(parent, width=15, font=('Arial', 9))
        fields['prayer_time'].grid(row=1, column=1, padx=5, pady=2)
        
        # Duration of period
        tk.Label(parent, text="Duration of period:", bg='white', font=('Arial', 9)).grid(row=2, column=0, sticky='w', padx=5, pady=2)
        fields['period_duration'] = tk.Entry(parent, width=15, font=('Arial', 9))
        fields['period_duration'].grid(row=2, column=1, padx=5, pady=2)
        tk.Label(parent, text="(in min, e.g., 40)", bg='white', font=('Arial', 7), fg='gray').grid(row=2, column=2, sticky='w', padx=2)
        
        # Dispersal time
        tk.Label(parent, text="Dispersal Time:", bg='white', font=('Arial', 9)).grid(row=3, column=0, sticky='w', padx=5, pady=2)
        tk.Label(parent, text="(e.g., 15:30)", bg='white', font=('Arial', 7), fg='gray').grid(row=3, column=2, sticky='w', padx=2)
        fields['dispersal_time'] = tk.Entry(parent, width=15, font=('Arial', 9))
        fields['dispersal_time'].grid(row=3, column=1, padx=5, pady=2)
        
        # Extra class checkbox for senior secondary only
        if level == 'senior_secondary':
            fields['extra_class_var'] = tk.BooleanVar()
            extra_class_cb = tk.Checkbutton(parent, text="Extra Class", variable=fields['extra_class_var'],
                                          bg='white', font=('Arial', 9), 
                                          command=lambda: self.toggle_extra_class_timing(level))
            extra_class_cb.grid(row=4, column=0, columnspan=3, pady=5)
            
            # Extra class timing (initially hidden)
            fields['extra_class_frame'] = tk.Frame(parent, bg='white')
            fields['extra_class_frame'].grid(row=5, column=0, columnspan=3, sticky='ew', padx=5, pady=5)
            fields['extra_class_frame'].grid_remove()  # Hide initially
            
            tk.Label(fields['extra_class_frame'], text="Extra Class Timing:", bg='white', font=('Arial', 8)).grid(row=0, column=0, sticky='w', padx=2)
            tk.Label(fields['extra_class_frame'], text="(e.g., 16:00-17:00)", bg='white', font=('Arial', 7), fg='gray').grid(row=1, column=0, padx=2)
            fields['extra_class_timing'] = tk.Entry(fields['extra_class_frame'], width=15, font=('Arial', 8))
            fields['extra_class_timing'].grid(row=0, column=1, padx=5)
        
        # Break timings section
        break_row = 6 if level == 'senior_secondary' else 4
        break_frame = tk.LabelFrame(parent, text="BREAK TIMINGS", bg='white', font=('Arial', 9, 'bold'))
        break_frame.grid(row=break_row, column=0, columnspan=3, sticky='ew', padx=5, pady=5)
        
        # 1st Break
        tk.Label(break_frame, text="1ST BREAK:", bg='white', font=('Arial', 8, 'bold')).grid(row=0, column=0, columnspan=2, pady=2)
        tk.Label(break_frame, text="AFTER CLASS:", bg='white', font=('Arial', 8)).grid(row=1, column=0, sticky='w', padx=2)
        fields['break1_after'] = tk.Entry(break_frame, width=8, font=('Arial', 8))
        fields['break1_after'].grid(row=1, column=1, padx=2)
        tk.Label(break_frame, text="DURATION:", bg='white', font=('Arial', 8)).grid(row=1, column=2, sticky='w', padx=2)
        fields['break1_duration'] = tk.Entry(break_frame, width=8, font=('Arial', 8))
        fields['break1_duration'].grid(row=1, column=3, padx=2)
        tk.Label(break_frame, text="(period no.)", bg='white', font=('Arial', 6), fg='gray').grid(row=2, column=0, columnspan=2)
        tk.Label(break_frame, text="(minutes)", bg='white', font=('Arial', 6), fg='gray').grid(row=2, column=2, columnspan=2)
        
        # Lunch time
        tk.Label(break_frame, text="LUNCH TIME:", bg='white', font=('Arial', 8, 'bold')).grid(row=3, column=0, columnspan=2, pady=2)
        tk.Label(break_frame, text="AFTER CLASS:", bg='white', font=('Arial', 8)).grid(row=4, column=0, sticky='w', padx=2)
        fields['lunch_after'] = tk.Entry(break_frame, width=8, font=('Arial', 8))
        fields['lunch_after'].grid(row=4, column=1, padx=2)
        tk.Label(break_frame, text="DURATION:", bg='white', font=('Arial', 8)).grid(row=4, column=2, sticky='w', padx=2)
        fields['lunch_duration'] = tk.Entry(break_frame, width=8, font=('Arial', 8))
        fields['lunch_duration'].grid(row=4, column=3, padx=2)
        tk.Label(break_frame, text="(period no.)", bg='white', font=('Arial', 6), fg='gray').grid(row=5, column=0, columnspan=2)
        tk.Label(break_frame, text="(minutes)", bg='white', font=('Arial', 6), fg='gray').grid(row=5, column=2, columnspan=2)
        
        # 2nd Break
        tk.Label(break_frame, text="2ND BREAK:", bg='white', font=('Arial', 8, 'bold')).grid(row=6, column=0, columnspan=2, pady=2)
        tk.Label(break_frame, text="AFTER CLASS:", bg='white', font=('Arial', 8)).grid(row=7, column=0, sticky='w', padx=2)
        fields['break2_after'] = tk.Entry(break_frame, width=8, font=('Arial', 8))
        fields['break2_after'].grid(row=7, column=1, padx=2)
        tk.Label(break_frame, text="DURATION:", bg='white', font=('Arial', 8)).grid(row=7, column=2, sticky='w', padx=2)
        fields['break2_duration'] = tk.Entry(break_frame, width=8, font=('Arial', 8))
        fields['break2_duration'].grid(row=7, column=3, padx=2)
        tk.Label(break_frame, text="(period no.)", bg='white', font=('Arial', 6), fg='gray').grid(row=8, column=0, columnspan=2)
        tk.Label(break_frame, text="(minutes)", bg='white', font=('Arial', 6), fg='gray').grid(row=8, column=2, columnspan=2)
        
        # Load existing data if available
        if self.school_data:
            timing_key = f'{level}_timings'
            if timing_key in self.school_data:
                existing_timings = self.school_data[timing_key]
                for field_name, widget in fields.items():
                    if field_name in existing_timings and hasattr(widget, 'insert'):
                        widget.insert(0, str(existing_timings[field_name]))
        
        if level == 'primary':
            self.primary_fields = fields
        elif level == 'secondary':
            self.secondary_fields = fields
        else:  # senior_secondary
            self.senior_secondary_fields = fields
    
    def toggle_extra_class_timing(self, level):
        """Show/hide extra class timing based on checkbox"""
        if level == 'senior_secondary':
            extra_class_frame = self.senior_secondary_fields['extra_class_frame']
            if self.senior_secondary_fields['extra_class_var'].get():
                extra_class_frame.grid()
            else:
                extra_class_frame.grid_remove()
    
    def save_school_details(self):
        if not self.school_name_entry.get() or not self.board_var.get() or not self.region_var.get():
            messagebox.showerror("Error", "Please fill in school name, select board, and select region")
            return
            
        # Get regional language based on region
        regional_languages = {
            "Tamil Nadu": "Tamil",
            "Karnataka": "Kannada", 
            "Kerala": "Malayalam",
            "Andhra Pradesh": "Telugu",
            "Telangana": "Telugu",
            "Maharashtra": "Marathi",
            "Gujarat": "Gujarati",
            "Rajasthan": "Rajasthani",
            "Punjab": "Punjabi",
            "Haryana": "Hindi",
            "Uttar Pradesh": "Hindi",
            "Bihar": "Hindi",
            "West Bengal": "Bengali",
            "Odisha": "Odia",
            "Jharkhand": "Hindi",
            "Chhattisgarh": "Hindi",
            "Madhya Pradesh": "Hindi",
            "Assam": "Assamese",
            "Other": "Regional Language"
        }
        
        regional_language = regional_languages.get(self.region_var.get(), "Regional Language")
        
        # Update board subjects with actual regional language
        for board in self.board_subjects:
            for class_num in self.board_subjects[board]:
                subjects = self.board_subjects[board][class_num]
                # Replace REGIONAL_LANGUAGE placeholder with actual regional language
                if "REGIONAL_LANGUAGE" in subjects:
                    idx = subjects.index("REGIONAL_LANGUAGE")
                    subjects[idx] = regional_language
        
        # Update stream subjects with regional language
        for stream in self.stream_subjects:
            if "REGIONAL_LANGUAGE" in self.stream_subjects[stream]["core"]:
                idx = self.stream_subjects[stream]["core"].index("REGIONAL_LANGUAGE")
                self.stream_subjects[stream]["core"][idx] = regional_language
        
        # Save extra class data for senior secondary
        extra_class_enabled = self.senior_secondary_fields.get('extra_class_var', tk.BooleanVar()).get()
        extra_class_timing = ""
        if extra_class_enabled:
            extra_class_timing = self.senior_secondary_fields.get('extra_class_timing', tk.Entry()).get()
            if not extra_class_timing:
                messagebox.showerror("Error", "Please specify extra class timing for senior secondary")
                return
        
        self.school_data = {
            'name': self.school_name_entry.get(),
            'board': self.board_var.get(),
            'region': self.region_var.get(),
            'regional_language': regional_language,
            'primary_timings': {k: v.get() if hasattr(v, 'get') else v for k, v in self.primary_fields.items() if k not in ['extra_class_var', 'extra_class_frame', 'extra_class_timing']},
            'secondary_timings': {k: v.get() if hasattr(v, 'get') else v for k, v in self.secondary_fields.items() if k not in ['extra_class_var', 'extra_class_frame', 'extra_class_timing']},
            'senior_secondary_timings': {k: v.get() if hasattr(v, 'get') else v for k, v in self.senior_secondary_fields.items() if k not in ['extra_class_var', 'extra_class_frame', 'extra_class_timing']},
            'working_days': [day for day, var in self.working_days.items() if var.get()],
            'extra_class_enabled': extra_class_enabled,
            'extra_class_timing': extra_class_timing
        }
        
        messagebox.showinfo("Success", "School details saved successfully!")
        self.class_details_screen()

    def class_details_screen(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add HOME button
        self.create_home_button(self.current_frame)
        
        # Title
        title_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        title_frame.pack(fill='x', pady=10)
        tk.Label(title_frame, text="CLASS DETAILS", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Main container with scrollbars
        main_container = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        main_container.pack(fill='both', expand=True, pady=10)
        
        scrollable_frame = self.create_scrollable_frame(main_container)
        
        # Input section
        input_frame = tk.Frame(scrollable_frame, bg='white')
        input_frame.pack(fill='x', pady=10)
        
        # Class selection
        tk.Label(input_frame, text="SELECT CLASS:", bg='white', font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(input_frame, text="(Choose class number 1-12)", bg='white', font=('Arial', 8), fg='gray').grid(row=1, column=0, padx=10)
        self.class_var = tk.StringVar()
        class_combo = ttk.Combobox(input_frame, textvariable=self.class_var, 
                                  values=[str(i) for i in range(1, 13)], width=15)
        class_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # Sections
        tk.Label(input_frame, text="ADD SECTIONS:", bg='white', font=('Arial', 10)).grid(row=0, column=2, padx=10, pady=5)
        tk.Label(input_frame, text="(e.g., A,B,C or leave blank)", bg='white', font=('Arial', 8), fg='gray').grid(row=1, column=2, padx=10)
        self.sections_entry = tk.Entry(input_frame, width=20)
        self.sections_entry.grid(row=0, column=3, padx=10, pady=5)
        
        # No section checkbox
        self.no_section_var = tk.BooleanVar()
        tk.Checkbutton(input_frame, text="NO SECTION:", variable=self.no_section_var, 
                      bg='white', font=('Arial', 10)).grid(row=2, column=2, columnspan=2, pady=5)
        tk.Label(input_frame, text="(Check if class has no sections)", bg='white', font=('Arial', 8), fg='gray').grid(row=3, column=2, columnspan=2)
        
        # Add class button
        add_btn = self.create_styled_button(input_frame, "ADD CLASS", self.add_class, width=15)
        add_btn.grid(row=4, column=1, columnspan=2, pady=10)
        
        # Class list
        list_frame = tk.LabelFrame(scrollable_frame, text="CLASS LIST", bg='white', font=('Arial', 12, 'bold'))
        list_frame.pack(fill='both', expand=True, pady=10)
        
        # Headers
        headers_frame = tk.Frame(list_frame, bg='white', relief='solid', bd=1)
        headers_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(headers_frame, text="CLASS", bg='white', font=('Arial', 10, 'bold'), 
                relief='solid', bd=1, width=20).pack(side='left', fill='x', expand=True)
        tk.Label(headers_frame, text="SECTIONS", bg='white', font=('Arial', 10, 'bold'), 
                relief='solid', bd=1, width=20).pack(side='left', fill='x', expand=True)
        
        # Scrollable list
        self.class_list_frame = tk.Frame(list_frame, bg='white')
        self.class_list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.update_class_list()
        
        # Buttons
        btn_frame = tk.Frame(self.current_frame, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        continue_btn = self.create_styled_button(btn_frame, "Continue", self.subject_details_screen, width=15, bg_color='lightgreen')
        continue_btn.pack(side='left', padx=10)
        
        back_btn = self.create_styled_button(btn_frame, "Back", self.school_details_screen, width=15, bg_color='lightcoral')
        back_btn.pack(side='left', padx=10)
    
    def add_class(self):
        if not self.class_var.get():
            messagebox.showerror("Error", "Please select a class")
            return
            
        class_num = int(self.class_var.get())
        
        if self.no_section_var.get():
            sections = []
        else:
            sections_text = self.sections_entry.get().strip()
            if sections_text:
                sections = [s.strip().upper() for s in sections_text.split(',')]
            else:
                sections = []
        
        # Check if class already exists
        for existing_class in self.classes_data:
            if existing_class['class'] == class_num:
                messagebox.showerror("Error", f"Class {class_num} already exists")
                return
        
        self.classes_data.append({
            'class': class_num,
            'sections': sections
        })
        
        self.update_class_list()
        self.class_var.set('')
        self.sections_entry.delete(0, tk.END)
        self.no_section_var.set(False)
    
    def update_class_list(self):
        for widget in self.class_list_frame.winfo_children():
            widget.destroy()
            
        for class_data in self.classes_data:
            row_frame = tk.Frame(self.class_list_frame, bg='white', relief='solid', bd=1)
            row_frame.pack(fill='x', pady=1)
            
            tk.Label(row_frame, text=f"Class {class_data['class']}", bg='white', 
                    relief='solid', bd=1, width=20).pack(side='left', fill='x', expand=True)
            
            sections_text = ', '.join(class_data['sections']) if class_data['sections'] else 'No Sections'
            tk.Label(row_frame, text=sections_text, bg='white', 
                    relief='solid', bd=1, width=20).pack(side='left', fill='x', expand=True)

    def subject_details_screen(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add HOME button
        self.create_home_button(self.current_frame)
        
        # Check if classes exist
        if not self.classes_data:
            # Show message and provide navigation options
            message_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
            message_frame.pack(expand=True, padx=50, pady=50)
            
            tk.Label(message_frame, text="No Classes Added Yet!", 
                    font=('Arial', 16, 'bold'), bg='white', fg='red').pack(pady=20)
            tk.Label(message_frame, text="Please add classes first before setting up subjects.", 
                    font=('Arial', 12), bg='white').pack(pady=10)
            
            btn_frame = tk.Frame(message_frame, bg='white')
            btn_frame.pack(pady=20)
            
            add_classes_btn = self.create_styled_button(btn_frame, "Add Classes", self.class_details_screen, width=15, bg_color='lightgreen')
            add_classes_btn.pack(side='left', padx=10)
            
            back_btn = self.create_styled_button(btn_frame, "Back to Home", self.create_main_menu, width=15, bg_color='lightcoral')
            back_btn.pack(side='left', padx=10)
            return
            
        if not self.school_data.get('board'):
            messagebox.showerror("Error", "Please set school board first")
            self.school_details_screen()
            return
        
        # Title
        title_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        title_frame.pack(fill='x', pady=10)
        tk.Label(title_frame, text="SUBJECT DETAILS", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Instructions
        instruction_frame = tk.Frame(self.current_frame, bg='white')
        instruction_frame.pack(fill='x', pady=5)
        tk.Label(instruction_frame, text="Select subjects for each class. For classes 11-12, choose stream first.", 
                bg='white', font=('Arial', 10), fg='gray').pack()
        
        # Main container with scrollbars
        main_container = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        main_container.pack(fill='both', expand=True, pady=10)
        
        scrollable_frame = self.create_scrollable_frame(main_container)
        
        # Subject selection for each class
        self.subject_vars = {}
        self.stream_vars = {}
        board = self.school_data['board']
        
        for class_data in self.classes_data:
            class_num = class_data['class']
            
            class_frame = tk.LabelFrame(scrollable_frame, text=f"CLASS {class_num}", 
                                       bg='white', font=('Arial', 12, 'bold'))
            class_frame.pack(fill='x', padx=10, pady=10)
            
            # For classes 11-12, add stream selection
            if class_num >= 11:
                stream_frame = tk.Frame(class_frame, bg='white', relief='solid', bd=1)
                stream_frame.pack(fill='x', padx=10, pady=5)
                
                tk.Label(stream_frame, text="SELECT STREAM:", bg='white', font=('Arial', 11, 'bold')).pack(anchor='w', padx=10, pady=5)
                
                stream_var = tk.StringVar()
                self.stream_vars[class_num] = stream_var
                stream_var.trace('w', lambda *args, cn=class_num: self.update_stream_subjects(cn))
                
                stream_combo = ttk.Combobox(stream_frame, textvariable=stream_var,
                                          values=list(self.stream_subjects.keys()), width=20)
                stream_combo.pack(anchor='w', padx=10, pady=5)
                
                # Load existing stream data
                if class_num in self.stream_data:
                    stream_var.set(self.stream_data[class_num])
                
                # Create placeholder for subjects
                subjects_frame = tk.Frame(class_frame, bg='white', relief='solid', bd=1)
                subjects_frame.pack(fill='x', padx=10, pady=10)
                
                # Store reference for later updates
                if not hasattr(self, 'class_subject_frames'):
                    self.class_subject_frames = {}
                self.class_subject_frames[class_num] = subjects_frame
                
                self.subject_vars[class_num] = {}
                
            else:
                # For classes 1-10, use regular board subjects
                subjects_frame = tk.Frame(class_frame, bg='white', relief='solid', bd=1)
                subjects_frame.pack(fill='x', padx=10, pady=10)
                
                if class_num in self.board_subjects[board]:
                    subjects = self.board_subjects[board][class_num]
                    self.subject_vars[class_num] = {}
                    
                    # Create checkboxes in 2 columns
                    for i, subject in enumerate(subjects):
                        var = tk.BooleanVar()
                        # Load existing data
                        if class_num in self.subjects_data and subject in self.subjects_data[class_num]:
                            var.set(True)
                        self.subject_vars[class_num][subject] = var
                        
                        row = i // 2
                        col = i % 2
                        
                        cb = tk.Checkbutton(subjects_frame, text=subject, variable=var, 
                                           bg='white', font=('Arial', 10))
                        cb.grid(row=row, column=col, sticky='w', padx=20, pady=2)

            # Add ECA checkbox for all classes
            eca_var = tk.BooleanVar()
            # Load existing ECA data
            if class_num in self.eca_data:
                eca_var.set(True)
            eca_var.trace('w', lambda *args, cn=class_num: self.toggle_eca_details(cn))
            self.subject_vars[class_num]['ECA'] = eca_var

            eca_cb = tk.Checkbutton(class_frame, text="ECA (Extra Curricular Activities)", 
                                   variable=eca_var, bg='white', font=('Arial', 10, 'bold'))
            eca_cb.pack(anchor='w', padx=20, pady=5)

            # ECA details frame (initially hidden)
            eca_details_frame = tk.Frame(class_frame, bg='white')
            eca_details_frame.pack(anchor='w', padx=40, pady=5)
            if class_num not in self.eca_data:
                eca_details_frame.pack_forget()  # Hide initially

            tk.Label(eca_details_frame, text="ECA Day:", bg='white', font=('Arial', 9)).grid(row=0, column=0, padx=5)
            tk.Label(eca_details_frame, text="(Select day for ECA)", bg='white', font=('Arial', 7), fg='gray').grid(row=1, column=0, padx=5)
            eca_day_var = tk.StringVar()
            # Load existing ECA day
            if class_num in self.eca_data:
                eca_day_var.set(self.eca_data[class_num]['day'])
            eca_day_combo = ttk.Combobox(eca_details_frame, textvariable=eca_day_var,
                                        values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                                        width=10, font=('Arial', 9))
            eca_day_combo.grid(row=0, column=1, padx=5)

            tk.Label(eca_details_frame, text="ECA Time:", bg='white', font=('Arial', 9)).grid(row=0, column=2, padx=5)
            tk.Label(eca_details_frame, text="(e.g., 14:00-15:00)", bg='white', font=('Arial', 7), fg='gray').grid(row=1, column=2, padx=5)
            eca_time_entry = tk.Entry(eca_details_frame, width=15, font=('Arial', 9))
            eca_time_entry.grid(row=0, column=3, padx=5)
            # Load existing ECA time
            if class_num in self.eca_data:
                eca_time_entry.insert(0, self.eca_data[class_num]['time'])

            # Store ECA details widgets for later access
            if not hasattr(self, 'eca_widgets'):
                self.eca_widgets = {}
            self.eca_widgets[class_num] = {
                'frame': eca_details_frame,
                'day_var': eca_day_var,
                'time_entry': eca_time_entry
            }

            # Add Lab Activities for higher secondary classes (11-12)
            if class_num >= 11:
                lab_var = tk.BooleanVar()
                # Load existing lab data
                if class_num in self.lab_data:
                    lab_var.set(True)
                lab_var.trace('w', lambda *args, cn=class_num: self.toggle_lab_details(cn))
                self.subject_vars[class_num]['LAB'] = lab_var

                lab_cb = tk.Checkbutton(class_frame, text="Lab Activities", 
                                       variable=lab_var, bg='white', font=('Arial', 10, 'bold'))
                lab_cb.pack(anchor='w', padx=20, pady=5)

                # Lab details frame (initially hidden)
                lab_details_frame = tk.Frame(class_frame, bg='white')
                lab_details_frame.pack(anchor='w', padx=40, pady=5)
                if class_num not in self.lab_data:
                    lab_details_frame.pack_forget()  # Hide initially

                tk.Label(lab_details_frame, text="Lab Days:", bg='white', font=('Arial', 9)).grid(row=0, column=0, padx=5)
                tk.Label(lab_details_frame, text="(Select days for lab)", bg='white', font=('Arial', 7), fg='gray').grid(row=1, column=0, padx=5)
                
                # Lab days selection
                lab_days_frame = tk.Frame(lab_details_frame, bg='white')
                lab_days_frame.grid(row=0, column=1, columnspan=3, padx=5)
                
                lab_days_vars = {}
                for i, day in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]):
                    var = tk.BooleanVar()
                    # Load existing lab days
                    if class_num in self.lab_data and day in self.lab_data[class_num]['days']:
                        var.set(True)
                    lab_days_vars[day] = var
                    cb = tk.Checkbutton(lab_days_frame, text=day[:3], variable=var, bg='white', font=('Arial', 8))
                    cb.grid(row=0, column=i, padx=2)

                tk.Label(lab_details_frame, text="Lab Time:", bg='white', font=('Arial', 9)).grid(row=2, column=0, padx=5)
                tk.Label(lab_details_frame, text="(e.g., 14:00-16:00)", bg='white', font=('Arial', 7), fg='gray').grid(row=3, column=0, padx=5)
                lab_time_entry = tk.Entry(lab_details_frame, width=15, font=('Arial', 9))
                lab_time_entry.grid(row=2, column=1, padx=5)
                # Load existing lab time
                if class_num in self.lab_data:
                    lab_time_entry.insert(0, self.lab_data[class_num]['time'])

                # Store Lab details widgets for later access
                if not hasattr(self, 'lab_widgets'):
                    self.lab_widgets = {}
                self.lab_widgets[class_num] = {
                    'frame': lab_details_frame,
                    'days_vars': lab_days_vars,
                    'time_entry': lab_time_entry
                }
        
        # Buttons
        btn_frame = tk.Frame(self.current_frame, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        save_btn = self.create_styled_button(btn_frame, "Save & Continue", self.save_subjects, width=15, bg_color='lightgreen')
        save_btn.pack(side='left', padx=10)
        
        back_btn = self.create_styled_button(btn_frame, "Back", self.class_details_screen, width=15, bg_color='lightcoral')
        back_btn.pack(side='left', padx=10)
    
    def update_stream_subjects(self, class_num):
        """Update subjects based on selected stream for classes 11-12"""
        if class_num not in self.stream_vars:
            return
            
        stream = self.stream_vars[class_num].get()
        if not stream or class_num not in self.class_subject_frames:
            return
        
        # Clear existing subject checkboxes
        subjects_frame = self.class_subject_frames[class_num]
        for widget in subjects_frame.winfo_children():
            widget.destroy()
        
        # Get subjects for the selected stream
        stream_data = self.stream_subjects[stream]
        all_subjects = stream_data['core'] + stream_data['optional']
        
        # Create new checkboxes
        self.subject_vars[class_num] = {}
        
        # Core subjects (mandatory)
        tk.Label(subjects_frame, text="CORE SUBJECTS (Mandatory):", bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=5)
        
        for i, subject in enumerate(stream_data['core']):
            var = tk.BooleanVar()
            var.set(True)  # Core subjects are selected by default
            self.subject_vars[class_num][subject] = var
            
            row = (i // 2) + 1
            col = i % 2
            
            cb = tk.Checkbutton(subjects_frame, text=subject, variable=var, 
                               bg='white', font=('Arial', 10), state='disabled')
            cb.grid(row=row, column=col, sticky='w', padx=20, pady=2)
        
        # Optional subjects
        start_row = (len(stream_data['core']) // 2) + 2
        tk.Label(subjects_frame, text="OPTIONAL SUBJECTS:", bg='white', font=('Arial', 10, 'bold')).grid(row=start_row, column=0, columnspan=2, sticky='w', padx=10, pady=5)
        
        for i, subject in enumerate(stream_data['optional']):
            var = tk.BooleanVar()
            # Load existing data
            if class_num in self.subjects_data and subject in self.subjects_data[class_num]:
                var.set(True)
            self.subject_vars[class_num][subject] = var
            
            row = start_row + (i // 2) + 1
            col = i % 2
            
            cb = tk.Checkbutton(subjects_frame, text=subject, variable=var, 
                               bg='white', font=('Arial', 10))
            cb.grid(row=row, column=col, sticky='w', padx=20, pady=2)
        
        # Store stream selection
        self.stream_data[class_num] = stream
    
    def toggle_eca_details(self, class_num):
        """Show/hide ECA details based on checkbox"""
        if class_num in self.eca_widgets:
            eca_frame = self.eca_widgets[class_num]['frame']
            if self.subject_vars[class_num]['ECA'].get():
                eca_frame.pack(anchor='w', padx=40, pady=5)
            else:
                eca_frame.pack_forget()
    
    def toggle_lab_details(self, class_num):
        """Show/hide Lab details based on checkbox"""
        if class_num in self.lab_widgets:
            lab_frame = self.lab_widgets[class_num]['frame']
            if self.subject_vars[class_num]['LAB'].get():
                lab_frame.pack(anchor='w', padx=40, pady=5)
            else:
                lab_frame.pack_forget()
    
    def save_subjects(self):
        self.subjects_data = {}
        self.eca_data = {}
        self.lab_data = {}
        
        for class_num, subjects in self.subject_vars.items():
            selected_subjects = []
            for subject, var in subjects.items():
                if var.get():
                    if subject == 'ECA':
                        # Handle ECA separately
                        if class_num in self.eca_widgets:
                            day = self.eca_widgets[class_num]['day_var'].get()
                            time = self.eca_widgets[class_num]['time_entry'].get()
                            if day and time:
                                self.eca_data[class_num] = {'day': day, 'time': time}
                                selected_subjects.append('ECA')
                            else:
                                messagebox.showerror("Error", f"Please specify ECA day and time for Class {class_num}")
                                return
                    elif subject == 'LAB':
                        # Handle Lab separately
                        if class_num in self.lab_widgets:
                            lab_days = [day for day, var in self.lab_widgets[class_num]['days_vars'].items() if var.get()]
                            time = self.lab_widgets[class_num]['time_entry'].get()
                            if lab_days and time:
                                self.lab_data[class_num] = {'days': lab_days, 'time': time}
                                selected_subjects.append('LAB')
                            else:
                                messagebox.showerror("Error", f"Please specify lab days and time for Class {class_num}")
                                return
                    else:
                        selected_subjects.append(subject)
            
            if selected_subjects:
                self.subjects_data[class_num] = selected_subjects
        
        if not self.subjects_data:
            messagebox.showerror("Error", "Please select at least one subject for one class")
            return
            
        messagebox.showinfo("Success", "Subjects, ECA, and Lab details saved successfully!")
        self.teacher_details_screen()
    
    def teacher_details_screen(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add HOME button
        self.create_home_button(self.current_frame)
        
        # Title
        title_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        title_frame.pack(fill='x', pady=10)
        tk.Label(title_frame, text="TEACHER DETAILS", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Main container with scrollbars
        main_container = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        main_container.pack(fill='both', expand=True, pady=10)
        
        scrollable_frame = self.create_scrollable_frame(main_container)
        
        # Input section
        input_frame = tk.Frame(scrollable_frame, bg='white')
        input_frame.pack(fill='x', pady=10, padx=20)
        
        # Teacher info
        info_frame = tk.Frame(input_frame, bg='white')
        info_frame.pack(fill='x', pady=10)
        
        tk.Label(info_frame, text="TEACHER NAME:", bg='white', font=('Arial', 10)).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(info_frame, text="(Enter full name)", bg='white', font=('Arial', 8), fg='gray').grid(row=1, column=0, padx=10)
        self.teacher_name_entry = tk.Entry(info_frame, width=20, font=('Arial', 10))
        self.teacher_name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(info_frame, text="EMPLOYEE ID:", bg='white', font=('Arial', 10)).grid(row=0, column=2, padx=10, pady=5)
        tk.Label(info_frame, text="(Unique ID)", bg='white', font=('Arial', 8), fg='gray').grid(row=1, column=2, padx=10)
        self.employee_id_entry = tk.Entry(info_frame, width=20, font=('Arial', 10))
        self.employee_id_entry.grid(row=0, column=3, padx=10, pady=5)
        
        tk.Label(info_frame, text="EMAIL:", bg='white', font=('Arial', 10)).grid(row=2, column=0, padx=10, pady=5)
        tk.Label(info_frame, text="(Optional)", bg='white', font=('Arial', 8), fg='gray').grid(row=3, column=0, padx=10)
        self.teacher_email_entry = tk.Entry(info_frame, width=20, font=('Arial', 10))
        self.teacher_email_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(info_frame, text="QUALIFICATION:", bg='white', font=('Arial', 10)).grid(row=2, column=2, padx=10, pady=5)
        tk.Label(info_frame, text="(Optional)", bg='white', font=('Arial', 8), fg='gray').grid(row=3, column=2, padx=10)
        self.teacher_qualification_entry = tk.Entry(info_frame, width=20, font=('Arial', 10))
        self.teacher_qualification_entry.grid(row=2, column=3, padx=10, pady=5)
        
        # Class selection
        class_frame = tk.LabelFrame(input_frame, text="SELECT CLASS:", bg='white', font=('Arial', 10, 'bold'))
        class_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(class_frame, text="(Select classes this teacher will teach)", bg='white', font=('Arial', 8), fg='gray').pack()
        
        self.teacher_class_vars = {}
        class_inner = tk.Frame(class_frame, bg='white')
        class_inner.pack(pady=5)
        
        col = 0
        row = 0
        for class_data in self.classes_data:
            class_num = class_data['class']
            sections = class_data['sections']
            
            if not sections:  # No sections
                var = tk.BooleanVar()
                var.trace('w', self.update_subject_selection)
                self.teacher_class_vars[f"Class {class_num}"] = var
                cb = tk.Checkbutton(class_inner, text=f"Class {class_num}", variable=var, 
                                   bg='white', font=('Arial', 9))
                cb.grid(row=row, column=col, sticky='w', padx=10, pady=2)
                col += 1
                if col > 3:
                    col = 0
                    row += 1
            else:
                for section in sections:
                    var = tk.BooleanVar()
                    var.trace('w', self.update_subject_selection)
                    self.teacher_class_vars[f"Class {class_num}-{section}"] = var
                    cb = tk.Checkbutton(class_inner, text=f"Class {class_num}-{section}", variable=var, 
                                       bg='white', font=('Arial', 9))
                    cb.grid(row=row, column=col, sticky='w', padx=10, pady=2)
                    col += 1
                    if col > 3:
                        col = 0
                        row += 1
        
        # Subject selection
        self.subject_frame = tk.LabelFrame(input_frame, text="SELECT SUBJECT:", bg='white', font=('Arial', 10, 'bold'))
        self.subject_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(self.subject_frame, text="(Select subjects this teacher can teach)", bg='white', font=('Arial', 8), fg='gray').pack()
        
        self.teacher_subject_vars = {}
        
        # Add teacher button
        add_btn = self.create_styled_button(input_frame, "ADD TEACHER +", self.add_teacher, width=20)
        add_btn.pack(pady=20)
        
        # Teachers summary (simplified)
        summary_frame = tk.LabelFrame(scrollable_frame, text="TEACHERS SUMMARY", bg='white', font=('Arial', 12, 'bold'))
        summary_frame.pack(fill='both', expand=True, pady=10, padx=20)
        
        self.teachers_summary_label = tk.Label(summary_frame, text="No teachers added yet", 
                                             bg='white', font=('Arial', 10))
        self.teachers_summary_label.pack(pady=20)
        
        self.update_teachers_summary()
        
        # Buttons
        btn_frame = tk.Frame(self.current_frame, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        continue_btn = self.create_styled_button(btn_frame, "Continue", self.generate_timetable_screen, width=15, bg_color='lightgreen')
        continue_btn.pack(side='left', padx=10)
        
        back_btn = self.create_styled_button(btn_frame, "Back", self.safe_back_to_subjects, width=15, bg_color='lightcoral')
        back_btn.pack(side='left', padx=10)
    
    def safe_back_to_subjects(self):
        """Safe navigation back to subjects with proper error handling"""
        if not self.classes_data:
            messagebox.showwarning("Warning", "No classes found. Redirecting to Class Details.")
            self.class_details_screen()
        else:
            self.subject_details_screen()
    
    def update_subject_selection(self, *args):
        # Clear existing subject checkboxes
        for widget in self.subject_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        
        self.teacher_subject_vars = {}
        
        # Get selected classes
        selected_classes = []
        for class_name, var in self.teacher_class_vars.items():
            if var.get():
                if '-' in class_name:
                    class_num = int(class_name.split('-')[0].replace('Class ', ''))
                else:
                    class_num = int(class_name.replace('Class ', ''))
                selected_classes.append(class_num)
        
        # Show subjects for selected classes
        all_subjects = set()
        for class_num in selected_classes:
            if class_num in self.subjects_data:
                all_subjects.update(self.subjects_data[class_num])
        
        if all_subjects:
            subjects_inner = tk.Frame(self.subject_frame, bg='white')
            subjects_inner.pack(pady=5)
            
            col = 0
            row = 0
            for subject in sorted(all_subjects):
                var = tk.BooleanVar()
                self.teacher_subject_vars[subject] = var
                cb = tk.Checkbutton(subjects_inner, text=subject, variable=var, 
                                   bg='white', font=('Arial', 9))
                cb.grid(row=row, column=col, sticky='w', padx=10, pady=2)
                col += 1
                if col > 2:
                    col = 0
                    row += 1
    
    def add_teacher(self):
        name = self.teacher_name_entry.get().strip()
        emp_id = self.employee_id_entry.get().strip()
        email = self.teacher_email_entry.get().strip()
        qualification = self.teacher_qualification_entry.get().strip()
        
        if not name or not emp_id:
            messagebox.showerror("Error", "Please enter teacher name and employee ID")
            return
        
        # Check if employee ID already exists
        for teacher in self.teachers_data:
            if teacher['employee_id'] == emp_id:
                messagebox.showerror("Error", "Employee ID already exists")
                return
        
        selected_classes = [class_name for class_name, var in self.teacher_class_vars.items() if var.get()]
        selected_subjects = [subject for subject, var in self.teacher_subject_vars.items() if var.get()]
        
        if not selected_classes or not selected_subjects:
            messagebox.showerror("Error", "Please select at least one class and one subject")
            return
        
        self.teachers_data.append({
            'name': name,
            'employee_id': emp_id,
            'email': email,
            'qualification': qualification,
            'classes': selected_classes,
            'subjects': selected_subjects
        })
        
        # Clear form
        self.teacher_name_entry.delete(0, tk.END)
        self.employee_id_entry.delete(0, tk.END)
        self.teacher_email_entry.delete(0, tk.END)
        self.teacher_qualification_entry.delete(0, tk.END)
        for var in self.teacher_class_vars.values():
            var.set(False)
        for var in self.teacher_subject_vars.values():
            var.set(False)
        
        self.update_teachers_summary()
        messagebox.showinfo("Success", "Teacher added successfully!")
    
    def update_teachers_summary(self):
        """Update the simplified teachers summary"""
        if not self.teachers_data:
            self.teachers_summary_label.config(text="No teachers added yet")
            return
        
        summary_text = f"Total Teachers Added: {len(self.teachers_data)}\n\n"
        
        # Group by subjects
        subject_teachers = {}
        for teacher in self.teachers_data:
            for subject in teacher['subjects']:
                if subject not in subject_teachers:
                    subject_teachers[subject] = []
                subject_teachers[subject].append(teacher['name'])
        
        summary_text += "Teachers by Subject:\n"
        for subject, teachers in sorted(subject_teachers.items()):
            summary_text += f"• {subject}: {len(teachers)} teacher(s)\n"
        
        self.teachers_summary_label.config(text=summary_text, justify='left')
    
    def teachers_details_view_screen(self):
        """Display detailed teacher information with workload analysis"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add HOME button
        self.create_home_button(self.current_frame)
        
        # Title
        title_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        title_frame.pack(fill='x', pady=10)
        tk.Label(title_frame, text="TEACHER'S LIST", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Check if teachers exist
        if not self.teachers_data:
            message_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
            message_frame.pack(expand=True, padx=50, pady=50)
            
            tk.Label(message_frame, text="No Teachers Added Yet!", 
                    font=('Arial', 16, 'bold'), bg='white', fg='red').pack(pady=20)
            tk.Label(message_frame, text="Please add teachers first before viewing details.", 
                    font=('Arial', 12), bg='white').pack(pady=10)
            
            btn_frame = tk.Frame(message_frame, bg='white')
            btn_frame.pack(pady=20)
            
            add_teachers_btn = self.create_styled_button(btn_frame, "Add Teachers", self.teacher_details_screen, width=15, bg_color='lightgreen')
            add_teachers_btn.pack(side='left', padx=10)
            
            back_btn = self.create_styled_button(btn_frame, "Back to Home", self.create_main_menu, width=15, bg_color='lightcoral')
            back_btn.pack(side='left', padx=10)
            return
        
        # Main content frame with scrollbars
        content_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        content_frame.pack(fill='both', expand=True, pady=10)
        
        scrollable_frame = self.create_scrollable_frame(content_frame)
        
        # Header with Edit button in right corner
        header_frame = tk.Frame(scrollable_frame, bg='white')
        header_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(header_frame, text=f"Total Teachers: {len(self.teachers_data)}", 
                font=('Arial', 12, 'bold'), bg='white').pack(side='left')
        
        edit_btn = self.create_styled_button(header_frame, "Edit Teacher", self.edit_teacher_screen, 
                                           width=12, height=1, bg_color='#FFD700')
        edit_btn.pack(side='right')
        
        # Sort teachers alphabetically by name
        sorted_teachers = sorted(self.teachers_data, key=lambda x: x['name'].lower())
        
        # Display each teacher's details
        for i, teacher in enumerate(sorted_teachers):
            teacher_frame = tk.LabelFrame(scrollable_frame, text=f"Teacher {i+1}: {teacher['name']}", 
                                        bg='white', font=('Arial', 12, 'bold'), fg='navy')
            teacher_frame.pack(fill='x', padx=10, pady=10)
            
            # Teacher basic info
            info_frame = tk.Frame(teacher_frame, bg='white')
            info_frame.pack(fill='x', padx=10, pady=5)
            
            # Employee ID
            tk.Label(info_frame, text="Employee ID:", bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5)
            tk.Label(info_frame, text=teacher['employee_id'], bg='white', font=('Arial', 10)).grid(row=0, column=1, sticky='w', padx=10)
            
            # Email and Qualification
            tk.Label(info_frame, text="Email:", bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='w', padx=5)
            tk.Label(info_frame, text=teacher.get('email', 'N/A'), bg='white', font=('Arial', 10)).grid(row=0, column=3, sticky='w', padx=10)
            
            tk.Label(info_frame, text="Qualification:", bg='white', font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=5)
            tk.Label(info_frame, text=teacher.get('qualification', 'N/A'), bg='white', font=('Arial', 10)).grid(row=1, column=1, sticky='w', padx=10)
            
            # Classes and Subjects
            classes_subjects_frame = tk.Frame(teacher_frame, bg='white')
            classes_subjects_frame.pack(fill='x', padx=10, pady=5)
            
            # Number of classes
            num_classes = len(teacher['classes'])
            tk.Label(classes_subjects_frame, text="Number of Classes:", bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5)
            tk.Label(classes_subjects_frame, text=str(num_classes), bg='white', font=('Arial', 10), fg='blue').grid(row=0, column=1, sticky='w', padx=10)
            
            # Classes list
            tk.Label(classes_subjects_frame, text="Classes:", bg='white', font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=5)
            classes_text = ', '.join(teacher['classes'])
            if len(classes_text) > 50:
                classes_text = classes_text[:47] + "..."
            tk.Label(classes_subjects_frame, text=classes_text, bg='white', font=('Arial', 9), wraplength=300).grid(row=1, column=1, sticky='w', padx=10)
            
            # Subjects
            tk.Label(classes_subjects_frame, text="Subjects:", bg='white', font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', padx=5)
            subjects_text = ', '.join(teacher['subjects'])
            if len(subjects_text) > 50:
                subjects_text = subjects_text[:47] + "..."
            tk.Label(classes_subjects_frame, text=subjects_text, bg='white', font=('Arial', 9), wraplength=300).grid(row=2, column=1, sticky='w', padx=10)
            
            # Workload Analysis
            workload_frame = tk.LabelFrame(teacher_frame, text="Daily Workload Analysis", bg='white', font=('Arial', 10, 'bold'))
            workload_frame.pack(fill='x', padx=10, pady=5)
            
            workload_data = self.calculate_teacher_workload(teacher)
            
            workload_info_frame = tk.Frame(workload_frame, bg='white')
            workload_info_frame.pack(fill='x', padx=5, pady=5)
            
            # Average periods per day
            tk.Label(workload_info_frame, text="Avg Periods/Day:", bg='white', font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky='w', padx=5)
            tk.Label(workload_info_frame, text=f"{workload_data['avg_periods']:.1f}", bg='white', font=('Arial', 9), fg='green').grid(row=0, column=1, sticky='w', padx=10)
            
            # Total weekly periods
            tk.Label(workload_info_frame, text="Weekly Periods:", bg='white', font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky='w', padx=5)
            tk.Label(workload_info_frame, text=str(workload_data['total_periods']), bg='white', font=('Arial', 9), fg='green').grid(row=0, column=3, sticky='w', padx=10)
            
            # Workload status
            tk.Label(workload_info_frame, text="Workload Status:", bg='white', font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky='w', padx=5)
            status_color = 'red' if workload_data['status'] == 'Heavy' else 'orange' if workload_data['status'] == 'Moderate' else 'green'
            tk.Label(workload_info_frame, text=workload_data['status'], bg='white', font=('Arial', 9), fg=status_color).grid(row=1, column=1, sticky='w', padx=10)
            
            # Daily breakdown
            if workload_data['daily_breakdown']:
                tk.Label(workload_info_frame, text="Daily Breakdown:", bg='white', font=('Arial', 9, 'bold')).grid(row=2, column=0, sticky='w', padx=5)
                breakdown_text = ', '.join([f"{day}: {periods}" for day, periods in workload_data['daily_breakdown'].items()])
                if len(breakdown_text) > 60:
                    breakdown_text = breakdown_text[:57] + "..."
                tk.Label(workload_info_frame, text=breakdown_text, bg='white', font=('Arial', 8), wraplength=400).grid(row=2, column=1, columnspan=3, sticky='w', padx=10)
        
        # Back button
        btn_frame = tk.Frame(self.current_frame, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        back_btn = self.create_styled_button(btn_frame, "Back to Home", self.create_main_menu, width=15, bg_color='lightcoral')
        back_btn.pack()
    
    def edit_teacher_screen(self):
        """Screen to edit teacher details"""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add HOME button
        self.create_home_button(self.current_frame)
        
        # Title
        title_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        title_frame.pack(fill='x', pady=10)
        tk.Label(title_frame, text="EDIT TEACHER", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        if not self.teachers_data:
            tk.Label(self.current_frame, text="No teachers to edit!", 
                    font=('Arial', 14), bg="#FFFFFF", fg='red').pack(pady=50)
            back_btn = self.create_styled_button(self.current_frame, "Back", self.teachers_details_view_screen, width=15, bg_color='lightcoral')
            back_btn.pack()
            return
        
        # Main container with scrollbars
        main_container = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        main_container.pack(fill='both', expand=True, pady=10)
        
        scrollable_frame = self.create_scrollable_frame(main_container)
        
        # Teacher selection
        selection_frame = tk.Frame(scrollable_frame, bg='white')
        selection_frame.pack(fill='x', pady=10, padx=20)
        
        tk.Label(selection_frame, text="Select Teacher to Edit:", bg='white', font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.selected_teacher_var = tk.StringVar()
        teacher_names = [f"{teacher['name']} (ID: {teacher['employee_id']})" for teacher in sorted(self.teachers_data, key=lambda x: x['name'].lower())]
        
        teacher_combo = ttk.Combobox(selection_frame, textvariable=self.selected_teacher_var,
                                   values=teacher_names, width=50, font=('Arial', 10))
        teacher_combo.pack(pady=10)
        teacher_combo.bind('<<ComboboxSelected>>', self.load_teacher_for_edit)
        
        # Edit form (initially hidden)
        self.edit_form_frame = tk.Frame(scrollable_frame, bg='white')
        self.edit_form_frame.pack(fill='both', expand=True, pady=10, padx=20)
        self.edit_form_frame.pack_forget()  # Hide initially
        
        # Buttons
        btn_frame = tk.Frame(self.current_frame, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        back_btn = self.create_styled_button(btn_frame, "Back", self.teachers_details_view_screen, width=15, bg_color='lightcoral')
        back_btn.pack()
    
    def load_teacher_for_edit(self, event=None):
        """Load selected teacher data into edit form"""
        selected = self.selected_teacher_var.get()
        if not selected:
            return
        
        # Extract employee ID from selection
        emp_id = selected.split("ID: ")[1].rstrip(")")
        
        # Find teacher data
        selected_teacher = None
        for teacher in self.teachers_data:
            if teacher['employee_id'] == emp_id:
                selected_teacher = teacher
                break
        
        if not selected_teacher:
            return
        
        # Clear existing form
        for widget in self.edit_form_frame.winfo_children():
            widget.destroy()
        
        # Show form
        self.edit_form_frame.pack(fill='both', expand=True, pady=10, padx=20)
        
        tk.Label(self.edit_form_frame, text=f"Editing: {selected_teacher['name']}", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Teacher info form
        info_frame = tk.Frame(self.edit_form_frame, bg='white')
        info_frame.pack(fill='x', pady=10)
        
        # Name
        tk.Label(info_frame, text="Teacher Name:", bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.edit_name_entry = tk.Entry(info_frame, width=25, font=('Arial', 10))
        self.edit_name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.edit_name_entry.insert(0, selected_teacher['name'])
        
        # Employee ID (read-only)
        tk.Label(info_frame, text="Employee ID:", bg='white', font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='w', padx=10, pady=5)
        tk.Label(info_frame, text=selected_teacher['employee_id'], bg='lightgray', font=('Arial', 10), relief='solid', bd=1, width=20).grid(row=0, column=3, padx=10, pady=5)
        
        # Email
        tk.Label(info_frame, text="Email:", bg='white', font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.edit_email_entry = tk.Entry(info_frame, width=25, font=('Arial', 10))
        self.edit_email_entry.grid(row=1, column=1, padx=10, pady=5)
        self.edit_email_entry.insert(0, selected_teacher.get('email', ''))
        
        # Qualification
        tk.Label(info_frame, text="Qualification:", bg='white', font=('Arial', 10, 'bold')).grid(row=1, column=2, sticky='w', padx=10, pady=5)
        self.edit_qualification_entry = tk.Entry(info_frame, width=25, font=('Arial', 10))
        self.edit_qualification_entry.grid(row=1, column=3, padx=10, pady=5)
        self.edit_qualification_entry.insert(0, selected_teacher.get('qualification', ''))
        
        # Classes selection
        classes_frame = tk.LabelFrame(self.edit_form_frame, text="Classes", bg='white', font=('Arial', 10, 'bold'))
        classes_frame.pack(fill='x', padx=10, pady=10)
        
        self.edit_class_vars = {}
        class_inner = tk.Frame(classes_frame, bg='white')
        class_inner.pack(pady=5)
        
        col = 0
        row = 0
        for class_data in self.classes_data:
            class_num = class_data['class']
            sections = class_data['sections']
            
            if not sections:  # No sections
                var = tk.BooleanVar()
                class_key = f"Class {class_num}"
                if class_key in selected_teacher['classes']:
                    var.set(True)
                self.edit_class_vars[class_key] = var
                cb = tk.Checkbutton(class_inner, text=class_key, variable=var, bg='white', font=('Arial', 9))
                cb.grid(row=row, column=col, sticky='w', padx=10, pady=2)
                col += 1
                if col > 3:
                    col = 0
                    row += 1
            else:
                for section in sections:
                    var = tk.BooleanVar()
                    class_key = f"Class {class_num}-{section}"
                    if class_key in selected_teacher['classes']:
                        var.set(True)
                    self.edit_class_vars[class_key] = var
                    cb = tk.Checkbutton(class_inner, text=class_key, variable=var, bg='white', font=('Arial', 9))
                    cb.grid(row=row, column=col, sticky='w', padx=10, pady=2)
                    col += 1
                    if col > 3:
                        col = 0
                        row += 1
        
        # Subjects selection
        subjects_frame = tk.LabelFrame(self.edit_form_frame, text="Subjects", bg='white', font=('Arial', 10, 'bold'))
        subjects_frame.pack(fill='x', padx=10, pady=10)
        
        # Get all available subjects
        all_subjects = set()
        for class_num in self.subjects_data:
            all_subjects.update(self.subjects_data[class_num])
        
        self.edit_subject_vars = {}
        subjects_inner = tk.Frame(subjects_frame, bg='white')
        subjects_inner.pack(pady=5)
        
        col = 0
        row = 0
        for subject in sorted(all_subjects):
            var = tk.BooleanVar()
            if subject in selected_teacher['subjects']:
                var.set(True)
            self.edit_subject_vars[subject] = var
            cb = tk.Checkbutton(subjects_inner, text=subject, variable=var, bg='white', font=('Arial', 9))
            cb.grid(row=row, column=col, sticky='w', padx=10, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Save and Delete buttons
        button_frame = tk.Frame(self.edit_form_frame, bg='white')
        button_frame.pack(pady=20)
        
        save_btn = self.create_styled_button(button_frame, "Save Changes", 
                                           lambda: self.save_teacher_changes(selected_teacher['employee_id']), 
                                           width=15, bg_color='lightgreen')
        save_btn.pack(side='left', padx=10)
        
        delete_btn = self.create_styled_button(button_frame, "Delete Teacher", 
                                             lambda: self.delete_teacher(selected_teacher['employee_id']), 
                                             width=15, bg_color='red')
        delete_btn.pack(side='left', padx=10)
    
    def save_teacher_changes(self, emp_id):
        """Save changes to teacher data"""
        # Find teacher to update
        teacher_index = -1
        for i, teacher in enumerate(self.teachers_data):
            if teacher['employee_id'] == emp_id:
                teacher_index = i
                break
        
        if teacher_index == -1:
            messagebox.showerror("Error", "Teacher not found!")
            return
        
        # Validate input
        name = self.edit_name_entry.get().strip()
        email = self.edit_email_entry.get().strip()
        qualification = self.edit_qualification_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Teacher name is required!")
            return
        
        # Get selected classes and subjects
        selected_classes = [class_name for class_name, var in self.edit_class_vars.items() if var.get()]
        selected_subjects = [subject for subject, var in self.edit_subject_vars.items() if var.get()]
        
        if not selected_classes or not selected_subjects:
            messagebox.showerror("Error", "Please select at least one class and one subject!")
            return
        
        # Update teacher data
        self.teachers_data[teacher_index].update({
            'name': name,
            'email': email,
            'qualification': qualification,
            'classes': selected_classes,
            'subjects': selected_subjects
        })
        
        messagebox.showinfo("Success", "Teacher details updated successfully!")
        self.teachers_details_view_screen()
    
    def delete_teacher(self, emp_id):
        """Delete a teacher"""
        result = messagebox.askyesno("Confirm Delete", 
                                   "Are you sure you want to delete this teacher?\nThis action cannot be undone.")
        
        if result:
            # Find and remove teacher
            for i, teacher in enumerate(self.teachers_data):
                if teacher['employee_id'] == emp_id:
                    del self.teachers_data[i]
                    break
            
            messagebox.showinfo("Success", "Teacher deleted successfully!")
            self.teachers_details_view_screen()

    def generate_timetable_screen(self):
        if not self.teachers_data:
            messagebox.showerror("Error", "Please add teachers first")
            return
        
        # Generate timetables
        self.generate_timetables()
        
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add HOME button
        self.create_home_button(self.current_frame)
        
        # Title
        title_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        title_frame.pack(fill='x', pady=10)
        tk.Label(title_frame, text="GENERATE TIME TABLE", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Main container with scrollbars
        main_container = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        main_container.pack(fill='both', expand=True, pady=10)
        
        scrollable_frame = self.create_scrollable_frame(main_container)
        
        # Instructions
        instruction_frame = tk.Frame(scrollable_frame, bg='white')
        instruction_frame.pack(fill='x', pady=5)
        tk.Label(instruction_frame, text="Select a class to view its timetable. Physical Education is limited to 2 periods per week.", 
                bg='white', font=('Arial', 10), fg='gray').pack()
        
        # Manual change checkbox
        manual_frame = tk.Frame(scrollable_frame, bg='white')
        manual_frame.pack(fill='x', pady=5)
        
        self.manual_edit_var = tk.BooleanVar()
        self.manual_edit_var.set(True)
        tk.Checkbutton(manual_frame, text="MANUAL CHANGE", variable=self.manual_edit_var,
                      command=self.toggle_manual_edit, bg='white', font=('Arial', 12)).pack(side='right', padx=20)
        tk.Label(manual_frame, text="(Enable to edit timetable manually)", bg='white', font=('Arial', 8), fg='gray').pack(side='right', padx=5)
        
        # Class selection
        class_select_frame = tk.Frame(scrollable_frame, bg='white')
        class_select_frame.pack(fill='x', pady=10)
        
        tk.Label(class_select_frame, text="Select Class:", bg='white', font=('Arial', 12)).pack(side='left', padx=10)
        tk.Label(class_select_frame, text="(Choose class to view timetable)", bg='white', font=('Arial', 8), fg='gray').pack(side='left', padx=5)
        
        self.selected_class_var = tk.StringVar()
        class_options = []
        for class_data in self.classes_data:
            class_num = class_data['class']
            if not class_data['sections']:
                class_options.append(f"Class {class_num}")
            else:
                for section in class_data['sections']:
                    class_options.append(f"Class {class_num}-{section}")
        
        class_combo = ttk.Combobox(class_select_frame, textvariable=self.selected_class_var,
                                  values=class_options, width=20)
        class_combo.pack(side='left', padx=10)
        class_combo.bind('<<ComboboxSelected>>', self.display_timetable)
        
        # Timetable display
        self.timetable_frame = tk.Frame(scrollable_frame, bg='white', relief='solid', bd=2)
        self.timetable_frame.pack(fill='both', expand=True, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(self.current_frame, bg="#FFFFFF")
        btn_frame.pack(pady=20)
        
        regenerate_btn = self.create_styled_button(btn_frame, "Regenerate", self.regenerate_timetable, width=15)
        regenerate_btn.pack(side='left', padx=10)
        
        export_btn = self.create_styled_button(btn_frame, "Export", self.export_timetable_screen, width=15, bg_color='lightgreen')
        export_btn.pack(side='left', padx=10)
        
        back_btn = self.create_styled_button(btn_frame, "Back", self.teacher_details_screen, width=15, bg_color='lightcoral')
        back_btn.pack(side='left', padx=10)
        
        # Display first class timetable if available
        if class_options:
            self.selected_class_var.set(class_options[0])
            self.display_timetable()
    
    def generate_timetables(self):
        """Generate varied timetables for all classes with limited PE periods"""
        self.timetables = {}
        working_days = self.school_data.get('working_days', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        
        for class_data in self.classes_data:
            class_num = class_data['class']
            
            # Determine if primary, secondary, or senior secondary
            if class_num <= 5:
                timings = self.school_data.get('primary_timings', {})
            elif class_num <= 10:
                timings = self.school_data.get('secondary_timings', {})
            else:  # 11-12
                timings = self.school_data.get('senior_secondary_timings', {})
            
            if not class_data['sections']:
                class_key = f"Class {class_num}"
                self.timetables[class_key] = self.create_class_timetable(class_key, class_num, timings, working_days)
            else:
                for section in class_data['sections']:
                    class_key = f"Class {class_num}-{section}"
                    self.timetables[class_key] = self.create_class_timetable(class_key, class_num, timings, working_days)
    
    def create_class_timetable(self, class_key, class_num, timings, working_days):
        """Create varied timetable for a specific class with limited PE periods"""
        # Get subjects for this class
        subjects = self.subjects_data.get(class_num, [])
        
        # Remove special subjects from regular rotation
        regular_subjects = [s for s in subjects if s not in ['ECA', 'LAB']]
        
        # Get teachers for this class
        class_teachers = {}
        for teacher in self.teachers_data:
            if class_key in teacher['classes']:
                for subject in teacher['subjects']:
                    if subject in regular_subjects:
                        class_teachers[subject] = teacher['name']
        
        if not class_teachers:
            return {}
        
        # Create time slots
        try:
            start_time = datetime.strptime(timings.get('start_time', '9:00'), '%H:%M')
            period_duration = int(timings.get('period_duration', '40'))
            
            # Calculate periods and breaks
            periods_per_day = 8  # Default
            time_slots = []
            current_time = start_time
            
            for period in range(1, periods_per_day + 1):
                end_time = current_time + timedelta(minutes=period_duration)
                time_slots.append({
                    'period': period,
                    'start': current_time.strftime('%H:%M'),
                    'end': end_time.strftime('%H:%M'),
                    'type': 'period'
                })
                current_time = end_time
                
                # Add breaks
                if period == int(timings.get('break1_after', '2')):
                    break_duration = int(timings.get('break1_duration', '15'))
                    current_time += timedelta(minutes=break_duration)
                    time_slots.append({
                        'period': f"Break 1",
                        'start': (current_time - timedelta(minutes=break_duration)).strftime('%H:%M'),
                        'end': current_time.strftime('%H:%M'),
                        'type': 'break'
                    })
                elif period == int(timings.get('lunch_after', '4')):
                    lunch_duration = int(timings.get('lunch_duration', '30'))
                    current_time += timedelta(minutes=lunch_duration)
                    time_slots.append({
                        'period': f"Lunch",
                        'start': (current_time - timedelta(minutes=lunch_duration)).strftime('%H:%M'),
                        'end': current_time.strftime('%H:%M'),
                        'type': 'break'
                    })
                elif period == int(timings.get('break2_after', '6')):
                    break_duration = int(timings.get('break2_duration', '15'))
                    current_time += timedelta(minutes=break_duration)
                    time_slots.append({
                        'period': f"Break 2",
                        'start': (current_time - timedelta(minutes=break_duration)).strftime('%H:%M'),
                        'end': current_time.strftime('%H:%M'),
                        'type': 'break'
                    })
        except:
            # Fallback to simple time slots
            time_slots = [
                {'period': 1, 'start': '9:00', 'end': '9:40', 'type': 'period'},
                {'period': 2, 'start': '9:40', 'end': '10:20', 'type': 'period'},
                {'period': 'Break 1', 'start': '10:20', 'end': '10:35', 'type': 'break'},
                {'period': 3, 'start': '10:35', 'end': '11:15', 'type': 'period'},
                {'period': 4, 'start': '11:15', 'end': '11:55', 'type': 'period'},
                {'period': 'Lunch', 'start': '11:55', 'end': '12:25', 'type': 'break'},
                {'period': 5, 'start': '12:25', 'end': '13:05', 'type': 'period'},
                {'period': 6, 'start': '13:05', 'end': '13:45', 'type': 'period'},
            ]
        
        # Create subject distribution for varied daily schedules with PE limitation
        period_slots = [slot for slot in time_slots if slot['type'] == 'period']
        subject_list = list(class_teachers.keys())
        
        # Separate PE from other subjects
        pe_subject = 'Physical Education'
        other_subjects = [s for s in subject_list if s != pe_subject]
        
        # Generate different timetable for each day
        timetable = {}
        pe_periods_assigned = 0  # Track PE periods across the week
        
        for day_idx, day in enumerate(working_days):
            timetable[day] = []
            
            # Create a shuffled subject list for this day to ensure variety
            daily_subjects = other_subjects.copy()
            random.shuffle(daily_subjects)
            
            # Add PE only if we haven't reached the limit of 2 periods per week
            # Assign PE to specific days (e.g., Tuesday and Thursday)
            if pe_subject in class_teachers and pe_periods_assigned < 2:
                if day in ['Tuesday', 'Thursday'] or (pe_periods_assigned == 0 and day_idx >= len(working_days) - 2):
                    # Insert PE at a random position (not first or last period)
                    if len(period_slots) > 2:
                        pe_position = random.randint(1, min(len(period_slots) - 2, 4))
                        daily_subjects.insert(pe_position, pe_subject)
                        pe_periods_assigned += 1
            
            # Extend the list to cover all periods
            while len(daily_subjects) < len(period_slots):
                daily_subjects.extend(other_subjects)
            
            subject_index = 0
            
            for slot in time_slots:
                if slot['type'] == 'break':
                    timetable[day].append({
                        'time': f"{slot['start']}-{slot['end']}",
                        'subject': slot['period'],
                        'type': 'break'
                    })
                else:
                    if subject_index < len(daily_subjects):
                        subject = daily_subjects[subject_index]
                        teacher = class_teachers.get(subject, 'TBD')
                        timetable[day].append({
                            'time': f"{slot['start']}-{slot['end']}",
                            'subject': subject,
                            'teacher': teacher,
                            'type': 'period'
                        })
                        subject_index += 1
                    else:
                        timetable[day].append({
                            'time': f"{slot['start']}-{slot['end']}",
                            'subject': 'Free Period',
                            'type': 'period'
                        })
        
        # Handle ECA if present
        if class_num in self.eca_data:
            eca_info = self.eca_data[class_num]
            eca_day = eca_info['day']
            eca_time = eca_info['time']
            
            if eca_day in timetable:
                timetable[eca_day].append({
                    'time': eca_time,
                    'subject': 'ECA',
                    'type': 'eca'
                })
        
        # Handle Lab Activities for higher secondary classes
        if class_num in self.lab_data:
            lab_info = self.lab_data[class_num]
            lab_days = lab_info['days']
            lab_time = lab_info['time']
            
            # Get stream-specific lab subjects
            stream = self.stream_data.get(class_num, 'Science')
            lab_subjects = self.stream_subjects.get(stream, {}).get('labs', ['Lab'])
            
            for day in lab_days:
                if day in timetable:
                    # Randomly assign a lab subject for this day
                    lab_subject = random.choice(lab_subjects)
                    timetable[day].append({
                        'time': lab_time,
                        'subject': lab_subject,
                        'type': 'lab'
                    })
        
        # Handle extra class for senior secondary (classes 11-12)
        if class_num >= 11 and self.school_data.get('extra_class_enabled', False):
            extra_class_timing = self.school_data.get('extra_class_timing', '')
            if extra_class_timing:
                # Add extra class to all working days
                for day in working_days:
                    timetable[day].append({
                        'time': extra_class_timing,
                        'subject': 'Extra Class',
                        'type': 'extra_class'
                    })
        
        return timetable
    
    def display_timetable(self, event=None):
        """Display timetable for selected class"""
        class_key = self.selected_class_var.get()
        if not class_key or class_key not in self.timetables:
            return
        
        # Clear existing timetable
        for widget in self.timetable_frame.winfo_children():
            widget.destroy()
        
        # Class label with stream info for 11-12
        class_num = int(class_key.split('-')[0].replace('Class ', ''))
        title_text = class_key
        if class_num >= 11 and class_num in self.stream_data:
            title_text += f" ({self.stream_data[class_num]} Stream)"
        
        tk.Label(self.timetable_frame, text=title_text, font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # PE limitation notice
        pe_notice = tk.Label(self.timetable_frame, text="Note: Physical Education is limited to 2 periods per week", 
                           font=('Arial', 10), bg='white', fg='blue')
        pe_notice.pack(pady=5)
        
        timetable = self.timetables[class_key]
        
        # Create table
        table_frame = tk.Frame(self.timetable_frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Headers
        days = list(timetable.keys())
        if not days:
            tk.Label(table_frame, text="No timetable generated", bg='white').pack()
            return
        
        # Time column header
        tk.Label(table_frame, text="Time", font=('Arial', 10, 'bold'), 
                relief='solid', bd=1, bg='lightgray').grid(row=0, column=0, sticky='nsew')
        
        # Day headers
        for col, day in enumerate(days, 1):
            tk.Label(table_frame, text=day, font=('Arial', 10, 'bold'), 
                    relief='solid', bd=1, bg='lightgray').grid(row=0, column=col, sticky='nsew')
        
        # Get maximum number of time slots across all days
        max_slots = max(len(timetable[day]) for day in days)
        
        # Create rows
        for row in range(1, max_slots + 1):
            # Time column - use first day's time slot
            first_day = days[0]
            if row-1 < len(timetable[first_day]):
                time_text = timetable[first_day][row-1]['time']
            else:
                time_text = ""
            
            tk.Label(table_frame, text=time_text, font=('Arial', 9), 
                    relief='solid', bd=1, bg='white').grid(row=row, column=0, sticky='nsew')
            
            # Subject for each day
            for col, day in enumerate(days, 1):
                if row-1 < len(timetable[day]):
                    day_slot = timetable[day][row-1]
                    if day_slot['type'] == 'break':
                        text = day_slot['subject']
                        bg_color = 'lightblue'
                    elif day_slot['type'] == 'eca':
                        text = day_slot['subject']
                        bg_color = 'lightgreen'
                    elif day_slot['type'] == 'lab':
                        text = day_slot['subject']
                        bg_color = 'lightyellow'
                    elif day_slot['type'] == 'extra_class':
                        text = day_slot['subject']
                        bg_color = 'lightcoral'
                    else:
                        text = f"{day_slot['subject']}\n({day_slot.get('teacher', 'TBD')})"
                        # Highlight PE periods
                        bg_color = 'lightpink' if day_slot['subject'] == 'Physical Education' else 'white'
                    
                    if self.manual_edit_var.get() and day_slot['type'] not in ['break', 'eca', 'lab', 'extra_class']:
                        # Create editable entry
                        entry = tk.Text(table_frame, height=3, width=15, font=('Arial', 8),
                                       relief='solid', bd=1, bg=bg_color)
                        entry.insert('1.0', text)
                        entry.grid(row=row, column=col, sticky='nsew')
                    else:
                        # Create label
                        label = tk.Label(table_frame, text=text, font=('Arial', 8), 
                                        relief='solid', bd=1, bg=bg_color, wraplength=100)
                        label.grid(row=row, column=col, sticky='nsew')
                else:
                    # Empty cell
                    tk.Label(table_frame, text="", font=('Arial', 8), 
                            relief='solid', bd=1, bg='white').grid(row=row, column=col, sticky='nsew')
        
        # Configure grid weights
        for i in range(len(days) + 1):
            table_frame.columnconfigure(i, weight=1)
        for i in range(max_slots + 1):
            table_frame.rowconfigure(i, weight=1)
    
    def toggle_manual_edit(self):
        """Toggle manual edit mode"""
        self.display_timetable()
    
    def regenerate_timetable(self):
        """Regenerate all timetables"""
        self.generate_timetables()
        self.display_timetable()
        messagebox.showinfo("Success", "Timetables regenerated successfully!\nPhysical Education limited to 2 periods per week.")
    
    def export_timetable_screen(self):
        if not self.timetables:
            messagebox.showerror("Error", "No timetables to export. Please generate timetables first.")
            return
            
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.current_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Add HOME button
        self.create_home_button(self.current_frame)
        
        # Title
        title_frame = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        title_frame.pack(fill='x', pady=10)
        tk.Label(title_frame, text="EXPORT TIME TABLE", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Main container with scrollbars
        main_container = tk.Frame(self.current_frame, bg='white', relief='solid', bd=2)
        main_container.pack(fill='both', expand=True, pady=10)
        
        scrollable_frame = self.create_scrollable_frame(main_container)
        
        # Instructions
        tk.Label(scrollable_frame, text="SELECT TIMETABLE OF CLASS TO EXPORT", 
                bg='white', font=('Arial', 12)).pack(pady=10)
        tk.Label(scrollable_frame, text="(Choose which class timetables to save as image files)", 
                bg='white', font=('Arial', 10), fg='gray').pack()
        
        # Export all checkbox
        self.export_all_var = tk.BooleanVar()
        tk.Checkbutton(scrollable_frame, text="EXPORT ALL", variable=self.export_all_var,
                      bg='white', font=('Arial', 12), command=self.toggle_export_all).pack(pady=10)
        tk.Label(scrollable_frame, text="(Select all classes at once)", bg='white', font=('Arial', 8), fg='gray').pack()
        
        # Individual class checkboxes
        self.export_class_vars = {}
        for class_key in sorted(self.timetables.keys()):
            var = tk.BooleanVar()
            self.export_class_vars[class_key] = var
            
            # Add stream info for display
            class_num = int(class_key.split('-')[0].replace('Class ', ''))
            display_text = class_key
            if class_num >= 11 and class_num in self.stream_data:
                display_text += f" ({self.stream_data[class_num]})"
            
            tk.Checkbutton(scrollable_frame, text=display_text, variable=var,
                          bg='white', font=('Arial', 11)).pack(anchor='w', padx=20, pady=2)
        
        # Export format selection
        format_frame = tk.LabelFrame(scrollable_frame, text="Export Format", bg='white', font=('Arial', 10, 'bold'))
        format_frame.pack(fill='x', padx=20, pady=10)
        
        self.export_format_var = tk.StringVar(value="PNG")
        tk.Radiobutton(format_frame, text="PNG Image", variable=self.export_format_var, value="PNG",
                      bg='white', font=('Arial', 10)).pack(anchor='w', padx=10)
        tk.Radiobutton(format_frame, text="JPG Image", variable=self.export_format_var, value="JPG",
                      bg='white', font=('Arial', 10)).pack(anchor='w', padx=10)
        tk.Radiobutton(format_frame, text="Text File", variable=self.export_format_var, value="TXT",
                      bg='white', font=('Arial', 10)).pack(anchor='w', padx=10)
        
        # Buttons
        btn_frame = tk.Frame(self.current_frame, bg='#90EE90')
        btn_frame.pack(pady=20)
        
        export_btn = self.create_styled_button(btn_frame, "Export Selected", self.export_selected_timetables, width=15, bg_color='lightgreen')
        export_btn.pack(side='left', padx=10)
        
        preview_btn = self.create_styled_button(btn_frame, "Preview", self.preview_export, width=15)
        preview_btn.pack(side='left', padx=10)
        
        back_btn = self.create_styled_button(btn_frame, "Back", self.generate_timetable_screen, width=15, bg_color='lightcoral')
        back_btn.pack(side='left', padx=10)
    
    def toggle_export_all(self):
        """Toggle all class selections"""
        export_all = self.export_all_var.get()
        for var in self.export_class_vars.values():
            var.set(export_all)
    
    def create_timetable_image(self, class_key, timetable):
        """Create a timetable image using PIL"""
        try:
            # Image dimensions
            img_width = 1200
            img_height = 800
            
            # Create image
            img = Image.new('RGB', (img_width, img_height), 'white')
            draw = ImageDraw.Draw(img)
            
            # Try to use a better font, fallback to default
            try:
                title_font = ImageFont.truetype("arial.ttf", 24)
                header_font = ImageFont.truetype("arial.ttf", 16)
                cell_font = ImageFont.truetype("arial.ttf", 12)
            except:
                title_font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                cell_font = ImageFont.load_default()
            
            # Title
            class_num = int(class_key.split('-')[0].replace('Class ', ''))
            title_text = f"TIMETABLE FOR {class_key}"
            if class_num >= 11 and class_num in self.stream_data:
                title_text += f" ({self.stream_data[class_num]} Stream)"
            
            # Draw title
            title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((img_width - title_width) // 2, 20), title_text, fill='black', font=title_font)
            
            # School info
            school_info = f"School: {self.school_data.get('name', 'N/A')} | Board: {self.school_data.get('board', 'N/A')}"
            info_bbox = draw.textbbox((0, 0), school_info, font=header_font)
            info_width = info_bbox[2] - info_bbox[0]
            draw.text(((img_width - info_width) // 2, 60), school_info, fill='gray', font=header_font)
            
            # PE notice
            pe_notice = "Note: Physical Education limited to 2 periods per week"
            notice_bbox = draw.textbbox((0, 0), pe_notice, font=cell_font)
            notice_width = notice_bbox[2] - notice_bbox[0]
            draw.text(((img_width - notice_width) // 2, 90), pe_notice, fill='blue', font=cell_font)
            
            # Table setup
            days = list(timetable.keys())
            if not days:
                return None
            
            max_slots = max(len(timetable[day]) for day in days)
            
            # Table dimensions
            table_start_y = 130
            table_width = img_width - 100
            table_height = img_height - table_start_y - 50
            
            cell_width = table_width // (len(days) + 1)
            cell_height = table_height // (max_slots + 1)
            
            # Draw table borders and headers
            start_x = 50
            
            # Time column header
            draw.rectangle([start_x, table_start_y, start_x + cell_width, table_start_y + cell_height], 
                          outline='black', fill='lightgray')
            draw.text((start_x + 10, table_start_y + 10), "Time", fill='black', font=header_font)
            
            # Day headers
            for col, day in enumerate(days, 1):
                x = start_x + col * cell_width
                draw.rectangle([x, table_start_y, x + cell_width, table_start_y + cell_height], 
                              outline='black', fill='lightgray')
                draw.text((x + 10, table_start_y + 10), day, fill='black', font=header_font)
            
            # Table content
            for row in range(1, max_slots + 1):
                y = table_start_y + row * cell_height
                
                # Time column
                first_day = days[0]
                if row-1 < len(timetable[first_day]):
                    time_text = timetable[first_day][row-1]['time']
                else:
                    time_text = ""
                
                draw.rectangle([start_x, y, start_x + cell_width, y + cell_height], 
                              outline='black', fill='white')
                draw.text((start_x + 5, y + 5), time_text, fill='black', font=cell_font)
                
                # Subject cells
                for col, day in enumerate(days, 1):
                    x = start_x + col * cell_width
                    
                    if row-1 < len(timetable[day]):
                        day_slot = timetable[day][row-1]
                        
                        # Determine cell color and text
                        if day_slot['type'] == 'break':
                            fill_color = 'lightblue'
                            text = day_slot['subject']
                        elif day_slot['type'] == 'eca':
                            fill_color = 'lightgreen'
                            text = day_slot['subject']
                        elif day_slot['type'] == 'lab':
                            fill_color = 'lightyellow'
                            text = day_slot['subject']
                        elif day_slot['type'] == 'extra_class':
                            fill_color = 'lightcoral'
                            text = day_slot['subject']
                        else:
                            fill_color = 'lightpink' if day_slot['subject'] == 'Physical Education' else 'white'
                            text = f"{day_slot['subject']}\n({day_slot.get('teacher', 'TBD')})"
                    else:
                        fill_color = 'white'
                        text = ""
                    
                    draw.rectangle([x, y, x + cell_width, y + cell_height], 
                                  outline='black', fill=fill_color)
                    
                    # Draw text with word wrapping
                    if text:
                        lines = text.split('\n')
                        for i, line in enumerate(lines[:2]):  # Max 2 lines
                            if len(line) > 15:  # Truncate long lines
                                line = line[:12] + "..."
                            draw.text((x + 5, y + 5 + i * 15), line, fill='black', font=cell_font)
            
            return img
            
        except Exception as e:
            print(f"Error creating image: {e}")
            return None
    
    def export_selected_timetables(self):
        """Export selected timetables to image or text files"""
        selected_classes = [class_key for class_key, var in self.export_class_vars.items() if var.get()]
        
        if not selected_classes:
            messagebox.showerror("Error", "Please select at least one class to export")
            return
        
        try:
            # Ask user for directory to save files
            export_dir = filedialog.askdirectory(title="Select Directory to Save Timetables")
            if not export_dir:
                return
            
            export_format = self.export_format_var.get()
            
            for class_key in selected_classes:
                class_num = int(class_key.split('-')[0].replace('Class ', ''))
                
                if export_format in ["PNG", "JPG"]:
                    # Create image
                    img = self.create_timetable_image(class_key, self.timetables[class_key])
                    if img:
                        filename = os.path.join(export_dir, f"{class_key.replace(' ', '_').replace('-', '_')}_timetable.{export_format.lower()}")
                        if export_format == "JPG":
                            img = img.convert('RGB')
                        img.save(filename)
                else:
                    # Create text file
                    filename = os.path.join(export_dir, f"{class_key.replace(' ', '_').replace('-', '_')}_timetable.txt")
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"TIMETABLE FOR {class_key}\n")
                        if class_num >= 11 and class_num in self.stream_data:
                            f.write(f"Stream: {self.stream_data[class_num]}\n")
                        f.write(f"School: {self.school_data.get('name', 'N/A')}\n")
                        f.write(f"Board: {self.school_data.get('board', 'N/A')}\n")
                        f.write("Note: Physical Education limited to 2 periods per week\n")
                        f.write("=" * 80 + "\n\n")
                        
                        timetable = self.timetables[class_key]
                        
                        # Write timetable
                        for day, slots in timetable.items():
                            f.write(f"{day.upper()}\n")
                            f.write("-" * 40 + "\n")
                            
                            for slot in slots:
                                if slot['type'] == 'break':
                                    f.write(f"{slot['time']}: {slot['subject']}\n")
                                elif slot['type'] == 'eca':
                                    f.write(f"{slot['time']}: {slot['subject']}\n")
                                elif slot['type'] == 'lab':
                                    f.write(f"{slot['time']}: {slot['subject']}\n")
                                elif slot['type'] == 'extra_class':
                                    f.write(f"{slot['time']}: {slot['subject']}\n")
                                else:
                                    teacher_info = f" - {slot.get('teacher', 'TBD')}" if slot.get('teacher') else ""
                                    f.write(f"{slot['time']}: {slot['subject']}{teacher_info}\n")
                            
                            f.write("\n")
            
            messagebox.showinfo("Success", f"Timetables exported successfully to {export_dir} as {export_format} files!\nPhysical Education limited to 2 periods per week.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export timetables: {str(e)}")
    
    def preview_export(self):
        """Preview selected timetables"""
        selected_classes = [class_key for class_key, var in self.export_class_vars.items() if var.get()]
        
        if not selected_classes:
            messagebox.showerror("Error", "Please select at least one class to preview")
            return
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Timetable Preview")
        preview_window.geometry("800x600")
        preview_window.configure(bg='white')
        
        # Create scrollable text widget
        text_frame = tk.Frame(preview_window, bg='white')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap='word', font=('Courier', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Generate preview content
        preview_content = ""
        for class_key in selected_classes:
            class_num = int(class_key.split('-')[0].replace('Class ', ''))
            
            preview_content += f"TIMETABLE FOR {class_key}\n"
            if class_num >= 11 and class_num in self.stream_data:
                preview_content += f"Stream: {self.stream_data[class_num]}\n"
            preview_content += f"School: {self.school_data.get('name', 'N/A')}\n"
            preview_content += f"Board: {self.school_data.get('board', 'N/A')}\n"
            preview_content += "Note: Physical Education limited to 2 periods per week\n"
            preview_content += "=" * 60 + "\n\n"
            
            timetable = self.timetables[class_key]
            
            for day, slots in timetable.items():
                preview_content += f"{day.upper()}\n"
                preview_content += "-" * 30 + "\n"
                
                for slot in slots:
                    if slot['type'] == 'break':
                        preview_content += f"{slot['time']}: {slot['subject']}\n"
                    elif slot['type'] == 'eca':
                        preview_content += f"{slot['time']}: {slot['subject']}\n"
                    elif slot['type'] == 'lab':
                        preview_content += f"{slot['time']}: {slot['subject']}\n"
                    elif slot['type'] == 'extra_class':
                        preview_content += f"{slot['time']}: {slot['subject']}\n"
                    else:
                        teacher_info = f" - {slot.get('teacher', 'TBD')}" if slot.get('teacher') else ""
                        preview_content += f"{slot['time']}: {slot['subject']}{teacher_info}\n"
                
                preview_content += "\n"
            
            preview_content += "\n" + "=" * 60 + "\n\n"
        
        text_widget.insert('1.0', preview_content)
        text_widget.config(state='disabled')
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Close button
        close_btn = self.create_styled_button(preview_window, "Close", preview_window.destroy, width=15, bg_color='lightcoral')
        close_btn.pack(pady=10)

    def save_project(self):
        """Save all project data to a file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".ttg",
                filetypes=[("Timetable Generator files", "*.ttg"), ("All files", "*.*")],
                title="Save Timetable Project"
            )
            
            if filename:
                project_data = {
                    'school_data': self.school_data,
                    'classes_data': self.classes_data,
                    'teachers_data': self.teachers_data,
                    'subjects_data': self.subjects_data,
                    'stream_data': self.stream_data,
                    'eca_data': self.eca_data,
                    'lab_data': self.lab_data,
                    'timetables': self.timetables
                }
                
                with open(filename, 'wb') as f:
                    pickle.dump(project_data, f)
                
                messagebox.showinfo("Success", f"Project saved successfully to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save project: {str(e)}")
    
    def load_project(self):
        """Load project data from a file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Timetable Generator files", "*.ttg"), ("All files", "*.*")],
                title="Load Timetable Project"
            )
            
            if filename:
                with open(filename, 'rb') as f:
                    project_data = pickle.load(f)
                
                self.school_data = project_data.get('school_data', {})
                self.classes_data = project_data.get('classes_data', [])
                self.teachers_data = project_data.get('teachers_data', [])
                self.subjects_data = project_data.get('subjects_data', {})
                self.stream_data = project_data.get('stream_data', {})
                self.eca_data = project_data.get('eca_data', {})
                self.lab_data = project_data.get('lab_data', {})
                self.timetables = project_data.get('timetables', {})
                
                messagebox.showinfo("Success", f"Project loaded successfully from {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load project: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TimetableGenerator()
    app.run()
