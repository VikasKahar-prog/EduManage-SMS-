import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageFont,ImageSequence
from datetime import datetime, date
from time import strftime
from tkinter import filedialog
import os
import tkcalendar
from tkcalendar import DateEntry
from tkinter import ttk
import mysql.connector as mycon
from tkinter import messagebox
import win32api
import textwrap
import warnings
import time
import tkintermapview
from threading import Thread
import yagmail
from tooltip import ToolTip
import wikipedia
import pyttsx3
import speech_recognition as sr
import fitz
import mimetypes
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
import re

class HoverColor:
    def __init__(self,button, image_name, image_name1):
        button.bind("<Enter>", lambda e : button.configure(fg_color = "#EE4E4E", image = image_name, text_color = "white"))
        button.bind("<Leave>", lambda e : button.configure(fg_color = "#0766AD", image = image_name1, text_color = "white"))

class FocusColor:
    def __init__(self,entry, border_color):
        entry.bind("<FocusIn>", lambda e : entry.configure(border_width = 2, border_color=border_color))
        entry.bind("<FocusOut>", lambda e : entry.configure(border_width = 0,))
        
class ChangeLabel(ctk.CTkLabel):
    def __init__(self, parent_frame, text, fg_color, text_color ):
        self.my_label = ctk.CTkLabel(parent_frame, text = text, width = 1092, height = 40, fg_color=fg_color, text_color=text_color, font = ("Verdana", 20))
        self.my_label.place(x = 0, y = 0)

class SetImage(ctk.CTkImage):
    def __init__(self, image_path, width, height):
        light_img = Image.open(image_path)
        dark_img = Image.open(image_path)
        super().__init__(light_image=light_img, dark_image=dark_img, size=(width, height))

class HeadingFrame(ctk.CTkFrame):
    def __init__(self, parent_frame, width=1526, height=90, heading_image_path="image/heading_image_ss.png",
                 heading_logo_path="image/logo_comp.png",fg_color="white", border_width=1, border_color="#0766AD", corner_radius=1):
        super().__init__(parent_frame, width=width, height=height, fg_color=fg_color, border_width=border_width,
                         border_color=border_color, corner_radius=corner_radius)

        self.heading_logo_path = heading_logo_path
        self.heading_image_path = heading_image_path

        self.create_widgets()
        self.update_date_time()

    def create_widgets(self):
        self.heading_logo = ctk.CTkImage(light_image=Image.open(self.heading_logo_path),dark_image=Image.open(self.heading_logo_path), size=(100, 75))
        self.heading_logo_label = ctk.CTkLabel(self, text="", image=self.heading_logo)
        self.heading_logo_label.place(x=140, y=10)
        self.heading_image = ctk.CTkImage(light_image=Image.open(self.heading_image_path),dark_image=Image.open(self.heading_image_path), size=(1000, 80))
        self.heading_label = ctk.CTkLabel(self, text="", image=self.heading_image)
        self.heading_label.place(x=250, y=3)
        self.time_label = ctk.CTkLabel(self, text="time", font=("Courier", 24, "bold"), text_color="red")
        self.time_label.place(x=1370, y=18)
        self.date_label = ctk.CTkLabel(self, text="date", font=("Verdana Pro", 14), text_color="red")
        self.date_label.place(x=1370, y=48)

    def update_date_time(self):
        current_time = time.strftime("%I:%M:%S")
        current_date = time.strftime("%a, %d %B %Y")
        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)
        self.after(1000, self.update_date_time)

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="white")
        self.title("School Management System")
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.geometry(f"{self.width}x{self.height}-10-7")
        self.iconbitmap("image/slogo.ico")

        #========bind the close event=========#
        self.protocol("WM_DELETE_WINDOW", self.confirm_exit) 

    def confirm_exit(self):
        answer = messagebox.askquestion("Confirm Exit", "Are you sure you want to exit?")
        if answer == "yes":
            self.destroy()
       
    #========functions=============# 
    def home_page(self):
        self.x = 1
        def move():
            global x
            img1 = ctk.CTkImage(light_image=Image.open("image/slideshow1.png"), dark_image=Image.open("image/slideshow1.png"), size = (896, 446))
            img2 = ctk.CTkImage(light_image=Image.open("image/slideshow2.png"), dark_image=Image.open("image/slideshow2.png"), size = (896, 446))
            img3 = ctk.CTkImage(light_image=Image.open("image/slideshow3.png"), dark_image=Image.open("image/slideshow3.png"), size = (896, 446))
            img4 = ctk.CTkImage(light_image=Image.open("image/slideshow4.png"), dark_image=Image.open("image/slideshow4.png"), size = (896, 446))
            
            if self.x == 1:
                self.slide_label.configure(image = img1)
            elif self.x == 2:
                self.slide_label.configure(image = img2)
            elif self.x == 3:
                self.slide_label.configure(image = img3)
            elif self.x == 4:
                self.slide_label.configure(image = img4)
            elif self.x == 5:
                self.x= -1
            self.x = self.x + 1
            self.after(1000, move)
        
        #=====calling the admin_login_page=========#
        def admin_login_page():
            self.withdraw()
            new_window = AdminLoginWindow()
            new_window.title("School Management System")

        def ask_a_question_page():
            self.withdraw()
            askquestion_window = AskAQuestionWindow()
            askquestion_window.title("School Management System")

        def announcement_page():
            self.withdraw()
            notice_window = AnnouncementWindow()
            notice_window.title("School Management System")

        def contact_us_page():
            self.withdraw()
            contac_window = ContactUsWindow()
            contac_window.title("School Management System")

        def again_home_page():
            self.home_page()

        #======calling heading label class =======#
        self.heading_frame = HeadingFrame(self)
        self.heading_frame.place(x = 5, y = 5)

        #=====tabs menu========#
        self.tab_frame = ctk.CTkFrame(self, width = 1526, height = 60, fg_color="#0766AD", corner_radius=0, border_width=0, border_color="black")

        home_img = SetImage(image_path="image/home.png", width= 30, height = 30)
        self.home_button = ctk.CTkButton(self.tab_frame, text = "Home", width = 250, height = 52, border_width=0, border_color="#0766AD", font = ("Verdana Pro",18), text_color="white", fg_color="#0766AD", corner_radius=0, hover_color="white", cursor = "hand2", command=again_home_page, image=home_img)
        self.home_button.place(x = 1, y = 0)
        HoverColor(self.home_button, image_name=home_img, image_name1=home_img)
        
        admin_image = SetImage(image_path="image/settings.png", width= 30, height = 30)
        self.admin_button = ctk.CTkButton(self.tab_frame, text = "Admin Panel"
        , width = 250, height = 52, border_width=0, border_color="#0766AD", font = ("Verdana Pro", 18), text_color="white", fg_color="#0766AD", corner_radius=0, hover_color="white", cursor = "hand2", command = admin_login_page, image = admin_image)
        self.admin_button.place(x = 251 , y = 0)
        HoverColor(self.admin_button, image_name=admin_image, image_name1=admin_image)

        announcement_image = SetImage(image_path="image/attention.png", width= 30, height = 30)
        announcement_image1 = SetImage(image_path="image/attention (2).png", width= 30, height = 30)
        self.announcement_button = ctk.CTkButton(self.tab_frame, text = "Announcement", width = 250, height = 52, border_width=0, border_color="#0766AD", font = ("Verdana Pro", 18), text_color="white", fg_color="#0766AD", corner_radius=0, hover_color="white", cursor = "hand2", command=announcement_page, image = announcement_image)
        self.announcement_button.place(x = 501, y = 0)
        HoverColor(self.announcement_button, image_name=announcement_image1, image_name1=announcement_image)

        question_image = SetImage(image_path="image/question-and-answer (1).png", width= 30, height = 30)
        question_image1 = SetImage(image_path="image/question-and-answer.png", width= 30, height = 30)
        self.ask_a_question_button = ctk.CTkButton(self.tab_frame, text = "Ask a question", width = 250, height = 52, border_width=0, border_color="#0766AD", font = ("Verdana Pro", 18), text_color="white", fg_color="#0766AD", corner_radius=0, hover_color="white", cursor = "hand2", command=ask_a_question_page, image = question_image)
        self.ask_a_question_button.place(x = 751, y = 0)
        HoverColor(self.ask_a_question_button, image_name=question_image1, image_name1= question_image)

        contact_image = SetImage(image_path="image/contact-mail (1).png", width= 30, height = 30)
        self.contact_us = ctk.CTkButton(self.tab_frame, text = "Contact Us", width = 250, height = 52, border_width=0, border_color="#0766AD", font = ("Verdana Pro", 18), text_color="white", fg_color="#0766AD", corner_radius=0, hover_color="white", cursor = "hand2", command = contact_us_page, image = contact_image)
        self.contact_us.place(x = 1001, y = 0)
        HoverColor(self.contact_us, image_name=contact_image, image_name1=contact_image)

        self.tab_frame.pack_propagate(False)
        self.tab_frame.place(x = 5, y = 94)
        
        #======main_frame========#
        self.main_frame = ctk.CTkFrame(self, width = 1526, height = 690, fg_color="white", corner_radius=1, border_width=1, border_color="#0766AD")

        #+========left side frame==========#
        self.leftside_frame = ctk.CTkFrame(self.main_frame, width = 440, height = 670, fg_color="white", corner_radius=1, border_width=0, border_color="#0766AD")

        def student_login():
            global student_email_entry, student_password_entry

            #====show password====#
            self.show = "*"
            def show_password():
                global show
                if self.show  == "*":
                    self.hide_image_button.configure(image = self.show_image)
                    student_password_entry.configure(show = "")
                    self.show = ""
                else:
                    self.hide_image_button.configure(image = self.hide_image)
                    student_password_entry.configure(show = "*")
                    self.show = "*"      

            #======focus next bind event=========#
            def on_return(event):
                event.widget.tk_focusNext().focus()
                return "break"
        
            #=======main login frame==============#
            self.student_login_frame = ctk.CTkFrame(self.leftside_frame, width = 420, height = 335, fg_color="white", corner_radius=1, border_width=1, border_color="blue")

            #=======button frame================#
            self.button_frame = ctk.CTkFrame(self.student_login_frame, width = 420, height = 40, fg_color="white")

            self.my_account_button = ctk.CTkButton(self.button_frame, text = "My Account", font = ("Verdana Pro", 18), corner_radius=0, fg_color="#074173", text_color="white", width = 210, height = 40)
            self.my_account_button.place(x = 0, y = 0)

            self.registration_button = ctk.CTkButton(self.button_frame, text = "Registration", font = ("Verdana Pro", 18), corner_radius=0, fg_color="#378CE7", text_color="white", width = 212, height = 40, command = self.student_registration)
            self.registration_button.place(x = 209, y = 0)
            ToolTip(self.registration_button, text = "Enter personal details to register.")
            
            self.button_frame.place(x = 0, y = 0)

            #=========student email entry=============#
            student_email_entry = ctk.CTkEntry(self.student_login_frame, border_width=0, border_color="black", width = 320, height = 30, corner_radius=0, font = ("Verdana Pro", 15), placeholder_text="Email", fg_color="white")
            student_email_entry.place(x = 18, y = 70)
            student_email_entry.bind("<FocusIn>", lambda e : self.line1.config(bg = "#074173"))
            student_email_entry.bind("<FocusOut>", lambda e : self.line1.config(bg = "grey"))
            ToolTip(student_email_entry, text = "Enter your username.")

            self.line1 = tk.Label(self.student_login_frame, bg="grey")
            self.line1.place(x = 30, y = 130, width = 440, height = 2)

            #=======student password entry===========#
            student_password_entry = ctk.CTkEntry(self.student_login_frame, border_width=0, border_color="black", width = 320, height = 30, corner_radius=0, font = ("Verdana Pro", 16), placeholder_text="Password", fg_color="white", show = "*")
            student_password_entry.place(x = 18, y = 130)
            student_password_entry.bind("<FocusIn>", lambda e : self.line2.config(bg = "#074173"))
            student_password_entry.bind("<FocusOut>", lambda e : self.line2.config(bg = "grey"))
            ToolTip(student_password_entry, text = "Enter your password.")

            self.line2 = tk.Label(self.student_login_frame, bg="grey")
            self.line2.place(x = 30, y = 205, width = 445, height = 2)

            #========hide image=========#
            self.hide_image = SetImage(image_path="image/hide.png", width = 25, height=25)
            self.show_image = SetImage(image_path="image/eye.png", width = 25, height=25)

            self.hide_image_button = ctk.CTkButton(self.student_login_frame, text = "", image = self.hide_image, width = 0, height = 0, hover="disabled", fg_color="transparent", bg_color="transparent", cursor = "hand2", command = show_password)
            self.hide_image_button.place(x = 342, y = 130)
            
            #========login button==========#
            self.student_login_button = ctk.CTkButton(self.student_login_frame, text = "LOGIN", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=0, width = 120, height = 35, command=self.student_login)
            self.student_login_button.place(x = 25, y = 200)

            #========message frame==========#
            self.student_message_frame = ctk.CTkFrame(self.student_login_frame, width = 420 ,height = 65, fg_color="#378CE7", corner_radius=0, border_width=0)

            self.student_image = SetImage(image_path="image/student (3).png", width = 50, height=50)  
            self.student_image_label = ctk.CTkLabel(self.student_message_frame, text = "", image = self.student_image)
            self.student_image_label.place(x = 5, y = 5)

            self.student_text_label = ctk.CTkLabel(self.student_message_frame, text = "Student Login with username and password and view reports", wraplength=350, font = ("Verdana Pro", 15), text_color="white")
            self.student_text_label.place(x = 60, y = 10)

            self.student_message_frame.place(x = 0, y = 270)

            #======bind the entry box for enter button==========#
            student_email_entry.bind("<Return>", on_return)
            student_password_entry.bind("<Return>", on_return)

            self.student_login_frame.place(x = 10, y = 10) 

        #======================================#
        def teacher_login():
            global teacher_email_entry, teacher_password_entry
            #====show password====#
            self.show = "*"
            def show_password():
                global show
                if self.show  == "*":
                    self.hide_image_button.configure(image = self.show_image)
                    teacher_password_entry.configure(show = "")
                    self.show = ""
                else:
                    self.hide_image_button.configure(image = self.hide_image)
                    teacher_password_entry.configure(show = "*")
                    self.show = "*"  

            #======focus next bind event=========#
            def on_return(event):
                event.widget.tk_focusNext().focus()
                return "break"    
        
            #=======main login frame==============#
            self.teacher_login_frame = ctk.CTkFrame(self.leftside_frame, width = 420, height = 335, fg_color="white", corner_radius=0, border_width=1, border_color="blue")

            #=======button frame================#
            self.button_frame = ctk.CTkFrame(self.teacher_login_frame, width = 420, height = 40, fg_color="white")

            self.my_account_button = ctk.CTkButton(self.button_frame, text = "My Account", font = ("Verdana Pro", 18), corner_radius=0, fg_color="#401F71", text_color="white", width = 210, height = 40, hover_color="#401F71")
            self.my_account_button.place(x = 0, y = 0)

            self.registration_button = ctk.CTkButton(self.button_frame, text = "Registration", font = ("Verdana Pro", 18), corner_radius=0, fg_color="#912BBC", text_color="white", width = 212, height = 40, command=self.teacher_registration, hover_color = "#912BBC")
            self.registration_button.place(x = 209, y = 0)
            ToolTip(self.registration_button, text = "Enter personal details to register.")

            self.button_frame.place(x = 0, y = 0)

            #=========teacher email entry=============#
            teacher_email_entry = ctk.CTkEntry(self.teacher_login_frame, border_width=0, border_color="black", width = 320, height = 30, corner_radius=0, font = ("Verdana Pro", 15), placeholder_text="Email", fg_color="white")
            teacher_email_entry.place(x = 18, y = 70)
            teacher_email_entry.bind("<FocusIn>", lambda e : self.line1.config(bg = "#074173"))
            teacher_email_entry.bind("<FocusOut>", lambda e : self.line1.config(bg = "grey"))
            ToolTip(teacher_email_entry, text = "Enter your username.")

            self.line1 = tk.Label(self.teacher_login_frame, bg="grey")
            self.line1.place(x = 30, y = 130, width = 440, height = 2)

            #=======teacher password entry===========#
            teacher_password_entry = ctk.CTkEntry(self.teacher_login_frame, border_width=0, border_color="black", width = 320, height = 30, corner_radius=0, font = ("Verdana Pro", 16), placeholder_text="Password", fg_color="white", show = "*")
            teacher_password_entry.place(x = 18, y = 130)
            teacher_password_entry.bind("<FocusIn>", lambda e : self.line2.config(bg = "#074173"))
            teacher_password_entry.bind("<FocusOut>", lambda e : self.line2.config(bg = "grey"))
            ToolTip(teacher_password_entry, text = "Enter your password.")

            self.line2 = tk.Label(self.teacher_login_frame, bg="grey")
            self.line2.place(x = 30, y = 205, width = 440, height = 2)

            #========hide image=========#
            self.hide_image = SetImage(image_path="image/hide.png", width = 25, height=25) 
            self.show_image = SetImage(image_path="image/eye.png", width = 25, height=25) 

            self.hide_image_button = ctk.CTkButton(self.teacher_login_frame, text = "", image = self.hide_image, width = 0, height = 0, hover="disabled", fg_color="transparent", bg_color="transparent", cursor = "hand2", command=show_password)
            self.hide_image_button.place(x = 342, y = 130)
            
            #========login button==========#
            self.teacher_login_button = ctk.CTkButton(self.teacher_login_frame, text = "LOGIN", font = ("Verdana Pro", 18), fg_color="#401F71", corner_radius=0, width = 120, height = 35, command=self.teacher_login, hover_color="#912BBC")
            self.teacher_login_button.place(x = 25, y = 200)

            #========message frame==========#
            self.teacher_message_frame = ctk.CTkFrame(self.teacher_login_frame, width = 420 ,height = 65, fg_color="#912BBC", corner_radius=0, border_width=0)

            self.teacher_image = SetImage(image_path="image/teacher (1).png", width = 50, height=50) 
            self.teacher_image_label = ctk.CTkLabel(self.teacher_message_frame, text = "", image = self.teacher_image)
            self.teacher_image_label.place(x = 5, y = 5)

            self.teacher_text_label = ctk.CTkLabel(self.teacher_message_frame, text = "Staff can make attendance of student and generate reports after login to system", wraplength=350, font = ("Verdana Pro", 15), text_color="white")
            self.teacher_text_label.place(x = 60, y = 10)

            self.teacher_message_frame.place(x = 0, y = 270)

            #===bind the entry box for focusnext========#
            teacher_email_entry.bind("<Return>", on_return)
            teacher_password_entry.bind("<Return>", on_return)

            self.teacher_login_frame.place(x = 10, y = 10) 

        #========student and teacher choose button===========#
        self.ask_teacher_image = SetImage(image_path="image/school.png", width = 60, height=60) 
        self.ask_teacher_label = ctk.CTkLabel(self.leftside_frame, text = "", image = self.ask_teacher_image)
        self.ask_teacher_label.place(x = 10, y = 500)

        self.choose_teacher_button = ctk.CTkButton(self.leftside_frame, text = "Staff", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=1, width = 120, height = 35, command = teacher_login, cursor = "hand2")
        self.choose_teacher_button.place(x = 80, y = 510)

        self.ask_student_image = SetImage(image_path="image/reading-book (1).png", width = 60, height=60) 
        self.ask_student_label = ctk.CTkLabel(self.leftside_frame, text = "", image = self.ask_student_image)
        self.ask_student_label.place(x = 10, y = 580)

        self.choose_student_button = ctk.CTkButton(self.leftside_frame, text = "Student", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=1, width = 120, height = 35, command = student_login, cursor = "hand2")
        self.choose_student_button.place(x = 80, y = 590)

        #======calling the function===========#
        student_login()

        self.leftside_frame.place(x = 30, y = 15)
        #========================================#

        #====slide show============#
        self.slideshow_frame = ctk.CTkFrame(self.main_frame, width = 930, height = 670, fg_color="white", corner_radius=1, border_width=0, border_color="green")
        #===========================
        self.inside_frame = ctk.CTkFrame(self.slideshow_frame, width = 900, height = 450, fg_color="white", corner_radius=0)

        self.slide_label = ctk.CTkLabel(self.inside_frame, text = "", fg_color="black")
        self.slide_label.place(x = 2, y = 2)
        move()         #calling move function

        self.inside_frame.place(x = 10, y = 10)
        #===========================
        self.quote_image = SetImage(image_path="image/slogan.png", width = 900, height=150) 
        self.quote_label = ctk.CTkLabel(self.slideshow_frame, text = "", image = self.quote_image)
        self.quote_label.place(x = 10, y = 480)

        self.slideshow_frame.place(x = 550, y = 10)
        self.main_frame.place(x = 5, y = 145)
        self.main_frame.pack_propagate(False)

    #=======student personal detail page===========#
    def student_registration(self):
        self.withdraw() 
        new_window = StudentWindow()
        new_window.title("Student Management System")

    #=======Teacher personal detail page===========#
    def teacher_registration(self):
        self.withdraw()
        new_window=TeacherWindow()
        new_window.title("School Management System")

    def student_login(self):
        global student_username, student_password
        #========email and password from entry box=========#
        student_username = student_email_entry.get()
        student_password = student_password_entry.get()

        #========check username and password from database=======#
        if student_username == "" and student_password == "":
            messagebox.showerror("Empty Fields", "Please enter both email and password.")
            return
        if student_username == "":
            messagebox.showerror("Missing Email", "Please enter your email address.")
            return
        if student_password == "":
            messagebox.showerror("Missing Password", "Please enter your password.")
            return
        else:        
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #fetch username and password
                cur.execute("select email, concat(first_name,'@',student_id) as password from student where email = %s and concat(first_name,'@',student_id) = %s", (student_username, student_password))

                db_records = cur.fetchone()

                if db_records is None:
                    messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")
                    # return
                elif student_username == db_records[0] and student_password == db_records[1]:
                    #======open home window===========#
                    self.withdraw()
                    new_window = StudentHomeWindow()
                    new_window.title("School Management System")
                    new_window.profile_frame()
                    messagebox.showinfo("Login Successful", "Welcome back!")

                #clear the textbox
                student_email_entry.delete(0, tk.END)
                student_password_entry.delete(0, tk.END)

                #close the connection
                con.close()

            except Exception as e:
                print("Error :", e)
        
    #=========Teacher home page===========#
    def teacher_login(self):
        global teacher_username, teacher_password
        #========email and password from entry box=========#
        teacher_username = teacher_email_entry.get()
        teacher_password = teacher_password_entry.get()

        #========check username and password from database=======#
        if teacher_username == "" and teacher_password == "":
            messagebox.showerror("Empty Fields", "Please enter both email and password.")
            return
        if teacher_username == "":
            messagebox.showerror("Missing Email", "Please enter your email address.")
            return
        if teacher_password == "":
            messagebox.showerror("Missing Password", "Please enter your password.")
            return
        else:        
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #fetch username and password
                cur.execute("select email, concat(first_name,'@',staff_id) as password from staff where email = %s and concat(first_name,'@',staff_id) = %s", (teacher_username,teacher_password))

                db_records = cur.fetchone()
                if db_records is None:
                    messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")

                elif teacher_username == db_records[0] and teacher_password == db_records[1]:
                    #======open home window===========#
                    self.withdraw()
                    new_window=TeacherHomeWindow()
                    new_window.title("School Management System")
                    new_window.profile_frame()
                    messagebox.showinfo("Login Successful", "Welcome back!")

                #clear the textbox
                teacher_email_entry.delete(0, tk.END)
                teacher_password_entry.delete(0, tk.END)

                #close the connection
                con.close()

            except Exception as e:
                print("Error :", e)

class AdminLoginWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__(fg_color="#8B93FF")
        self.geometry("1536x864-10-7")
        self.title("School Management System")
        self.after(200, lambda : self.iconbitmap("image/slogo.ico"))
        
        #===call the return to main
        def return_to_home():
            self.destroy()
            root.deiconify()

        def underline_to_label(event):
            self.underline_label = tk.Label(self.admin_login_frame,bg="blue")
            self.underline_label.place(x = 163, y = 350, width = 150, height=4)

        def noline_to_label(event):
            self.underline_label = tk.Label(self.admin_login_frame,bg="white")
            self.underline_label.place(x = 163, y = 350, width = 150, height=4)

        def admin_home_page():
            global admin_username, admin_password
            admin_username = self.admin_username_entry.get()
            admin_password = self.admin_password_entry.get()

            if not admin_username and not admin_password:
                messagebox.showerror("Error", "Please enter a username and password.")
                return
            if not admin_username:
                messagebox.showerror("Error", "Please enter a username.")
                return 
            if not admin_password:
                messagebox.showerror("Error", "Please enter a password.")
                return
            if admin_username == "admin" and admin_password == "secret":
                self.destroy()
                new_window = AdminHomeWindow()
                new_window.title("School Management System")
                new_window.dashboard_frame()
                messagebox.showinfo("Login Successful","Welcome back, Administrator!")
            else:
                messagebox.showerror("Login Failed", "Invalid admin login credentials. Please try again.")

        #=======event for next focus of entry widgets=======#
        def on_return(event):
            event.widget.tk_focusNext().focus()
            return "break"

        #====show password====#
        self.show = "*"
        def show_password():
            global show
            if self.show  == "*":
                self.hide_image_button.configure(image = self.show_image)
                self.admin_password_entry.configure(show = "")
                self.show = ""
            else:
                self.hide_image_button.configure(image = self.hide_image)
                self.admin_password_entry.configure(show = "*")
                self.show = "*" 
 
        #======calling heading label class =======#
        self.heading_frame = HeadingFrame(self)
        self.heading_frame.place(x = 5, y = 5)

        self.admin_login_frame = ctk.CTkFrame(self, width = 420, height=300, corner_radius=0, fg_color="white", border_width=2, border_color="#1D49CB")

        # #======other widgets=========#
        self.admin_login_panel = ctk.CTkLabel(self.admin_login_frame, text = "Admin Login Panel", text_color="white", font = ("Verdana Pro", 18), width = 420, height = 40, fg_color="#1D49CB")
        self.admin_login_panel.place(x = 0, y = 0)

        #========admin username===========#
        self.admin_username_entry = ctk.CTkEntry(self.admin_login_frame, border_width=0, border_color="black", width = 320, height = 30, corner_radius=0, font = ("Verdana Pro", 15), placeholder_text="Admin username", fg_color="white")
        self.admin_username_entry.place(x = 18, y = 70)
        self.admin_username_entry.bind("<FocusIn>", lambda e : self.line1.config(bg = "#074173"))
        self.admin_username_entry.bind("<FocusOut>", lambda e : self.line1.config(bg = "grey"))
        ToolTip(self.admin_username_entry, text = "Admin username required.")

        self.line1 = tk.Label(self.admin_login_frame, bg="grey")
        self.line1.place(x = 30, y = 130, width = 440, height = 2)

        #===========admin password===========#
        self.admin_password_entry = ctk.CTkEntry(self.admin_login_frame, border_width=0, border_color="black", width = 320, height = 30, corner_radius=0, font = ("Verdana Pro", 16), placeholder_text="Admin password", fg_color="white", show = "*")
        self.admin_password_entry.place(x = 18, y = 130)
        self.admin_password_entry.bind("<FocusIn>", lambda e : self.line2.config(bg = "#074173"))
        self.admin_password_entry.bind("<FocusOut>", lambda e : self.line2.config(bg = "grey"))
        ToolTip(self.admin_password_entry, text = "Admin password required.")

        self.line2 = tk.Label(self.admin_login_frame, bg="grey")
        self.line2.place(x = 30, y = 205, width = 440, height = 2)

        #========hide image=========#
        self.hide_image = SetImage(image_path="image/hide.png", width = 25, height=25)
        self.show_image = SetImage(image_path="image/eye.png", width = 25, height=25)

        self.hide_image_button = ctk.CTkButton(self.admin_login_frame, text = "", image = self.hide_image, width = 0, height = 0, hover="disabled", fg_color="transparent", bg_color="transparent", cursor = "hand2", command=show_password)
        self.hide_image_button.place(x = 342, y = 130)
            
        #========login button==========#
        self.admin_login_button = ctk.CTkButton(self.admin_login_frame, text = "LOGIN", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=0, width = 120, height = 35, command=admin_home_page)
        self.admin_login_button.place(x = 25, y = 200)

        #=====back to home==========#
        self.admin_logout_button = ctk.CTkButton(self.admin_login_frame, text = "Back to Home",width = 0, height = 0, font = ("Consolas", 18), text_color="blue", hover = "disabled", cursor = "hand2", fg_color="transparent" , command= return_to_home)
        self.admin_logout_button.place(x = 130, y = 250)

        self.admin_logout_button.bind("<Enter>", underline_to_label)
        self.admin_logout_button.bind("<Leave>", noline_to_label)

        #==bind the all entry box for focus next=====#
        self.admin_username_entry.bind("<Return>", on_return)
        self.admin_password_entry.bind("<Return>", on_return)

        self.admin_login_frame.place(x = 550 , y = 200)

class StudentWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__(fg_color="#E0F4FF")
        self.geometry("1536x864-10-7")
        self.title("School Management System")

        #======functions=======#
        self.file = ""
        def upload_photo():
            global file
            photo_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("JPG Files", "*.jpg"),("PNG Files", "*.png"),("All files", "*.*")], initialdir="C:/Users/vikas/OneDrive/Documents", title="Open File")

            if photo_path:
                self.file = photo_path
                self.file_path_label.configure(text = f"{os.path.basename(photo_path)}", text_color = "red")

        def open_calendar():
            global cal
            calendar_window = ctk.CTkToplevel(self)
            calendar_window.geometry("300x200+950+700")
            calendar_window.title("Calendar")
            calendar_window.resizable(False, False)

            cal = tkcalendar.Calendar(calendar_window,date_pattern = "yyyy-mm-dd" ,background = "#388E3C")
            cal.pack(fill = "both", expand = True)
            cal.bind("<<CalendarSelected>>", lambda e : grab_date(cal))

            calendar_window.grab_set()

        def grab_date(event):
            global cal
            self.dob_entry.delete(0, tk.END)
            self.dob_entry.insert(tk.END, cal.get_date())

        def return_to_main():
            self.destroy()
            root.deiconify()

        #=======fetch standard record ==========#
        def fetch_std_record():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #execute the cursor query
                cur.execute("select std_name from standard")

                records = cur.fetchall()

                std_list = []
                for record in records:
                    std_list.append(record[0])
                
                #======configure the option menu for standard values
                self.standard_values = std_list
                self.standard_option.configure(values = self.standard_values)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        def on_return(event):
            event.widget.tk_focusNext().focus()
            return "break"
        
        #=======fetch division record ==========#
        def fetch_div_record():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #execute the cursor query
                cur.execute("select div_name from division group by div_name")

                records = cur.fetchall()

                div_list = []
                for record in records:
                    div_list.append(record[0])
                
                #======configure the option menu for standard values
                self.division_values= div_list
                self.division_option.configure(values = self.division_values)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        def student_registration():
            first_name = self.firstname_entry.get().capitalize()
            last_name = self.lastname_entry.get().capitalize()
            std = std_var_reg.get()
            div = div_var_reg.get()
            father_name = self.father_entry.get().capitalize()
            mother_name = self.mother_entry.get().capitalize()
            gender = gender_value.get().upper()
            contact = self.phone_entry.get()
            email = self.email_entry.get()
            address = self.address_textbox.get("0.0", tk.END)
            city = self.city_entry.get().capitalize()
            pincode = self.pincode_var.get()
            dob = self.dob_var.get()
            nationality = self.nationality_entry.get().capitalize()
            religion = self.religion_entry.get().capitalize()
            mother_tongue = self.mothertongue_entry.get().capitalize()
            image_path = self.file

            if (first_name or last_name or std or div or father_name or mother_name or gender or contact or email or address or city or pincode or dob or nationality or religion or mother_tongue or image_path) == "":
                messagebox.showerror("Error", "Please fill out all required fields before submitting.")

            else:
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #====Condition====#
                    flag=True
                    if not first_name.isalpha():
                        self.firstname_entry.configure(border_color="red")
                        flag=False
                    if not last_name.isalpha():
                        self.lastname_entry.configure(border_color="red")
                        flag=False
                    if not std:
                        flag=False
                    if not div:
                        flag=False
                    if not father_name.isalpha():
                        self.father_entry.configure(border_color="red")
                        flag=False
                    if not mother_name.isalpha():
                        self.mother_entry.configure(border_color="red")
                        flag=False
                    if not re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email):
                        self.email_entry.configure(border_color="red")
                        flag=False
                    if not re.match(r"^[789]\d{9}$", contact):
                        self.phone_entry.configure(border_color="red")
                        flag=False
                    if not dob:
                        flag=False
                    if not re.match(r"^[A-Za-z0-9\s\-.,]+", address):
                        self.address_textbox.configure(border_color="red")
                        flag=False
                    if not city.isalpha():
                        self.city_entry.configure(border_color="red")
                        flag=False
                    if not re.match(r"^\d{5,6}$", pincode):
                        self.pincode_entry.configure(border_color="red")
                        flag=False
                    if not gender:
                        flag=False
                    if not image_path:
                        flag=False
                    if not nationality.isalpha():
                        self.nationality_entry.configure(border_color="red")
                        flag=False
                    if not religion.isalpha():
                        self.religion_entry.configure(border_color="red")
                        flag=False
                    if not mother_tongue.isalpha():
                        self.mother_entry.configure(border_color="red")
                        flag=False

                    if flag:
                        # Assuming you have a database connection established as 'con' and cursor as 'cur'
                        insert_query = "insert into student(first_name, last_name, std_name, div_name, father_name, mother_name, gender, mobile, email, address, city, pincode, dob, nationality, religion, mother_tongue, image_path) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        insert_value = (first_name, last_name, std, div, father_name, mother_name, gender, contact, email, address, city, pincode, dob, nationality, religion, mother_tongue, image_path)
                        cur.execute(insert_query, insert_value)
                        con.commit()
                        messagebox.showinfo("Registration Successfull", "Registration submitted! You will receive an email notification once your account is activated.")
                        #return to main_window
                        return_to_main()
                    else:
                        # You might want to display a general error message here
                        messagebox.showerror("Error", "Please correct the highlighted fields.")

                except Exception as e:
                    print("Error ", e)

        def underline_to_label(event):
            self.underline_label = tk.Label(self,bg="blue")
            self.underline_label.place(x = 52, y = 180, width = 50, height=4)

        def noline_to_label(event):
            self.underline_label = tk.Label(self,bg="#E0F4FF")
            self.underline_label.place(x = 52, y = 180, width = 50, height=4)

        #======calling heading label class =======#
        self.heading_frame = HeadingFrame(self)
        self.heading_frame.place(x = 5, y = 5)

        #======back button==========#
        self.back_button = ctk.CTkButton(self, text = "< Back",width = 0, height = 0, font = ("Consolas", 18), text_color="blue", hover = "disabled", cursor = "hand2", fg_color="transparent" , command = return_to_main)
        self.back_button.place(x = 20, y = 120)
        self.back_button.bind("<Enter>", underline_to_label)
        self.back_button.bind("<Leave>", noline_to_label)

        #======Student===========#
        self.student_register_frame = ctk.CTkFrame(self, width = 800, height=700, corner_radius=0, border_width=2, border_color="black", fg_color="#36454F")

        self.personal_heading_label = ctk.CTkLabel(self.student_register_frame, text = "Student Personal Information", fg_color="#00ADB5", text_color="white", width = 800, height = 45, font=("Verdana Pro", 20))
        self.personal_heading_label.place(x = 0, y = 0)

        #=======label and entry========

        self.firstname_label = ctk.CTkLabel(self.student_register_frame, text = "First Name:", font = ("Verdana Pro", 18), text_color="white")
        self.firstname_label.place(x = 10, y = 100)

        self.firstname_entry = ctk.CTkEntry(self.student_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.firstname_entry.place(x = 180, y = 100)
        self.firstname_entry.bind("<Return>", on_return)

        self.lastname_label = ctk.CTkLabel(self.student_register_frame, text = "Last Name:", font = ("Verdana Pro", 18), text_color="white")
        self.lastname_label.place(x = 10, y = 150)

        self.lastname_entry = ctk.CTkEntry(self.student_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.lastname_entry.place(x = 180, y = 150)
        self.lastname_entry.bind("<Return>", on_return)

        self.std_label = ctk.CTkLabel(self.student_register_frame, text = "Standard:", font = ("Verdana Pro", 18), text_color="white")
        self.std_label.place(x = 10, y = 200)

        self.standard_values = []
        std_var_reg = tk.StringVar(value="")
        self.standard_option = ctk.CTkOptionMenu(self.student_register_frame, width = 200, height = 30, corner_radius=2, values=self.standard_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=std_var_reg, button_color="#00ADB5", button_hover_color="#00ADB5")
        self.standard_option.place(x = 180, y = 200)

        self.section_label = ctk.CTkLabel(self.student_register_frame, text = "Section:", font = ("Verdana Pro", 18), text_color="white")
        self.section_label.place(x = 10, y = 250)

        self.division_values = []
        div_var_reg = tk.StringVar(value="")
        self.division_option = ctk.CTkOptionMenu(self.student_register_frame, width = 200, height = 30, corner_radius=2, values=self.division_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Consolas", 18), font=("Consolas", 18),variable=div_var_reg,button_color="#00ADB5", button_hover_color="#00ADB5")
        self.division_option.place(x = 180, y = 250)

        self.father_label = ctk.CTkLabel(self.student_register_frame, text = "Father Name:", font = ("Verdana Pro", 18), text_color="white")
        self.father_label.place(x = 10, y = 300)

        self.father_entry = ctk.CTkEntry(self.student_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.father_entry.place(x = 180, y = 300)
        self.father_entry.bind("<Return>", on_return)

        self.mother_label = ctk.CTkLabel(self.student_register_frame, text = "Mother Name:", font = ("Verdana Pro", 18), text_color="white")
        self.mother_label.place(x = 10, y = 350)

        self.mother_entry = ctk.CTkEntry(self.student_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.mother_entry.place(x = 180, y = 350)
        self.mother_entry.bind("<Return>", on_return)

        self.gender_label = ctk.CTkLabel(self.student_register_frame, text = "Gender:", font = ("Verdana Pro", 18), text_color="white")
        self.gender_label.place(x = 10, y = 400)

        gender_value= ctk.StringVar(value = "other")
        self.male_radio=ctk.CTkRadioButton(self.student_register_frame,text="Male",value="Male",variable=gender_value,font=("Verdana Pro", 17), text_color="white",fg_color="white", hover_color="#00ADB5",border_color="white")
        self.male_radio.place(x=180,y=400)

        self.female_radio=ctk.CTkRadioButton(self.student_register_frame,text="Female",value="Female",variable=gender_value,font=("Verdana Pro", 17), text_color="white", fg_color="white",hover_color="#00ADB5", border_color="white")
        self.female_radio.place(x=280,y=400)

        self.phone_label = ctk.CTkLabel(self.student_register_frame, text = "Contact No:", font = ("Verdana Pro", 18), text_color="white")
        self.phone_label.place(x = 10, y = 450)

        self.phone_entry = ctk.CTkEntry(self.student_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.phone_entry.place(x = 180, y = 450)
        self.phone_entry.bind("<Return>", on_return)

        self.email_label = ctk.CTkLabel(self.student_register_frame, text = "Parent's Email:", font = ("Verdana Pro", 18), text_color="white")
        self.email_label.place(x = 10, y = 500)

        self.email_entry = ctk.CTkEntry(self.student_register_frame,width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.email_entry.place(x = 180, y = 500)
        self.email_entry.bind("<Return>", on_return)

        self.address_label = ctk.CTkLabel(self.student_register_frame, text = "Residential Address:", font = ("Verdana Pro", 18), text_color="white", wraplength=125)
        self.address_label.place(x = 10, y = 550)

        self.address_textbox = ctk.CTkTextbox(self.student_register_frame, height = 80, corner_radius=4, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2, wrap = "word")
        self.address_textbox.place(x = 180, y = 550)
        self.address_textbox.bind("<Return>", on_return)

        self.city_label = ctk.CTkLabel(self.student_register_frame, text = "City:", font = ("Verdana Pro", 18), text_color="white", wraplength=125)
        self.city_label.place(x = 10, y = 650)

        self.city_entry = ctk.CTkEntry(self.student_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.city_entry.place(x = 180, y = 650)
        self.city_entry.bind("<Return>", on_return)

        self.pincode_label = ctk.CTkLabel(self.student_register_frame, text = "Pincode:", font = ("Verdana Pro", 18), text_color="white", wraplength=125)
        self.pincode_label.place(x = 400, y = 100)

        self.pincode_var = tk.StringVar()
        self.pincode_entry = ctk.CTkEntry(self.student_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2, textvariable=self.pincode_var)
        self.pincode_entry.place(x = 580, y = 100)
        self.pincode_entry.bind("<Return>", on_return)

        self.dob_label = ctk.CTkLabel(self.student_register_frame, text = "Date of Birth:", font = ("Verdana Pro", 18), text_color="white")
        self.dob_label.place(x = 400, y = 150)

        self.dob_var = tk.StringVar()
        self.dob_entry = ctk.CTkEntry(self.student_register_frame, width = 170, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2, textvariable=self.dob_var)
        self.dob_entry.place(x = 580, y = 150)
        self.dob_entry.bind("<Return>", on_return)

        self.calendar_image = SetImage(image_path="image/calendar (1).png", width = 30, height=35)
        self.calendar_button = ctk.CTkButton(self.student_register_frame, width = 0, height = 0, fg_color="transparent", hover="disabled", bg_color="transparent", text = "", image = self.calendar_image, command=open_calendar)
        self.calendar_button.place(x = 750, y = 145)
        
        self.nationality_label = ctk.CTkLabel(self.student_register_frame, text = "Nationality:", font = ("Verdana Pro", 18), text_color="white")
        self.nationality_label.place(x = 400, y = 200)

        self.nationality_entry = ctk.CTkEntry(self.student_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.nationality_entry.place(x = 580, y = 200)
        self.nationality_entry.bind("<Return>", on_return)

        self.religion_label = ctk.CTkLabel(self.student_register_frame, text = "Religion:", font = ("Verdana Pro", 18), text_color="white")
        self.religion_label.place(x = 400, y = 250)

        self.religion_entry = ctk.CTkEntry(self.student_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.religion_entry.place(x = 580, y = 250)
        self.religion_entry.bind("<Return>", on_return)

        self.mothertongue_label = ctk.CTkLabel(self.student_register_frame, text = "Mother Tongue:", font = ("Verdana Pro", 18), text_color="white")
        self.mothertongue_label.place(x = 400, y = 300)

        self.mothertongue_entry = ctk.CTkEntry(self.student_register_frame,width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.mothertongue_entry.place(x = 580, y = 300)
        self.mothertongue_entry.bind("<Return>", on_return)

        self.upload_photo_label = ctk.CTkLabel(self.student_register_frame, text = "Upload Photo:", font = ("Verdana Pro", 18), text_color="white")
        self.upload_photo_label.place(x = 400, y = 350)

        self.upload_photo_button = ctk.CTkButton(self.student_register_frame, text = "Choose File", width = 150, height = 35, border_width=2, border_color="black", font = ("Consolas", 20), text_color="black", fg_color="#D8D9DA", corner_radius=50, hover_color="white", cursor = "hand2", command=upload_photo)
        self.upload_photo_button.place(x = 580, y = 350)

        self.file_path_label = ctk.CTkLabel(self.student_register_frame, text = "No File Choosen", font = ("Verdana Pro", 18), text_color="#00ADB5")
        self.file_path_label.place(x = 580, y = 390)

        self.register_button = ctk.CTkButton(self.student_register_frame, text = "Register", width = 150, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#272829", corner_radius=4, hover_color=None, border_width=2, border_color="white", cursor = "hand2", command=student_registration)
        self.register_button.place(x = 500, y = 450)

        #============calling the function=========#
        fetch_std_record()
        fetch_div_record()

        self.student_register_frame.place(x = 370, y = 120)

#======Teacher personal detail page=====#
class TeacherWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__(fg_color="#E0F4FF")
        self.geometry("1536x864-10-7")
        self.title("School Management System")

        self.file = ""
        def upload_photo():
            global file
            photo_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("JPG Files", ".jpg"),("PNG Files", ".png"),("All files", ".")], initialdir="C:/Users/Vikas/OneDrive/Documents", title="Open File")

            if photo_path:
                self.file = photo_path
                self.file_path_label.configure(text = f"{os.path.basename(photo_path)}", text_color = "red")
    
        def return_to_main():
            self.destroy()
            root.deiconify()

        def teacher_registration():
            global file
            first_name = self.firstname_entry.get()
            last_name = self.lastname_entry.get()
            email = self.email_entry.get()
            mobile = self.mobile_entry.get()
            qualification = self.qualification_entry.get()
            address = self.address_textbox.get("0.0", tk.END)
            city = self.city_entry.get()
            pincode = self.pincode_entry.get()
            gender = self.gender_value.get()
            path = self.file
            
            if not first_name or not last_name or not email or not mobile or not qualification or not address or not city or not pincode or not gender or not path:
                messagebox.showerror("Error", "Please fill out all required fields before submitting.")
            
            else:
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #====Condition====#
                    flag = True
                    if not first_name.isalpha():
                        self.firstname_entry.configure(border_color="red")
                        flag = False
                    if not last_name.isalpha():
                        self.lastname_entry.configure(border_color="red")
                        flag = False
                    if not re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email):
                        self.email_entry.configure(border_color="red")
                        flag = False
                    if not re.match(r"^[789]\d{9}$", mobile):
                        self.mobile_entry.configure(border_color="red")
                        flag = False
                    if not re.match(r"^[A-Za-z0-9\s]+$", qualification):
                        self.qualification_entry.configure(border_color="red")
                        flag = False
                    if not re.match(r"^[A-Za-z0-9\s\-.,]+", address):
                        self.address_textbox.configure(border_color="red")
                        flag = False
                    if not city.isalpha():
                        self.city_entry.configure(border_color="red")
                        flag = False
                    if not re.match(r"^\d{5,6}$", pincode):
                        self.pincode_entry.configure(border_color="red")
                        flag = False
                    if not gender:
                        flag = False
                    if not path:
                        flag = False

                    if flag:
                        # Assuming you have a database connection established as 'con' and cursor as 'cur'
                        insert_query = "insert into staff(first_name, last_name, email, mobile, qualification, address, city, pincode, gender, image_path) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        insert_value = (first_name, last_name, email, mobile, qualification, address, city, pincode, gender, path)
                        cur.execute(insert_query, insert_value)
                        con.commit()
                        messagebox.showinfo("Registration Successfull", "Registration submitted! You will receive an email notification once your account is activated.")
                        #return to main_window
                        return_to_main()
                    else:
                        # You might want to display a general error message here
                        messagebox.showerror("Error", "Please correct the highlighted fields.")

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

        def underline_to_label(event):
            self.underline_label = tk.Label(self,bg="blue")
            self.underline_label.place(x = 52, y = 180, width = 50, height=4)

        def noline_to_label(event):
            self.underline_label = tk.Label(self,bg="white")
            self.underline_label.place(x = 52, y = 180, width = 50, height=4)

        def on_return(event):
            event.widget.tk_focusNext().focus()
            return "break"

        #======calling heading label class =======#
        self.heading_frame = HeadingFrame(self)
        self.heading_frame.place(x = 5, y = 5)

        #======back button==========#
        self.back_button = ctk.CTkButton(self, text = "< Back",width = 0, height = 0, font = ("Consolas", 18), text_color="blue", hover = "disabled", cursor = "hand2", fg_color="transparent" , command = return_to_main)
        self.back_button.place(x = 20, y = 120)
        self.back_button.bind("<Enter>", underline_to_label)
        self.back_button.bind("<Leave>", noline_to_label)

        #=======================#
        self.teacher_register_frame = ctk.CTkFrame(self, width = 800, height=700, corner_radius=0,  border_width=2, border_color="black", fg_color="#36454F")

        self.teacher_personal_heading_label = ctk.CTkLabel(self.teacher_register_frame, text = "Teacher Personal Information", fg_color="#00ADB5", text_color="white", width = 800, height = 45, font=("Verdana Pro", 20))
        self.teacher_personal_heading_label.place(x = 0, y = 0)

        #=======label and entry========
        self.firstname_label = ctk.CTkLabel(self.teacher_register_frame, text = "First Name:", font = ("Verdana Pro", 18), text_color="white")
        self.firstname_label.place(x = 200, y = 55)

        self.firstname_entry = ctk.CTkEntry(self.teacher_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.firstname_entry.place(x = 370, y = 55)
        self.firstname_entry.bind("<Return>", on_return)
        self.firstname_entry.bind("<KeyRelease>",lambda e:self.firstname_entry.configure(border_color="white"))

        self.lastname_label = ctk.CTkLabel(self.teacher_register_frame, text = "Last Name:", font = ("Verdana Pro", 18), text_color="white")
        self.lastname_label.place(x = 200, y = 100)

        self.lastname_entry = ctk.CTkEntry(self.teacher_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.lastname_entry.place(x = 370, y = 100)
        self.lastname_entry.bind("<Return>", on_return)
        self.lastname_entry.bind("<KeyRelease>",lambda e:self.lastname_entry.configure(border_color="white"))

        self.email_label = ctk.CTkLabel(self.teacher_register_frame, text = "Email:", font = ("Verdana Pro", 18), text_color="white")
        self.email_label.place(x = 200, y = 150)

        self.email_entry = ctk.CTkEntry(self.teacher_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.email_entry.place(x = 370, y = 150)
        self.email_entry.bind("<Return>", on_return)
        self.email_entry.bind("<KeyRelease>",lambda e:self.email_entry.configure(border_color="white"))

        self.mobile_label = ctk.CTkLabel(self.teacher_register_frame, text = "Mobile no:", font = ("Verdana Pro", 18), text_color="white")
        self.mobile_label.place(x = 200, y = 200)

        self.mobile_entry = ctk.CTkEntry(self.teacher_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.mobile_entry.place(x = 370, y = 200)
        self.mobile_entry.bind("<Return>", on_return)
        self.mobile_entry.bind("<KeyRelease>",lambda e:self.mobile_entry.configure(border_color="white"))
        
        self.qualification_label = ctk.CTkLabel(self.teacher_register_frame, text = "Qualification:", font = ("Verdana Pro", 18), text_color="white")
        self.qualification_label.place(x = 200, y = 250)

        self.qualification_entry = ctk.CTkEntry(self.teacher_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.qualification_entry.place(x = 370, y = 250)
        self.qualification_entry.bind("<Return>", on_return)
        self.qualification_entry.bind("<KeyRelease>",lambda e:self.qualification_entry.configure(border_color="white"))

        self.address_label = ctk.CTkLabel(self.teacher_register_frame, text = "Residential Address:", font = ("Verdana Pro", 18), text_color="white", wraplength=125)
        self.address_label.place(x = 200, y = 300)

        self.address_textbox = ctk.CTkTextbox(self.teacher_register_frame, height = 80, corner_radius=4, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2, wrap = "word")
        self.address_textbox.place(x = 370, y = 300)
        self.address_textbox.bind("<Return>", on_return)
        self.address_textbox.bind("<KeyRelease>",lambda e:self.address_textbox.configure(border_color="white"))

        self.city_label = ctk.CTkLabel(self.teacher_register_frame, text = "City:", font = ("Verdana Pro", 18), text_color="white", wraplength=125)
        self.city_label.place(x = 200, y = 400)

        self.city_entry = ctk.CTkEntry(self.teacher_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.city_entry.place(x = 370, y = 400)
        self.city_entry.bind("<Return>", on_return)
        self.city_entry.bind("<KeyRelease>",lambda e:self.city_entry.configure(border_color="white"))

        self.pincode_label = ctk.CTkLabel(self.teacher_register_frame, text = "Pincode:", font = ("Verdana Pro", 18), text_color="white", wraplength=125)
        self.pincode_label.place(x = 200, y = 450)

        self.pincode_entry = ctk.CTkEntry(self.teacher_register_frame, width = 200, height= 35, corner_radius=1, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2)
        self.pincode_entry.place(x = 370, y = 450)
        self.pincode_entry.bind("<Return>", on_return)
        self.pincode_entry.bind("<KeyRelease>",lambda e:self.pincode_entry.configure(border_color="white"))

        self.gender_label = ctk.CTkLabel(self.teacher_register_frame, text = "Gender:", font = ("Verdana Pro", 18), text_color="white")
        self.gender_label.place(x = 200, y = 500)

        self.gender_value=ctk.StringVar(value="")
        self.male_radio=ctk.CTkRadioButton(self.teacher_register_frame,text="Male",value="Male",variable=self.gender_value,font=("Verdana Pro", 17), text_color="white",fg_color="white", hover_color="#00ADB5",border_color="white")
        self.male_radio.place(x=370,y=500)
        
        self.female_radio=ctk.CTkRadioButton(self.teacher_register_frame,text="Female",value="Female",variable=self.gender_value,font=("Verdana Pro", 17), text_color="white",fg_color="white", hover_color="#00ADB5",border_color="white")
        self.female_radio.place(x=460,y=500)

        self.upload_photo_label = ctk.CTkLabel(self.teacher_register_frame, text = "Upload Photo:", font = ("Verdana Pro", 18), text_color="white")
        self.upload_photo_label.place(x = 200, y = 550)

        self.upload_photo_button = ctk.CTkButton(self.teacher_register_frame, text = "Choose File", width = 150, height = 35, border_width=2, border_color="black", font = ("Consolas", 20), text_color="black", fg_color="#D8D9DA", corner_radius=50, hover_color="white", cursor = "hand2", command=upload_photo)
        self.upload_photo_button.place(x = 370, y = 550)
        self.upload_photo_button.bind("<Return>", on_return)

        self.file_path_label = ctk.CTkLabel(self.teacher_register_frame, text = "No File Choosen", font = ("Verdana Pro", 16), text_color="#00ADB5")
        self.file_path_label.place(x = 380, y = 590)

        self.register_button = ctk.CTkButton(self.teacher_register_frame, text = "Register", width = 150, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#272829", corner_radius=4, hover_color=None, border_width=2, border_color="white", cursor = "hand2", command=teacher_registration)
        self.register_button.place(x = 290, y = 630)

        self.teacher_register_frame.place(x = 370, y = 120)

class AdminHomeWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("1536x864-10-7")

        #======switch_frame=======#
        def switch_frame(page, indicator_button):
            for frame in self.admin_rightside_frame.winfo_children():
                frame.destroy()
                self.update()
            page()

            for child in self.admin_sidebar_frame.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    child.configure(fg_color = "#1D49CB")

            indicator_button.configure(fg_color= "#1C1678")

        def confirm_exit():
            answer = messagebox.askquestion("Confirm Exit", "Are you sure you want to exit?")
            if answer == "yes":
                self.destroy()
                AdminLoginWindow()
        
        #=====fetching the std record=====#
        def fetch_all_std_value(e):
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #execute the cursor query
                cur.execute("select std_name from standard")

                records = cur.fetchall()

                std_list = []
                for record in records:
                    std_list.append(record[0])
                
                #======configure the option menu for standard values
                self.select_standard_values = std_list
                self.select_standard_opt.configure(values = self.select_standard_values)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #======calling heading label class =======#
        self.heading_frame = HeadingFrame(self)
        self.heading_frame.place(x = 5, y = 5)

        #======student home frame=======#
        self.admin_homepage_frame = ctk.CTkFrame(self, width = 1526, height=730, corner_radius=0,  border_width=1, border_color="green", fg_color="#D8D9DA")

        self.admin_sidebar_frame = ctk.CTkFrame(self.admin_homepage_frame, width = 348, height=700, corner_radius=0, fg_color="#1D49CB")

        self.admin_sidebar_head_label = ctk.CTkLabel(self.admin_sidebar_frame, text = "Admin Menu", height = 40, width = 348, fg_color="#1C1678", font = ("Verdana Pro", 20), text_color="white")
        self.admin_sidebar_head_label.place(x = 0, y = 0)

        #=======admin dashboard========#
        self.admin_image = SetImage(image_path="image/computer.png", width = 80, height=80)
        self.admin_image_label = ctk.CTkLabel(self.admin_sidebar_frame, text = "", image = self.admin_image)
        self.admin_image_label.place(x = 40, y = 60)

        self.admin_greet_label = ctk.CTkLabel(self.admin_sidebar_frame, text = "Hello, Admin", font = ("Verdana Pro", 18), text_color="white")
        self.admin_greet_label.place(x = 140, y = 85)

        #=======sidebar menu========#
        self.dashboard_button = ctk.CTkButton(self.admin_sidebar_frame, text = "Dashboard", width = 300, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#1C1678", corner_radius=50, hover_color="#1C1678", cursor = "hand2", command=lambda : switch_frame(page=self.dashboard_frame, indicator_button=self.dashboard_button), border_width=1, border_color="white")
        self.dashboard_button.place(x = 24, y = 180)  #180

        self.add_standard_button = ctk.CTkButton(self.admin_sidebar_frame, text = "Manage Standards", width = 300, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#1D49CB", corner_radius=50, hover_color="#1C1678", cursor = "hand2", command= lambda : switch_frame(page = self.add_standard_frame, indicator_button=self.add_standard_button), border_width=1, border_color="white")
        self.add_standard_button.place(x = 24, y = 225)   #225

        self.add_division_button = ctk.CTkButton(self.admin_sidebar_frame, text = "Manage Divisions", width = 300, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#1D49CB", corner_radius=50, hover_color="#1C1678", cursor = "hand2", command= lambda : switch_frame(page = self.add_divison_frame, indicator_button=self.add_division_button), border_width=1, border_color="white")
        self.add_division_button.place(x = 24, y = 270)   #270
        self.add_division_button.bind("<Button-1>", fetch_all_std_value)

        self.add_subject_button = ctk.CTkButton(self.admin_sidebar_frame, text = "Manage Subjects", width = 300, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#1D49CB", corner_radius=50, hover_color="#1C1678", cursor = "hand2", command= lambda : switch_frame(page = self.add_subject_frame,indicator_button=self.add_subject_button), border_width=1, border_color="white")
        self.add_subject_button.place(x = 24, y = 315)     #315

        self.assign_class_all_button = ctk.CTkButton(self.admin_sidebar_frame, text = "Teacher Assignments", width = 300, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#1D49CB", corner_radius=50, hover_color="#1C1678", cursor = "hand2", command= lambda : switch_frame(page = self.assign_staff_frame,indicator_button=self.assign_class_all_button), border_width=1, border_color="white")
        self.assign_class_all_button.place(x = 24, y = 360)    #360

        self.staff_report_button = ctk.CTkButton(self.admin_sidebar_frame, text = "Teacher Reports", width = 300, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#1D49CB", corner_radius=50, hover_color="#1C1678", cursor = "hand2", command=lambda : switch_frame(page=self.staff_report_frame, indicator_button=self.staff_report_button), border_width=1, border_color="white")
        self.staff_report_button.place(x = 24, y = 405) #450

        self.student_report_button = ctk.CTkButton(self.admin_sidebar_frame, text = "Student Reports", width = 300, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#1D49CB", corner_radius=50, hover_color="#1C1678", cursor = "hand2", command= lambda : switch_frame(page = self.student_report_frame, indicator_button=self.student_report_button), border_width=1, border_color="white")
        self.student_report_button.place(x = 24, y = 450)   #495

        self.feedback_report_button = ctk.CTkButton(self.admin_sidebar_frame, text = "Feedback", width = 300, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#1D49CB", corner_radius=50, hover_color="#1C1678", cursor = "hand2", command= lambda : switch_frame(page = self.feedback_frame, indicator_button=self.feedback_report_button), border_width=1, border_color="white")
        self.feedback_report_button.place(x = 24, y = 495)    #540

        self.admin_announcemnt_button = ctk.CTkButton(self.admin_sidebar_frame, text = "Announcements", width = 300, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#1D49CB", corner_radius=50, hover_color="#1C1678", cursor = "hand2", command= lambda : switch_frame(page = self.make_announcement_frame, indicator_button=self.admin_announcemnt_button), border_width=1, border_color="white")
        self.admin_announcemnt_button.place(x = 24, y = 540)  #585

        self.logout_button = ctk.CTkButton(self.admin_sidebar_frame, text = "Logout", width = 300, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#1D49CB", corner_radius=50, hover_color="#1C1678", cursor = "hand2", command = confirm_exit, border_width=1, border_color="white")
        self.logout_button.place(x = 24, y = 585)

        self.admin_sidebar_frame.place(x = 30, y = 10)

        #=====rightside=========#
        self.admin_rightside_frame = ctk.CTkFrame(self.admin_homepage_frame, width = 1092, height=700, corner_radius=0,  border_width=None, fg_color="white")
        self.admin_rightside_frame.place(x = 400, y = 10)

        self.admin_homepage_frame.place(x = 5, y = 100)
    
    def dashboard_frame(self):
        self.dashboard_page_frame = ctk.CTkFrame(self.admin_rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="blue", fg_color="white")
        ChangeLabel(self.dashboard_page_frame, text = "Admin Dashboard", fg_color="#074173",text_color="white")

        self.graph_frame = tk.Frame(self.dashboard_page_frame, borderwidth=2, bg = "#DFF5FF")
        try:
            con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

            #create a cursor instance
            cur = con.cursor()

            cur.execute("select count(*) from student")
            student_count = cur.fetchone()

            cur.execute("select count(*) from staff")
            teacher_count = cur.fetchone()

            cur.execute("select count(*) from subject")
            subject_count = cur.fetchone()

            cur.execute("select gender, COUNT(*) FROM student GROUP BY gender")
            data = cur.fetchall()

            cur.execute("select announcement_subject, date_format(event_date, '%d %M, %Y') as date from announcement where type = 'Event'")
            notice_data = cur.fetchall()

            #close the connection
            con.close()

        except Exception as e:
            print("Error ", e)

        def create_pie_chart():
            labels = [row[0] for row in data]
            sizes = [row[1] for row in data]
            counts = [f"{label}:{count}" for label, count in data]
            colors = ['#0766AD', 'cyan']
            total_students = sum(sizes)

            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(sizes, autopct='%1.1f%%',pctdistance=0.85, startangle=90, wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, colors=colors)
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig.gca().add_artist(centre_circle)

            # Add total students to the center
            ax.text(0, 0, f"{total_students}", ha='center', va='center', fontsize=18)
            legend_handles = [patches.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor='black', linewidth=1) for color in colors]
            legend = ax.legend(legend_handles,counts, loc='lower center', ncol=2)
            legend.get_frame().set_edgecolor('none')
            for text in legend.get_texts():
                text.set_fontsize(14)

            student_label = ctk.CTkLabel(self.dashboard_page_frame, text = "Total Students by Gender", font = ("Verdana Pro", 20))
            student_label.place(x = 70, y = 195)

            # ax.set_title("Total Students by Gender", fontsize=18)
            plt.tight_layout(w_pad=2.0)   #space between pie chart and legend

            for text in ax.texts:
                text.set_fontsize(14)
            return fig
        
        def embed_chart(fig):
            canvas = FigureCanvasTkAgg(fig, master = self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.graph_frame.place(x = 10, y = 280)

        # create the pie chart
        fig = create_pie_chart()

        embed_chart(fig=fig)
        # ==================#
        self.notice_frame = ctk.CTkScrollableFrame(self.dashboard_page_frame, width = 600, height = 400, corner_radius=0, border_width=2, border_color="#DFF5FF", fg_color="#F2F6F5")

        notice_content = [row[0] for row in notice_data]
        notice_date = [row[1] for row in notice_data]

        notice_label = ctk.CTkLabel(self.dashboard_page_frame, text = "Notice Board", font = ("Verdana Pro", 20))
        notice_label.place(x = 450, y = 195)

        for i in range(len(notice_content)):
            image = SetImage(image_path="image/admin_notice.png", width = 25, height = 25)
            frame2 = ctk.CTkFrame(self.notice_frame, width = 50, height = 60,fg_color="#F2F6F5")
            image_label = ctk.CTkLabel(frame2, text = "", image = image)
            image_label.place(x = 10, y = 15)
            frame2.grid(row = i+1, column = 0, padx = 10)
        
        for i, col in enumerate(notice_content):
            frame = ctk.CTkFrame(self.notice_frame,width = 300, height = 60,fg_color="#F2F6F5")
            content_box = ctk.CTkLabel(frame, text = col, text_color="black", anchor = "w", font = ("Helvetica", 17), wraplength=280, width = 300)
            content_box.place(x = 10, y = 10)
            frame.grid(row = i+1, column = 1, padx = 10)

        for i, col in enumerate(notice_date):
            date_var = tk.StringVar(value = col)
            frame1 = ctk.CTkFrame(self.notice_frame,width = 200, height = 60,fg_color="#F2F6F5")
            date_box = ctk.CTkButton(frame1, width = 140, height = 40, corner_radius=2, fg_color="#0766AD", text_color="white", textvariable=date_var, font = ("Verdana Pro", 15), hover=tk.DISABLED)
            date_box.place(x = 10, y = 10)
            frame1.grid(row = i+1, column = 2, padx = 10)

        self.notice_frame.place(x = 450, y = 225)

        self.student_frame = ctk.CTkFrame(self.dashboard_page_frame, width = 250, height = 100, fg_color="#DFF5FF")
        imag1 =SetImage(image_path="image/admin-student.png", width = 50, height = 50)
        label1 = ctk.CTkLabel(self.student_frame, text = "", image = imag1)
        label1.place(x = 10, y = 20)
        label2 = ctk.CTkLabel(self.student_frame, text = "Total Student", font = ("Verdana Pro", 18))
        label2.place(x = 70, y = 20)
        label3 = ctk.CTkLabel(self.student_frame, text= f"{student_count[0]}", font = ("Verdana Pro", 18), text_color="#6C7A89")
        label3.place(x = 70, y = 50)
        self.student_frame.place(x = 10, y = 50)

        self.teacher_frame = ctk.CTkFrame(self.dashboard_page_frame, width = 250, height = 100, fg_color="#DFF5FF")
        imag2 =SetImage(image_path="image/teacher (2).png", width = 50, height = 50)
        label4 = ctk.CTkLabel(self.teacher_frame, text = "", image = imag2)
        label4.place(x = 10, y = 20)
        label5 = ctk.CTkLabel(self.teacher_frame, text = "Total Teacher", font = ("Verdana Pro", 18))
        label5.place(x = 70, y = 20)
        label6 = ctk.CTkLabel(self.teacher_frame, text= f"{teacher_count[0]}", font = ("Verdana Pro", 18), text_color="#6C7A89")
        label6.place(x = 70, y = 50)
        self.teacher_frame.place(x = 270, y = 50)

        self.total_subject_frame = ctk.CTkFrame(self.dashboard_page_frame, width = 250, height = 100, fg_color="#DFF5FF")
        imag3 =SetImage(image_path="image/book.png", width = 50, height = 50)
        label7 = ctk.CTkLabel(self.total_subject_frame, text = "", image = imag3)
        label7.place(x = 10, y = 20)
        label8 = ctk.CTkLabel(self.total_subject_frame, text = "Total Subjects", font = ("Verdana Pro", 18))
        label8.place(x = 70, y = 20)
        label9 = ctk.CTkLabel(self.total_subject_frame, text= f"{subject_count[0]}", font = ("Verdana Pro", 18), text_color="#6C7A89")
        label9.place(x = 70, y = 50)
        self.total_subject_frame.place(x = 530, y = 50)

        
        self.dashboard_page_frame.place(x = 0, y = 0)
        self.dashboard_page_frame.pack_propagate(False)
    
    def add_standard_frame(self):
        self.standard_page_frame = ctk.CTkFrame(self.admin_rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.standard_page_frame, text = "Manage Standards", fg_color="#074173",text_color="white")
        #=======show record========#
        def show_std_record_auto():
            global count
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                cur.execute("select std_name from standard")

                records = cur.fetchall()

                #show record in treeview
                for record in records:
                    if self.count %2 == 0:
                        self.add_standard_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], ), tags=("evenrow",))
                    else:
                        self.add_standard_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], ), tags=("oddrow",))

                    self.count += 1

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #========add record==========#
        self.count = 0
        def add_std_record():
            global count
            standard = self.standard_entry.get().lower()

            if standard == "":
                messagebox.showerror("Error", "Please enter a standard.")
            else:
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #insert data from entry box into treeview
                    if self.count % 2 == 0:
                        self.add_standard_tree.insert(parent = "", index = tk.END, iid = self.count, values=(standard, ), tags=("evenrow",))
                    else:
                        self.add_standard_tree.insert(parent = "", index = tk.END, iid = self.count, values=(standard, ), tags=("oddrow",))

                    self.count += 1

                    #insert data from entry box to database
                    insert_query = "insert into standard(std_name) values(%s)"
                    insert_value = (standard, )

                    cur.execute(insert_query, insert_value)
                    
                    self.std_msg_label.configure(text = "Standard Added Successfully", text_color = "red")

                    #commit the changes
                    con.commit()

                    #clear the entry box
                    self.standard_entry.delete(0, tk.END)

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)
        
        def clear_record():
            #=======delete selected record==========#
            data = self.add_standard_tree.selection() 

            empty_list = []
            for all in data:
                value = self.add_standard_tree.item(all, "values")
                empty_list.append(value[0])
                self.add_standard_tree.delete(all)

            for std in empty_list:
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    delete_query = "delete from standard where std_name = %s"
                    delete_value = (std,)

                    #execute the cursor
                    cur.execute(delete_query, delete_value)

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

        #======treeview setting=========#
        #add some style
        style = ttk.Style()

        #pick a theme
        style.theme_use("alt")

        #configure the tree view color
        style.configure("Treeview", 
                        background = "#D3D3D3",
                        rowheight = 25,
                        fieldbackground = "#D3D3D3", font = ("Consolas", 14))
        
        style.configure("mystyle.Treeview", font=('Consolas', 15))

        #configure the selected color
        style.configure("Treeview", background = [("selected", "#347083")])

        #increse the font size of heading
        style.configure("Treeview.Heading", font=("Consolas", 18))

        self.data_frame = tk.Frame(self.standard_page_frame, bg = "lightgrey", borderwidth=5, relief="groove")
        self.data_frame.place(x = 500, y = 320, width = 320, height = 300)

        #create a scrollbar
        y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
        x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

        y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
        x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

        #create a treeview
        self.add_standard_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
        self.add_standard_tree.pack(fill = "both", expand= True)

        #define our columns
        self.add_standard_tree["columns"] = ("Standard Name",)

        #format column
        self.add_standard_tree.column("Standard Name", anchor="center", width = 100, minwidth=100)

        #create a heading
        self.add_standard_tree.heading("Standard Name", text = "Standard Name", anchor = "center")

        #Create striped to our tages
        self.add_standard_tree.tag_configure("oddrow", background="white")
        self.add_standard_tree.tag_configure("evenrow", background="lightblue")

        #========call the function==========#
        show_std_record_auto()

        #=====creating a entry box========#
        self.standard_label = ctk.CTkLabel(self.standard_page_frame, text = "Standard Name:", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.standard_label.place(x = 245, y = 100)
        
        self.standard_entry = ctk.CTkEntry(self.standard_page_frame, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.standard_entry.place(x = 400, y = 100)
        FocusColor(entry = self.standard_entry, border_color="#1D49CB")
        self.standard_entry.bind("<KeyRelease>", lambda e : self.std_msg_label.configure(text = ""))

        self.add_button = ctk.CTkButton(self.standard_page_frame, text = "Add", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 120, height = 35, command=add_std_record)
        self.add_button.place(x = 400, y = 140)

        self.clear_button = ctk.CTkButton(self.standard_page_frame, text = "Clear", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 120, height = 35, command=clear_record)
        self.clear_button.place(x = 530, y = 140)

        self.std_msg_label = ctk.CTkLabel(self.standard_page_frame, text = "", font = ("Consolas", 20), text_color="black")
        self.std_msg_label.place(x = 365, y = 220)

        self.standard_page_frame.place(x = 0, y = 0)

    def add_divison_frame(self):
        self.divison_page_frame = ctk.CTkFrame(self.admin_rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.divison_page_frame, text = "Manage Divisions", fg_color="#074173",text_color="white")

        def on_return(event):
            event.widget.tk_focusNext().focus()
            return "break"

        #=======show record========#
        def show_div_record_auto():
            global count
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                cur.execute("select div_name, std_name, seat from division")

                records = cur.fetchall()

                #show record in treeview
                for record in records:
                    if self.count %2 == 0:
                        self.add_division_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2]), tags=("evenrow",))
                    else:
                        self.add_division_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2]), tags=("oddrow",))
                    self.count += 1

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #=====add div record======#
        self.count = 0
        def add_div_record():
            global count
            division = self.division_entry.get().upper()
            seat = self.seat_entry.get()
            standard_opt = std_var.get()

            if not division and not seat and not standard_opt:
                messagebox.showerror("Error", "Please enter a standard.")
                return
            if not division:
                messagebox.showerror("Error", "Please enter a division.")
                return
            if not seat:
                messagebox.showerror("Error", "Please enter a seat.")
                return
            if not standard_opt:
                messagebox.showerror("Error", "Please choose a standard.")
                return
            else:
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #insert data from entry box into treeview
                    if self.count % 2 == 0:
                        self.add_division_tree.insert(parent = "", index = tk.END, iid = self.count, values=(division, standard_opt, seat), tags=("evenrow",))
                    else:
                        self.add_division_tree.insert(parent = "", index = tk.END, iid = self.count, values=(division, standard_opt, seat), tags=("oddrow",))

                    self.count += 1

                    #insert data from entry box to database
                    insert_query = "insert into division(div_name, std_name, seat) values(%s, %s, %s)"
                    insert_value = (division, standard_opt, seat)

                    cur.execute(insert_query, insert_value)
                    
                    self.div_msg_label.configure(text = "Record Added Successfully", text_color = "red")

                    #commit the changes
                    con.commit()

                    #clear the entry box
                    self.division_entry.delete(0, tk.END)
                    self.seat_entry.delete(0, tk.END)
                    std_var.set("")

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)
        
        #========clear the div record from both db and treeview
        def clear_div_record():
            #=======delete selected record==========#
            data = self.add_division_tree.selection() 

            empty_div_list = []
            for all in data:
                # print(all)
                value = self.add_division_tree.item(all, "values")
                empty_div_list.append(value)
                self.add_division_tree.delete(all)

            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                delete_query = "delete from division where div_name = %s and std_name = %s and seat = %s"
                delete_value = empty_div_list

                #execute the delete query
                cur.executemany(delete_query, delete_value)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #=======treeview setting========#
        #add some style
        style = ttk.Style()

        #pick a theme
        style.theme_use("alt")

        #configure the tree view color
        style.configure("Treeview", 
                        background = "#D3D3D3",
                        rowheight = 25,
                        fieldbackground = "#D3D3D3", font = ("Consolas", 14))
        
        style.configure("mystyle.Treeview", font=('Consolas', 15))

        #configure the selected color
        style.configure("Treeview", background = [("selected", "#347083")])

        #increse the font size of heading
        style.configure("Treeview.Heading", font=("Consolas", 18))

        self.data_frame = tk.Frame(self.divison_page_frame, bg = "lightgrey", borderwidth=5, relief="groove")
        self.data_frame.place(x = 400, y = 430, height = 300)

        #create a scrollbar
        y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
        x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

        y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
        x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

        #create a treeview
        self.add_division_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
        self.add_division_tree.pack(fill = "both", expand= True)

        #define our columns
        self.add_division_tree["columns"] = ("Division Name", "Standard Name", "Seat")

        #format column
        self.add_division_tree.column("Division Name", anchor="center", width = 200, minwidth=200)
        self.add_division_tree.column("Standard Name", anchor="center", width = 200, minwidth=200)
        self.add_division_tree.column("Seat", anchor="center", width = 100, minwidth=100)

        #create a heading
        self.add_division_tree.heading("Division Name", text = "Division Name", anchor = "center")
        self.add_division_tree.heading("Standard Name", text = "Standard Name", anchor = "center")
        self.add_division_tree.heading("Seat", text = "Seat", anchor = "center")

        #Create striped to our tages
        self.add_division_tree.tag_configure("oddrow", background="white")
        self.add_division_tree.tag_configure("evenrow", background="lightblue")
        #==========================#

        #========call the function==========#
        show_div_record_auto()

        #=====creating a entry box========#
        self.division_label = ctk.CTkLabel(self.divison_page_frame, text = "Division Name:", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.division_label.place(x = 260, y =100)

        self.division_entry = ctk.CTkEntry(self.divison_page_frame, width = 200, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.division_entry.place(x = 410, y = 100)
        FocusColor(entry = self.division_entry, border_color="#1D49CB")
        self.division_entry.bind("<Return>", on_return)
        self.division_entry.bind("<KeyRelease>", lambda e : self.div_msg_label.configure(text = ""))

        self.seat_label = ctk.CTkLabel(self.divison_page_frame, text = "Seat:", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.seat_label.place(x = 345, y =150)

        self.seat_entry = ctk.CTkEntry(self.divison_page_frame, width = 200, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.seat_entry.place(x = 410, y = 150)
        FocusColor(entry = self.seat_entry, border_color="#1D49CB")
        self.seat_entry.bind("<Return>", on_return)
        self.seat_entry.bind("<KeyRelease>", lambda e : self.div_msg_label.configure(text = ""))

        self.select_standard_label = ctk.CTkLabel(self.divison_page_frame, text = "Standard:", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.select_standard_label.place(x = 305, y = 200)

        self.select_standard_values = []
        std_var = tk.StringVar()        
        self.select_standard_opt = ctk.CTkOptionMenu(self.divison_page_frame, width = 200, height = 30, corner_radius=2, values=self.select_standard_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=std_var, button_color="#1D49CB", button_hover_color="#1D49CB")
        self.select_standard_opt.place(x = 410, y = 200)

        self.add_divison_button = ctk.CTkButton(self.divison_page_frame, text = "Add", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 100, height = 35, command = add_div_record)
        self.add_divison_button.place(x = 410, y = 250)

        self.delete_divison_button = ctk.CTkButton(self.divison_page_frame, text = "Clear", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 100, height = 35, command = clear_div_record)
        self.delete_divison_button.place(x = 515, y = 250)

        self.div_msg_label = ctk.CTkLabel(self.divison_page_frame, text = "", font = ("Verdana Pro", 16), text_color="black")
        self.div_msg_label.place(x = 365, y = 310)

        self.divison_page_frame.place(x = 0, y = 0)

    def add_subject_frame(self):
        self.subject_page_frame = ctk.CTkFrame(self.admin_rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.subject_page_frame, text = "Manage Subjects", fg_color="#074173",text_color="white")

        #===========function============#
        def show_subject_record():
            global count
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                cur.execute("select subject_id, subject_name from subject")

                records = cur.fetchall()

                self.count = 0
                #show record in treeview
                for record in records:
                    if self.count %2 == 0:
                        self.add_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1]), tags=("evenrow",))
                    else:
                        self.add_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1] ), tags=("oddrow",))
                    self.count += 1

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        def add_subject_func():
            global count
            subject_name = self.add_subject_entry.get()

            if not subject_name:
                messagebox.showerror("Error", "Please enter a subject name.")
                return
            
            else:
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #fetch max of rollno from database
                    cur.execute("select max(subject_id) from subject")
                    records = cur.fetchall()

                    for id in records:
                        list1 = list(id)
                        for i in list1:
                            pass

                    #insert data from entry box into treeview
                    if self.count % 2 == 0:
                        self.add_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(i + 1, subject_name,), tags=("evenrow",))
                    else:
                        self.add_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(i + 1 , subject_name,), tags=("oddrow",))

                    self.count += 1

                    #insert data from entry box to database
                    insert_query = "insert into subject(subject_id, subject_name) values(%s, %s)"
                    insert_value = (i + 1 , subject_name )

                    cur.execute(insert_query, insert_value)
                    
                    self.sub_msg_label.configure(text = "Subject Added Successfully", text_color = "red")

                    #commit the changes
                    con.commit()

                    #clear the entry box
                    self.add_subject_entry.delete(0, tk.END)

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

        def delete_subject_func():
            #=======delete selected record==========#
            subject_data = self.add_subject_tree.selection() 

            empty_subject_list = []
            for all in subject_data:
                value = self.add_subject_tree.item(all, "values")
                empty_subject_list.append(value)
                self.add_subject_tree.delete(all)

            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                delete_query = "delete from subject where subject_id = %s and subject_name = %s"
                delete_value = empty_subject_list

                #execute the delete query
                cur.executemany(delete_query, delete_value)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        def select_record(e):
            #clear the textbox
            self.add_subject_entry.delete(0, tk.END)

            selected = self.add_subject_tree.focus()

            if selected:
                #grab record values
                values = self.add_subject_tree.item(selected, "values")

                #insert selected values
                self.add_subject_entry.insert(tk.END, values[1])

        def update_subject_func():
            #clear the treeview
            selected = self.add_subject_tree.focus()

            if selected:
                values = self.add_subject_tree.item(selected, "values")
            
            id = values[0]
    
            #Update the values
            records = self.add_subject_tree.item(selected, values = (id, self.add_subject_entry.get()))
            
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #update into database
                cur.execute("update subject set subject_name = %s where subject_id = %s", (self.add_subject_entry.get(), id))

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #======treeview setting=========#
        #add some style
        style = ttk.Style()

        #pick a theme
        style.theme_use("alt")

        #configure the tree view color
        style.configure("Treeview", 
                        background = "#D3D3D3",
                        rowheight = 25,
                        fieldbackground = "#F3FBF1", font = ("Consolas", 14))
        
        style.configure("mystyle.Treeview", font=('Consolas', 15))

        #configure the selected color
        style.configure("Treeview", background = [("selected", "#347083")])

        #increse the font size of heading
        style.configure("Treeview.Heading", font=("Consolas", 18))

        self.data_frame = tk.Frame(self.subject_page_frame, bg = "lightgrey", borderwidth=5, relief="groove")
        self.data_frame.pack_propagate(False)
        self.data_frame.place(x = 410, y = 350, width = 450, height = 400)

        #create a scrollbar
        y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
        x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

        y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
        x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

        #create a treeview
        self.add_subject_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
        self.add_subject_tree.pack(fill = "both", expand= True)
        self.add_subject_tree.bind("<<TreeviewSelect>>", select_record)

        #configure the scrollbar
        x_scroll.config(command = self.add_subject_tree.xview)
        y_scroll.config(command = self.add_subject_tree.yview)

        #define our columns
        self.add_subject_tree["columns"] = ("Subject ID", "Subject Name")

        #format column
        self.add_subject_tree.column("Subject ID", anchor="center", width = 100, minwidth=100)
        self.add_subject_tree.column("Subject Name", anchor="center", width = 300, minwidth=300)

        #create a heading
        self.add_subject_tree.heading("Subject ID", text = "Subject ID", anchor = "center")
        self.add_subject_tree.heading("Subject Name", text = "Subject Name", anchor = "center")

        #Create striped to our tages
        self.add_subject_tree.tag_configure("oddrow", background="white")
        self.add_subject_tree.tag_configure("evenrow", background="lightblue")

        #================================
        self.add_subject_label = ctk.CTkLabel(self.subject_page_frame, text = "Subject Name:", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.add_subject_label.place(x = 200, y = 130)

        self.add_subject_entry = ctk.CTkEntry(self.subject_page_frame,width = 320, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.add_subject_entry.place(x = 350, y = 130)
        FocusColor(entry = self.add_subject_entry, border_color="#1D49CB")
        self.add_subject_entry.bind("<KeyRelease>", lambda e : self.sub_msg_label.configure(text = ""))

        self.add_subject_button = ctk.CTkButton(self.subject_page_frame, text = "Add", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 100, height = 35, command=add_subject_func)
        self.add_subject_button.place(x = 350, y = 190)

        self.delete_subject_button = ctk.CTkButton(self.subject_page_frame, text = "Delete", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 100, height = 35, command = delete_subject_func)
        self.delete_subject_button.place(x = 460, y = 190)

        self.update_subject_button = ctk.CTkButton(self.subject_page_frame, text = "Update", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 100, height = 35, command = update_subject_func)
        self.update_subject_button.place(x = 570, y = 190)

        self.sub_msg_label = ctk.CTkLabel(self.subject_page_frame, text = "", font = ("Consolas", 20), text_color="green")
        self.sub_msg_label.place(x = 350, y = 250)

        #==========calling the function========#
        show_subject_record()

        self.subject_page_frame.place(x = 0, y = 0)

    def assign_staff_frame(self):
        self.staff_page_frame = ctk.CTkFrame(self.admin_rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.staff_page_frame, text = "Manage Teacher Roles", fg_color="#074173",text_color="white")

        def assign_class_teacher():
            self.assign_class_teacher_frame=ctk.CTkFrame(self.staff_page_frame, width = 1082, height=590, corner_radius=0,fg_color="white")

            #======function==============#
            #=======fetch standard record ==========#
            def fetch_std_record():
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307,database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the cursor query
                    cur.execute("select concat(std_name, ' ', div_name) as grade from division group by div_id")

                    records = cur.fetchall()

                    std_list = []
                    for record in records:
                        std_list.append(record[0])
                    
                    #======configure the option menu for standard values
                    self.select_standard_values = std_list
                    self.select_standard_opt.configure(values = self.select_standard_values)

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

            #=========fetch staff record==========#
            def fetch_staff_record():
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307,database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the cursor query
                    cur.execute("select srno from staff order by srno asc")

                    records = cur.fetchall()

                    staff_list = []
                    for record in records:
                        staff_list.append(str(record[0]))

                    #======configure the option menu for staff values
                    self.select_staff_values = staff_list
                    self.select_staff_opt.configure(values = self.select_staff_values)

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

            #======show record auto==========#
            def show_assign_record_auto():
                global count
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root",port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the cursor query
                    cur.execute("select concat(s.first_name,' ', s.last_name) as name, concat(d.std_name,' ', d.div_name) as std_div from class_teachers ct, division d, staff s where ct.srno = s.srno and d.div_id = ct.div_id")

                    records = cur.fetchall()

                    for record in records:
                        if self.count % 2 == 0:
                            self.assign_teacher_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record), tags=("evenrow",))
                        else:
                            self.assign_teacher_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record), tags=("oddrow",))

                        self.count += 1

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

            #=========assiging teacher , class and div=====#
            self.count = 0
            def assign_classteacher():
                global count
                staff_no = staff_var.get()
                std_name = std_var.get()

                if not staff_no or not std_name:
                    messagebox.showerror("Error", "Please select above details.")
                    return
                
                else:
                    try:
                        con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307,database = "software")

                        #create a cursor instance
                        cur = con.cursor()

                        #fetch the name of staff
                        cur.execute("select concat(first_name, ' ', last_name) as staff_name from staff where srno = %s", (staff_no,))
                        staff_record = cur.fetchall()
                        
                        for staff_name in staff_record:
                            for staff in staff_name:
                                continue
                        
                        #spliting the record of std div
                        result = std_name.split(" ")
                        std = " ".join([result[0], result[1]])
                        div = result[2]

                        #fetching the div id from division
                        cur.execute("select div_id from division where std_name = %s and div_name = %s", (std, div))
                        div_record = cur.fetchall()
                        for div_no in div_record:
                            continue

                        #fetch record in database#
                        select_query=f"select srno,div_id from class_teachers where srno={staff_no} and div_id={div_no[0]}"
                        cur.execute(select_query)
                        result=cur.fetchall()

                        if result:
                            messagebox.showinfo("Error","Class already assign")
                            return
                        else:
                            # self.count = 0
                            #insert data from option menu into treeview
                            if self.count % 2 == 0:
                                self.assign_teacher_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(staff, std_name), tags=("evenrow",))
                            else:
                                self.assign_teacher_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(staff, std_name), tags=("oddrow",))

                            self.count += 1

                            #add record in database
                            insert_query = "insert into class_teachers(srno, div_id) values(%s, %s)"
                            insert_values = (staff_no, div_no[0])

                            cur.execute(insert_query, insert_values)

                            #commit the changes
                            con.commit()

                            #close the connection
                            con.close()

                    except Exception as e:
                        print("Error ", e)
            
            #=================================#
            #====for assigning class and all to teacher==========#
            self.search_staff_label = ctk.CTkLabel(self.assign_class_teacher_frame, text = "Select Staff", font = ("Verdana Pro", 18), text_color="#1D49CB")
            self.search_staff_label.place(x = 20, y = 50)

            self.select_staff_values = []
            staff_var = tk.StringVar()        
            self.select_staff_opt = ctk.CTkOptionMenu(self.assign_class_teacher_frame, width = 200, height = 30, corner_radius=2, values=self.select_staff_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=staff_var)
            self.select_staff_opt.place(x = 20, y = 90)

            self.search_std_label = ctk.CTkLabel(self.assign_class_teacher_frame, text = "Select Std & Div", font = ("Verdana Pro", 18), text_color="#1D49CB")
            self.search_std_label.place(x = 250, y = 50)

            self.select_standard_values = []
            std_var = tk.StringVar()        
            self.select_standard_opt = ctk.CTkOptionMenu(self.assign_class_teacher_frame, width = 200, height = 30, corner_radius=2, values=self.select_standard_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=std_var)
            self.select_standard_opt.place(x = 250, y = 90)

            self.assign_button = ctk.CTkButton(self.assign_class_teacher_frame, text = "Assign", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 120, height = 35,command=assign_classteacher)
            self.assign_button.place(x = 470, y = 87)

            #=======treeview setting========#
            #add some style
            style = ttk.Style()

            #pick a theme
            style.theme_use("alt")

            #configure the tree view color
            style.configure("Treeview", 
                            background = "#EEF0E5",
                            rowheight = 25,
                            fieldbackground = "#F3FBF1", font = ("Consolas", 14))
            
            style.configure("mystyle.Treeview", font=('Consolas', 15))

            #configure the selected color
            style.configure("Treeview", background = [("selected", "#347083")])

            #increse the font size of heading
            style.configure("Treeview.Heading", font=("Consolas", 18))

            self.data_frame = tk.Frame(self.assign_class_teacher_frame, bg = "lightgrey", borderwidth=0, relief="solid")
            self.data_frame.pack_propagate(False)
            self.data_frame.place(x = 20, y = 200, height = 500, width = 1000)

            #create a scrollbar
            y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
            x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

            y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
            x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

            #create a treeview
            self.assign_teacher_subject_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
            self.assign_teacher_subject_tree.pack(fill = "both", expand= True)

            #configure the scrollbar
            x_scroll.config(command = self.assign_teacher_subject_tree.xview)
            y_scroll.config(command = self.assign_teacher_subject_tree.yview)

            #define our columns
            self.assign_teacher_subject_tree["columns"] = ("Staff Name", "Standard & Division Name")

            #format column
            self.assign_teacher_subject_tree.column("Staff Name", anchor="center", width = 250, minwidth=250)
            self.assign_teacher_subject_tree.column("Standard & Division Name", anchor="center", width = 250, minwidth=250)
            
            #create a heading
            self.assign_teacher_subject_tree.heading("Staff Name", text = "Staff Name", anchor = "center")
            self.assign_teacher_subject_tree.heading("Standard & Division Name", text = "Standard & Division Name", anchor = "center")
        
            #Create striped to our tages
            self.assign_teacher_subject_tree.tag_configure("oddrow", background="white")
            self.assign_teacher_subject_tree.tag_configure("evenrow", background="lightblue")
            #==========================#

            #=========calling the function==========#
            fetch_staff_record()
            fetch_std_record()
            show_assign_record_auto()

            self.assign_class_teacher_frame.place(x = 5, y = 105)

        def assign_subject():
            self.assign_subject_frame=ctk.CTkFrame(self.staff_page_frame, width = 1082, height=590, corner_radius=0,fg_color="white")

            #======function==============#
            #=======fetch standard record ==========#
            def fetch_std_record():
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307,database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the cursor query
                    cur.execute("select concat(std_name, ' ', div_name) as grade from division group by div_id")

                    records = cur.fetchall()

                    std_list = []
                    for record in records:
                        std_list.append(record[0])
                    
                    #======configure the option menu for standard values
                    self.select_standard_values = std_list
                    self.select_standard_opt.configure(values = self.select_standard_values)

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)
        
            #=======fetch subject record ==========#
            def fetch_subject_record():
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the cursor query
                    cur.execute("select subject_name from subject")

                    records = cur.fetchall()

                    subject_list = []
                    for record in records:
                        subject_list.append(record[0])
                    
                    #======configure the option menu for standard values
                    self.select_subject_values = subject_list
                    self.select_subject_opt.configure(values = self.select_subject_values)

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

            #=========fetch staff record==========#
            def fetch_staff_record():
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307,database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the cursor query
                    cur.execute("select srno from staff order by srno asc")

                    records = cur.fetchall()

                    staff_list = []
                    for record in records:
                        staff_list.append(str(record[0]))

                    #======configure the option menu for staff values
                    self.select_staff_values = staff_list
                    self.select_staff_opt.configure(values = self.select_staff_values)

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

            #======show record auto==========#
            def show_assign_record_auto():
                global count
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307,database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the cursor query
                    cur.execute("select concat(staff.first_name,' ', staff.last_name) as name, concat(d.std_name,' ', d.div_name) as std_div, s.subject_name from teacher_assignments ta, division d, subject s , staff where ta.srno = staff.srno and d.div_id = ta.std_div_id and s.subject_id = ta.subject_id")

                    records = cur.fetchall()

                    for record in records:
                        if self.count % 2 == 0:
                            self.assign_teacher_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record), tags=("evenrow",))
                        else:
                            self.assign_teacher_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record), tags=("oddrow",))

                        self.count += 1

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

            #=========assiging teacher , class and div=====#
            self.count = 0
            def assign_teacher_subject():
                global count
                staff_no = staff_var.get()
                std_name = std_var.get()
                subject_name= subject_var.get()

                if not staff_no or not std_name or not subject_name:
                    messagebox.showerror("Error", "Please select above details.")
                    return
                
                else:
                    try:
                        con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                        #create a cursor instance
                        cur = con.cursor()

                        #fetch the name of staff
                        cur.execute("select concat(first_name, ' ', last_name) as staff_name from staff where srno = %s", (staff_no,))
                        staff_record = cur.fetchall()
                        
                        for staff_name in staff_record:
                            for staff in staff_name:
                                continue
                        
                        #spliting the record of std div
                        result = std_name.split(" ")
                        std = " ".join([result[0], result[1]])
                        div = result[2]

                        #fetching the div id from division
                        cur.execute("select div_id from division where std_name = %s and div_name = %s", (std, div))
                        div_record = cur.fetchall()
                        for div_no in div_record:
                            continue

                        #fetching the subject_id from division
                        cur.execute("select subject_id from subject where subject_name = %s", (subject_name,))
                        subject_record = cur.fetchall()
                        for sub in subject_record:
                            continue

                        #fetch record in database#
                        select_query=f"select srno,std_div_id,subject_id from teacher_assignments where srno={staff_no} and std_div_id={div_no[0]} and subject_id={sub[0]}"
                        cur.execute(select_query)
                        result=cur.fetchall()
                        if result:
                            messagebox.showinfo("Error","Subject already assign")
                            return
                        #fetch record in database#
                        select_query=f"select std_div_id,subject_id from teacher_assignments where std_div_id={div_no[0]} and subject_id={sub[0]}"
                        cur.execute(select_query)
                        result=cur.fetchall()
                        if result:
                            messagebox.showinfo("Error","Subject already assign")
                            return
                        else:
                            # self.count = 0
                            #insert data from option menu into treeview
                            if self.count % 2 == 0:
                                self.assign_teacher_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(staff, std_name, subject_name), tags=("evenrow",))
                            else:
                                self.assign_teacher_subject_tree.insert(parent = "", index = tk.END, iid = self.count, values=(staff, std_name, subject_name), tags=("oddrow",))

                            self.count += 1
                            #add record in database
                            insert_query = "insert into teacher_assignments(srno, std_div_id, subject_id) values(%s, %s, %s)"
                            insert_values = (staff_no, div_no[0], sub[0])

                            cur.execute(insert_query, insert_values)

                            #commit the changes
                            con.commit()

                            #close the connection
                            con.close()

                    except Exception as e:
                        print("Error ", e)
            
            #=================================#

            #====for assigning class and all to teacher==========#
            self.search_staff_label = ctk.CTkLabel(self.assign_subject_frame, text = "Select Staff", font = ("Verdana Pro", 18), text_color="#1D49CB")
            self.search_staff_label.place(x = 20, y = 50)

            self.select_staff_values = []
            staff_var = tk.StringVar()        
            self.select_staff_opt = ctk.CTkOptionMenu(self.assign_subject_frame, width = 200, height = 30, corner_radius=2, values=self.select_staff_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=staff_var)
            self.select_staff_opt.place(x = 20, y = 90)

            self.search_std_label = ctk.CTkLabel(self.assign_subject_frame, text = "Select Std & Div", font = ("Verdana Pro", 18), text_color="#1D49CB")
            self.search_std_label.place(x = 250, y = 50)

            self.select_standard_values = []
            std_var = tk.StringVar()        
            self.select_standard_opt = ctk.CTkOptionMenu(self.assign_subject_frame, width = 200, height = 30, corner_radius=2, values=self.select_standard_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=std_var)
            self.select_standard_opt.place(x = 250, y = 90)

            self.select_subject_label = ctk.CTkLabel(self.assign_subject_frame, text = "Select Subject", font = ("Verdana Pro", 18), text_color="#1D49CB")
            self.select_subject_label.place(x = 480, y = 50)
            self.select_subject_values = []
            subject_var = tk.StringVar()        
            self.select_subject_opt = ctk.CTkOptionMenu(self.assign_subject_frame, width = 200, height = 30, corner_radius=2, values=self.select_subject_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=subject_var)
            self.select_subject_opt.place(x = 480, y = 90)

            self.assign_button = ctk.CTkButton(self.assign_subject_frame, text = "Assign", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 120, height = 35,command=assign_teacher_subject)

            self.assign_button.place(x = 700, y = 86)
    
            #=======treeview setting========#
            #add some style
            style = ttk.Style()

            #pick a theme
            style.theme_use("alt")

            #configure the tree view color
            style.configure("Treeview", 
                            background = "#EEF0E5",
                            rowheight = 25,
                            fieldbackground = "#F3FBF1", font = ("Consolas", 14))
            
            style.configure("mystyle.Treeview", font=('Consolas', 15))

            #configure the selected color
            style.configure("Treeview", background = [("selected", "#347083")])

            #increse the font size of heading
            style.configure("Treeview.Heading", font=("Consolas", 18))

            self.data_frame = tk.Frame(self.assign_subject_frame, bg = "lightgrey", borderwidth=0, relief="solid")
            self.data_frame.pack_propagate(False)
            self.data_frame.place(x = 20, y = 200, height = 500, width = 1000)

            #create a scrollbar
            y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
            x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

            y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
            x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

            #create a treeview
            self.assign_teacher_subject_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
            self.assign_teacher_subject_tree.pack(fill = "both", expand= True)

            #configure the scrollbar
            x_scroll.config(command = self.assign_teacher_subject_tree.xview)
            y_scroll.config(command = self.assign_teacher_subject_tree.yview)

            #define our columns
            self.assign_teacher_subject_tree["columns"] = ("Staff Name", "Standard & Division Name","Subject Name")

            #format column
            self.assign_teacher_subject_tree.column("Staff Name", anchor="center", width = 250, minwidth=250)
            self.assign_teacher_subject_tree.column("Standard & Division Name", anchor="center", width = 250, minwidth=250)
            self.assign_teacher_subject_tree.column("Subject Name", anchor="center", width = 250, minwidth = 250)
            
            #create a heading
            self.assign_teacher_subject_tree.heading("Staff Name", text = "Staff Name", anchor = "center")
            self.assign_teacher_subject_tree.heading("Standard & Division Name", text = "Standard & Division Name", anchor = "center")
            self.assign_teacher_subject_tree.heading("Subject Name", text = "Subject Name", anchor = "center")
        
            #Create striped to our tages
            self.assign_teacher_subject_tree.tag_configure("oddrow", background="white")
            self.assign_teacher_subject_tree.tag_configure("evenrow", background="lightblue")
            #==========================#

            #=========calling the function==========#
            fetch_staff_record()
            fetch_std_record()
            fetch_subject_record()
            show_assign_record_auto()

            self.assign_subject_frame.place(x = 5, y = 105)

        self.assign_class_teacher_button = ctk.CTkButton(self.staff_page_frame, text = "Assign Class Teachers", width = 300, height = 45,font = ("Verdana Pro", 17), cursor = "hand2", fg_color="#1D49CB", text_color="white", hover_color="#1C1678", corner_radius=2,command=assign_class_teacher)
        self.assign_class_teacher_button.place(x = 20, y = 60)

        self.assign_subject_button = ctk.CTkButton(self.staff_page_frame, text = "Subject & Class Assignments", width = 300, height = 45,font = ("Verdana Pro", 17), cursor = "hand2", fg_color="#1D49CB", text_color="white", hover_color="#1C1678", corner_radius=2,command=assign_subject)
        self.assign_subject_button.place(x = 340, y = 60)
        
        self.staff_page_frame.place(x = 0, y = 0)

    def staff_report_frame(self):
        self.staff_report_page_frame = ctk.CTkFrame(self.admin_rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.staff_report_page_frame, text = "Manage Staff Reports", fg_color="#074173",text_color="white")

        def show_staff_record_auto():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                select_query = "select srno, staff_id, concat(first_name, ' ', last_name) as name, email, mobile, gender, qualification, city, pincode, selection_status from staff"

                #execute the select query
                cur.execute(select_query)

                records = cur.fetchall()

                self.count = 0
                #show record in treeview
                for record in records:
                    if self.count %2 == 0:
                        self.add_staff_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("evenrow",))
                    else:
                        self.add_staff_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("oddrow",))
                    self.count += 1

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #=====search staff record========#
        def search_staff_record():
            search_type = self.search_var.get()
            search_paramter = self.search_entry.get()

            # #clear the treeview
            for record in self.add_staff_tree.get_children():
                self.add_staff_tree.delete(record)

            #connection with database to pull out search records
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                if search_type == "Name":
                    cur.execute("select srno,staff_id, concat(first_name, ' ', last_name) as name, email, mobile, gender, qualification, city, pincode, selection_status from staff where concat(first_name, ' ', last_name) = %s", (search_paramter,))

                elif search_type == "Contact":
                    cur.execute("select srno,staff_id, concat(first_name, ' ', last_name) as name, email, mobile, gender, qualification, city, pincode, selection_status from staff where mobile = %s", (search_paramter,))
                
                records = cur.fetchall()

                self.count = 0
                #show search record in treeview
                for record in records:
                    if self.count %2 == 0:
                        self.add_staff_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8],  record[9]), tags=("evenrow",))
                    else:
                        self.add_staff_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("oddrow",))
                    self.count += 1

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)
        
        def reset_std_record():
            #clear the treeview
            for record in self.add_staff_tree.get_children():
                self.add_staff_tree.delete(record)

            #show all record of staff
            show_staff_record_auto()

        def approve_staff_func():
            #grab a record number
            selected_approve_data = self.add_staff_tree.selection() 

            approve_list = []
            for all in selected_approve_data:
                value = self.add_staff_tree.item(all, "values")
                approve_list.append(value)

            for staff in approve_list:
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the update query
                    update_query = "update staff set selection_status = %s where srno = %s"
                    update_value = (self.approve_button.cget("text"), staff[0])

                    cur.execute(update_query, update_value)

                    #clear the treeview
                    for record in self.add_staff_tree.get_children():
                        self.add_staff_tree.delete(record)

                    #executing select query 
                    select_query = "select srno, staff_id, concat(first_name, ' ', last_name) as name, email, mobile, gender, qualification, city, pincode, selection_status from staff"

                    cur.execute(select_query)

                    records = cur.fetchall()

                    #show record in treeview
                    for record in records:
                        if self.count %2 == 0:
                            self.add_staff_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("evenrow",))
                        else:
                            self.add_staff_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8],  record[9]), tags=("oddrow",))
                        self.count += 1

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

        def reject_staff_func():
            #grab a record number
            selected_reject_data = self.add_staff_tree.selection() 

            reject_list = []
            for all in selected_reject_data:
                value = self.add_staff_tree.item(all, "values")
                reject_list.append(value)

            for staff in reject_list:
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the update query
                    update_query = "update staff set selection_status = %s where srno = %s"
                    update_value = (self.reject_button.cget("text"), staff[0])

                    cur.execute(update_query, update_value)

                    #==========================
                    #clear the treeview
                    for record in self.add_staff_tree.get_children():
                        self.add_staff_tree.delete(record)

                    #executing select query 
                    select_query = "select srno, staff_id, concat(first_name, ' ', last_name) as name, email, mobile, gender, qualification, city, pincode, selection_status from staff"
                    
                    cur.execute(select_query)

                    records = cur.fetchall()

                    #show record in treeview
                    for record in records:
                        if self.count %2 == 0:
                            self.add_staff_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("evenrow",))
                        else:
                            self.add_staff_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("oddrow",))
                        self.count += 1

                    #commit the changes
                    con.commit()

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

        def update_staff_tree():
            #clear the treeview
            for record in self.add_staff_tree.get_children():
                self.add_staff_tree.delete(record)
            
            print(record)

            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #execute the delete query
                cur.execute("delete from staff where selection_status = 'Reject'")

                #commit the changes
                con.commit()

                #calling the show_staff_record_auto func
                show_staff_record_auto()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #=====generate id=============#
        def generate_id():
            for record in self.add_staff_tree.get_children():
                self.add_staff_tree.delete(record)

            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                srno_list=[]
                #execute the delete query
                cur.execute("select srno from staff order by srno asc")
                records=cur.fetchall()
                for record in records:
                    for staff_no in record:
                        # print(staff_no)
                        srno_list.append(staff_no)
                       
                id=1001
                for i in range(len(srno_list)):
                    # print(srno_list[i])
                    cur.execute(f"update staff set staff_id={id} where srno={srno_list[i]}")
                    id=id+1

                #commit the changes
                con.commit()

                #calling the show_staff_record_auto func
                show_staff_record_auto()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #=======generate teacher id card==========#
        def generate_teacher_card(teacher_data):
            global records
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root",port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #fetch student_data
                cur.execute("select srno, mobile, address, image_path, concat(first_name,' ', last_name) as name, first_name from staff where srno = %s", (teacher_data[0],))

                records = cur.fetchone()

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)
            
            teacher_id = records[0]
            contact = records[1]
            address = records[2]
            image_path = records[3]
            full_name = records[4]
            first_name = records[5].lower()
        
            wrapped_address = textwrap.fill(text=address, width=25)

            #==================================#
            teacher_frame_image = Image.open("image/teacher_id.png")
            teacher_image_pic = Image.open(f"{image_path}").resize((94, 98))

            #creating an object for using student_frame_image
            draw = ImageDraw.Draw(teacher_frame_image)
            text_font = ImageFont.truetype("VerdanaPro-CondRegular.ttf", 13)
            text2_font = ImageFont.truetype("VerdanaPro-CondRegular.ttf", 16)

            #showing student photo on id frame
            teacher_frame_image.paste(teacher_image_pic, (98,127)) 

            draw.text(xy = (98, 230), text = f"{full_name}", fill = (255, 0, 0), font = ImageFont.truetype("tahomabd.ttf", 15))
            draw.text(xy = (110, 277), text = f"{teacher_id}", fill = (0, 0, 0), font = text_font)
            # draw.text(xy = (97, 297), text = f"{dob}", fill = (0, 0, 0), font = text_font)
            draw.text(xy = (110, 302), text = f"{contact}", fill = (0, 0, 0), font = text_font)
            draw.text(xy = (110, 325), text = f"{wrapped_address}", fill = (0, 0, 0), font = text_font)
            draw.text(xy = (110, 350), text = "Lecturer", fill = (255, 0, 0), font = text2_font)

            teacher_id_window = ctk.CTkToplevel(fg_color="white")
            teacher_id_window.geometry("600x500+800+250")
            teacher_id_window.title("School Management System")
            teacher_id_window.lift()
            teacher_id_window.grab_set()

            #======card frame===========#
            self.teacher_card_page_frame = ctk.CTkFrame(teacher_id_window, border_width=2,border_color="#074173", fg_color="white", width = 580, height = 480, corner_radius=2)

            #======card label===========#
            self.head_label = ctk.CTkLabel(self.teacher_card_page_frame, text = "Identity Card",width = 580, height = 40, fg_color="#074173", text_color="white", font = ("Verdana Pro", 18))
            self.head_label.place(x = 0, y = 0)

            #====ignore warnings===========#
            warnings.filterwarnings("ignore", category=UserWarning)

            #=====iid card image label==========#
            id_card_image = ImageTk.PhotoImage(teacher_frame_image)
            self.teacher_card_label = ctk.CTkLabel(self.teacher_card_page_frame, text = "", image = id_card_image)
            self.teacher_card_label.place(x = 170, y = 50)

            # #===========save button=============#
            def save_teacher_card():
                file_name = "C:/Users/vikas/OneDrive/Documents/software project/teacher_id"

                if os.path.exists(f"{file_name}/{teacher_id}_{first_name} id_card.png"):
                    error_message = f"The file '{file_name}' already exists."
                    messagebox.showinfo("File Exists", message=error_message)
                else:
                    #convert photo_image into PIL image
                    image_to_save = ImageTk.getimage(id_card_image) 
                    image_to_save.save(f"{file_name}/{teacher_id}_{first_name} id_card.png")
                    success_message = f"The Teacher ID card for {full_name} has been saved successfully!"
                    messagebox.showinfo("Success", message=success_message)

            # #============print button===========#
            def print_teacher_card():
                path = filedialog.askdirectory()

                if path:
                    image_to_save = ImageTk.getimage(id_card_image) 
                    image_to_save.save(f"{path}/{teacher_id}_{first_name} id_card_print.png")
                    win32api.ShellExecute(0,"print", f"{path}/{teacher_id}_{first_name} id_card_print.png",None, ".", 0)

            self.save_image = SetImage(image_path="image/download.png", width = 20, height=20)
            self.save_button = ctk.CTkButton(self.teacher_card_page_frame, text = "Save", width = 120, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", fg_color="#074173", text_color="white", image = self.save_image,command=save_teacher_card)
            self.save_button.place(x = 160, y = 400)

            self.print_image = SetImage(image_path="image/printer.png", width = 20, height=20)
            self.print_button = ctk.CTkButton(self.teacher_card_page_frame, text = "Print", width = 120, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", fg_color="#074173", text_color="white", command=print_teacher_card, image = self.print_image)
            self.print_button.place(x = 300, y = 400)

            self.teacher_card_page_frame.place(x = 10, y = 10)

        def on_tree_view_selection():
            selected = self.add_staff_tree.selection()[0]
            teacher_data = self.add_staff_tree.item(selected, "values")
            generate_teacher_card(teacher_data = teacher_data)

        #=========Send Email======#
        def send_email():
            try:
                start_time=time.time()
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307,database = "software")

                #create a cursor instance
                cur = con.cursor()

                email_list=[]
                #fetch email query
                cur.execute("select email from staff where selection_status = 'Approve' and staff_id is null order by srno asc")
                records=cur.fetchall()
                for record in records:
                    for staff_email in record:
                        email_list.append(staff_email)
                print(email_list)

                #fetch name query
                name_list=[]
                cur.execute("select first_name from staff where selection_status = 'Approve' and staff_id is null order by srno asc")
                records=cur.fetchall()
                for record in records:
                    for student_name in record:
                        name_list.append(student_name)
                print(name_list)

                #fetch password
                password_list=[]
                cur.execute("select concat(first_name,'@',staff_id) as password from staff where selection_status = 'Approve' and staff_id is null order by srno asc")
                records=cur.fetchall()
                for record in records:
                    for teacher_password in record:
                        password_list.append(teacher_password)
                print(password_list)

                for i in range(len(email_list)):
                    def send_email(subject, message, recipient_email, sender_email, sender_password):
                        try:
                            yag = yagmail.SMTP(sender_email, sender_password)
                            yag.send(to=recipient_email, subject=subject, contents=message)
                            print("Email sent successfully!")
                        except Exception as e:
                            print("Email failed to send. Error:", str(e))

                    subjects="Welcome to School Management System - Your Login Credentials"
                    body=f"Dear {name_list[i]},\n\nWe are pleased to inform you that your account for the Vivekandand Vidya Bhavan Management System has been successfully created.\n\nPlease find your login credentials below:\n\nUsername: {email_list[i]}\nPassword: {password_list[i]}\n\nIf you experience any issues or have any questions, please contact support at vvb.admin@gmail.com or +91 9619148774.\n\nThis message is generated automatically. Please do not reply to this email.\n\nThank you,\n\nVivekandand Vidya Bhavan Management System"

                    # Usage example:
                    send_email(subject=subjects, message=body,recipient_email=email_list[i], sender_email="vikas.kahar.4471804@ves.ac.in", sender_password="VIKAS@4471804")

                #commit the changes
                con.commit()
                end_time=time.time()
                total_time=end_time-start_time
                print(total_time)
                messagebox.showinfo("Login","Email Sent Successful")

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)
            
        #==============================#
        #=======treeview setting========#
        #add some style
        style = ttk.Style()

        #pick a theme
        style.theme_use("alt")

        #configure the tree view color
        style.configure("Treeview", 
                        background = "#EEF0E5",
                        rowheight = 25,
                        fieldbackground = "#F3FBF1", font = ("Consolas", 14))
        
        style.configure("mystyle.Treeview", font=('Consolas', 15))

        #configure the selected color
        style.configure("Treeview", background = [("selected", "#347083")])

        #increse the font size of heading
        style.configure("Treeview.Heading", font=("Consolas", 18))

        self.data_frame = tk.Frame(self.staff_report_page_frame, bg = "lightgrey", borderwidth=0, relief="solid")
        self.data_frame.pack_propagate(False)
        self.data_frame.place(x = 20, y = 200, height = 550, width = 1320)

        #create a scrollbar
        y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
        x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

        y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
        x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

        #create a treeview
        self.add_staff_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
        self.add_staff_tree.pack(fill = "both", expand= True)

        #configure the scrollbar
        x_scroll.config(command = self.add_staff_tree.xview)
        y_scroll.config(command = self.add_staff_tree.yview)

        #define our columns
        self.add_staff_tree["columns"] = ("Sr No","Teacher ID","Name", "Email", "Mobile", "Gender", "Qualification", "City", "Pincode", "Selection Status")

        #format column
        self.add_staff_tree.column("Sr No", anchor="center", width = 100, minwidth=100)
        self.add_staff_tree.column("Teacher ID", anchor="center", width = 200, minwidth=200)
        self.add_staff_tree.column("Name", anchor="center", width = 300, minwidth=300)
        self.add_staff_tree.column("Email", anchor="center", width = 300, minwidth = 300)
        self.add_staff_tree.column("Mobile", anchor="center", width = 300, minwidth = 300)
        self.add_staff_tree.column("Gender", anchor="center", width = 300, minwidth = 300)
        self.add_staff_tree.column("Qualification", anchor="center", width = 300, minwidth = 300)
        self.add_staff_tree.column("City", anchor="center", width = 300, minwidth = 300)
        self.add_staff_tree.column("Pincode", anchor="center", width = 300, minwidth = 300)
        self.add_staff_tree.column("Selection Status", anchor="center", width = 300, minwidth = 300)
        
        #create a heading
        self.add_staff_tree.heading("Sr No", text = "Sr No", anchor = "center")
        self.add_staff_tree.heading("Teacher ID", text = "Teacher ID", anchor = "center")
        self.add_staff_tree.heading("Name", text = "Name", anchor = "center")
        self.add_staff_tree.heading("Email", text = "Email", anchor = "center")
        self.add_staff_tree.heading("Mobile", text = "Mobile", anchor = "center")
        self.add_staff_tree.heading("Gender", text = "Gender", anchor = "center")
        self.add_staff_tree.heading("Qualification", text = "Qualification", anchor = "center")
        self.add_staff_tree.heading("City", text = "City", anchor = "center")
        self.add_staff_tree.heading("Pincode", text = "Pincode", anchor = "center")
        self.add_staff_tree.heading("Selection Status", text = "Selection Status", anchor = "center")

        #Create striped to our tages
        self.add_staff_tree.tag_configure("oddrow", background="white")
        self.add_staff_tree.tag_configure("evenrow", background="lightblue")
        #==========================#
        
        #=====calling the show record function====#
        show_staff_record_auto()

        #======searching options=========#
        self.search_staff_label = ctk.CTkLabel(self.staff_report_page_frame, text = "Search By", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.search_staff_label.place(x = 15, y = 80)

        self.search_staff_by=["Name", "Contact"]
        self.search_var = tk.StringVar(value = "")
        self.search_staff_option=ctk.CTkOptionMenu(self.staff_report_page_frame,width=200,height=30,corner_radius=2,values=self.search_staff_by,fg_color="#D8D9DA",text_color="black",dropdown_font=("Verdana Pro", 15),font=("Verdana Pro", 18), variable=self.search_var)
        self.search_staff_option.place(x=140,y=80)

        self.search_entry = ctk.CTkEntry(self.staff_report_page_frame, width = 200, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.search_entry.place(x = 360, y = 78)
        FocusColor(entry=self.search_entry, border_color="#1D49CB")

        self.search_button = ctk.CTkButton(self.staff_report_page_frame, text = "Search", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 120, height = 35,command=search_staff_record)
        self.search_button.place(x = 580, y = 78)

        self.showall_button = ctk.CTkButton(self.staff_report_page_frame, text = "Show All", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 120, height = 35, command = reset_std_record)
        self.showall_button.place(x = 720, y = 78)

        #===button======#
        self.approve_image = SetImage(image_path="image/checked.png", width = 25, height=25)
        self.approve_button = ctk.CTkButton(self.staff_report_page_frame, text = "Approve", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=approve_staff_func, fg_color="#074173", text_color="white", image = self.approve_image)
        self.approve_button.place(x = 20, y = 630)

        self.reject_image =SetImage(image_path="image/crossed.png", width = 25, height=25)
        self.reject_button = ctk.CTkButton(self.staff_report_page_frame,  text = "Reject", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command= reject_staff_func, fg_color="#074173", text_color="white", image = self.reject_image)
        self.reject_button.place(x = 200, y = 630)

        self.update_image = SetImage(image_path="image/updated.png", width = 25, height=25)
        self.update_button = ctk.CTkButton(self.staff_report_page_frame, text = "Update", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=update_staff_tree, fg_color="#074173", text_color="white", image = self.update_image)
        self.update_button.place(x = 380, y = 630)

        self.generated_id_image = SetImage(image_path="image/list.png", width = 25, height=25)
        self.generate_id_button = ctk.CTkButton(self.staff_report_page_frame, text = "Teacher ID", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=generate_id, fg_color="#074173", text_color="white", image = self.generated_id_image)
        self.generate_id_button.place(x = 560, y = 630)

        self.generate_id_card_image = SetImage(image_path="image/id-card.png", width = 25, height=25)
        self.generate_teacher_card_button = ctk.CTkButton(self.staff_report_page_frame, text = "ID Card", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=on_tree_view_selection, fg_color="#074173", text_color="white", image = self.generate_id_card_image)
        self.generate_teacher_card_button.place(x = 740, y = 630)

        self.send_mail_image = SetImage(image_path="image/send-mail.png", width = 25, height=25)
        self.send_email_button = ctk.CTkButton(self.staff_report_page_frame, text = "Send Email", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=send_email, fg_color="#074173", text_color="white", image = self.send_mail_image)
        self.send_email_button.place(x = 920, y = 630)

        self.staff_report_page_frame.place(x = 0, y = 0)

    def student_report_frame(self):
        self.student_report_page_frame = ctk.CTkFrame(self.admin_rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.student_report_page_frame, text = "Manage Student Reports", fg_color="#074173",text_color="white")

        def fetch_std_div_record():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #execute the std query
                cur.execute("select std_name from standard")

                std_record = cur.fetchall()
                std_list = []
                for std in std_record:
                    std_list.append(str(std[0]))
                
                self.standard_values_list = std_list
                self.selected_standard_option.configure(values = self.standard_values_list)

                #execute the div query
                cur.execute("select div_name from division group by div_name")

                div_record = cur.fetchall()
                div_list = []
                for div in div_record:
                    div_list.append(str(div[0]))
                
                self.division_values_list = div_list
                self.selected_division_option.configure(values = self.division_values_list)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        def show_student_record():
            #=======treeview setting========#
            #add some style
            style = ttk.Style()

            #pick a theme
            style.theme_use("alt")

            #configure the tree view color
            style.configure("Treeview", 
                            background = "#EEF0E5",
                            rowheight = 25,
                            fieldbackground = "#F3FBF1", font = ("Consolas", 14))
            
            style.configure("mystyle.Treeview", font=('Consolas', 15))

            #configure the selected color
            style.configure("Treeview", background = [("selected", "#347083")])

            #increse the font size of heading
            style.configure("Treeview.Heading", font=("Consolas", 18))

            self.data_frame = tk.Frame(self.student_report_page_frame, bg = "lightgrey", borderwidth=0, relief="solid")
            self.data_frame.pack_propagate(False)
            self.data_frame.place(x = 20, y = 230, height = 550, width = 1320)

            #create a scrollbar
            y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
            x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

            y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
            x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

            #create a treeview
            self.show_student_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
            self.show_student_tree.pack(fill = "both", expand= True)

            #configure the scrollbar
            x_scroll.config(command = self.show_student_tree.xview)
            y_scroll.config(command = self.show_student_tree.yview)

            #define our columns
            self.show_student_tree["columns"] = ("Sr No", "Student ID", "Name", "Gender", "Mobile", "Date of Birth", "Email", "City", "Pincode")

            #format column
            self.show_student_tree.column("Sr No", anchor="center", width = 100, minwidth=100)
            self.show_student_tree.column("Student ID", anchor="center", width = 200, minwidth=200)
            self.show_student_tree.column("Name", anchor="center", width = 300, minwidth=300)
            self.show_student_tree.column("Gender", anchor="center", width = 300, minwidth = 300)
            self.show_student_tree.column("Mobile", anchor="center", width = 300, minwidth = 300)
            self.show_student_tree.column("Date of Birth", anchor="center", width = 300, minwidth = 300)
            self.show_student_tree.column("Email", anchor="center", width = 300, minwidth = 300)
            self.show_student_tree.column("City", anchor="center", width = 300, minwidth = 300)
            self.show_student_tree.column("Pincode", anchor="center", width = 300, minwidth = 300)

            #create a heading
            self.show_student_tree.heading("Sr No", text = "Sr No", anchor = "center")
            self.show_student_tree.heading("Student ID", text = "Student ID", anchor = "center")
            self.show_student_tree.heading("Name", text = "Name", anchor = "center")
            self.show_student_tree.heading("Gender", text = "Gender", anchor = "center")
            self.show_student_tree.heading("Mobile", text = "Mobile", anchor = "center")
            self.show_student_tree.heading("Date of Birth", text = "Date of Birth", anchor = "center")
            self.show_student_tree.heading("Email", text = "Email", anchor = "center")
            self.show_student_tree.heading("City", text = "City", anchor = "center")
            self.show_student_tree.heading("Pincode", text = "Pincode", anchor = "center")

            #Create striped to our tages
            self.show_student_tree.tag_configure("oddrow", background="white")
            self.show_student_tree.tag_configure("evenrow", background="lightblue")

            #========show student record========#
            def show_record_auto():
                #========fetch std and div======#
                std = std_var.get()
                div = div_var.get()

                #=========fetch record==========#
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #======fetch student details============#
                    #execute the select query
                    cur.execute("select srno, student_id,concat(first_name, ' ' , last_name), gender, mobile, dob, email, city, pincode from student where std_name = %s and div_name = %s", (std, div))

                    records = cur.fetchall()

                    self.count = 0
                    #show record in treeview
                    for record in records:
                        if self.count %2 == 0:
                            self.show_student_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]), tags=("evenrow",))
                        else:
                            self.show_student_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8]), tags=("oddrow",))
                        self.count += 1

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

            show_record_auto()

        self.choose_standard_label = ctk.CTkLabel(self.student_report_page_frame, text = "Select Standard :", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.choose_standard_label.place(x = 30, y = 60)

        self.standard_values_list = []
        std_var = tk.StringVar(value = "")
        self.selected_standard_option = ctk.CTkOptionMenu(self.student_report_page_frame, width = 200, height = 30, corner_radius=2, values=self.standard_values_list, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=std_var)
        self.selected_standard_option.place(x = 210, y = 60)

        self.choose_division_label = ctk.CTkLabel(self.student_report_page_frame, text = "Select Division :", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.choose_division_label.place(x = 43, y =100)

        self.division_values_list = []
        div_var = tk.StringVar(value = "")
        self.selected_division_option = ctk.CTkOptionMenu(self.student_report_page_frame, width = 200, height = 30, corner_radius=2, values=self.division_values_list, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=div_var)
        self.selected_division_option.place(x = 210, y = 100)

        self.select_button = ctk.CTkButton(self.student_report_page_frame, text = "Select", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 120, height = 35, command=show_student_record)
        self.select_button.place(x = 210, y = 140)

        #===========calling the function============#
        fetch_std_div_record()
   
        self.student_report_page_frame.place(x = 0, y = 0)

    def feedback_frame(self):
        self.feedback_page_frame = ctk.CTkFrame(self.admin_rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.feedback_page_frame, text = "Feedback Management", fg_color="#074173",text_color="white")

        def on_return(event):
            event.widget.tk_focusNext().focus()
            return "break"

        #===========save feedback function===========#
        def save_feedback_question():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                cur = con.cursor()

                #insert feedback into table
                insert_query = "insert into feedback_question(question_text, choice1_text,choice2_text,choice3_text,choice4_text) values(%s, %s, %s, %s, %s)"
                insert_values = (self.feedback_question_entry.get(), self.option1_entry.get(),self.option2_entry.get(),self.option3_entry.get(),self.option4_entry.get())

                cur.execute(insert_query, insert_values)

                #commit the changes
                con.commit()

                messagebox.showinfo("Success", "Feedback added successfully.")

                #close the connection
                con.close()

                #=========clear the textbox===========#
                self.feedback_question_entry.delete(0, tk.END)
                self.option1_entry.delete(0, tk.END)
                self.option2_entry.delete(0, tk.END)
                self.option3_entry.delete(0, tk.END)
                self.option4_entry.delete(0, tk.END)

            except Exception as e:
                print(e)

        #=============create feedback question entry===================#
        self.feedback_question = ctk.CTkLabel(self.feedback_page_frame, text = "Feedback question: ", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.feedback_question.place(x = 23, y = 60)

        self.feedback_question_entry = ctk.CTkEntry(self.feedback_page_frame, width = 300, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.feedback_question_entry.place(x = 230, y = 60)
        FocusColor(entry=self.feedback_question_entry, border_color="#1D49CB")
        self.feedback_question_entry.bind("<Return>", on_return)

        self.feedback_options = ctk.CTkLabel(self.feedback_page_frame, text = "Feedback Options: ", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.feedback_options.place(x = 30, y = 110)

        self.option1_label = ctk.CTkLabel(self.feedback_page_frame, text = "1. ", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.option1_label.place(x = 230, y = 110)

        self.option1_entry = ctk.CTkEntry(self.feedback_page_frame,width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.option1_entry.place(x = 260, y = 110)
        FocusColor(entry=self.option1_entry , border_color="#1D49CB")
        self.option1_entry.bind("<Return>", on_return)

        self.option2_label = ctk.CTkLabel(self.feedback_page_frame, text = "2. ", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.option2_label.place(x = 230, y = 150)

        self.option2_entry = ctk.CTkEntry(self.feedback_page_frame, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.option2_entry.place(x = 260, y = 150)
        FocusColor(entry=self.option2_entry , border_color="#1D49CB")
        self.option2_entry.bind("<Return>", on_return)

        self.option3_label = ctk.CTkLabel(self.feedback_page_frame, text = "3. ", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.option3_label.place(x = 230, y = 190)

        self.option3_entry = ctk.CTkEntry(self.feedback_page_frame, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.option3_entry.place(x = 260, y = 190)
        FocusColor(entry=self.option3_entry , border_color="#1D49CB")
        self.option3_entry.bind("<Return>", on_return)

        self.option4_label = ctk.CTkLabel(self.feedback_page_frame, text = "4. ", font = ("Verdana Pro", 18), text_color="#1D49CB")
        self.option4_label.place(x = 230, y = 230)

        self.option4_entry = ctk.CTkEntry(self.feedback_page_frame,width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.option4_entry.place(x = 260, y = 230)
        FocusColor(entry=self.option4_entry , border_color="#1D49CB")
        self.option4_entry.bind("<Return>", on_return)

        self.add_button = ctk.CTkButton(self.feedback_page_frame, text = "Add", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 120, height = 35, command=save_feedback_question)
        self.add_button.place(x = 260, y = 300)

        self.feedback_page_frame.place(x = 0, y = 0)

    def make_announcement_frame(self):
        self.anouncement_page_frame = ctk.CTkFrame(self.admin_rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.anouncement_page_frame, text = "Manage Events & Notices", fg_color="#074173",text_color="white")

        #=========functions=========#
        def notice_frame():
            #=====inside frame======#
            self.make_notice = ctk.CTkFrame(self.anouncement_page_frame, width = 1072, height=500, corner_radius=0,fg_color="white")

            def on_return(event):
                event.widget.tk_focusNext().focus()
                return "break"

            #=======function============#
            def create_notices():
                #=======datetime========#
                current_date = date.today()
                hour = strftime("%I")          #for 12 hours = I and for 24 hours = H
                minute = strftime("%M")
                second = strftime("%S")
                time = f"{hour}:{minute}:{second}"
                date_time = f"{current_date} {time}"

                notice_subject = self.notice_entry.get()
                notice_content = self.notice_content_entry.get("0.0", tk.END)
                
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    cur = con.cursor()

                    cur.execute("insert into announcement(type, announcement_subject, announcement_content, edate) value(%s, %s, %s, %s)", ("Notice", notice_subject, notice_content, date_time))

                    #commit the changes
                    con.commit()

                    messagebox.showinfo("Successfull", "Notice created successfully!")

                    #close the connection
                    con.close()
                except Exception as e:
                    print(e)

            #==========subject=============#
            self.notice_subject = ctk.CTkLabel(self.make_notice, text="Enter notice subject:",font = ("Verdana Pro", 18), text_color="#1D49CB")
            self.notice_subject.place(x = 15, y = 15)

            self.notice_entry = ctk.CTkEntry(self.make_notice, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
            self.notice_entry.place(x = 220, y = 15)
            FocusColor(entry=self.notice_entry , border_color="#1D49CB")
            self.notice_entry.bind("<Return>", on_return)

            #=========main body=============#
            self.notice_content = ctk.CTkLabel(self.make_notice, text="Enter notice content:",font = ("Verdana Pro", 18), text_color="#1D49CB")
            self.notice_content.place(x = 15, y = 60)

            self.notice_content_entry = ctk.CTkTextbox(self.make_notice, width=250, height = 80, corner_radius=2, font = ("Verdana Pro", 16), wrap = "word", fg_color = "#D8D9DA", text_color= "black", border_width=0)
            self.notice_content_entry.place(x = 220, y = 60)
            FocusColor(entry=self.notice_content_entry , border_color="#1D49CB")
            self.notice_content_entry.bind("<Return>", on_return)

            self.create_notice_button = ctk.CTkButton(self.make_notice, text = "Publish Notices", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 180, height = 35,  command=create_notices)
            self.create_notice_button.place(x = 220, y = 150)

            self.make_notice.place(x = 10, y = 150)

        def event_frame():
            #=====inside frame======#
            self.make_event = ctk.CTkFrame(self.anouncement_page_frame, width = 1072, height=500, corner_radius=0,fg_color="white")

            def on_return(event):
                event.widget.tk_focusNext().focus()
                return "break"

            #=======function============#
            def create_event():
                event_subject = self.event_entry.get()
                event_content = self.event_content_entry.get("0.0", tk.END)
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    cur = con.cursor()

                    cur.execute("insert into announcement(type, announcement_subject, announcement_content) value(%s, %s)", ("Event", event_subject,event_content))

                    #commit the changes
                    con.commit()

                    messagebox.showinfo("Successfull", "Event created successfully!")

                    #close the connection
                    con.close()
                except Exception as e:
                    print(e)

            #==========subject=============#
            self.event_subject = ctk.CTkLabel(self.make_event, text="Enter event subject:",font = ("Verdana Pro", 18), text_color="#1D49CB")
            self.event_subject.place(x = 18, y = 15)

            self.event_entry = ctk.CTkEntry(self.make_event, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black", border_width=0)
            self.event_entry.place(x = 230, y = 15)
            FocusColor(entry=self.event_entry , border_color="#1D49CB")
            self.event_entry.bind("<Return>", on_return)

            #=========main body=============#
            self.event_content = ctk.CTkLabel(self.make_event, text="Enter event content:",font = ("Verdana Pro", 18), text_color="#1D49CB")
            self.event_content.place(x = 15, y = 60)

            self.event_content_entry = ctk.CTkTextbox(self.make_event, width=250, height = 80, corner_radius=2, font = ("Verdana Pro", 16), wrap = "word", fg_color = "#D8D9DA", text_color= "black", border_width=0)
            self.event_content_entry.place(x = 230, y = 60)
            FocusColor(entry=self.event_content_entry , border_color="#1D49CB")
            self.event_content_entry.bind("<Return>", on_return)

            self.create_event_button = ctk.CTkButton(self.make_event, text = "Publish Events", font = ("Verdana Pro", 18), fg_color="#074173", corner_radius=2, width = 180, height = 35,  command=create_event)
            self.create_event_button.place(x = 230, y = 310)

            self.make_event.place(x = 10, y = 150)

        #=======notice======#
        self.send_notice_button = ctk.CTkButton(self.anouncement_page_frame, text = "Create Notices", width = 300, height = 45,font = ("Verdana Pro", 17), cursor = "hand2", fg_color="#1D49CB", text_color="white", hover_color="#1C1678", corner_radius=2,command=notice_frame)
        self.send_notice_button.place(x=10,y=60)

        #=======event======#
        self.send_event_button = ctk.CTkButton(self.anouncement_page_frame, text = "Create Events", width = 300, height = 45,font = ("Verdana Pro", 17), cursor = "hand2", fg_color="#1D49CB", text_color="white", hover_color="#1C1678", corner_radius=2, command=event_frame)
        self.send_event_button.place(x=330,y=60)

        self.anouncement_page_frame.place(x = 0, y = 0)
        
class StudentHomeWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("1536x864-10-7")
        self.after(200, lambda : self.iconbitmap("image/slogo.ico"))

        #======switch_frame=======#
        def switch_frame(page, indicator_button):
            for frame in self.rightside_frame.winfo_children():
                frame.destroy()
                self.update()
            page()

            for child in self.student_sidebar_frame.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    child.configure(fg_color = "#2d6a4f")

            indicator_button.configure(fg_color= "#163020")

        #=====return to main window=======#
        def confirm_exit():
            answer = messagebox.askquestion("Confirm Exit", "Are you sure you want to exit?")
            if answer == "yes":
                self.destroy()
                root.deiconify()

        #======calling heading label class =======#
        self.heading_frame = HeadingFrame(self)
        self.heading_frame.place(x = 5, y = 5)

        #======student home frame=======#
        self.student_homepage_frame = ctk.CTkFrame(self, width = 1526, height=730, corner_radius=0,  border_width=1, border_color="green", fg_color="#D8D9DA")
        
        self.student_sidebar_frame = ctk.CTkFrame(self.student_homepage_frame, width=350,height=700, corner_radius=0,  border_width=0, border_color="green", fg_color="#2d6a4f")

        self.sidebar_head_label = ctk.CTkLabel(self.student_sidebar_frame, text = "", height = 5, width = 348, fg_color="#163020")
        self.sidebar_head_label.place(x = 0, y = 0)

        #======photo frame==========#
        self.student_photo_frame = ctk.CTkFrame(self.student_sidebar_frame, width = 150, height=170, corner_radius=0, fg_color="#2d6a4f")
        self.student_photo_frame.place(x = 100, y = 40)

        self.student_photo_label = ctk.CTkLabel(self.student_photo_frame, text = "", width = 149, height=169, fg_color="#2d6a4f")
        self.student_photo_label.place(x = 0, y = 0)

        self.student_greet_label = ctk.CTkLabel(self.student_sidebar_frame, text = "", font=("Verdana Pro", 18), text_color="white")
        self.student_greet_label.place(x = 95, y = 220)

        #==========solve the warning=========#
        warnings.filterwarnings("ignore", category=UserWarning)

        # Function to create buttons with aligned image and text
        def create_button(frame, text, image_path, image_width, image_height, width, height, command, y_position, fg_color = "#2d6a4f"):
            # Adjust the text with padding spaces
            button_text = " " * 5 + text  # Add spaces before the text for alignment
            image = SetImage(image_path=image_path, width=image_width, height=image_height)
            
            button = ctk.CTkButton(
                frame,
                text=button_text,
                width=width,
                height=height,
                font=("Verdana Pro", 18),
                text_color="white",
                fg_color="#2d6a4f",
                corner_radius=60,
                hover_color="#163020",
                cursor="hand2",
                command=command,
                image=image,
                anchor="w"  # Use "w" to left-align text and image
            )
            button.place(x=24, y=y_position)
            return button

        # Create buttons with consistent image sizes
        self.profile_button = create_button(
            self.student_sidebar_frame, 
            "My Profile", 
            "image/user.png", 
            22, 22,  # Image size
            300, 45,  # Button size
            lambda: switch_frame(page=self.profile_frame, indicator_button=self.profile_button), 
            270,
            "#163020"
            
        )

        self.home_button = create_button(
            self.student_sidebar_frame, 
            "Home", 
            "image/home-dashboard.png", 
            22, 22, 
            300, 45, 
            lambda: switch_frame(page=self.home_frame, indicator_button=self.home_button), 
            317
        )

        self.view_result_button = create_button(
            self.student_sidebar_frame, 
            "View Result", 
            "image/result_icon.png", 
            22, 22, 
            300, 45, 
            lambda: switch_frame(page=self.view_result_frame, indicator_button=self.view_result_button), 
            364
        )

        self.notes_button = create_button(
            self.student_sidebar_frame, 
            "View Notes", 
            "image/view_note.png", 
            22, 22, 
            300, 45, 
            lambda: switch_frame(self.view_notes_frame, indicator_button=self.notes_button), 
            411
        )

        self.attend_report_button = create_button(
            self.student_sidebar_frame, 
            "View Attendance", 
            "image/view-attendance.png", 
            22, 22,  # Adjusted to maintain uniformity
            300, 45, 
            lambda: switch_frame(page=self.attendance_frame, indicator_button=self.attend_report_button), 
            458
        )

        self.leave_button = create_button(
            self.student_sidebar_frame, 
            "Leave", 
            "image/leave_icon.png", 
            22, 22,  # Adjusted to maintain uniformity
            300, 45, 
            lambda: switch_frame(page=self.leave_frame, indicator_button=self.leave_button), 
            505
        )

        self.complain_button = create_button(
            self.student_sidebar_frame, 
            "Complain", 
            "image/feedback.png", 
            22, 22,  # Adjusted to maintain uniformity
            300, 45, 
            lambda: switch_frame(page=self.complain_frame, indicator_button=self.complain_button), 
            552
        )

        self.feedback_button = create_button(
            self.student_sidebar_frame, 
            "Feedback", 
            "image/feedback_icon.png", 
            22, 22,  # Adjusted to maintain uniformity
            300, 45, 
            lambda: switch_frame(page=self.feedback_frame, indicator_button=self.feedback_button), 
            599
        )

        self.logout_button = create_button(
            self.student_sidebar_frame, 
            "Logout", 
            "image/logout_icon.png", 
            22, 22,  # Adjusted to maintain uniformity
            300, 45, 
            confirm_exit, 
            646
        )

        self.student_sidebar_frame.place(x=30, y=10)

        #=====rightside=========#
        self.rightside_frame = ctk.CTkFrame(self.student_homepage_frame, width = 1092, height=700, corner_radius=0,  border_width=None, fg_color="white")
        self.rightside_frame.place(x = 400, y = 10)

        self.student_homepage_frame.place(x = 5, y = 100)

    def home_frame(self):
        self.home_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.home_page_frame, text = "Welcome to Attendance Portal", fg_color="#2d6a4f", text_color="white")

        try:
            con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

            #create a cursor instance
            cur = con.cursor()

            #==fetch total count =========#
            cur.execute("select count(a.student_no) as total_count from student s, attendance a where s.srno = a.student_no and email = %s",(student_username,))

            total_count = cur.fetchone()

            #====fetch present count========#
            cur.execute("select count(a.student_no) as present from student s, attendance a where  s.srno = a.student_no and email = %s and attendance_status = 'Present'",(student_username,))

            present_count = cur.fetchone()

            #====fetch absent count========#
            cur.execute("select count(a.student_no) as absent from student s, attendance a where  s.srno = a.student_no and email = %s and attendance_status = 'Absent'",(student_username,))

            absent_count = cur.fetchone()

            #====fetch leave count========#
            cur.execute("select count(a.student_no) as absent from student s, attendance a where  s.srno = a.student_no and email = %s and attendance_status = 'Leave'",(student_username,))

            leave_count = cur.fetchone()

            #====fetch complain record=========#
            cur.execute("select count(c.rollno) as complain from student s, complain c where  s.srno = c.rollno and email = %s",(student_username,))

            complain_count = cur.fetchone()

            #close the connection
            con.close()

        except Exception as e:
            print("Error ", e)
            
        #=======attendance frame========#
        self.attendance_page_frame = ctk.CTkFrame(self.home_page_frame, width = 992, height=170, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        def display_frame(parent, frame_color,title,count ,image_relative_path, x, y):
            #=======about us buttons=======#
            frame = ctk.CTkFrame(parent, width = 330, height = 150, fg_color=f"{frame_color}", corner_radius=4, border_width=0)

            self.label = ctk.CTkLabel(frame, text = f"{title}",font = ("Verdana Pro",18), text_color="white")
            self.label.place(x = 10, y = 90)

            self.total_label=ctk.CTkLabel(frame,text=f"{count}", text_color="white",font=("Verdana Pro",40, "bold"))
            self.total_label.place(x=10,y=20)

            self.image = ctk.CTkImage(light_image=Image.open(f"{image_relative_path}"), dark_image=Image.open(f"{image_relative_path}"), size = (45, 45))
            
            self.image_label = ctk.CTkLabel(frame, text = "", image = self.image, fg_color="transparent")
            self.image_label.place(x = 260, y = 50)

            frame.place(x= x, y = y)

        #======total attendance==========#
        display_frame(self.home_page_frame, frame_color="#2D9596", title="Total Attendance", image_relative_path="image/bar-graph (1).png",x = 20, y = 60, count = f"{total_count[0]}")

        #=====total absent========#
        display_frame(self.home_page_frame, frame_color="#388E3C", title="Total Absent", image_relative_path="image/bar-graph (1).png",x = 380, y = 60, count = f"{absent_count[0]}")

        #=====total present_count=======#
        display_frame(self.home_page_frame, frame_color="#FF204E", title="Total Present", image_relative_path="image/bar-graph (1).png",x = 740, y = 60, count = f"{present_count[0]}")

        #=====total leave_count=======#
        display_frame(self.home_page_frame, frame_color="#9A3B3B", title="Total Leave", image_relative_path="image/bar-graph (1).png",x = 200, y = 240, count = f"{leave_count[0]}")

        #=====total complain_count=======#
        display_frame(self.home_page_frame, frame_color="#A61F69", title="Total Complain", image_relative_path="image/bar-graph (1).png",x = 560, y = 240, count = f"{complain_count[0]}")

        self.home_page_frame.place(x = 0, y = 0)
    
    def profile_frame(self):
        self.profile_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.profile_page_frame, text = "My Profile", fg_color="#2d6a4f", text_color="white")

        #========functions========#
        def show_profile():
            global path, imageo
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #execute the cursor query
                select_query = "select concat(first_name,' ', last_name) as name, srno , email, mobile, address, city, pincode, image_path, first_name from student where email = %s"
                cur.execute(select_query,(student_username,))

                records = cur.fetchone()

                # show this detail in entry box
                self.name_entry.configure(text = records[0])
                self.rollno_entry.configure(text = records[1])
                email_var.set(value=records[2])
                contact_var.set(value = records[3])
                self.address_entry.insert(tk.END, records[4])
                # address_var.set(value = records[4])
                city_var.set(value=records[5])
                pincode_var.set(value=records[6])

                image_path = records[7]

                #open the image
                try:
                    image = Image.open(image_path)
                except FileNotFoundError:
                    print(f"Error: Could not find image at path: {image_path}")

                #base name of the image
                image_file_name = os.path.basename(image_path)

                #save the image
                image.save(image_file_name)
                
                #open image in form of ctk.CTkImage
                imageo = ctk.CTkImage(light_image=image, dark_image=image, size = (140, 160))

                #configure the left side frame label
                self.student_photo_label.configure(image = imageo)
                self.student_photo_label.image = imageo
                
                #configure the image welcome label
                self.student_greet_label.configure(text = f"Welcome {records[8]}")

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        def update_photo():
            global changed_image_path
            changed_image_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("JPG Files", ".jpg"),("PNG Files", ".png"),("All files", ".")], initialdir="C:/Users/vikas/OneDrive/Documents/software project/image", title="Open File")

            try:
                image = Image.open(changed_image_path)

            except FileNotFoundError:
                print(f"Error: Could not find image at path: {changed_image_path}")

            #====configure the image===========#
            #base name of the image
            image_file_name = os.path.basename(changed_image_path)

            #save the image
            image.save(image_file_name)
                
            #open image in form of ctk.CTkImage
            imageo = ctk.CTkImage(light_image=image, dark_image=image, size = (140, 160))

            self.photo_button.configure(image = imageo)
            self.photo_button.image = imageo

            self.upload_photo_label.configure(text = f"{image_file_name}", wraplength = 110)

            #configure the left side frame label
            self.student_photo_label.configure(image = imageo)
            self.student_photo_label.image = imageo
                
        def add_photo_database():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #update the image_path
                update_query = "update student set image_path = %s where email = %s"
                update_value = (changed_image_path, self.email_entry.get())

                cur.execute(update_query, update_value)

                #commit the changes
                con.commit()

                messagebox.showinfo("Update Successful", "Image updated successfully!")

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #============fetch id card============#
        def view_id_card():
            id_card_window = ctk.CTkToplevel(fg_color="white")
            id_card_window.geometry("600x500+800+250")
            id_card_window.title("School Management System")

            #==========function==========#
            def show_id_card():
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    cur.execute("select srno, first_name from student where email = %s", (student_username,))

                    result = cur.fetchone()
                    return result

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

            #======card frame===========#
            self.student_card_frame = ctk.CTkFrame(id_card_window, border_width=2,border_color="#2d6a4f", fg_color="white", width = 580, height = 480, corner_radius=2)

            #======card label===========#
            self.head_label = ctk.CTkLabel(self.student_card_frame, text = "Identity Card",width = 580, height = 40, fg_color="#2d6a4f", text_color="white", font = ("Verdana Pro", 18))
            self.head_label.place(x = 0, y = 0)

            # #====ignore warnings===========#
            warnings.filterwarnings("ignore", category=UserWarning)

            #==========call the show id card function==============#
            results = show_id_card()

            # #=====iid card image label==========#
            file_name = "C:/Users/vikas/OneDrive/Documents/software project/student_id"
            student_image = Image.open(f"{file_name}/{results[0]}_{results[1]} id_card.png")

            id_card_image = ImageTk.PhotoImage(student_image)
            self.student_card_label = ctk.CTkLabel(self.student_card_frame, text = "", image = id_card_image)
            self.student_card_label.place(x = 170, y = 50)

            # #===========save button=============#
            def save_student_card():
                file_path = filedialog.askdirectory(initialdir="C:/Users/vikas/OneDrive/Documents/save id cards")

                if file_path:
                    # print(file_path)
                    if os.path.exists(f"{file_path}/{results[0]}_{results[1]} id_card.png"):
                        error_message = f"The file '{file_path}/{results[0]}_{results[1]} id_card.png' already exists."
                        messagebox.showinfo("File Exists", message=error_message)
                    else:
                        image_to_save = ImageTk.getimage(id_card_image) 
                        image_to_save.save(f"{file_path}/{results[0]}_{results[1]} id_card.png")
                        success_message = f"The student ID card for {results[1]} has been saved successfully!"
                        messagebox.showinfo("Success", message=success_message)

            #=========button===============#
            self.save_image = SetImage(image_path="image/download.png", width = 20, height=20)
            self.save_button = ctk.CTkButton(self.student_card_frame, text = "Save", width = 120, height = 38, font = ("Verdana Pro", 18), cursor = "hand2", command =  save_student_card,fg_color="#2d6a4f", text_color="white", hover_color="#40A578", image = self.save_image)
            self.save_button.place(x = 220, y = 400)

            self.student_card_frame.place(x = 10, y = 10)

            #=====calling the function==========#
            show_id_card()
    
            id_card_window.grab_set()

        #=======inside widget========#
        self.name_label =  ctk.CTkLabel(self.profile_page_frame, text = "Name : ", text_color="green", font=("Verdana Pro", 18))
        self.name_label.place(x = 110, y = 80)

        self.name_entry =  ctk.CTkLabel(self.profile_page_frame, text = "", text_color="red", font=("Verdana Pro", 16))
        self.name_entry.place(x = 190, y = 80)

        self.rollno_label =  ctk.CTkLabel(self.profile_page_frame, text = "Roll No : ", text_color="green", font=("Verdana Pro", 18))
        self.rollno_label.place(x = 100, y = 120)

        self.rollno_entry =  ctk.CTkLabel(self.profile_page_frame, text = "", text_color="red", font=("Verdana Pro", 16))
        self.rollno_entry.place(x = 190, y = 120)

        self.email_label =  ctk.CTkLabel(self.profile_page_frame, text = "Email : ", text_color="green", font=("Verdana Pro", 18))
        self.email_label.place(x = 113, y = 160)

        email_var = tk.StringVar()
        self.email_entry = ctk.CTkEntry(self.profile_page_frame, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16) , fg_color = "#D8D9DA", text_color= "black", textvariable=email_var, state="disabled", border_width=0)
        self.email_entry.place(x = 190, y = 160)
        FocusColor(entry = self.email_entry, border_color="#2d6a4f")

        self.contact_label =  ctk.CTkLabel(self.profile_page_frame, text = "Contact No : ", text_color="green", font=("Verdana Pro", 18))
        self.contact_label.place(x = 62, y = 200)

        contact_var = tk.StringVar()
        self.contact_entry = ctk.CTkEntry(self.profile_page_frame, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black",textvariable=contact_var, state="disabled", border_width=0)
        self.contact_entry.place(x = 190, y = 200)
        FocusColor(entry = self.contact_entry, border_color="#2d6a4f")

        self.address_label =  ctk.CTkLabel(self.profile_page_frame, text = "Address : ", text_color="green", font=("Verdana Pro", 18))
        self.address_label.place(x = 90, y = 240)

        self.address_entry = ctk.CTkTextbox(self.profile_page_frame,width=250, height = 60, corner_radius=2, font = ("Verdana Pro", 16), wrap = "word", fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.address_entry.place(x = 190, y = 240)
        FocusColor(entry = self.address_entry, border_color="#2d6a4f")

        self.city_label =  ctk.CTkLabel(self.profile_page_frame, text = "City : ", text_color="green", font=("Verdana Pro", 18))
        self.city_label.place(x = 123, y = 305)

        city_var = tk.StringVar()
        self.city_entry = ctk.CTkEntry(self.profile_page_frame, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16),textvariable=city_var, state="disabled" , fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.city_entry.place(x = 190, y = 305)
        FocusColor(entry = self.city_entry, border_color="#2d6a4f")

        self.pincode_label =  ctk.CTkLabel(self.profile_page_frame, text = "Pincode : ", text_color="green", font=("Verdana Pro", 18))
        self.pincode_label.place(x = 90, y = 345)

        pincode_var = tk.StringVar()
        self.pincode_entry = ctk.CTkEntry(self.profile_page_frame, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16),textvariable=pincode_var, state="disabled", fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.pincode_entry.place(x = 190, y = 345)
        FocusColor(entry = self.pincode_entry, border_color="#2d6a4f")
        
        self.update_image = SetImage(image_path="image/updated.png", width = 25, height=25)
        self.update_button = ctk.CTkButton(self.profile_page_frame, text = "Update", width = 170, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=None, image = self.update_image, fg_color="#2d6a4f", text_color="white", hover_color="#40A578")
        self.update_button.place(x = 190, y = 390)

        self.id_card_image = SetImage(image_path="image/id-card.png", width = 25, height=25)
        self.view_id_button = ctk.CTkButton(self.profile_page_frame, text = "View ID Card", width = 170, height = 40,cursor = "hand2",font = ("Verdana Pro", 16), command=view_id_card, image = self.id_card_image, fg_color="#2d6a4f", text_color="white", hover_color="#40A578")
        self.view_id_button.place(x = 190, y = 435)

        self.save_image = SetImage(image_path="image/add-image.png", width = 22, height=22)
        self.upload_photo_label = ctk.CTkLabel(self.profile_page_frame, text = "No file choosen", text_color="black", font=("Verdana Pro", 16))
        self.upload_photo_label.place(x = 905, y = 305)

        self.add_photo_button = ctk.CTkButton(self.profile_page_frame, text = "Add", width = 150, height = 38,font = ("Verdana Pro", 16), cursor = "hand2", command = add_photo_database, image = self.save_image, fg_color="#2d6a4f", text_color="white", hover_color="#40A578")
        self.add_photo_button.place(x = 900, y = 260)

        self.updated_photo_frame = ctk.CTkFrame(self.profile_page_frame, width = 150, height=170, corner_radius=0,  border_width=2, border_color="black", fg_color="white")
        self.updated_photo_frame.place(x=900,y=80)

        self.photo_button = ctk.CTkButton(self.updated_photo_frame, text = "", fg_color="SystemButtonFace", hover_color= "SystemButtonFace", border_width=2, border_color="black", corner_radius=3, command = update_photo, width = 150, height = 170, image = "")
        self.photo_button.place(x = 0, y = 0)

        self.profile_page_frame.place(x=0,y=0)

        #======calling the function======#
        show_profile()
        self.profile_page_frame.place(x = 0, y = 0)

    def leave_frame(self):
        self.leave_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.leave_page_frame, text = "Leave", fg_color="#2d6a4f", text_color="white")

        #=========functions=========#
        def student_apply_leave_frame():
            #=====inside frame======#
            self.leave_main_frame = ctk.CTkFrame(self.leave_page_frame, width = 1072, height=270, corner_radius=0,  border_width=0, border_color="green", fg_color="white")

            #=======functions==============#
            def apply_for_leave():
                leave_msg = self.leave_textbox.get("1.0", tk.END)
                days = no_of_day_var.get()
                current_date = date.today()
                hour = strftime("%I")          #for 12 hours = I and for 24 hours = H
                minute = strftime("%M")
                second = strftime("%S")
                time = f"{hour}:{minute}:{second}"
                date_time = f"{current_date} {time}"

                #===connecting to the database and sending leave to teacher=========#
                if leave_msg == "" or days == "":
                    messagebox.showerror("Error","Please fill all the fields!")
                else:
                    try:
                        con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                        cur = con.cursor()
                        
                        #fetch some personal details
                        cur.execute("select srno, concat(first_name,' ',last_name) as name, std_name from student where email = %s",(student_username,))

                        std_record = cur.fetchone()
                        
                        #insert record in database
                        insert_query = "insert into student_leave(rollno, student_name, std_name, message, no_days, edate) value(%s, %s, %s, %s, %s, %s)"
                        insert_value = (std_record[0], std_record[1], std_record[2], leave_msg, days,date_time )

                        cur.execute(insert_query, insert_value)

                        #commit the changes
                        con.commit()

                        self.apply_leave_label.configure(text = "Apply for leave Successfully")

                        #close the connection
                        con.close()

                        #===clear the textbox========#
                        self.leave_textbox.delete("0.0", tk.END)
                        no_of_day_var.set("")

                    except Exception as e:
                        print(e)
                        # messagebox.showerror("Error", e)

            #======leave reason label=====#
            self.leave_label = ctk.CTkLabel(self.leave_main_frame, text = "Leave Reason:", font = ("Verdana Pro", 18), text_color="green")
            self.leave_label.place(x = 300, y = 75)

            #======leave reason textbox=====#
            self.leave_textbox = ctk.CTkTextbox(self.leave_main_frame,width=300, height = 80, corner_radius=2, border_width=0, fg_color = "#D8D9DA", text_color= "black",border_color="grey", font = ("Verdana Pro", 16), wrap = "word")
            self.leave_textbox.place(x = 450, y = 50)
            self.leave_textbox.bind("<KeyRelease>", lambda e: self.apply_leave_label.configure(text=""))
            FocusColor(entry = self.leave_textbox, border_color="#2d6a4f")

            #======no. of days label=====#
            self.days_label = ctk.CTkLabel(self.leave_main_frame, text = "No of Days:", font = ("Verdana Pro", 18), text_color="green")
            self.days_label.place(x = 322, y = 150)

            #==========Drop down menu===========#
            self.select_days_values=["01","02","03","04","05","06","07","08","09","10"]
            no_of_day_var = tk.StringVar(value = "")
            self.select_days_option=ctk.CTkOptionMenu(self.leave_main_frame,width=80,height=30,corner_radius=2,values=self.select_days_values,fg_color="#D8D9DA",text_color="black",dropdown_font=("Verdana Pro", 15),font=("Verdana Pro", 18), variable=no_of_day_var, button_color="#9DDE8B", button_hover_color="#9DDE8B")
            self.select_days_option.place(x=450,y=150)

            #========apply leave buttons=========#
            self.apply_leave_button = ctk.CTkButton(self.leave_main_frame, text = "Apply Leave", width = 150, height = 38,font = ("Verdana Pro", 17), cursor = "hand2", command = apply_for_leave, fg_color="#2d6a4f", text_color="white", hover_color="#40A578", corner_radius=2)
            self.apply_leave_button.place(x = 450, y = 200)

            self.apply_leave_label = ctk.CTkLabel(self.leave_main_frame, text = "", font = ("Verdana Pro", 15), text_color="black")
            self.apply_leave_label.place(x = 410, y = 240)

            self.leave_main_frame.place(x = 10, y = 150)

        def student_leave_status_frame():
            #=====inside frame======#
            self.leave_status_frame = ctk.CTkFrame(self.leave_page_frame, width = 1072, height=270, corner_radius=0,  border_width=0, border_color="green", fg_color="white")

            #====================function====================#
            def show_leave_record():
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #fetch the leave record detail to see status
                    cur.execute("select message, no_days, status from student_leave sl, student s where sl.rollno = s.srno and s.email = %s",(student_username,))

                    records = cur.fetchall()

                    self.count = 0
                    #show record in treeview
                    for record in records:
                        if self.count %2 == 0:
                            self.leave_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], record[1], record[2]), tags=("evenrow",))
                        else:
                            self.leave_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], record[1], record[2]), tags=("oddrow",))
                        self.count += 1
                    
                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)
                
            #=======treeview setting========#
            #add some style
            style = ttk.Style()

            #pick a theme
            style.theme_use("alt")

            #configure the tree view color
            style.configure("Treeview", 
                            background = "#EEF0E5",
                            rowheight = 25,
                            fieldbackground = "#F3FBF1", font = ("Verdana", 15))
            
            style.configure("mystyle.Treeview", font=('Consolas', 15))

            #configure the selected color
            style.configure("Treeview", background = [("selected", "#2d6a4f")])

            #increse the font size of heading
            style.configure("Treeview.Heading", font=("Consolas", 18))

            self.data_frame = tk.Frame(self.leave_status_frame, bg = "lightgrey", borderwidth=0, relief="solid")
            self.data_frame.pack_propagate(False)
            self.data_frame.place(x = 10, y = 50, height = 200, width = 1320)

            #create a scrollbar
            y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
            x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

            y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
            x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

            #create a treeview
            self.leave_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
            self.leave_tree.pack(fill = "both", expand= True)

            #configure the scrollbar
            x_scroll.config(command = self.leave_tree.xview)
            y_scroll.config(command = self.leave_tree.yview)

            #define our columns
            self.leave_tree["columns"] = ("Leave Reason", "Days", "Status")

            #format column
            self.leave_tree.column("Leave Reason", anchor="center", width = 300, minwidth=300)
            self.leave_tree.column("Days", anchor="center", width = 100, minwidth=100)
            self.leave_tree.column("Status", anchor="center", width = 100, minwidth = 100)
            
            #create a heading
            self.leave_tree.heading("Leave Reason", text = "Leave Reason", anchor = "center")
            self.leave_tree.heading("Days", text = "Days", anchor = "center")
            self.leave_tree.heading("Status", text = "Status", anchor = "center")
            
            #Create striped to our tages
            self.leave_tree.tag_configure("oddrow", background="white")
            self.leave_tree.tag_configure("evenrow", background="#9DDE8B")

            #=======calling the function==========#
            show_leave_record()

            self.leave_status_frame.place(x = 10, y = 150)
        
        #========inside widgets=========#
        #=======apply for leave button======#
        self.apply_leave_button = ctk.CTkButton(self.leave_page_frame, text = "Apply for Leave", width = 300, height = 45,font = ("Verdana Pro", 17), cursor = "hand2", command = student_apply_leave_frame, fg_color="#2d6a4f", text_color="white", hover_color="#40A578", corner_radius=2)
        self.apply_leave_button.place(x=10,y=80)

        #=======leave status report button======#
        self.leave_status_button = ctk.CTkButton(self.leave_page_frame, text = "Leave Status Report", width = 300, height = 45,font = ("Verdana Pro", 17), cursor = "hand2", command = student_leave_status_frame, fg_color="#2d6a4f", text_color="white", hover_color="#40A578", corner_radius=2)
        self.leave_status_button.place(x=330,y=80)

        self.leave_page_frame.place(x = 0, y = 0)

    def complain_frame(self):
        self.complain_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.complain_page_frame, text = "Complain", fg_color="#2d6a4f", text_color="white")

        def student_complain_apply_frame():
            def send_complain_func():
                subject = self.complain_entry.get()
                message = self.message_textbox.get("1.0", tk.END)
                current_date = date.today()
                hour = strftime("%I")          #for 12 hours = I and for 24 hours = H
                minute = strftime("%M")
                second = strftime("%S")
                time = f"{hour}:{minute}:{second}"
                date_time = f"{current_date} {time}"

                #================
                try:
                    con = mycon.connect(host = "localhost", username = "root", password ="root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #fetch the leave record detail to see status
                    cur.execute("select srno, concat(first_name,' ',last_name) as name from student where email = %s",(student_username,))

                    records = cur.fetchall()

                    if not self.complain_entry.get() and not self.message_textbox.get("0.0", tk.END) == "":
                        messagebox.showerror("Complain Error", "Fields are required!")
                        return
                    
                    for record in records:
                        # inserting the values
                        cur.execute("insert into complain(rollno, student_name, subject,message, edate) value(%s, %s, %s, %s, %s)", (record[0], record[1],subject, message, date_time))

                        #commit the changes
                    con.commit()
                            
                    self.complain_label.configure(text = f"Complain Sent")

                    #clear the textbox
                    self.complain_entry.delete(0, tk.END)
                    self.message_textbox.delete("0.0", tk.END)

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)
                    con.rollback()
                
            #========inside widgets=========#
            self.apply_complain_frame = ctk.CTkFrame(self.complain_page_frame, width = 1072, height=500, corner_radius=0,  border_width=0, border_color="green", fg_color="white")

            #======Complain label=====#
            self.complain_label = ctk.CTkLabel(self.apply_complain_frame, text = "Complain About:", font = ("Verdana Pro", 18), text_color="green")
            self.complain_label.place(x = 320, y = 100)

            #======Complain entry========#
            self.complain_entry = ctk.CTkEntry(self.apply_complain_frame, width = 300, height = 35, corner_radius=2, font = ("Verdana Pro", 16) , fg_color = "#D8D9DA", text_color= "black",  border_width=0)
            self.complain_entry.place(x = 500, y = 100)
            FocusColor(entry = self.complain_entry, border_color="#2d6a4f")

            #======message label=====#
            self.message_label = ctk.CTkLabel(self.apply_complain_frame, text = "Message:", font = ("Verdana Pro", 18), text_color="green")
            self.message_label.place(x = 398, y = 175)

            #======message textbox========#
            self.message_textbox = ctk.CTkTextbox(self.apply_complain_frame,width=300, height = 80, corner_radius=2, border_width=0, fg_color = "#D8D9DA", text_color= "black",border_color="grey", font = ("Verdana Pro", 16), wrap = "word")
            self.message_textbox.place(x = 500, y = 150)
            FocusColor(entry = self.message_textbox, border_color="#2d6a4f")

            #====Send buttons======#
            self.send_button = ctk.CTkButton(self.apply_complain_frame, text = "Send Complain", width = 150, height = 38,font = ("Verdana Pro", 17), cursor = "hand2", command = send_complain_func, fg_color="#2d6a4f", text_color="white", hover_color="#40A578", corner_radius=2)
            self.send_button.place(x = 500, y = 240)

            self.apply_complain_frame.place(x = 10, y = 150)

        def student_complain_status_frame():
            self.complain_status_frame = ctk.CTkFrame(self.complain_page_frame, width = 1072, height=500, corner_radius=0,  border_width=0, border_color="green", fg_color="white")

            def show_complain_record():
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #fetch the detail of complain
                    cur.execute("select subject, message, reply from complain c, student s where s.srno = c.rollno and s.email = %s and concat(s.first_name,'@',s.student_id) = %s",(student_username, student_password))

                    complain_record = cur.fetchall()

                    #===showing the data in treeview=====#
                    self.count = 0
                    for fetch_record in complain_record:
                        if self.count %2 == 0:
                            self.complain_tree.insert(parent = "", index = tk.END, iid = self.count, values=(fetch_record[0], fetch_record[1], fetch_record[2]), tags=("evenrow",))
                        else:
                            self.complain_tree.insert(parent = "", index = tk.END, iid = self.count, values=(fetch_record[0], fetch_record[1], fetch_record[2]), tags=("oddrow",))
                        self.count += 1

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

            #=======treeview setting========#
            #add some style
            style = ttk.Style()

            #pick a theme
            style.theme_use("alt")

            #configure the tree view color
            style.configure("Treeview", 
                            background = "#EEF0E5",
                            rowheight = 25,
                            fieldbackground = "#F3FBF1", font = ("Verdana", 15))
                    
            style.configure("mystyle.Treeview", font=("Verdana", 15))

            #configure the selected color
            style.configure("Treeview", background = [("selected", "#2d6a4f")])

            #increse the font size of heading
            style.configure("Treeview.Heading", font=("Consolas", 18))

            self.data_frame = tk.Frame(self.complain_status_frame, bg = "lightgrey", borderwidth=0, relief="solid")
            self.data_frame.pack_propagate(False)
            self.data_frame.place(x = 80, y = 100 , height = 500, width = 1200)

            #create a scrollbar
            y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
            x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

            y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
            x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

            #create a treeview
            self.complain_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
            self.complain_tree.pack(fill = "both", expand= True)

            #configure the scrollbar
            x_scroll.config(command = self.complain_tree.xview)
            y_scroll.config(command = self.complain_tree.yview)

            #define our columns
            self.complain_tree["columns"] = ("About", "Message", "Status")

            #format column
            self.complain_tree.column("About", anchor="center", width = 200, minwidth=300)
            self.complain_tree.column("Message", anchor="center", width = 300, minwidth=400)
            self.complain_tree.column("Status", anchor="center", width = 100, minwidth = 100)
                    
            #create a heading
            self.complain_tree.heading("About", text = "About", anchor = "center")
            self.complain_tree.heading("Message", text = "Message", anchor = "center")
            self.complain_tree.heading("Status", text = "Status", anchor = "center")
                    
            #Create striped to our tages
            self.complain_tree.tag_configure("oddrow", background="white")
            self.complain_tree.tag_configure("evenrow", background="lightblue") 

            #=======calling the function==========#
            show_complain_record()

            self.complain_status_frame.place(x = 10, y = 150)

        #=======apply for leave button======#
        self.apply_complain_button = ctk.CTkButton(self.complain_page_frame, text = "Apply for Complain", width = 300, height = 45,font = ("Verdana Pro", 17), cursor = "hand2", command = student_complain_apply_frame, fg_color="#2d6a4f", text_color="white", hover_color="#40A578", corner_radius=2)
        self.apply_complain_button.place(x=10,y=80)

        #=======leave status report button======#
        self.complain_status_button = ctk.CTkButton(self.complain_page_frame, text = "Complain Status Report", width = 300, height = 45,font = ("Verdana Pro", 17), cursor = "hand2", command =  student_complain_status_frame, fg_color="#2d6a4f", text_color="white", hover_color="#40A578", corner_radius=2)
        self.complain_status_button.place(x=330,y=80)
            
        self.complain_page_frame.place(x = 0, y = 0)

    def attendance_frame(self):
        self.attendance_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        #=========calling the function====================#
        def show_attendance_student():
            month_name = month_var.get()

            if not month_name:
                messagebox.showerror("Error", "Please first select month.")
                return
            else:
                def show_attendance():
                    try:
                        con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                        #create a cursor instance
                        cur = con.cursor()

                        #fetch the detail of complain
                        select_query = "select attendance_date, attendance_status, concat(s.first_name,' ',s.last_name) as staff_name from attendance a, staff s, student st where a.staff_id = s.srno and st.srno = a.student_no and st.email = %s and concat(st.first_name,'@',st.student_id) = %s"
                        cur.execute(select_query, (student_username, student_password))

                        attendance_record = cur.fetchall()

                        #===convert the date into month==========#
                        month_list = []
                        for fetch_record in attendance_record:
                            fetch_date = fetch_record[0]
                            month = fetch_date.strftime("%B")
                            month_list.append(month)

                        #=======check the condition for selected month==========#
                        if month_list[0] != month_name:
                            messagebox.showinfo("Attendance Record", f"There is no attendance record for month '{month_list[0]}'")
                            return
                        else:
                            #===showing the data in treeview=====#
                            self.count = 0
                            for fetch_record in attendance_record:
                                if self.count %2 == 0:
                                    self.attendance_report_tree.insert(parent = "", index = tk.END, iid = self.count, values=(fetch_record[0], fetch_record[1], fetch_record[2]), tags=("evenrow",))
                                else:
                                    self.attendance_report_tree.insert(parent = "", index = tk.END, iid = self.count, values=(fetch_record[0], fetch_record[1], fetch_record[2]), tags=("oddrow",))
                                self.count += 1

                        #commit the changes
                        con.commit()

                        #close the connection
                        con.close()

                    except Exception as e:
                        print("Error ", e)
                

                #add some style
                style = ttk.Style()

                #pick a theme
                style.theme_use("alt")

                #configure the tree view color
                style.configure("Treeview", 
                                background = "#55AD98",
                                rowheight = 25,
                                fieldbackground = "#F3FBF1", font = ("Verdana Pro", 14))
                        
                style.configure("mystyle.Treeview", font=('Verdana Pro', 15))
                

                #configure the selected color
                style.configure("mystyle.Treeview", background = [("selected", "#0D9276")])

                #increse the font size of heading
                style.configure("Treeview.Heading", font=("Consolas", 18))

                self.data_frame = tk.Frame(self.attendance_page_frame, bg = "lightgrey", borderwidth=0, relief="solid")
                self.data_frame.pack_propagate(False)
                self.data_frame.place(x = 50, y = 200 , height = 200, width = 1200)

                #create a scrollbar
                y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
                x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

                y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
                x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

                #create a treeview
                self.attendance_report_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
                self.attendance_report_tree.pack(fill = "both", expand= True)

                #configure the scrollbar
                x_scroll.config(command = self.attendance_report_tree.xview)
                y_scroll.config(command = self.attendance_report_tree.yview)

                #define our columns
                self.attendance_report_tree["columns"] = ("Attendance Date", "Attendance Status", "By Staff")

                #format column
                self.attendance_report_tree.column("Attendance Date", anchor="center", width = 200, minwidth=200)
                self.attendance_report_tree.column("Attendance Status", anchor="center", width = 200, minwidth=200)
                self.attendance_report_tree.column("By Staff", anchor="center", width = 100, minwidth = 100)
                        
                #create a heading
                self.attendance_report_tree.heading("Attendance Date", text = "Attendance Date", anchor = "center")
                self.attendance_report_tree.heading("Attendance Status", text = "Attendance Status", anchor = "center")
                self.attendance_report_tree.heading("By Staff", text = "By Staff", anchor = "center")
                        
                #Create striped to our tages
                self.attendance_report_tree.tag_configure("oddrow", background="white")
                self.attendance_report_tree.tag_configure("evenrow", background="#9DDE8B") 

                show_attendance()
        #===========================================#
        ChangeLabel(self.attendance_page_frame, text = "View Attendance", fg_color="#2d6a4f", text_color="white")

        #======select month label=====#
        self.month_label = ctk.CTkLabel(self.attendance_page_frame, text = "Select Month:", font = ("Verdana", 18), text_color="green")
        self.month_label.place(x = 70, y = 70)

        #==========Drop down menu===========#
        self.select_month_values=["January","February","March","April","May","June","July","August","September","October","November","December"]
        month_var = tk.StringVar(value = "")
        self.select_month_option=ctk.CTkOptionMenu(self.attendance_page_frame,width=200,height=30,corner_radius=2,values=self.select_month_values,fg_color="#D8D9DA",text_color="black",dropdown_font=("Verdana Pro", 15),font=("Verdana Pro", 18), variable=month_var, button_color="#9DDE8B", button_hover_color="#9DDE8B")
        self.select_month_option.place(x=230,y=70)

        #=====Report buttons=====#
        self.report_button = ctk.CTkButton(self.attendance_page_frame, text = "Report", width = 150, height = 38,font = ("Verdana Pro", 17), cursor = "hand2", command = show_attendance_student, fg_color="#2d6a4f", text_color="white", hover_color="#40A578", corner_radius=2)
        self.report_button.place(x = 460, y = 68)

        self.attendance_page_frame.place(x = 0, y = 0)
    
    def feedback_frame(self):
        self.feedback_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")

        ChangeLabel(self.feedback_page_frame, text = "Feedback", fg_color="#2d6a4f", text_color="white")

        def save_feedback_response():
            choice_0_answer = self.first1_var.get()
            choice_1_answer = self.first2_var.get()
            choice_2_answer = self.first3_var.get()
            other_feedback0 = self.feedback_textbox1.get("0.0", tk.END)
            other_feedback1 = self.feedback_textbox2.get("0.0", tk.END)
            other_feedback2 = self.feedback_textbox3.get("0.0", tk.END)

            #=======insert feedback into database============#
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                cur.execute("select student_id from feedback where student_id = %s group by student_id", (student_srno[0],))
                submitted = cur.fetchall()

                if submitted:
                    messagebox.showerror("Error", "Feedback already submitted. Thank you!")
                
                else:
                    insert_query = "insert into feedback(student_id, question_id, answer_choices, brief_answer_text) values(%s, %s, %s, %s)"
                    insert_values = [(student_srno[0], question_id_list[0], choice_0_answer, other_feedback0),(student_srno[0], question_id_list[1], choice_1_answer, other_feedback1),(student_srno[0], question_id_list[2], choice_2_answer, other_feedback2 )]

                    cur.executemany(insert_query, insert_values)

                    #commit the changes
                    con.commit()

                    messagebox.showinfo("Success", "Thank you for your feedback!")

                #close the connection
                con.close()

                #=====clear the textbox============#
                self.first1_var.set(value = "")
                self.first2_var.set(value = "")
                self.first3_var.set(value = "")
                self.feedback_textbox1.delete("0.0", tk.END)
                self.feedback_textbox2.delete("0.0", tk.END)
                self.feedback_textbox3.delete("0.0", tk.END)

            except Exception as e:
                print("Error ", e)

        def question_frame(frame, question1, choice1, choice2, choice3, choice4, choice_var):
            global feedback_textbox
            please_label = ctk.CTkLabel(frame, text = "Please help us to serve you better by taking a couple of minutes", text_color="white", font = ("Verdana Pro", 18))
            please_label.place(x = 25, y = 20)

            question1_label = ctk.CTkLabel(frame, text = f"{question1}", text_color="#5DEBD7", font = ("Verdana Pro", 18))
            question1_label.place(x = 25, y = 60)

            choice1=ctk.CTkRadioButton(frame, text=choice1 ,value="choice1",variable = choice_var,font=("Verdana Pro", 16), fg_color="white", hover_color="yellow", text_color="white", border_color="white")
            choice1.place(x = 50, y = 100)

            choice2=ctk.CTkRadioButton(frame, text=choice2 ,value="choice2",variable = choice_var,font=("Verdana Pro", 16), fg_color="white", hover_color="yellow", text_color="white", border_color="white")
            choice2.place(x = 50, y = 140)

            choice3=ctk.CTkRadioButton(frame, text=choice3 ,value="choice3",variable = choice_var,font=("Verdana Pro", 16), fg_color="white", hover_color="yellow", text_color="white", border_color="white")
            choice3.place(x = 50, y = 180)

            choice4=ctk.CTkRadioButton(frame, text=choice4 ,value="choice4",variable = choice_var,font=("Verdana Pro", 16), fg_color="white", hover_color="yellow", text_color="white", border_color="white")
            choice4.place(x = 50, y = 220)

            specific_feedback = "If you have specific feedback please write to us."
            specific_feedback_label = ctk.CTkLabel(frame, text = specific_feedback, text_color="#5DEBD7", font = ("Verdana Pro", 18))
            specific_feedback_label.place(x = 25, y = 260)

        #=========fetch feedback from databass============#
        try:
            con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

            #create a cursor instance
            cur = con.cursor()

            #=====fetch feedback question and option=============#
            cur.execute("select * from feedback_question limit 3")

            feedback_record = cur.fetchall()

            question_id_list = []
            question_list= []
            option1_list= [] 
            option2_list= [] 
            option3_list= [] 
            option4_list= []
            for feedback in feedback_record:
                question_id_list.append(feedback[0])
                question_list.append(feedback[1])
                option1_list.append(feedback[2])
                option2_list.append(feedback[3])
                option3_list.append(feedback[4])
                option4_list.append(feedback[5])

            # #=========fetch student srno============#
            cur.execute("select srno from student where email = %s", (student_username,))

            student_srno = cur.fetchone()
        
            #commit the changes
            con.commit()

            #close the connection
            con.close()

        except Exception as e:
            print("Error ", e)

        #==========first frame===========#
        self.first_frame = ctk.CTkFrame(self.feedback_page_frame, width = 700, height=550, corner_radius=0,  border_width=1, border_color="green", fg_color="#36454F")

        self.first1_var = tk.StringVar(value = "")
        question_frame(frame = self.first_frame, question1=question_list[0], choice1=option1_list[0], choice2=option2_list[0], choice3 = option3_list[0], choice4 = option4_list[0], choice_var=self.first1_var)

        self.feedback_textbox1 = ctk.CTkTextbox(self.first_frame, width = 650, height = 130, corner_radius=4, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2, wrap = "word")
        self.feedback_textbox1.place(x = 25, y = 300)

        self.page1_page2_btn = ctk.CTkButton(self.first_frame, text = "NEXT", width = 100, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#272829", corner_radius=4, hover_color=None, border_width=2, border_color="white", cursor = "hand2", command= lambda : self.second_frame.tkraise())
        self.page1_page2_btn.place(x = 575, y = 460)

        self.first_frame.place(x = 200, y = 100)
        #================================#

        #==========second frame=========#
        self.second_frame = ctk.CTkFrame(self.feedback_page_frame, width = 700, height=550, corner_radius=0,  border_width=1, border_color="green", fg_color="#36454F")

        self.first2_var = tk.StringVar(value = "")
        question_frame(frame = self.second_frame, question1=question_list[1], choice1=option1_list[1], choice2=option2_list[1], choice3 = option3_list[1], choice4 = option4_list[1], choice_var=self.first2_var)

        self.feedback_textbox2 = ctk.CTkTextbox(self.second_frame, width = 650, height = 130, corner_radius=4, font = ("Verdana Pro", 15), border_color="white", text_color="white", fg_color="#272829", border_width=2, wrap = "word")
        self.feedback_textbox2.place(x = 25, y = 300)

        self.page2_page1_btn = ctk.CTkButton(self.second_frame, text = "PREVIOUS", width = 120, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#272829", corner_radius=4, hover_color=None, border_width=2, border_color="white", cursor = "hand2", command= lambda : self.first_frame.tkraise())
        self.page2_page1_btn.place(x = 20, y = 460)
  
        self.page2_page3_btn = ctk.CTkButton(self.second_frame, text = "NEXT", width = 100, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#272829", corner_radius=4, hover_color=None, border_width=2, border_color="white", cursor = "hand2", command= lambda : self.third_frame.tkraise())
        self.page2_page3_btn.place(x = 575, y = 460)

        self.second_frame.place(x = 200, y = 100)
        #================================#

        #==========third frame=========#
        self.third_frame = ctk.CTkFrame(self.feedback_page_frame, width = 700, height=550, corner_radius=0,  border_width=1, border_color="green", fg_color="#36454F")

        self.first3_var = tk.StringVar(value = "")
        question_frame(frame = self.third_frame, question1=question_list[2], choice1=option1_list[2], choice2=option2_list[2], choice3 = option3_list[2], choice4 = option4_list[2], choice_var=self.first3_var)

        self.feedback_textbox3 = ctk.CTkTextbox(self.third_frame, width = 650, height = 130, corner_radius=4, font = ("Verdana Pro", 18), border_color="white", text_color="white", fg_color="#272829", border_width=2, wrap = "word")
        self.feedback_textbox3.place(x = 25, y = 300)

        self.page3_page2_btn = ctk.CTkButton(self.third_frame, text = "PREVIOUS", width = 120, height = 40, font = ("Verdana Pro", 15), text_color="white", fg_color="#272829", corner_radius=4, hover_color=None, border_width=2, border_color="white", cursor = "hand2", command= lambda : self.second_frame.tkraise())
        self.page3_page2_btn.place(x = 20, y = 460)

        self.submit_btn = ctk.CTkButton(self.third_frame, text = "SUBMIT", width = 100, height = 40, font = ("Verdana Pro", 18), text_color="white", fg_color="#272829", corner_radius=4, hover_color=None, border_width=2, border_color="white", cursor = "hand2", command= save_feedback_response)
        self.submit_btn.place(x = 575, y = 460)

        self.third_frame.place(x = 200, y = 100)
        #================================#

        #==========raise first frame=======#
        self.first_frame.tkraise()

        self.feedback_page_frame.place(x = 0, y = 0)

    def view_result_frame(self):
        self.result_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.result_page_frame, text = "View Result", fg_color="#2d6a4f", text_color="white")

        # show semester selection dropdown menu
        def student_detail():
            global subject_code_list, subject_name_list, std_name

            student_detail_frame = ctk.CTkFrame(self.result_page_frame, width = 1035, height=100, corner_radius=2,  border_width=0, fg_color="#F6F5F5")

            term = self.term_var.get()

            # fetch student records
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                cur.execute("select Upper(concat(first_name,' ',father_name,' ',last_name)), s.student_id, upper(e.exam_type), std_name from exam_result e, student s where e.student_id = s.srno and concat(s.first_name,'@',s.student_id) = %s and exam_type = %s limit 1",(student_password,term))

                result = cur.fetchone()

                if result is None:
                    messagebox.showerror("Error", "There is no result record for this student.")
                    student_result_frame.destroy()
            
                std_name = result[3]
                
                if std_name == "5th std":
                    cur.execute("select * from subject where subject_name in (select * from std5th)")
                elif std_name == "6th std":
                    cur.execute("select * from subject where subject_name in (select * from std6th)")
                elif std_name == "7th std" or std_name == "8th std":
                    cur.execute("select * from subject where subject_name in (select * from std7th)")
                elif std_name == "9th std":
                    cur.execute("select * from subject where subject_name in (select * from std9th)")
                elif std_name == "10th std":
                    cur.execute("select * from subject where subject_name in (select * from std10th)")

                subject_record = cur.fetchall()

                subject_code_list = []
                subject_name_list = []
                for i in subject_record:
                    subject_code_list.append(i[0])
                    subject_name_list.append(i[1])

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

            student_name_label = ctk.CTkLabel(student_detail_frame, text = "Student Name :", font = ("Verdana Pro", 16), text_color="darkgreen")
            student_name_label.grid(row = 0, column = 0, pady = 2, padx = 5)

            student_name_text = ctk.CTkLabel(student_detail_frame, text = f"{result[0]}", font = ("Verdana Pro", 16), text_color="black")
            student_name_text.grid(row = 0, column = 1, pady = 2, padx = 5, sticky = "nw")

            student_rollno_label = ctk.CTkLabel(student_detail_frame, text = "Student Rollno :", font = ("Verdana Pro", 16), text_color="darkgreen")
            student_rollno_label.grid(row = 1, column = 0, pady = 2, padx = 5)

            student_rollno_text = ctk.CTkLabel(student_detail_frame, text = f"{result[1]}", font = ("Verdana Pro", 16), text_color="black")
            student_rollno_text.grid(row = 1, column = 1, pady = 2, padx = 5, sticky = "nw")

            exam_type_label = ctk.CTkLabel(student_detail_frame, text = "Term/Semester :", font = ("Verdana Pro", 16), text_color="darkgreen")
            exam_type_label.grid(row = 2, column = 0, pady = 2, padx = 5)

            student_exam_text = ctk.CTkLabel(student_detail_frame, text = f"{result[2]}", font = ("Verdana Pro", 16), text_color="black")
            student_exam_text.grid(row = 2, column = 1, pady = 2, padx = 5, sticky = "nw")
            
            student_detail_frame.place(x = 25, y = 110)
            student_detail_frame.grid_propagate(False)

        def show_result():
            global student_result_frame, status
            student_detail()

            #exam result frame
            student_result_frame = ctk.CTkFrame(self.result_page_frame, corner_radius=2,  border_width=0, fg_color="#F6F5F5", width = 1000, height = 600)
            
            if std_name in ("5th std", "6th std", "7th std", "8th std"):
                column_list = ["SUB CODE", "SUBJECT", "GRADE"]
            else:
                column_list = ["SUB CODE", "SUBJECT", "MARKS"]

            column_widths = {
                "SUB CODE":200,
                "SUBJECT":350,
                "GRADE":200,
                "MARKS":200
            }

            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                cur.execute("select srno from student where concat(first_name,'@',student_id) = %s", (student_password,))
                student_srno = cur.fetchone()
 
                if std_name == "5th std":
                    cur.execute("select English, Hindi, Marathi, Mathematics, EVS_I, EVS_II, status from exam_result where student_id = %s", (student_srno[0],))
                elif std_name == "6th std":
                    cur.execute("select English, Hindi, Marathi, Mathematics, EVS, History_Civics, Geography,status  from exam_result where student_id = %s", (student_srno[0],))
                elif std_name == "7th std" or std_name == "8th std":
                    cur.execute("select English, Hindi, Marathi, Mathematics, History_Civics, Geography, General_Science,status from exam_result where student_id = %s", (student_srno[0],))
                elif std_name == "9th std":
                    cur.execute("select English, Hindi, Marathi, Geography, History_Political_Science , Mathematics_Part_I, Mathematics_Part_II ,Science_technology,status from exam_result where student_id = %s", (student_srno[0],))
                elif std_name == "10th std":
                    cur.execute("select English, Hindi, Marathi, Geography, History_Political_Science , Mathematics_Part_I, Mathematics_Part_II ,Science_technology_Part_I, Science_technology_Part_II,status from exam_result where student_id = %s", (student_srno[0],))
                
                results = cur.fetchone()

                all_list = []
                grade_tuple = results
                status = grade_tuple[-1]

                grades = []
                marks = []
                for j in grade_tuple:
                    if j!='PASS':
                        grade, mark = j.split("/")
                        all_list.append(j)
                        grades.append(grade)
                        marks.append(mark)
                print(grades)
                print(marks)

                if std_name in ("9th std", "10th std"):
                    cur.execute("select Overall_percentage from exam_result where student_id = %s", (student_srno[0],))
                    average_mark = cur.fetchone()

                con.close()

            except Exception as e:
                print("Error :", e)

            for i, col in enumerate(column_list):
                col_var = tk.StringVar(value = col)
                width = column_widths.get(col, 150)
                column_entry = ctk.CTkEntry(student_result_frame, width = width, height = 45, font = ("Verdana Pro", 17), corner_radius=0, fg_color="#4B70F5", text_color="white", textvariable=col_var,state="readonly",justify = "center")
                column_entry.grid(row = 0, column = i)

            for i, code in enumerate(subject_code_list):
                code_var = tk.StringVar(value = code)
                width = column_widths.get(col,150)
                code_entry = ctk.CTkEntry(student_result_frame, width = 200, height = 40, font = ("Verdana Pro", 17), corner_radius=0, fg_color="#F6F5F5", text_color="black", textvariable=code_var,state="readonly",justify = "center")
                code_entry.grid(row = i+1, column = 0)

            for i, subject in enumerate(subject_name_list):
                subject_var = tk.StringVar(value = subject)
                width = column_widths.get(subject,150)
                subject_entry = ctk.CTkEntry(student_result_frame, width = 350, height = 40, font = ("Verdana Pro", 17), corner_radius=0, fg_color="#F6F5F5", text_color="black", textvariable=subject_var,state="readonly")
                subject_entry.grid(row = i+1, column = 1)

            if std_name in ("5th std", "6th std", "7th std", "8th std"):
                for i, gm in enumerate(grades):
                    grade_marks_var = tk.StringVar(value = gm)
                    width = column_widths.get(col,150)
                    grade_marks_entry = ctk.CTkEntry(student_result_frame, width = 200, height = 40, font = ("Verdana Pro", 17), corner_radius=0, fg_color="#F6F5F5", text_color="black", textvariable=grade_marks_var,state="readonly",justify = "center")
                    grade_marks_entry.grid(row = i+1, column = 2)
            else:
                for i, gm in enumerate(marks):
                    grade_marks_var = tk.StringVar(value = gm)
                    width = column_widths.get(col,150)
                    grade_marks_entry = ctk.CTkEntry(student_result_frame, width = 200, height = 40, font = ("Verdana Pro", 17), corner_radius=0, fg_color="#F6F5F5", text_color="black", textvariable=grade_marks_var,state="readonly",justify = "center")
                    grade_marks_entry.grid(row = i+1, column = 2)

            status_var = tk.StringVar(value = status)
            status_entry = ctk.CTkEntry(student_result_frame, width = 200, height = 40, font = ("Verdana Pro", 17), corner_radius=0, fg_color="#06D001", text_color="black", textvariable=status_var,state="readonly",justify = "center")
            status_entry.grid(row = len(subject_name_list)+1, column = 2)

            result_var = tk.StringVar(value = "RESULT")
            result_entry = ctk.CTkEntry(student_result_frame, width = 200, height = 40, font = ("Verdana Pro", 17), corner_radius=0, fg_color="#4B70F5", text_color="white", textvariable=result_var,state="readonly",justify = "center")
            result_entry.grid(row = len(subject_name_list)+1, column = 0)

            if std_name in ("9th std", "10th std"):
                avg_status_var = tk.StringVar(value = f"AVERAGE = {average_mark[0]}")
                avg_status_entry = ctk.CTkEntry(student_result_frame, width = 350, height = 40, font = ("Verdana Pro", 17), corner_radius=0, fg_color="#4B70F5", text_color="white", textvariable=avg_status_var,state="readonly",justify = "center")
                avg_status_entry.grid(row = len(subject_name_list)+1, column = 1)

            if status == "PASS":
                status_entry.configure(fg_color = "#06D001")
            elif status == "FAIL":
                status_entry.configure(fg_color = "red", text_color = "white")

            student_result_frame.place(x = 25, y = 230)

        #====select term =============#
        self.term_label = ctk.CTkLabel(self.result_page_frame, text = "Select Semester :", font = ("Verdana Pro", 18), text_color="darkgreen")
        self.term_label.place(x = 25, y = 60)

        self.choose_term_values = ["Semester-I", "Semester-II"]
        self.term_var = tk.StringVar(value = "")
        self.choose_term_option=ctk.CTkOptionMenu(self.result_page_frame,width=200,height=30,corner_radius=2,values=self.choose_term_values,fg_color="#D8D9DA",text_color="black",dropdown_font=("Verdana Pro", 15),font=("Verdana Pro", 18), button_color="green", button_hover_color="#9DDE8B", variable=self.term_var)
        self.choose_term_option.place(x = 210, y = 60)

        # result image
        self.result_paper_image = SetImage(image_path="image/exam-result.png", width = 25, height=25)

        # get result button
        self.get_result_btn = ctk.CTkButton(self.result_page_frame, text = "Get Result", width = 150, height = 38,font = ("Verdana Pro", 17), cursor = "hand2", command = show_result, fg_color="#2d6a4f", text_color="white", hover_color="#40A578", corner_radius=2, image = self.result_paper_image)
        self.get_result_btn.place(x = 430, y = 60)

        self.result_page_frame.place(x = 0, y = 0)
        self.result_page_frame.pack_propagate(False)

    def view_notes_frame(self):
        self.notes_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.notes_page_frame, text = "View Notes", fg_color="#2d6a4f", text_color="white")

        self.see_notes_frame = ctk.CTkFrame(self.notes_page_frame, width = 1072, height=585, corner_radius=0,  border_width=0, border_color="green", fg_color="white")

        # view notes table
        table_frame = ctk.CTkScrollableFrame(self.see_notes_frame, width = 1000, height = 500, corner_radius=0, border_width=2, border_color="black")
        table_frame.pack(pady = 50)

        # fetch all values of uploaded notes
        def fetch_notes():
            global results
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                # create a cursor instance
                cur = con.cursor()

                cur.execute("select n.file_name, date(n.upload_date), n.file_path, s.first_name,s.gender from notes n, staff s, division d where n.teacher_id = s.srno and n.std_div_id = d.div_id and d.std_name = (select std_name from student stu where concat(stu.first_name,'@',stu.student_id) = %s)  and d.div_name = (select div_name from student stu where concat(stu.first_name,'@',stu.student_id) = %s)", (student_password, student_password))

                results = cur.fetchall()

                if results:
                    self.see_notes_frame.place(x = 10, y = 105)
                    self.see_notes_frame.pack_propagate(False)
                    return
                else:
                    message_label = ctk.CTkLabel(self.notes_page_frame, text = "No notes available at the moment.", font = ("Verdana Pro", 18), text_color = "black")
                    message_label.place(x = 100, y = 500)

                #close the connection
                con.close()

            except Exception as e:
                print("Error :", e)

        # call the function
        fetch_notes()

        column_widths = {
                "TITLE":300,
                "DATE UPLOADED": 250,
                "UPLOADED BY":245,
                "ACTION":200  
            }
        
        title_list = []
        date_list = []
        mam_list = []
        path_list = []
        gen_list = []
        for i in results:
            title_list.append(i[0])
            date_list.append(i[1])
            path_list.append(i[2])
            mam_list.append(i[3])
            gen_list.append(i[4])

        def open_file_in_browser(name):
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                # create a cursor instance
                cur = con.cursor()

                cur.execute("select file_path from notes n where n.file_name = %s", (name,))

                results = cur.fetchone()
                    
                #close the connection
                con.close()

            except Exception as e:
                print("Error :", e)

            fetched_path = results[0]

            # convert path to url formats
            file_url = "file://" + os.path.abspath(fetched_path)

            # open the file in browser
            webbrowser.open_new(file_url)

        column_list = ["TITLE", "DATE UPLOADED", "UPLOADED BY","ACTION" ]
        for i, col in enumerate(column_list):
            column_var = tk.StringVar(value = col)
            width = column_widths.get(col, 150)
            column_box = ctk.CTkEntry(table_frame, font = ("Helvetica", 17), border_width=1,border_color = "black", width = width, height = 40, textvariable=column_var,corner_radius=0, justify = "center", state = "readonly", fg_color="#176B87",text_color="white")
            column_box.grid(row = 0, column = i)

        for i, name_file in enumerate(title_list):
            type_var = tk.StringVar(value = name_file)
            type_box = ctk.CTkEntry(table_frame, font = ("Helvetica", 17), border_width=1,border_color = "black", width =300, height = 42, textvariable=type_var,corner_radius=0, state = "readonly", fg_color="#F6F5F5", text_color="black", justify = "center")
            type_box.grid(row = i+1, column = 0)

        for i, date_file in enumerate(date_list):
            date_var = tk.StringVar(value = date_file)
            date_box = ctk.CTkEntry(table_frame, font = ("Helvetica", 17), border_width=1,border_color = "black", width =250, height = 42, textvariable=date_var,corner_radius=0, state = "readonly", fg_color="#F6F5F5", text_color="black", justify = "center")
            date_box.grid(row = i+1, column = 1)

        for i, mam_file in enumerate(mam_list):
            teacher_title = "Prof." if gen_list[i] == "Male" else "Prof. (Ms./Mrs.)"
            mam_var = tk.StringVar(value = f"{teacher_title}{mam_file}")
            mam_box = ctk.CTkEntry(table_frame, font = ("Helvetica", 17), border_width=1,border_color = "black", width =245, height = 42, textvariable=mam_var,corner_radius=0, state = "readonly", fg_color="#F6F5F5", text_color="black", justify = "center")
            mam_box.grid(row = i+1, column = 2)

        open_link_image = ctk.CTkImage(light_image=Image.open("image/external-link.png"),dark_image=Image.open("image/external-link.png"), size = (20, 20))
        for i, name in enumerate(title_list):
            action_box = ctk.CTkButton(table_frame, font = ("Helvetica", 17), width = 200, height = 42, text = "Open file", corner_radius=0, fg_color="black", text_color = "white", hover = tk.DISABLED, command = lambda n = name: open_file_in_browser(n), image=open_link_image, cursor = "hand2")
            action_box.grid(row = i+1, column = 3)
            
        self.notes_page_frame.place(x = 0, y = 0)

class TeacherHomeWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__(fg_color="white")
        self.geometry("1536x864-10-7")
        self.title("School Management System")
        self.after(200, lambda : self.iconbitmap("image/slogo.ico"))

        #=======switch frame========#
        def switch_frame(page, indicator_button):
            for frame in self.rightside_frame.winfo_children():
                frame.destroy()
                self.update()
            page()

            for child in self.teacher_sidebar_frame.winfo_children():
                if isinstance(child, ctk.CTkButton):
                    child.configure(fg_color = "#912BBC")

            indicator_button.configure(fg_color= "#6D0C74")
        
        #=====return to main window=======#
        def confirm_exit():
            answer = messagebox.askquestion("Confirm Exit", "Are you sure you want to exit?")
            if answer == "yes":
                self.destroy()
                root.deiconify()

        #====calling heading label====#
        self.heading_frame=HeadingFrame(self)
        self.heading_frame.place(x=5,y=5)

        #=====teacher home frame=====#
        self.teacher_homepage_frame=ctk.CTkFrame(self,border_color="green",border_width=1,fg_color="#D8D9DA",width=1526,height=730,corner_radius=1)

        #======teacher sidebar frame=====#
        self.teacher_sidebar_frame=ctk.CTkFrame(self.teacher_homepage_frame,border_color="green",border_width=0,width=350,height=700, corner_radius=0,fg_color="#912BBC")

        #====heading label====#
        self.sidebar_head_label=ctk.CTkLabel(self.teacher_sidebar_frame,text="",width=348,height=5,fg_color="#6D0C74")
        self.sidebar_head_label.place(x=0,y=0)

        #=======photo frame======#
        self.teacher_photo_frame = ctk.CTkFrame(self.teacher_sidebar_frame, width = 150, height=160, corner_radius=0,  border_width=2, border_color="black", fg_color="#912BBC")
        self.teacher_photo_frame.place(x=100,y=30)

        self.teacher_photo_label = ctk.CTkLabel(self.teacher_photo_frame, text = "", fg_color="#912BBC", width = 149, height=159)
        self.teacher_photo_label.place(x = 0, y = 0)

        self.teacher_greet_label = ctk.CTkLabel(self.teacher_sidebar_frame, text = "", font=("Verdana Pro", 18), text_color="white")
        self.teacher_greet_label.place(x = 100, y = 200)

        #======Sidebar menu=======#
        def create_button(frame, text, image_path, image_width, image_height, width, height, command, y_position, fg_color = "#912BBC"):
            button_text = f"       {text.ljust(22)}"  # Adjust text padding for alignment
            image = SetImage(image_path=image_path, width=image_width, height=image_height)

            button = ctk.CTkButton(
                frame,
                text=button_text,
                width=width,
                height=height,
                font=("Verdana Pro", 18),
                text_color="white",
                fg_color="#912BBC",
                corner_radius=50,
                hover_color="#6D0C74",
                cursor="hand2",
                command=command,
                image=image,
                compound="left",
                anchor="w"  # Left-align text and image
            )
            button.place(x=24, y=y_position)
            return button

        # Create buttons with consistent image sizes and aligned text
        self.profile_button = create_button(
            self.teacher_sidebar_frame, 
            "My Profile", 
            "image/user.png", 
            20, 20, 
            300, 42, 
            lambda: switch_frame(page=self.profile_frame, indicator_button=self.profile_button), 
            245,
            "#6D0C74"
        )

        self.result_student_button = create_button(
            self.teacher_sidebar_frame, 
            "Result", 
            "image/result_icon.png", 
            20, 20, 
            300, 42, 
            lambda: switch_frame(page=self.result_student_frame, indicator_button=self.result_student_button), 
            289,
            "#912BBC"
        )

        self.student_notes_button = create_button(
            self.teacher_sidebar_frame, 
            "Notes", 
            "image/upload_notes.png", 
            23, 23, 
            300, 42, 
            lambda: switch_frame(page=self.student_notes_frame, indicator_button=self.student_notes_button), 
            333,
            "#912BBC"
        )

        self.student_report_button = create_button(
            self.teacher_sidebar_frame, 
            "Student Report", 
            "image/self-growth.png", 
            20, 20, 
            300, 42, 
            lambda: switch_frame(page=self.student_report_frame, indicator_button=self.student_report_button), 
            377,
            "#912BBC"
        )

        self.student_attendance_button = create_button(
            self.teacher_sidebar_frame, 
            "Attendance", 
            "image/attendance.png", 
            20, 20, 
            300, 42, 
            lambda: switch_frame(page=self.student_attendance_frame, indicator_button=self.student_attendance_button), 
            421,
            "#912BBC"
        )

        self.student_attendance_report_button = create_button(
            self.teacher_sidebar_frame, 
            "Attendance Report", 
            "image/view-attendance.png", 
            20, 20, 
            300, 42, 
            lambda: switch_frame(page=self.student_attendance_report_frame, indicator_button=self.student_attendance_report_button), 
            465,
            "#912BBC"
        )

        self.student_advance_report_button = create_button(
            self.teacher_sidebar_frame, 
            "Advance Reports", 
            "image/self-growth.png", 
            20, 20, 
            300, 42, 
            lambda: switch_frame(page=self.advance_report_frame, indicator_button=self.student_advance_report_button), 
            509,
            "#912BBC"
        )

        self.student_complain_button = create_button(
            self.teacher_sidebar_frame, 
            "Complain", 
            "image/complain_icon.png", 
            23, 23, 
            300, 42, 
            lambda: switch_frame(page=self.student_complain_frame, indicator_button=self.student_complain_button), 
            553,
            "#912BBC"
        )

        self.student_leave_button = create_button(
            self.teacher_sidebar_frame, 
            "Leave", 
            "image/leave_icon.png", 
            23, 23, 
            300, 42, 
            lambda: switch_frame(page=self.student_leave_frame, indicator_button=self.student_leave_button), 
            597,
            "#912BBC"
        )

        self.student_logout_button = create_button(
            self.teacher_sidebar_frame, 
            "Logout", 
            "image/logout_icon.png", 
            20, 20, 
            300, 42, 
            confirm_exit, 
            641,
            "#912BBC"
        )

        self.teacher_sidebar_frame.place(x=30,y=10)

        #=======rightside=====#
        self.rightside_frame=ctk.CTkFrame(self.teacher_homepage_frame,width=1092,height=700,corner_radius=0,border_width=0,fg_color="white")
        self.rightside_frame.place(x=400,y=10)

        self.teacher_homepage_frame.place(x=5,y=100)

    def profile_frame(self):
        self.profile_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.profile_page_frame,text="My Profile", fg_color="#912BBC", text_color="white")

        def show_profile():
            global path, imageo
            #=======fetch login email and password=============@
            teacher_email = teacher_username
            password = teacher_password 
            #===================================================#
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #execute the cursor query
                select_query = "select concat(first_name,' ', last_name) as name , d.std_name,d.div_name, email, mobile, address, city, pincode, image_path, first_name from staff, class_teachers ct, division d where staff.srno = ct.srno and d.div_id = ct.div_id and email = %s and concat(first_name,'@',staff_id) = %s"

                select_value = (teacher_email, password)
                cur.execute(select_query,select_value )

                records = cur.fetchone()

                # show this detail in entry box
                self.name_entry.configure(text = records[0])
                self.standard_division_entry.configure(text = f"{records[1][0:3]} / {records[2]}")
                self.email_entry.insert(tk.END, records[3])
                self.contact_entry.insert(tk.END, records[4])
                self.address_entry.insert(tk.END, records[5])
                self.city_entry.insert(tk.END, records[6])
                self.pincode_entry.insert(tk.END, records[7])

                image_path = records[8]

                #open the image
                try:
                    image = Image.open(image_path)
                except FileNotFoundError:
                    print(f"Error: Could not find image at path: {image_path}")

                #base name of the image
                image_file_name = os.path.basename(image_path)

                #save the image
                image.save(image_file_name)
                
                #open image in form of ctk.CTkImage
                imageo = ctk.CTkImage(light_image=image, dark_image=image, size = (146, 166))

                #configure the left side frame label
                self.teacher_photo_label.configure(image = imageo)
                self.teacher_photo_label.image = imageo
                
                #configure the image welcome label
                self.teacher_greet_label.configure(text = f"Welcome {records[9]}")

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        def update_photo():
            global changed_image_path
            changed_image_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("JPG Files", ".jpg"),("PNG Files", ".png"),("All files", ".")], initialdir="C:/Users/vikas/OneDrive/Documents/software project/image", title="Open File")

            try:
                image = Image.open(changed_image_path)

            except FileNotFoundError:
                print(f"Error: Could not find image at path: {changed_image_path}")

            #====configure the image===========#
                
            #base name of the image
            image_file_name = os.path.basename(changed_image_path)

            #save the image
            image.save(image_file_name)
                
            #open image in form of ctk.CTkImage
            imageo = ctk.CTkImage(light_image=image, dark_image=image, size = (146, 166))

            #configure the right side frame label
            self.photo_button.configure(image = imageo)
            self.photo_button.image = imageo

            self.upload_photo_label.configure(text = f"{image_file_name}", wraplength = 100)

            #configure the left side frame label
            self.teacher_photo_label.configure(image = imageo)
            self.teacher_photo_label.image = imageo
                
        def add_photo_database():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #update the image_path
                update_query = "update staff set image_path = %s where email = %s"
                update_value = (changed_image_path, self.email_entry.get())

                cur.execute(update_query, update_value)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #============fetch id card============#
        def view_id_card():
            id_card_window = ctk.CTkToplevel(fg_color="white")
            id_card_window.resizable(False, False)
            id_card_window.geometry("600x500+800+250")
            id_card_window.title("School Management System")

            #==========function==========#
            def show_id_card():
                teacher_email = teacher_username
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    cur.execute("select srno, first_name from staff where email = %s", (teacher_email,))

                    result = cur.fetchone()
                    return result

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

            #======card frame===========#
            self.teacher_card_frame = ctk.CTkFrame(id_card_window, border_width=2,border_color="#912BBC", fg_color="white", width = 580, height = 480, corner_radius=2)

            #======card label===========#
            self.head_label = ctk.CTkLabel(self.teacher_card_frame, text = "Identity Card",width = 580, height = 40, fg_color="#912BBC", text_color="white", font = ("Verdana Pro", 18))
            self.head_label.place(x = 0, y = 0)

            # #====ignore warnings===========#
            warnings.filterwarnings("ignore", category=UserWarning)

            #==========call the show id card function==============#
            results = show_id_card()
            # print(results)

            # #=====iid card image label==========#
            file_name = "C:/Users/vikas/OneDrive/Documents/software project/teacher_id"
            teacher_image = Image.open(f"{file_name}/{results[0]}_{results[1].lower()} id_card.png")

            id_card_image = ImageTk.PhotoImage(teacher_image)
            self.teacher_card_label = ctk.CTkLabel(self.teacher_card_frame, text = "", image = id_card_image)
            self.teacher_card_label.place(x = 170, y = 50)

            # #===========save button=============#
            def save_teacher_card():
                file_path = filedialog.askdirectory(initialdir="C:/Users/vikas/OneDrive/Documents/save id cards")

                if file_path:
                    if os.path.exists(f"{file_path}/{results[0]}_{results[1].lower()} id_card.png"):
                        error_message = f"The file '{file_path}/{results[0]}_{results[1].lower()} id_card.png' already exists."
                        messagebox.showinfo("File Exists", message=error_message)
                    else:
                        image_to_save = ImageTk.getimage(id_card_image) 
                        image_to_save.save(f"{file_path}/{results[0]}_{results[1].lower()} id_card.png")
                        success_message = f"The Teacher ID card for {results[1].lower()} has been saved successfully!"
                        messagebox.showinfo("Success", message=success_message)

            #=========button===============#
            self.save_image = SetImage(image_path="image/download.png", width = 20, height=20)
            self.save_button = ctk.CTkButton(self.teacher_card_frame, text = "Save", width = 120, height = 38, font = ("Verdana Pro", 18), cursor = "hand2", command =  save_teacher_card,fg_color="#912BBC", text_color="white", hover_color="#8D007B", image = self.save_image)
            self.save_button.place(x = 220, y = 400)

            self.teacher_card_frame.place(x = 10, y = 10)

            #=====calling the function==========#
            show_id_card()
            
            id_card_window.grab_set()

        #=======event for next focus of entry widgets=======#
        def on_return(event):
            event.widget.tk_focusNext().focus()
            return "break"
        
        #=======inside widget========#
        warnings.filterwarnings("ignore", category=UserWarning)

        self.name_label =  ctk.CTkLabel(self.profile_page_frame, text = "Name : ", text_color="#430A5D", font=("Verdana Pro", 18))
        self.name_label.place(x = 110, y = 80)

        self.name_entry =  ctk.CTkLabel(self.profile_page_frame, text = "", text_color="red", font=("Consolas", 18))
        self.name_entry.place(x = 190, y = 80)

        self.standard_division_label =  ctk.CTkLabel(self.profile_page_frame, text = "Std/Div :", text_color="#430A5D", font=("Verdana Pro", 18))
        self.standard_division_label.place(x = 93, y = 120)

        self.standard_division_entry =  ctk.CTkLabel(self.profile_page_frame, text = "", text_color="red", font=("Consolas", 18))
        self.standard_division_entry.place(x = 190, y = 120)

        self.email_label =  ctk.CTkLabel(self.profile_page_frame, text = "Email : ", text_color="#430A5D", font=("Verdana Pro", 18))
        self.email_label.place(x = 113, y = 160)

        self.email_entry = ctk.CTkEntry(self.profile_page_frame, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16) , fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.email_entry.place(x = 190, y = 160)
        FocusColor(entry = self.email_entry, border_color="#430A5D")

        self.contact_label =  ctk.CTkLabel(self.profile_page_frame, text = "Contact No : ", text_color="#430A5D", font=("Verdana Pro", 18))
        self.contact_label.place(x = 62, y = 200)

        self.contact_entry = ctk.CTkEntry(self.profile_page_frame, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16), fg_color = "#D8D9DA", text_color= "black",border_width=0)
        self.contact_entry.place(x = 190, y = 200)
        FocusColor(entry = self.contact_entry, border_color="#430A5D")

        self.address_label =  ctk.CTkLabel(self.profile_page_frame, text = "Address : ", text_color="#430A5D", font=("Verdana Pro", 18))
        self.address_label.place(x = 90, y = 240)

        self.address_entry = ctk.CTkTextbox(self.profile_page_frame,width=250, height = 60, corner_radius=2, font = ("Verdana Pro", 16), wrap = "word", fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.address_entry.place(x = 190, y = 240)
        FocusColor(entry = self.address_entry, border_color="#430A5D")

        self.city_label =  ctk.CTkLabel(self.profile_page_frame, text = "City : ", text_color="#430A5D", font=("Verdana Pro", 18))
        self.city_label.place(x = 123, y = 305)

        self.city_entry = ctk.CTkEntry(self.profile_page_frame, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 18),fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.city_entry.place(x = 190, y = 305)
        FocusColor(entry = self.city_entry, border_color="#430A5D")

        self.pincode_label =  ctk.CTkLabel(self.profile_page_frame, text = "Pincode : ", text_color="#430A5D", font=("Verdana Pro", 18))
        self.pincode_label.place(x = 90, y = 345)

        self.pincode_entry = ctk.CTkEntry(self.profile_page_frame, width = 250, height = 35, corner_radius=2, font = ("Verdana Pro", 16),fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.pincode_entry.place(x = 190, y = 345)
        FocusColor(entry = self.pincode_entry, border_color="#430A5D")

        self.update_image = SetImage(image_path="image/updated.png", width = 25, height=25)
        self.update_button = ctk.CTkButton(self.profile_page_frame, text = "Update", width = 170, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=None, image = self.update_image, fg_color="#912BBC", text_color="white", hover_color="#430A5D")
        self.update_button.place(x = 190, y = 390)

        self.id_card_image = SetImage(image_path="image/id-card.png", width = 25, height=25)
        self.view_id_button = ctk.CTkButton(self.profile_page_frame, text = "View ID Card", width = 170, height = 40,cursor = "hand2",font = ("Verdana Pro", 16), command=view_id_card, image = self.id_card_image, fg_color="#912BBC", text_color="white", hover_color="#430A5D")
        self.view_id_button.place(x = 190, y = 435)

        self.save_image = SetImage(image_path="image/add-image.png", width = 22, height=22)
        self.upload_photo_label = ctk.CTkLabel(self.profile_page_frame, text = "No file choosen", text_color="black", font=("Verdana Pro", 16))
        self.upload_photo_label.place(x = 905, y = 305)

        self.add_photo_button = ctk.CTkButton(self.profile_page_frame, text = "Add", width = 150, height = 38,font = ("Verdana Pro", 16), cursor = "hand2", command = add_photo_database, image = self.save_image, fg_color="#912BBC", text_color="white", hover_color="#430A5D")
        self.add_photo_button.place(x = 900, y = 260)

        self.updated_photo_frame = ctk.CTkFrame(self.profile_page_frame, width = 150, height=170, corner_radius=0,  border_width=2, border_color="black", fg_color="white")
        self.updated_photo_frame.place(x=900,y=80)

        self.photo_button = ctk.CTkButton(self.updated_photo_frame, text = "", fg_color="SystemButtonFace", hover_color= "SystemButtonFace", border_width=2, border_color="black", corner_radius=3, command = update_photo, width = 150, height = 170, image = "")
        self.photo_button.place(x = 0, y = 0)

        #==bind the all entry box for focus next=====#
        self.email_entry.bind("<Return>", on_return)
        self.contact_entry.bind("<Return>", on_return)
        self.address_entry.bind("<Return>", on_return)
        self.city_entry.bind("<Return>", on_return)
        self.pincode_entry.bind("<Return>", on_return)

        #=======calling the function========#
        show_profile()
        
        self.profile_page_frame.place(x=0,y=0)

    def std_div_select_func(self, parent):
    
        #=======fetch standard record ==========#
        def fetch_std_record():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #execute the cursor query
                cur.execute("select std_name from standard")

                records = cur.fetchall()

                std_list = []
                for record in records:
                    std_list.append(record[0])
                
                #======configure the option menu for standard values
                self.choose_division_values = std_list
                self.choose_standard_option.configure(values = self.choose_division_values)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)
        
        #=======fetch division record ==========#
        def fetch_div_record():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #execute the cursor query
                cur.execute("select div_name from division group by div_name")

                records = cur.fetchall()

                div_list = []
                for record in records:
                    div_list.append(record[0])
                
                #======configure the option menu for standard values
                self.choose_division_values= div_list
                self.choose_division_option.configure(values = self.choose_division_values)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)
        #=================================#

        self.choose_standard_label = ctk.CTkLabel(parent, text = "Select Standard :", font = ("Verdana Pro", 18), text_color="#430A5D")
        self.choose_standard_label.place(x = 30, y = 60)

        self.choose_standard_values = []
        self.std_value = tk.StringVar(value="")
        self.choose_standard_option = ctk.CTkOptionMenu(parent, width = 200, height = 30, corner_radius=2, values=self.choose_standard_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=self.std_value, button_color="#912BBC",button_hover_color="#912BBC")
        self.choose_standard_option.place(x = 220, y = 60)

        self.choose_division_label = ctk.CTkLabel(parent, text = "Select Division :", font = ("Verdana Pro", 18), text_color="#430A5D")
        self.choose_division_label.place(x = 40, y =100)

        self.choose_division_values = []
        self.div_value = tk.StringVar(value = "")
        self.choose_division_option = ctk.CTkOptionMenu(parent, width = 200, height = 30, corner_radius=2, values=self.choose_division_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=self.div_value, button_color="#912BBC", button_hover_color="#912BBC")
        self.choose_division_option.place(x = 220, y = 100)
        
        #==========calling the function===========#
        fetch_std_record()
        fetch_div_record()
        #==========================================#

    def result_student_frame(self):
        self.result_student_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.result_student_page_frame,text="Result", fg_color="#912BBC",text_color="white")

        self.std_div_select_func(self.result_student_page_frame)

        #===tkinter variables===#
        self.subjects_vars = []
        self.subject_labels = []
        self.total_marks_list = []
        self.grade_entries = []
        self.marks_entries = []
        self.grade_var_list = []

        #======function=======#
        def generate_report_card():
            global student_records, attendance_record
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root",port = 3307,database = "software")

                #create a cursor instance
                cur = con.cursor()

                #fetch the detail of student
                student_rollno = self.select_rollno_entry.get()
                
                cur.execute("select concat(first_name,' ',father_name,' ',last_name) as full_name, std_name, div_name , srno, student_id, dob from student s where s.student_id = %s", (student_rollno,))

                student_records = cur.fetchone()
                print(student_records)
                
                #====fetch absent count====#
                cur.execute("select count(*) as absent_count from attendance a, student s where a.student_no = s.srno  and attendance_status = 'Absent' and s.student_id = %s group by attendance_status", (student_rollno,))

                attendance_record = cur.fetchone()
                if attendance_record is None:
                    messagebox.showerror("Error","There is no attendance record of student.")
                else:
                    attendance_record == ""

                #====year=========#
                current_date = date.today()
                current_year = current_date.year
                next_year = current_year + 1

                #====fetch for report card only======#
                cur.execute("select first_name, last_name from student where student_id = %s", (student_rollno,))
                student_name = cur.fetchone()

                # commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #=====subject==========#
            subject_name = "\n".join(subject_list)

        #========calculated grade=========#
            if selected_std == "9th std" or selected_std == "10th std":
                grade_text = "\n".join(marks_l)
            else:
                grade_text = "\n".join(grade_list)

            #==================================#
            result_frame_image = Image.open("image/result_card.png").resize((700, 840))

            #creating an object for using student_frame_image
            draw = ImageDraw.Draw(result_frame_image)
            text_font = ImageFont.truetype("VerdanaPro-CondRegular.ttf", 15)

            self.sem = ""
            st = self.term_value.get()
            #====fetch sem=====#
            if st == "Semester-I":
                self.sem = st[:3] + st[-2:]
            elif st == "Semester-II":
                self.sem = st[:3] + st[-3:]

            #======fullname=======#
            draw.text(xy = (230, 167), text = f"{student_records[0]}", fill = (0, 0, 0), font = text_font)

            #===semester/year========#
            draw.text(xy = (295, 217), text = f"{st}/{current_year}-{next_year}", fill = (0, 0, 0), font = text_font)

            #===std/div========#
            draw.text(xy = (240, 260), text = f"{student_records[1]}/{student_records[2]}", fill = (0, 0, 0), font = text_font)

            #===reg/rollno========#
            draw.text(xy = (545, 260), text = f"{student_records[3]}/{student_records[4]}", fill = (0, 0, 0), font = text_font)

            #===no of days absent========#
            draw.text(xy = (285, 310), text = f"{attendance_record[0]}", fill = (0, 0, 0), font = text_font)

            #===date of birth========#
            draw.text(xy = (530, 310), text = f"{student_records[5]}", fill = (0, 0, 0), font = text_font)

            #=subject name==========#
            draw.multiline_text(xy = (240, 390), text = subject_name, fill = (0,0,0), font= text_font, spacing=12)

            #=====grade text=======#
            draw.multiline_text(xy = (500, 390), text = grade_text, fill = (0,0,0), font= text_font, spacing=12)

            # ======new window===============#
            result_report_window = ctk.CTkToplevel(fg_color="white")
            result_report_window.geometry("600x800+750+20")
            result_report_window.title("School Management System")

            #======report frame===========#
            self.result_card_page_frame = ctk.CTkFrame(result_report_window, border_width=2,border_color="#912BBC", fg_color="white", width = 580, height = 780, corner_radius=2)

            #======report label===========#
            self.head_label = ctk.CTkLabel(self.result_card_page_frame, text = "Report Card",width = 580, height = 40, fg_color="#912BBC", text_color="white", font = ("Verdana Pro", 18))
            self.head_label.place(x = 0, y = 0)

            #====ignore warnings===========#
            warnings.filterwarnings("ignore", category=UserWarning)

            #=====report card image label==========#
            report_card_image = ImageTk.PhotoImage(result_frame_image)
            self.result_card_label = ctk.CTkLabel(self.result_card_page_frame, text = "", image = report_card_image)
            self.result_card_label.place(x = 15, y = 42)

            # save report card
            def save_result_card():
                file_name = "C:/Users/vikas/OneDrive/Documents/software project/student_result_card"

                if os.path.exists(f"{file_name}/{student_rollno}_{student_name[0]} result_card.png"):
                    error_message = f"The file '{file_name}' already exists."
                    messagebox.showinfo("File Exists", message=error_message)
                else:
                    #convert photo_image into PIL image
                    image_to_save = ImageTk.getimage(report_card_image) 
                    image_to_save.save(f"{file_name}/{student_rollno}_{student_name[0]} result_card.png")
                    success_message = f"The student ID card for {student_name[0]} {student_name[0]} has been saved successfully!"
                    messagebox.showinfo("Success", message=success_message)

            def print_student_report_card():
                path = filedialog.askdirectory()
                print(path)

                if path:
                    image_to_save = ImageTk.getimage(report_card_image) 
                    image_to_save.save(f"{path}/{student_rollno}_{student_name[0]} report_card_print.png")
                    win32api.ShellExecute(0,"print", f"{path}/{student_rollno}_{student_name[0]} report_card_print.png",None, ".", 0)

            self.save_image = SetImage(image_path="image/download.png", width = 20, height=20)
            self.save_button = ctk.CTkButton(self.result_card_page_frame, text = "Save", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  save_result_card,fg_color="#912BBC", text_color="white", hover_color="#8D007B", image = self.save_image)
            self.save_button.place(x = 160, y = 730)

            self.print_image = SetImage(image_path="image/printer.png", width = 20, height=20)
            self.print_button = ctk.CTkButton(self.result_card_page_frame, text = "Print", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  print_student_report_card,fg_color="#912BBC", text_color="white", hover_color="#8D007B", image = self.print_image)
            self.print_button.place(x = 300, y = 730)

            result_report_window.grab_set()

            self.result_card_page_frame.place(x = 10, y = 10)

        def on_std_select(*args):
            global selected_std
            selected_std = self.std_value.get()
            validate_selection()

        def on_div_select(*args):
            global selected_div
            selected_div = self.div_value.get()
            validate_selection()

        def on_term_select(*args):
            global selected_term
            selected_term = self.term_value.get()
            validate_selection()

        def validate_selection():
            if self.std_value.get() == "" or self.div_value.get() == "":
                return
                # messagebox.showerror("Error", "Please select both Standard and Division.")
            elif self.term_value.get() == "":
                return
                # messagebox.showerror("Error", "Please select a Term/Semester.")
            else:
                messagebox.showinfo("Success", "Selections are valid.")
        
        def connect_to_database():
            global subject_list, student_name, student_srno, teacher_srno
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                cur = con.cursor()
                cur.execute("select concat(first_name,' ',last_name) as fullname from student where student_id = %s", (rollno,))
                student_name = cur.fetchone()

                #clear previous entry and labels
                clear_subject_entry()
            
                #fetch subject for selected standard
                if selected_std == "5th std":
                    cur.execute("select * from std5th")
                elif selected_std == "6th std":
                    cur.execute("select * from std6th")
                elif selected_std == "7th std":
                    cur.execute("select * from std7th")
                elif selected_std == "8th std":
                    cur.execute("select * from std8th")
                elif selected_std == "9th std":
                    cur.execute("select * from std9th")
                elif selected_std == "10th std":
                    cur.execute("select * from std10th")
                else:
                    messagebox.showerror("Error", "Invalid Standard.")

                subjects = cur.fetchall()
                subject_list = []
                for subject_record in subjects:
                    for subject in subject_record:
                        subject_list.append(subject)

            except Exception as e:
                print("Error : ", e)

        def calculate_marks():
            global grade_list, marks_l, sum_marks, percentage
            sum_marks = 0
            marks_l = []
            for entry in self.subjects_vars:
                marks_l.append(entry.get())
                if entry.get() == "":
                    messagebox.showerror("Error", "Some subjects are empty.")
                    return
            
            grade_list = []
            for mark in marks_l:
                if int(mark) < 0 or int(mark) > 100:
                    print("Negative marks is not allowed")
                    continue
                else:
                    sum_marks += int(mark)

                    # calculating grade execpt 9th and 10th
                    if selected_std in ("5th std", "6th std", "7th std", "8th std"): 
                        grade_boundaries = {'A1': 90, 'A2': 80, 'B1': 70, 'B2': 60, 'C1': 50, 'C2': 40, 'D': 35, 'F': 0}
                        grade = next((grade for grade, boundary in grade_boundaries.items() if int(mark) >= boundary), 'F')
                        grade_list.append(grade)
                    
            # set grade in entry
            if selected_std in ("5th std", "6th std", "7th std", "8th std"):
                is_fail = False 
                for i, grade_var in enumerate(self.grade_var_list):
                    grade_var.set(grade_list[i])
                    if grade_list[i] == "F":
                        is_fail = True
                        exam_status_var.set("FAIL")

                if is_fail:
                    print("fail")
                    exam_status_var.set("FAIL")
                else:
                    print("pass")
                    exam_status_var.set("PASS")
            else:
                is_fail = False
                for i, marks in enumerate(self.grade_var_list):
                    marks.set(marks_l[i])
                    if int(marks_l[i]) < 35:
                        is_fail = True
                        exam_status_var.set("FAIL")

                if is_fail:
                    print("fail")
                    exam_status_var.set("FAIL")
                else:
                    print("pass")
                    exam_status_var.set("PASS")
  
            # total sum
            total_sum = 0
            for total_marks in self.marks_entries:
                total_sum += int(total_marks.get())

            # set total marks
            overall_marks.set(value = int(sum_marks))

            # set percentage
            percentage = int(sum_marks) / total_sum * 100
            percentage_var.set(round(percentage, 2))

        def save_marks_database():
            global rollno
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                cur = con.cursor()

                # student srno
                cur.execute("select srno from student where student_id = %s", (rollno,))
                student_srno = cur.fetchone()

                # teacher srno
                cur.execute("select srno from staff where concat(first_name,'@',staff_id) = %s", (teacher_password,))
                teacher_srno = cur.fetchone()

                term = self.term_value.get()
  
                if selected_std == "5th std":
                    insert_query = "insert into exam_result(exam_type,student_id, teacher_id, English, Hindi, Marathi, Mathematics, EVS_I, EVS_II, Total_marks, Percentage, Overall_percentage,status) values(%s,%s, %s, %s, %s, %s, %s,%s, %s,%s, %s, %s, %s)"
                    insert_values = (term, student_srno[0], teacher_srno[0], f"{grade_list[0]}/{marks_l[0]}", f"{grade_list[1]}/{marks_l[1]}", f"{grade_list[2]}/{marks_l[2]}", f"{grade_list[3]}/{marks_l[3]}", f"{grade_list[4]}/{marks_l[4]}",f"{grade_list[5]}/{marks_l[5]}", sum_marks, percentage_var.get(),percentage_var.get(), exam_status_var.get())

                elif selected_std == "6th std":
                    insert_query = "insert into exam_result(exam_type,student_id, teacher_id, English, Hindi, Marathi, Mathematics, EVS, History_Civics,Geography, Total_marks, Percentage, Overall_percentage,status) values(%s,%s, %s, %s, %s, %s, %s,%s, %s,%s, %s, %s, %s, %s)"
                    insert_values = (term, student_srno[0], teacher_srno[0], f"{grade_list[0]}/{marks_l[0]}", f"{grade_list[1]}/{marks_l[1]}", f"{grade_list[2]}/{marks_l[2]}", f"{grade_list[3]}/{marks_l[3]}", f"{grade_list[4]}/{marks_l[4]}",f"{grade_list[5]}/{marks_l[5]}", f"{grade_list[6]}/{marks_l[6]}",sum_marks, percentage_var.get(),percentage_var.get(), exam_status_var.get())

                elif selected_std == "7th std" or selected_std == "8th std":
                    insert_query = "insert into exam_result(exam_type,student_id, teacher_id, English, Hindi, Marathi, Mathematics, History_Civics,Geography,General_Science, Total_marks, Percentage, Overall_percentage,status) values(%s,%s, %s, %s, %s, %s, %s,%s, %s,%s, %s, %s, %s, %s)"
                    insert_values = (term, student_srno[0], teacher_srno[0], f"{grade_list[0]}/{marks_l[0]}", f"{grade_list[1]}/{marks_l[1]}", f"{grade_list[2]}/{marks_l[2]}", f"{grade_list[3]}/{marks_l[3]}", f"{grade_list[4]}/{marks_l[4]}",f"{grade_list[5]}/{marks_l[5]}", f"{grade_list[6]}/{marks_l[6]}",sum_marks, percentage_var.get(),percentage_var.get(), exam_status_var.get())

                elif selected_std == "9th std":
                    insert_query = "insert into exam_result(exam_type,student_id, teacher_id, English, Hindi, Marathi, Geography,History_Political_Science,Mathematics_Part_I,Mathematics_Part_II,Science_technology, Total_marks, Percentage, Overall_percentage,status) values(%s,%s, %s, %s, %s, %s, %s,%s, %s,%s, %s, %s, %s, %s, %s)"
                    insert_values = (term ,student_srno[0], teacher_srno[0], f"{marks_l[0]}", f"{marks_l[1]}", f"{marks_l[2]}", f"{marks_l[3]}", f"{marks_l[4]}",f"{marks_l[5]}", f"{marks_l[6]}",f"{marks_l[7]}",sum_marks, percentage_var.get(),percentage_var.get(), exam_status_var.get())

                elif selected_std == "10th std":
                    # print(marks_l)
                    insert_query = "insert into exam_result(exam_type,student_id, teacher_id, English, Hindi, Marathi, Geography,History_Political_Science,Mathematics_Part_I,Mathematics_Part_II,Science_technology_Part_I,Science_technology_Part_II, Total_marks, Percentage, Overall_percentage,status) values(%s,%s, %s, %s, %s, %s, %s,%s, %s,%s, %s, %s, %s, %s, %s, %s)"
                    insert_values = (term, student_srno[0], teacher_srno[0], f"{marks_l[0]}", f"{marks_l[1]}", f"{marks_l[2]}", f"{marks_l[3]}", f"{marks_l[4]}",f"{marks_l[5]}", f"{marks_l[6]}",f"{marks_l[7]}",f"{marks_l[8]}",sum_marks, percentage_var.get(),percentage_var.get(), exam_status_var.get())

                cur.execute(insert_query, insert_values)
                con.commit()
                print(f"{cur.rowcount} records inserted")
                messagebox.showinfo("Success", "Student result saved successfully. You can now proceed to the next entry.")

            except Exception as e:   
                print("Error : ", e)

        def enter_marks():
            global rollno, overall_marks, percentage_var, exam_status_var, calculate_button, save_button, generate_result_button
            rollno = self.select_rollno_entry.get().strip()

            def on_return(event):
                event.widget.tk_focusNext().focus()
                return "break"

            if selected_std:
                if not rollno:
                    messagebox.showerror("Error", "Please enter a Roll Number.")
                    return

                # connect to database
                connect_to_database()

                self.marks_heading_label = ctk.CTkLabel(self.result_student_page_frame, text = f"", width = 1074, height = 35, fg_color="#912BBC", font = ("Verdana Pro", 18), text_color="white")
                self.marks_heading_label.place(x = 10, y = 283)

                if student_name:
                    #heading label
                    self.marks_heading_label.configure(text = f"Calculating Marks - {student_name[0]}")
                else:
                    self.marks_heading_label.configure(text = "No Student Data")

                #===frame for entry boxes==========#
                self.subject_frames = ctk.CTkFrame(self.result_student_page_frame, width = 1074, height=375, corner_radius=0,  border_width=2, border_color="#912BBC", fg_color="white")
                self.subject_frames.place(x = 10, y = 315)
                self.subject_frames.grid_propagate(False)

                #=====display subject label and entry box=====#
                for i, subject in enumerate(subject_list):
                    # subject labels
                    subject_label = ctk.CTkLabel(self.subject_frames, text = subject , font = ("Verdana Pro", 18))
                    subject_label.grid(row = i, column = 0, padx = 10, pady = (10, 0), sticky = "nw")
                    
                    # marks entry
                    marks_entry = ctk.CTkEntry(self.subject_frames, font = ("Verdana Pro", 17), width = 90)
                    marks_entry.grid(row = i, column = 1, padx = 10, pady = (10, 0), sticky = "ne")
                    marks_entry.bind("<Return>", on_return)

                    # total marks label
                    total_marks_label = ctk.CTkLabel(self.subject_frames, text = "out of" , font = ("Verdana Pro", 18))
                    total_marks_label.grid(row = i, column = 2, padx = 10, pady = (10,0), sticky = "ne")

                    # total marks entry
                    total_marks_var = tk.StringVar()
                    total_marks_var.set(100)
                    total_marks_entry = ctk.CTkEntry(self.subject_frames, font = ("Verdana Pro", 17), textvariable = total_marks_var, state="readonly", width = 90)
                    total_marks_entry.grid(row = i, column = 3, padx = 10, pady = (10, 0), sticky = "ne")

                    # grade entry
                    grade_entry_var = tk.StringVar(value="")
                    grade_entry = ctk.CTkEntry(self.subject_frames, font = ("Verdana Pro", 17), textvariable= grade_entry_var, state = "readonly",width = 90)
                    grade_entry.grid(row = i, column = 4, padx = 10, pady = (10, 0), sticky = "ne")
                
                    # append the entry and label in list
                    self.subject_labels.append(subject_label)
                    self.subjects_vars.append(marks_entry)
                    self.grade_entries.append(grade_entry)
                    self.total_marks_list.append(total_marks_label)
                    self.marks_entries.append(total_marks_entry)
                    self.grade_var_list.append(grade_entry_var)

                totalMarks_label = ctk.CTkLabel(self.subject_frames, text = "Total Marks: ", font = ("Verdana Pro", 18))
                totalMarks_label.place(x = 800, y = 5)

                overall_marks = tk.StringVar(value = "")
                totalMarks_entry = ctk.CTkEntry(self.subject_frames, font = ("Verdana Pro", 17), width = 90, textvariable=overall_marks, state="readonly")
                totalMarks_entry.place(x = 920, y = 5)

                percentage_label = ctk.CTkLabel(self.subject_frames, text = "Percentage: ", font = ("Verdana Pro", 18))
                percentage_label.place(x = 805, y = 45)

                percentage_var = tk.StringVar(value = "")
                percentage_entry = ctk.CTkEntry(self.subject_frames, font = ("Verdana Pro", 17), width = 90, textvariable = percentage_var, state = "readonly")
                percentage_entry.place(x = 920, y = 45)

                exam_status_label = ctk.CTkLabel(self.subject_frames, text = "Exam Status: ", font = ("Verdana Pro", 18))
                exam_status_label.place(x = 790, y = 85)

                exam_status_var = tk.StringVar(value = "")
                exam_status_entry = ctk.CTkEntry(self.subject_frames, font = ("Verdana Pro", 17), width = 90, textvariable = exam_status_var, state = "readonly")
                exam_status_entry.place(x = 920, y = 85)

                calculate_button = ctk.CTkButton(self.subject_frames, text = "Calculate", width = 140, height = 40, font = ("Verdana Pro", 18), cursor = "hand2", command=calculate_marks, fg_color="#912BBC", text_color="white", hover_color="#401F71")
                calculate_button.place(x = 920, y = 135)

                save_button = ctk.CTkButton(self.subject_frames, text = "Save Marks", width = 140, height = 40, font = ("Verdana Pro", 18), cursor = "hand2", command=save_marks_database, fg_color="#912BBC", text_color="white", hover_color="#401F71")
                save_button.place(x = 920, y = 185)

                generate_result_button = ctk.CTkButton(self.subject_frames, text = "Result", width = 140, height = 40, font = ("Verdana Pro", 18), cursor = "hand2", command=generate_report_card, fg_color="#912BBC", text_color="white", hover_color="#401F71")
                generate_result_button.place(x = 920, y = 235)

        def clear_subject_entry():
            # clear previous subject and entry widgets
            for entry_widget in self.subjects_vars:
                entry_widget.grid_forget()
                entry_widget.destroy()

            for label in self.subject_labels:
                label.grid_forget()
                label.destroy()

            for label2 in self.total_marks_list:
                label2.grid_forget()
                label2.destroy()

            for marks_entry_widget in self.marks_entries:
                marks_entry_widget.grid_forget()
                marks_entry_widget.destroy()

            for entry_grade in self.grade_entries:
                entry_grade.grid_forget()
                entry_grade.destroy()

            self.subjects_vars = []
            self.subject_labels = []
            self.grade_entries = []
            self.total_marks_list = []
            self.marks_entries = []
            self.grade_var_list = []

        #====select term =============#
        self.term_label = ctk.CTkLabel(self.result_student_page_frame, text = "Select Semester :", font = ("Verdana Pro", 18), text_color="#430A5D")
        self.term_label.place(x = 25, y =140)

        self.choose_term_values = ["Semester-I", "Semester-II"]
        self.term_value = tk.StringVar(value = "")
        self.choose_term_option = ctk.CTkOptionMenu(self.result_student_page_frame, width = 200, height = 30, corner_radius=2, values=self.choose_term_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=self.term_value, button_color="#912BBC", button_hover_color="#912BBC")
        self.choose_term_option.place(x = 220, y = 140)

        #=====trace the value for variable========#
        self.std_value.trace("w", on_std_select)
        self.div_value.trace("w", on_div_select)
        self.term_value.trace("w", on_term_select)

        self.rollno_label=ctk.CTkLabel(self.result_student_page_frame,text="Select Rollno :",font=("Verdana Pro", 18),text_color="#430A5D") 
        self.rollno_label.place(x = 55, y = 180)

        self.select_rollno_entry = ctk.CTkEntry(self.result_student_page_frame, width = 200, height = 35, corner_radius=2, font = ("Verdana Pro", 18), fg_color = "#D8D9DA", text_color= "black", border_width=0)
        self.select_rollno_entry.place(x = 220, y = 180)
        FocusColor(entry = self.select_rollno_entry, border_color="#430A5D")

        self.give_marks_button = ctk.CTkButton(self.result_student_page_frame, text = "Enter Marks", width = 170, height = 40, font = ("Verdana Pro", 18), cursor = "hand2", command=enter_marks, fg_color="#912BBC", text_color="white", hover_color="#401F71")
        self.give_marks_button.place(x = 220, y = 230)

        self.result_student_page_frame.place(x=0,y=0)

    def student_report_frame(self):
        self.student_report_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.student_report_page_frame,text="Student Report", fg_color="#912BBC", text_color="white")

        #=======function============#
        def show_student_record_auto():
            global std_div_records
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #====fetch std and div========#
                cur.execute("select d.std_name,d.div_name from staff,class_teachers ct,division d where staff.srno = ct.srno and d.div_id = ct.div_id and email = %s and concat(first_name,'@',staff_id) = %s", (teacher_username, teacher_password))

                std_div_records = cur.fetchone()

                self.fetch_std_label.configure(text = f"{std_div_records[0]}")
                self.fetch_div_label.configure(text = f"{std_div_records[1]}")

                #======fetch student details============#
                select_query = "select srno, student_id,concat(first_name, ' ' , last_name), gender, mobile, dob, email, city, pincode, selection_status from student where std_name = %s and div_name = %s"

                #execute the select query
                cur.execute(select_query, (std_div_records[0], std_div_records[1]))

                records = cur.fetchall()

                self.count = 0
                #show record in treeview
                for record in records:
                    if self.count %2 == 0:
                        self.add_student_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("evenrow",))
                    else:
                        self.add_student_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("oddrow",))
                    self.count += 1

                self.total_student_count_label.configure(text = f"{len(records)}")

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        def search_student_class_div():
            global std_div_records
            #clear the treeview
            for record in self.add_student_tree.get_children():
                self.add_student_tree.delete(record)

            #connection with database to pull out search records
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                cur.execute("select srno, student_id, concat(first_name, ' ' , last_name) as name, gender, mobile, dob, email, city, pincode, selection_status from student where std_name = %s and div_name = %s", (std_div_records[0], std_div_records[1]))

                records = cur.fetchall()
                count = len(records)
    
                self.count = 0
                #show search record in treeview
                for record in records:
                    if self.count %2 == 0:
                        self.add_student_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8],  record[9]), tags=("evenrow",))
                    else:
                        self.add_student_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("oddrow",))
                    self.count += 1

                self.total_student_count_label.configure(text = count)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        def approve_student_func():
            #grab a record number
            selected_approve_data = self.add_student_tree.selection() 

            approve_list = []
            for all in selected_approve_data:
                value = self.add_student_tree.item(all, "values")
                approve_list.append(value)

            for student in approve_list:
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the update query
                    update_query = "update student set selection_status = %s where srno = %s"
                    update_value = (self.approve_button.cget("text"), student[0])

                    cur.execute(update_query, update_value)

                    #clear the treeview
                    for record in self.add_student_tree.get_children():
                        self.add_student_tree.delete(record)

                    #executing select query 
                    select_query = "select srno,student_id, concat(first_name, ' ' , last_name), gender, mobile, dob, email, city, pincode, selection_status from student where std_name = %s and div_name = %s"

                    cur.execute(select_query, (std_div_records[0], std_div_records[1]))

                    records = cur.fetchall()

                    #show record in treeview
                    for record in records:
                        if self.count %2 == 0:
                            self.add_student_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("evenrow",))
                        else:
                            self.add_student_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("oddrow",))
                        self.count += 1

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

        def reject_student_func():
            #grab a record number
            selected_reject_data = self.add_student_tree.selection() 

            reject_list = []
            for all in selected_reject_data:
                value = self.add_student_tree.item(all, "values")
                reject_list.append(value)

            for student in reject_list:
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the update query
                    update_query = "update student set selection_status = %s where srno = %s"
                    update_value = (self.reject_button.cget("text"), student[0])

                    cur.execute(update_query, update_value)

                    #==========================
                    #clear the treeview
                    for record in self.add_student_tree.get_children():
                        self.add_student_tree.delete(record)

                    #executing select query 
                    select_query = "select srno,student_id, concat(first_name, ' ' , last_name), gender, mobile, dob, email, city, pincode, selection_status from student where std_name = %s and div_name = %s"
                    
                    cur.execute(select_query,(std_div_records[0], std_div_records[1]))

                    records = cur.fetchall()

                    #show record in treeview
                    for record in records:
                        if self.count %2 == 0:
                            self.add_student_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("evenrow",))
                        else:
                            self.add_student_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0],record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9]), tags=("oddrow",))
                        self.count += 1

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

        def update_student_tree():
            #clear the treeview
            for record in self.add_student_tree.get_children():
                self.add_student_tree.delete(record)

            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #execute the delete query
                cur.execute("delete from student where selection_status = 'Reject'")

                #commit the changes
                con.commit()

                #calling the show_staff_record_auto func
                show_student_record_auto()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)
        
        #=======generate id ==============#
        def generate_id():
            #clear the treeview
            for record in self.add_student_tree.get_children():
                self.add_student_tree.delete(record)

            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root",port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                srno_list=[]
                #execute the delete query
                cur.execute("select srno from student where std_name = %s and div_name = %s order by srno asc", (std_div_records[0], std_div_records[1]))
                records=cur.fetchall()
                for record in records:
                    for student_no in record:
                        srno_list.append(student_no)
                print(srno_list)

                id="01"
                for i in range(len(srno_list)):
                    # print(std[0]+div[0]+id)
                    cur.execute(f"update student set student_id='{std_div_records[0][0]+std_div_records[1]+id}' where srno={srno_list[i]}")
                    id=str(int(id)+1).zfill(2)

                #commit the changes
                con.commit()

                search_student_class_div()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #==========generate student ID Card=============#
        def generate_student_card(student_data):
            global records
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root",port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #fetch student_data
                cur.execute("select std_name, div_name, dob , mobile, address, srno, image_path, father_name, first_name, last_name from student where srno = %s and concat(first_name,' ', last_name) = %s and selection_status = %s", (student_data[0], student_data[2], student_data[9]))

                records = cur.fetchone()

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)
            
            std_name = records[0]
            div_name = records[1]
            dob = records[2]
            contact = records[3]
            address = records[4]
            rollno = records[5]
            image_path = records[6]
            father_fullname = records[7]
            first_name = records[8]
            last_name = records[9]
            wrapped_address = textwrap.fill(text=address, width=25)

            #======std and div==========#
            result = std_name.split(" ")
            std = result[0]

            result_father = father_fullname.split(" ")
            father_name = result_father[0]

            #==================================#
            student_frame_image = Image.open("image/student_id.png")
            student_image_pic = Image.open(f"{image_path}").resize((94, 98))

            #creating an object for using student_frame_image
            draw = ImageDraw.Draw(student_frame_image)
            text_font = ImageFont.truetype("VerdanaPro-CondRegular.ttf", 13)

            #showing student photo on id frame
            student_frame_image.paste(student_image_pic, (98,127)) 

            draw.text(xy = (98, 228), text = f"{first_name} {last_name}", fill = (255, 0, 0), font = ImageFont.truetype("tahomabd.ttf", 15))
            draw.text(xy = (97, 273), text = f"{std} {div_name}", fill = (0, 0, 0), font = text_font)
            draw.text(xy = (240, 273), text = f"{rollno}", fill = (0, 0, 0), font = text_font)
            draw.text(xy = (97, 297), text = f"{dob}", fill = (0, 0, 0), font = text_font)
            draw.text(xy = (97, 321), text = f"{contact}", fill = (0, 0, 0), font = text_font)
            draw.text(xy = (97, 345), text = f"{wrapped_address}", fill = (0, 0, 0), font = text_font)

            student_id_window = ctk.CTkToplevel(fg_color="white")
            student_id_window.geometry("600x500+800+250")
            student_id_window.title("School Management System")

            #======card frame===========#
            self.student_card_page_frame = ctk.CTkFrame(student_id_window, border_width=2,border_color="#912BBC", fg_color="white", width = 580, height = 480, corner_radius=2)

            #======card label===========#
            self.head_label = ctk.CTkLabel(self.student_card_page_frame, text = "Identity Card",width = 580, height = 40, fg_color="#912BBC", text_color="white", font = ("Verdana Pro", 18))
            self.head_label.place(x = 0, y = 0)

            #====ignore warnings===========#
            warnings.filterwarnings("ignore", category=UserWarning)

            #=====iid card image label==========#
            id_card_image = ImageTk.PhotoImage(student_frame_image)
            self.student_card_label = ctk.CTkLabel(self.student_card_page_frame, text = "", image = id_card_image)
            self.student_card_label.place(x = 170, y = 50)

            #===========save button=============#
            def save_student_card():
                file_name = "C:/Users/vikas/OneDrive/Documents/software project/student_id"

                if os.path.exists(f"{file_name}/{rollno}_{first_name} id_card.png"):
                    error_message = f"The file '{file_name}' already exists."
                    messagebox.showinfo("File Exists", message=error_message)
                else:
                    #convert photo_image into PIL image
                    image_to_save = ImageTk.getimage(id_card_image) 
                    image_to_save.save(f"{file_name}/{rollno}_{first_name} id_card.png")
                    success_message = f"The student ID card for {first_name} {last_name} has been saved successfully!"
                    messagebox.showinfo("Success", message=success_message)

            #============print button===========#
            def print_student_card():
                path = filedialog.askdirectory()

                if path:
                    image_to_save = ImageTk.getimage(id_card_image) 
                    image_to_save.save(f"{path}/{rollno}_{first_name} id_card_print.png")
                    win32api.ShellExecute(0,"print", f"{path}/{rollno}_{first_name} id_card_print.png",None, ".", 0)

            self.save_image = SetImage(image_path="image/download.png", width = 20, height=20)
            self.save_button = ctk.CTkButton(self.student_card_page_frame, text = "Save", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  save_student_card,fg_color="#912BBC", text_color="white", hover_color="#8D007B", image = self.save_image)
            self.save_button.place(x = 160, y = 400)

            self.print_image = SetImage(image_path="image/printer.png", width = 20, height=20)
            self.print_button = ctk.CTkButton(self.student_card_page_frame, text = "Print", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  print_student_card,fg_color="#912BBC", text_color="white", hover_color="#8D007B", image = self.print_image)
            self.print_button.place(x = 300, y = 400)

            self.student_card_page_frame.place(x = 10, y = 10)

        def on_tree_view_selection():
            selected = self.add_student_tree.selection()[0]
            student_data = self.add_student_tree.item(selected, "values")
            generate_student_card(student_data = student_data)

        #=========Send Email======#
        def send_email():
            global gif_window, label, frames, total_time, stddiv_records
            gif_window = tk.Toplevel(self)
            gif_window.geometry("100x100+700+500")
            gif_window.overrideredirect(True)
            gif_window.grab_set()
            gif_window.lift()

            try: 
                start_time=time.time()
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307,database = "software")

                #create a cursor instance
                cur = con.cursor()

                email_list=[]
                #fetch the email
                cur.execute("select email from student where std_name = %s and div_name = %s and selection_status = 'Approve' and student_id is null order by srno asc", (std_div_records[0], std_div_records[1]))
                records=cur.fetchall()
                for record in records:
                    for student_email in record:
                        email_list.append(student_email)
                print(email_list)

                #fetch name query
                name_list=[]
                cur.execute("select first_name from student where std_name = %s and div_name = %s and selection_status = 'Approve' and student_id is null order by srno asc",(std_div_records[0], std_div_records[1]))
                records=cur.fetchall()
                for record in records:
                    for student_name in record:
                        name_list.append(student_name)
                print(name_list)

                #fetch password
                password_list=[]
                cur.execute("select concat(first_name,'@',student_id) as password from student where std_name = %s and div_name = %s and selection_status = 'Approve' and student_id is null order by srno asc", (std_div_records[0], std_div_records[1]))
                records=cur.fetchall()
                for record in records:
                    for student_password in record:
                        password_list.append(student_password)
                print(password_list)

                #=======send email==========#
                for i in range(len(email_list)):
                    def send_email(subject, message, recipient_email, sender_email, sender_password):
                        try:
                            yag = yagmail.SMTP(sender_email, sender_password)
                            # run_task()
                            yag.send(to=recipient_email, subject=subject, contents=message)
                            print("Email sent successfully!")
                        except Exception as e:
                            print("Email failed to send. Error:", str(e))

                    subjects="Welcome to School Management System - Your Login Credentials"
                    body=f"Dear {name_list[i]},\n\nWe are pleased to inform you that your account for the Vivekandand Vidya Bhavan Management System has been successfully created. This platform will allow you to access important information about your classes, assignments, grades, and more.\n\nPlease find your login credentials below:\n\nUsername: {email_list[i]}\nPassword: {password_list[i]}\n\nIf you experience any issues or have any questions, please contact support at vvb.admin@gmail.com or +91 9619148774.\n\nThis message is generated automatically. Please do not reply to this email.\n\nThank you,\n\nVivekandand Vidya Bhavan Management System"

                    # run_task()
                    # Usage example:
                    send_email(subject=subjects, message=body,recipient_email=email_list[i], sender_email="vikas.kahar.4471804@ves.ac.in", sender_password="VIKAS@4471804")

                #commit the changes
                con.commit()

                end_time=time.time()
                total_time=end_time-start_time
                print(total_time)
                def run_task():
                    gif_path = "image/loading_play.gif"  # Replace with the actual path

                    img = Image.open(gif_path)
                    frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(img)]

                    label = tk.Label(gif_window)
                    label.pack()

                    def update_frame(index):
                        frame = frames[index % len(frames)]
                        label.configure(image=frame)  # Ensure you're using the correct variable
                        gif_window.after(frames_delay, update_frame, (index + 1) % len(frames))

                    # Get frames_delay from GIF metadata
                    frames_delay = img.info["duration"]
                    gif_window.after(0, update_frame, 0)
                    time.sleep(total_time)
                    gif_window.after(0, gif_window.destroy())
                    gif_window.after(0, lambda: messagebox.showinfo("Email", "Email sent successfully"))

                Thread(target=run_task).start()

                #close the connection
                con.close()

            except Exception as e:
                print("Email failed to send. Error:", e)

        #==============================================#
        self.choose_standard_label = ctk.CTkLabel(self.student_report_page_frame, text = "Select Standard :" ,font=("Verdana Pro", 18),text_color="#430A5D")
        self.choose_standard_label.place(x = 30, y = 60)

        self.fetch_std_label = ctk.CTkLabel(self.student_report_page_frame, text = "", font=("Verdana Pro", 18), text_color="black")
        self.fetch_std_label.place(x = 210, y = 60)

        self.choose_division_label = ctk.CTkLabel(self.student_report_page_frame, text = "Select Division :", font=("Verdana Pro", 18),text_color="#430A5D")
        self.choose_division_label.place(x = 42, y =100)

        self.fetch_div_label = ctk.CTkLabel(self.student_report_page_frame, text = "", font=("Verdana Pro", 18), text_color="black")
        self.fetch_div_label.place(x = 210, y =100)
        
        self.select_button = ctk.CTkButton(self.student_report_page_frame, text = "Select", width = 170, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=search_student_class_div, fg_color="#912BBC", text_color="white", hover_color="#401F71")
        self.select_button.place(x = 400, y = 95)

        self.total_student_label = ctk.CTkLabel(self.student_report_page_frame, text = "Total Student = ", font=("Verdana Pro", 18), text_color="black")
        self.total_student_label.place(x = 200, y = 140)

        self.total_student_count_label = ctk.CTkLabel(self.student_report_page_frame, text = "0", font = ("Verdana Pro", 18), text_color="black")
        self.total_student_count_label.place(x = 350, y = 140)

        #===button======#
        self.approve_image = SetImage(image_path="image/checked.png", width = 25, height=25)
        self.approve_button = ctk.CTkButton(self.student_report_page_frame, text = "Approve", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=approve_student_func, fg_color="#912BBC", text_color="white", hover_color="#401F71", image = self.approve_image)
        self.approve_button.place(x = 20, y = 640)

        self.reject_image = SetImage(image_path="image/crossed.png", width = 25, height=25)
        self.reject_button = ctk.CTkButton(self.student_report_page_frame, text = "Reject", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=reject_student_func, fg_color="#912BBC", text_color="white", hover_color="#401F71", image = self.reject_image)
        self.reject_button.place(x = 200, y = 640)

        self.update_image = SetImage(image_path="image/updated.png", width = 25, height=25)
        self.update_button = ctk.CTkButton(self.student_report_page_frame, text = "Update", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=update_student_tree, fg_color="#912BBC", text_color="white", hover_color="#401F71", image = self.update_image)
        self.update_button.place(x = 380, y = 640)

        self.generated_id_image = SetImage(image_path="image/list.png", width = 25, height=25)
        self.generate_id_button = ctk.CTkButton(self.student_report_page_frame, text = "Rollno", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=generate_id, fg_color="#912BBC", text_color="white", hover_color="#401F71", image = self.generated_id_image)
        self.generate_id_button.place(x = 560, y = 640)

        self.generate_id_card_image = SetImage(image_path="image/id-card.png", width = 25, height=25)
        self.generate_id_card_button = ctk.CTkButton(self.student_report_page_frame, text = "ID Card", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=on_tree_view_selection, fg_color="#912BBC", text_color="white", hover_color="#401F71", image = self.generate_id_card_image)
        self.generate_id_card_button.place(x = 740, y = 640)

        self.send_mail_image = SetImage(image_path="image/send-mail.png", width = 25, height=25)
        self.send_email_button = ctk.CTkButton(self.student_report_page_frame, text = "Send Email", width = 150, height = 40, font = ("Verdana Pro", 16), cursor = "hand2", command=send_email, fg_color="#912BBC", text_color="white", hover_color="#401F71", image = self.send_mail_image)
        self.send_email_button.place(x= 920, y = 640)
        
        #=======treeview setting========#
        #add some style
        style = ttk.Style()

        #pick a theme
        style.theme_use("alt")

        #configure the tree view color
        style.configure("Treeview", 
                        background = "#EEF0E5",
                        rowheight = 25,
                        fieldbackground = "#F3FBF1", font = ("Consolas", 14))
        
        style.configure("mystyle.Treeview", font=('Consolas', 15))

        #configure the selected color
        style.map("Treeview", 
        background=[("selected", "#912BBC")],
        foreground=[("selected", "white")])

        #increse the font size of heading
        style.configure("Treeview.Heading", font=("Consolas", 18))

        self.data_frame = tk.Frame(self.student_report_page_frame, bg = "lightgrey", borderwidth=0, relief="solid")
        self.data_frame.pack_propagate(False)
        self.data_frame.place(x = 20, y = 230, height = 550, width = 1320)

        #create a scrollbar
        y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
        x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

        y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
        x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

        #create a treeview
        self.add_student_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
        self.add_student_tree.pack(fill = "both", expand= True)

        #configure the scrollbar
        x_scroll.config(command = self.add_student_tree.xview)
        y_scroll.config(command = self.add_student_tree.yview)

        #define our columns
        self.add_student_tree["columns"] = ("Sr No", "Student ID", "Name", "Gender", "Mobile", "Date of Birth", "Email", "City", "Pincode", "Selection Status")

        #format column
        self.add_student_tree.column("Sr No", anchor="center", width = 100, minwidth=100)
        self.add_student_tree.column("Student ID", anchor="center", width = 150, minwidth=150)
        self.add_student_tree.column("Name", anchor="center", width = 300, minwidth=300)
        self.add_student_tree.column("Gender", anchor="center", width = 300, minwidth = 300)
        self.add_student_tree.column("Mobile", anchor="center", width = 300, minwidth = 300)
        self.add_student_tree.column("Date of Birth", anchor="center", width = 300, minwidth = 300)
        self.add_student_tree.column("Email", anchor="center", width = 300, minwidth = 300)
        self.add_student_tree.column("City", anchor="center", width = 300, minwidth = 300)
        self.add_student_tree.column("Pincode", anchor="center", width = 300, minwidth = 300)
        self.add_student_tree.column("Selection Status", anchor="center", width = 300, minwidth = 300)
        
        #create a heading
        self.add_student_tree.heading("Sr No", text = "Sr No", anchor = "center")
        self.add_student_tree.heading("Student ID", text = "Student ID", anchor = "center")
        self.add_student_tree.heading("Name", text = "Name", anchor = "center")
        self.add_student_tree.heading("Gender", text = "Gender", anchor = "center")
        self.add_student_tree.heading("Mobile", text = "Mobile", anchor = "center")
        self.add_student_tree.heading("Date of Birth", text = "Date of Birth", anchor = "center")
        self.add_student_tree.heading("Email", text = "Email", anchor = "center")
        self.add_student_tree.heading("City", text = "City", anchor = "center")
        self.add_student_tree.heading("Pincode", text = "Pincode", anchor = "center")
        self.add_student_tree.heading("Selection Status", text = "Selection Status", anchor = "center")

        #Create striped to our tages
        self.add_student_tree.tag_configure("evenrow", background="#D875C7")
        self.add_student_tree.tag_configure("oddrow", background="white")

        #======calling the show student record automatically======#
        show_student_record_auto()        

        self.student_report_page_frame.place(x=0,y=0)

    def student_attendance_frame(self):
        global student_username, std_div_records
        self.student_attendance_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.student_attendance_page_frame, text="Attendance", fg_color="#912BBC", text_color="white")

        def show_record_auto():
            global std_div_records
            self.standard_entry.configure(text = f"{std_div_records[0]}")
            self.division_entry.configure(text = f"{std_div_records[1]}")

            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                cur.execute("select srno, concat(first_name, ' ' , last_name) as name from student where std_name = %s and div_name = %s", (std_div_records[0], std_div_records[1]))

                records = cur.fetchall()
                self.count = 0
                #show record in treeview
                for record in records:
                    if self.count %2 == 0:
                        self.add_attendance_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], record[1], "N/A", date.today()), tags=("evenrow",))
                    else:
                        self.add_attendance_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], record[1], "N/A", date.today()), tags=("oddrow",))

                    self.count += 1

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)
        
        #========select record from treeview===========#
        def select_record(e):
            #grab record number
            selected = self.add_attendance_tree.focus()

            if selected:
                #grab record values
                values = self.add_attendance_tree.item(selected, "values")

                self.attendance_var.set(values[2])
        
        #======update attendance==========#
        def update():
            global values
            #clear the treeview
            selected = self.add_attendance_tree.focus()

            if selected:
                values = self.add_attendance_tree.item(selected, "values")
                attendance_status = self.attendance_var.get()

                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    # for item in self.add_attendance_tree.get_children():
                    update_query = "update attendance set attendance_status = %s where student_no = %s and attendance_date = %s"
                    cur.execute(update_query, (attendance_status, values[0], values[3]))
            
                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

                # #Update the values
                records = self.add_attendance_tree.item(selected, values = (values[0],values[1], self.attendance_var.get(),date.today()))

                self.attendance_var.set("")

        #======save attendance==========#
        def save_attendance():
            empty_data = list()
            values = self.add_attendance_tree.get_children()
            for i in values:
                data = self.add_attendance_tree.item(i, "values")
                empty_data.append(data)

            #====date=======#
            date = datetime.now()
            month = date.strftime("%B")
            day = date.strftime("%d")
            year = date.strftime("%Y")
                
            current_date = f"{month} {day}, {year}"
            
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #=====fetch the teacher=========#
                cur.execute("select srno from staff where email = %s and concat(first_name,'@',staff_id) = %s", (teacher_username, teacher_password))
                staff_id_records = cur.fetchone()

                # #=======append the staff_records in list of each tuples=========#
                updated_attendance_records = [tuple_ + staff_id_records for tuple_ in empty_data]
                for attendance_data in updated_attendance_records:
                    placeholder = ",".join(["%s"] * len(attendance_data))

                # for item in self.add_attendance_tree.get_children():
                insert_query = f"insert into attendance(student_no, student_name, attendance_status, attendance_date, staff_id) values({placeholder})" 
                insert_values = updated_attendance_records
                    
                cur.executemany(insert_query, insert_values)

                #commit the changes
                con.commit()

                messagebox.showinfo("Attendance", f"Class Attendance Saved Successfully for {current_date}")

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)
                messagebox.showwarning("Attendance Warning", f"Attendance for {current_date} already exists.")

        #============================================#
        self.standard_label = ctk.CTkLabel(self.student_attendance_page_frame, text = "Select Standard :", font = ("Verdana Pro", 18), text_color="#912BBC")
        self.standard_label.place(x = 40, y = 60)

        self.standard_entry = ctk.CTkLabel(self.student_attendance_page_frame, text = "", font = ("Verdana Pro", 18), text_color="black")
        self.standard_entry.place(x = 220, y = 60)

        self.division_label = ctk.CTkLabel(self.student_attendance_page_frame, text = "Select Division :", font = ("Verdana Pro", 18), text_color="#912BBC")
        self.division_label.place(x = 50, y = 100)

        self.division_entry = ctk.CTkLabel(self.student_attendance_page_frame, text = "", font = ("Verdana Pro", 18), text_color="black")
        self.division_entry.place(x = 220, y = 100)

        self.attendance_label = ctk.CTkLabel(self.student_attendance_page_frame, text = "Take Attendance :", font = ("Verdana Pro", 18), text_color="#912BBC")
        self.attendance_label.place(x = 30, y = 140)

        self.attendance_values = ["Absent", "Present", "Leave"]
        self.attendance_var = tk.StringVar(value = "N/A")
        self.attendance_option = ctk.CTkOptionMenu(self.student_attendance_page_frame, width = 200, height = 30, corner_radius=2, values=self.attendance_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=self.attendance_var, button_color="#912BBC", button_hover_color="#912BBC")
        self.attendance_option.place(x = 220, y = 140)

        self.select_button = ctk.CTkButton(self.student_attendance_page_frame, text = "Select", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  update ,fg_color="#912BBC", text_color="white", hover_color="#8D007B")
        self.select_button.place(x = 220, y = 180)

        #=======treeview setting========#
        #add some style
        style = ttk.Style()

        #pick a theme
        style.theme_use("alt")

        #configure the tree view color
        style.configure("Treeview", 
                        background = "#EEF0E5",
                        rowheight = 25,
                        fieldbackground = "#F3FBF1", font = ("Consolas", 14))
            
        style.configure("mystyle.Treeview", font=('Consolas', 15))

        #configure the selected color
        style.map("Treeview", 
        background=[("selected", "#912BBC")],
        foreground=[("selected", "white")])

        #increse the font size of heading
        style.configure("Treeview.Heading", font=("Consolas", 18))

        self.data_frame = tk.Frame(self.student_attendance_page_frame, bg = "lightgrey", borderwidth=0, relief="solid")
        self.data_frame.pack_propagate(False)
        self.data_frame.place(x = 20, y = 300, height = 500, width = 1000)

        #create a scrollbar
        y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
        x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

        y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
        x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

        #create a treeview
        self.add_attendance_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
        self.add_attendance_tree.pack(fill = "both", expand= True)
        self.add_attendance_tree.bind("<<TreeviewSelect>>", select_record)

        #configure the scrollbar
        x_scroll.config(command = self.add_attendance_tree.xview)
        y_scroll.config(command = self.add_attendance_tree.yview)

        #define our columns
        self.add_attendance_tree["columns"] = ("Roll No","Name", "Attendance", "Date")

        #format column
        self.add_attendance_tree.column("Roll No", anchor="center", width = 100, minwidth=100)
        self.add_attendance_tree.column("Name", anchor="center", width = 300, minwidth=300)
        self.add_attendance_tree.column("Attendance", anchor="center", width = 300, minwidth=300)
        self.add_attendance_tree.column("Date", anchor="center", width = 200, minwidth=200)
            
        #create a heading
        self.add_attendance_tree.heading("Roll No", text = "Roll No", anchor = "center")
        self.add_attendance_tree.heading("Name", text = "Name", anchor = "center")
        self.add_attendance_tree.heading("Attendance", text = "Attendance", anchor = "center")
        self.add_attendance_tree.heading("Date", text = "Date", anchor = "center")
            
        #Create striped to our tages
        self.add_attendance_tree.tag_configure("evenrow", background="#D875C7")
        self.add_attendance_tree.tag_configure("oddrow", background="white")

        self.add_attendance_button = ctk.CTkButton(self.student_attendance_page_frame, text = "Add Attendance", width = 180, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  save_attendance ,fg_color="#912BBC", text_color="white", hover_color="#8D007B")
        self.add_attendance_button.place(x = 20, y = 650)

        show_record_auto()
        
        self.student_attendance_page_frame.place(x=0,y=0)

    def student_attendance_report_frame(self):
        self.attendance_report_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.attendance_report_page_frame,text="Attendance Reports", fg_color="#912BBC", text_color="white")

        def fetch_std_record():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                cur.execute("select std_name, div_name from division d, staff s, class_teachers ct where s.srno = ct.srno and d.div_id = ct.div_id and email = %s and concat(s.first_name,'@',s.staff_id) = %s",(teacher_username, teacher_password))

                std_div = cur.fetchone()

                #fetch std record
                self.selected_standard_label.configure(text = f"{std_div[0]}")

                #execute the cursor query
                cur.execute("select div_name from division group by div_name")

                records = cur.fetchall()

                div_list = []
                for record in records:
                    div_list.append(record[0])
                
                #======configure the option menu for standard values
                self.choose_division_values= div_list
                self.choose_division_option.configure(values = self.choose_division_values)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        def attendance_report_func():
            choose_date = self.date_entry.get_date()
            format_date = f"{choose_date:%Y-%m-%d}"
            std = self.selected_standard_label.cget("text")
            div = div_var.get()

            #=======treeview setting========#
            #add some style
            style = ttk.Style()

            #pick a theme
            style.theme_use("alt")

            #configure the tree view color
            style.configure("Treeview", 
                            background = "#EEF0E5",
                            rowheight = 25,
                            fieldbackground = "#F3FBF1", font = ("Consolas", 14))
                
            style.configure("mystyle.Treeview", font=('Consolas', 15))

            #configure the selected color
            style.map("Treeview", 
            background=[("selected", "#912BBC")],
            foreground=[("selected", "white")])

            #increse the font size of heading
            style.configure("Treeview.Heading", font=("Consolas", 18))

            self.data_frame = tk.Frame(self.attendance_report_page_frame, bg = "lightgrey", borderwidth=0, relief="solid")
            self.data_frame.pack_propagate(False)
            self.data_frame.place(x = 20, y = 320, height = 300, width = 1000)

            #create a scrollbar
            y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
            x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

            y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
            x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

            #create a treeview
            self.add_attendance_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
            self.add_attendance_tree.pack(fill = "both", expand= True)
            
            #configure the scrollbar
            x_scroll.config(command = self.add_attendance_tree.xview)
            y_scroll.config(command = self.add_attendance_tree.yview)

            #define our columns
            self.add_attendance_tree["columns"] = ("Sr No","Name", "Attendance", "Date")

            #format column
            self.add_attendance_tree.column("Sr No", anchor="center", width = 100, minwidth=100)
            self.add_attendance_tree.column("Name", anchor="center", width = 300, minwidth=300)
            self.add_attendance_tree.column("Attendance", anchor="center", width = 300, minwidth=300)
            self.add_attendance_tree.column("Date", anchor="center", width = 200, minwidth=200)
                
            #create a heading
            self.add_attendance_tree.heading("Sr No", text = "Sr No", anchor = "center")
            self.add_attendance_tree.heading("Name", text = "Name", anchor = "center")
            self.add_attendance_tree.heading("Attendance", text = "Attendance", anchor = "center")
            self.add_attendance_tree.heading("Date", text = "Date", anchor = "center")
                
            #Create striped to our tages
            self.add_attendance_tree.tag_configure("evenrow", background="#D875C7")
            self.add_attendance_tree.tag_configure("oddrow", background="white")

            #=======show record in treeview============#
            if not div:
                messagebox.showerror("Invalid Division", "Please select a division.")
                return 
            if format_date is None:
                messagebox.showerror("Date", "Please select a date.")
                return 
            if not div and format_date is None:
                messagebox.showerror("Empty Selection", "Please select both divison and date")
                return 
            else:
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #execute the cursor query
                    cur.execute("select student_id, name, attendance_status, date from attendance a, student s where s.srno = a.student_no and s.std_name = %s and s.div_name = %s and a.date = %s", (std, div, format_date))

                    records = cur.fetchall()

                    if records:
                        self.count = 0
                        #show record in treeview
                        for record in records:
                            if self.count %2 == 0:
                                self.add_attendance_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], record[1], record[2], record[3]), tags=("evenrow",))
                            else:
                                self.add_attendance_tree.insert(parent  = "", index = tk.END, iid = self.count, values=(record[0], record[1], record[2], record[3]), tags=("oddrow",))

                            self.count += 1
                    else:
                        messagebox.showerror("Attendance Report", f"Attendance report for date: {format_date} is not available")

                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error ", e)

        #======other widgets=====#
        self.choose_standard_label = ctk.CTkLabel(self.attendance_report_page_frame, text = "Select Standard :", font=("Verdana Pro", 18), text_color="#912BBC")
        self.choose_standard_label.place(x = 35, y = 60)

        self.selected_standard_label = ctk.CTkLabel(self.attendance_report_page_frame, text = "", font = ("Consolas", 20), text_color="black")
        self.selected_standard_label.place(x = 210, y = 60)

        self.choose_division_label = ctk.CTkLabel(self.attendance_report_page_frame, text = "Select Division :", font=("Verdana Pro", 18), text_color="#912BBC")
        self.choose_division_label.place(x = 47, y =100)

        self.choose_division_values = []
        div_var = tk.StringVar(value = "")
        self.choose_division_option = ctk.CTkOptionMenu(self.attendance_report_page_frame, width = 200, height = 30, corner_radius=2, values=self.choose_division_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=div_var, button_color="#912BBC", button_hover_color="#912BBC")
        self.choose_division_option.place(x = 210, y = 100)

        self.select_date_label = ctk.CTkLabel(self.attendance_report_page_frame, text = "Select Date :", font=("Verdana Pro", 18), text_color="#912BBC")
        self.select_date_label.place(x = 75, y = 140)

        self.date_entry = DateEntry(self.attendance_report_page_frame, font = ("Verdana Pro", 15), state = "readonly") 
        self.date_entry.place(x = 260, y = 180)

        self.select_button = ctk.CTkButton(self.attendance_report_page_frame, text = "Select", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  attendance_report_func,fg_color="#912BBC", text_color="white", hover_color="#8D007B")
        self.select_button.place(x = 210, y = 190)

        #=========calling the function============#
        fetch_std_record()

        self.attendance_report_page_frame.place(x=0,y=0)

    def advance_report_frame(self):
        self.advance_report_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.advance_report_page_frame,text="Advance Reports", fg_color="#912BBC", text_color="white")

        def fetch_std_and_div():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                # #execute the cursor query
                cur.execute(f"select d.std_name,d.div_name from staff,class_teachers ct,division d where staff.srno = ct.srno and d.div_id = ct.div_id and email = '{teacher_username}' and concat(first_name,'@',staff_id) = '{teacher_password}'")

                records = cur.fetchone()

                self.selected_standard_label.configure(text = records[0])
                self.select_division_label.configure(text = records[1])

                #execute the cursor query
                cur.execute("select srno from student where std_name = %s and div_name = %s", (records[0], records[1]))

                roll_records = cur.fetchall()

                rollno_list = []
                for rollno in roll_records:
                    rollno_list.append(str(rollno[0]))

                #======configure the option menu for standard values
                self.choose_student_values = rollno_list
                self.choose_student_option.configure(values = self.choose_student_values)

                #commit the changes
                con.commit()

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)

        #=======functions=======#
        def report_sumary_frame():
            #======checking the condition==========#
            rollno = rollno_var.get()
            std = self.selected_standard_label.cget("text")
            div = self.select_division_label.cget("text")

            
            def fetch_student_summary():
                if std == "" and div == "" or rollno == "":
                    messagebox.showerror("Error", "Please select a roll number.")
                else:
                    try:
                        con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                        #create a cursor instance
                        cur = con.cursor()

                        #execute the cursor query
                        cur.execute("select srno, concat(first_name, ' ', last_name) as name,  email, mobile, dob, address, city, pincode, image_path from student where srno = %s and std_name = %s and div_name = %s", (rollno, std, div))

                        records = cur.fetchall()

                        for record in records:
                            self.report_frame_label.configure(text = f"Student Name: {record[1]}")
                            self.student_rollno.configure(text = record[0])
                            self.student_email.configure(text = record[2])
                            self.student_mobile.configure(text = record[3])
                            self.student_birthdate.configure(text = record[4])
                            self.student_address.configure(text = record[5], wraplength = 300)
                            self.student_city.configure(text = record[6])
                            self.student_pincode.configure(text = record[7])
                            image_path = record[8]

                        try:
                            image = Image.open(image_path)

                        except FileNotFoundError:
                            print(f"Error: Could not find image at path: {image_path}")

                        #====configure the image===========#
                            
                        #base name of the image
                        image_file_name = os.path.basename(image_path)

                        #save the image
                        image.save(image_file_name)
                            
                        #open image in form of ctk.CTkImage
                        imageo = ctk.CTkImage(light_image=image, dark_image=image, size = (127, 147))

                        #configure the right side frame label
                        self.student_photo_label.configure(image = imageo)
                        self.student_photo_label.image = imageo

                        #commit the changes
                        con.commit()

                        #close the connection
                        con.close()

                    except Exception as e:
                        print("Error ", e)

            #===========================================#
            self.report_frame = ctk.CTkFrame(self.advance_report_page_frame, width = 700, height=450, corner_radius=2,  border_width=2, border_color="#912BBC", fg_color="white")

            self.report_frame_label = ctk.CTkLabel(self.report_frame, width = 700, height = 40, text = "Student Name: ", font = ("Verdana Pro", 18), fg_color="#912BBC", text_color="white")
            self.report_frame_label.place(x = 0, y = 0)

            #======other entries=======#
            self.rollno = ctk.CTkLabel(self.report_frame, text = "Roll No: ", font = ("Verdana Pro", 18), text_color="#912BBC")
            self.rollno.place(x = 55, y = 50)

            self.student_rollno = ctk.CTkLabel(self.report_frame, text = "", font = ("Verdana Pro", 18), text_color="black")
            self.student_rollno.place(x = 140, y = 50)

            self.email = ctk.CTkLabel(self.report_frame, text = "Email: ", font = ("Verdana Pro", 18), text_color="#912BBC")
            self.email.place(x = 67, y = 90)

            self.student_email = ctk.CTkLabel(self.report_frame, text = "", font = ("Verdana Pro", 18), text_color="black")
            self.student_email.place(x = 140, y = 90)

            self.mobile = ctk.CTkLabel(self.report_frame, text = "Mobile: ", font = ("Verdana Pro", 18), text_color="#912BBC")
            self.mobile.place(x = 57, y = 130)

            self.student_mobile = ctk.CTkLabel(self.report_frame, text = "", font = ("Verdana Pro", 18), text_color="black")
            self.student_mobile.place(x = 140, y = 130)

            self.birthdate = ctk.CTkLabel(self.report_frame, text = "Birth Date: ", font = ("Verdana Pro", 18), text_color="#912BBC")
            self.birthdate.place(x = 25, y = 170)

            self.student_birthdate = ctk.CTkLabel(self.report_frame, text = "", font = ("Verdana Pro", 18), text_color="black")
            self.student_birthdate.place(x = 140, y = 170)

            self.address = ctk.CTkLabel(self.report_frame, text = "Address: ", font = ("Verdana Pro", 18), text_color="#912BBC")
            self.address.place(x = 45, y = 210)

            self.student_address = ctk.CTkLabel(self.report_frame, text = "", font = ("Verdana Pro", 18), text_color="black")
            self.student_address.place(x = 140, y = 210)

            self.city = ctk.CTkLabel(self.report_frame, text = "City: ", font = ("Verdana Pro", 18), text_color="#912BBC")
            self.city.place(x = 78, y = 290)

            self.student_city = ctk.CTkLabel(self.report_frame, text = "", font = ("Verdana Pro", 18), text_color="black")
            self.student_city.place(x = 140, y = 290)

            self.pincode = ctk.CTkLabel(self.report_frame, text = "Pincode: ", font = ("Verdana Pro", 18), text_color="#912BBC")
            self.pincode.place(x = 45, y = 330)

            self.student_pincode = ctk.CTkLabel(self.report_frame, text = "", font = ("Verdana Pro", 18), text_color="black")
            self.student_pincode.place(x = 140, y = 330)

            self.student_photo_frame = ctk.CTkFrame(self.report_frame, width = 130, height=150, corner_radius=0,  border_width=3, border_color="black", fg_color="white")
            self.student_photo_frame.place(x = 540, y = 60)

            self.student_photo_label = ctk.CTkLabel(self.student_photo_frame, text = "", fg_color="grey", width = 127, height=147)
            self.student_photo_label.place(x = 1, y = 1)

            #=======calling the function============#
            fetch_student_summary()

            self.report_frame.place(x = 200, y = 200)

        self.choose_standard_label = ctk.CTkLabel(self.advance_report_page_frame, text = "Select Standard :", font=("Verdana Pro", 18), text_color="#912BBC")
        self.choose_standard_label.place(x = 30, y = 60)

        self.selected_standard_label = ctk.CTkLabel(self.advance_report_page_frame, text = "", font = ("Verdana Pro", 18), text_color="black")
        self.selected_standard_label.place(x = 210, y = 60)

        self.choose_division_label = ctk.CTkLabel(self.advance_report_page_frame, text = "Select Division :", font=("Verdana Pro", 18), text_color="#912BBC")
        self.choose_division_label.place(x = 40, y =100)

        self.select_division_label = ctk.CTkLabel(self.advance_report_page_frame, text = "", font = ("Verdana Pro", 18), text_color="black")
        self.select_division_label.place(x = 210, y = 100)

        self.choose_student_label = ctk.CTkLabel(self.advance_report_page_frame, text = "Select Student :", font=("Verdana Pro", 18), text_color="#912BBC")
        self.choose_student_label.place(x = 41, y =140)

        self.choose_student_values = []
        rollno_var = tk.StringVar(value = "")
        self.choose_student_option = ctk.CTkOptionMenu(self.advance_report_page_frame, width = 200, height = 30, corner_radius=2, values=self.choose_student_values, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=rollno_var, button_color="#912BBC", button_hover_color="#912BBC")
        self.choose_student_option.place(x = 210, y = 140)

        self.select_button = ctk.CTkButton(self.advance_report_page_frame, text = "Select", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  report_sumary_frame,fg_color="#912BBC", text_color="white", hover_color="#8D007B")
        self.select_button.place(x = 435, y = 138)

        #==========calling the function==========#
        fetch_std_and_div()

        self.advance_report_page_frame.place(x=0,y=0)

    def student_complain_frame(self):
        self.complain_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.complain_page_frame,text="Complain", fg_color="#912BBC", text_color="white")

        def show_complain_record():
            try:
                con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                #create a cursor instance
                cur = con.cursor()

                #fetch the detail of complain
                cur.execute(f"select rollno, student_name, subject, message, reply,complain_id from complain c, student s where s.srno = c.rollno and s.std_name = (select d.std_name from division d, class_teachers ct, staff sf where d.div_id = ct.div_id and ct.srno = sf.srno and sf.email ='{teacher_username}') and div_name = (select d.div_name from division d, class_teachers ct, staff sf where d.div_id = ct.div_id and ct.srno = sf.srno and sf.email = '{teacher_username}')")

                complain_record = cur.fetchall()
  
                #===showing the data in treeview=====#
                self.count = 0
                for fetch_record in complain_record:
                    if self.count %2 == 0:
                        self.complain_tree.insert(parent = "", index = tk.END, iid = self.count, values=(fetch_record[0], fetch_record[1], fetch_record[2], fetch_record[3], fetch_record[4]), tags=("evenrow",))
                    else:
                        self.complain_tree.insert(parent = "", index = tk.END, iid = self.count, values=(fetch_record[0], fetch_record[1], fetch_record[2], fetch_record[3], fetch_record[4]), tags=("oddrow",))
                    self.count += 1

                #commit the changes
                con.commit()

                self.complain_count_label.configure(text = len(complain_record))

                #close the connection
                con.close()

            except Exception as e:
                print("Error ", e)
        
        def complain_reply_func():
            selected = self.complain_tree.focus()
            selected_values = self.complain_tree.item(selected, "values")
            
            if selected:
                #====open reply window ==========#
                reply_window = ctk.CTkToplevel(fg_color="white")
                reply_window.title("School Management System")
                reply_window.geometry("500x400+850+300")
                reply_window.overrideredirect(True)

                #======function======#
                def update_reply_msg():
                    answer = self.complain_answer_textbox.get("0.0", tk.END)
                    try:
                        con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                        #create a cursor instance
                        cur = con.cursor()

                        cur.execute("select complain_id, edate from complain where rollno = %s and student_name = %s and subject = %s and message = %s and reply = %s", (selected_values[0], selected_values[1], selected_values[2], selected_values[3], selected_values[4]))

                        records = cur.fetchall()
                        
                        #====update the database==========#
                        for record in records:
                            #fetch the complain record detail to see status
                            cur.execute("update complain set reply = %s where complain_id = %s and edate = %s", (answer, record[0], record[1]))

                        #commit the changes
                        con.commit()

                        #close the connection
                        con.close()

                    except Exception as e:
                        print("Error :", e)

                    #====update the values==========#
                    self.complain_tree.item(selected, values = (self.rollno_entry.cget("text"), self.name_entry.cget("text"), self.subject_entry.cget("text"), self.complain_entry.cget("text"), self.complain_answer_textbox.get("0.0", tk.END)))
                
                def destroy_reply_window(e):
                    reply_window.destroy()

                self.complain_reply_frame = ctk.CTkFrame(reply_window, width = 500, height=400, corner_radius=2,  border_width=2, border_color="#912BBC", fg_color="white")
                
                #===making heading label===========#
                self.reply_head_label =  ctk.CTkLabel(self.complain_reply_frame, text = "Reply Complain", font=("Verdana Pro", 18),text_color="white", fg_color="#912BBC", width = 500, height = 40)
                self.reply_head_label.place(x = 0, y = 0)

                #====destroy button=========#
                self.destroy_complain_button = ctk.CTkButton(self.complain_reply_frame, text = "X", fg_color="#912BBC", text_color = "white", width = 0, height = 0, font = ("Verdana Pro", 18, "bold"), hover = "disabled", bg_color="#912BBC", cursor = "hand2")
                self.destroy_complain_button.place(x = 470, y = 5)
                self.destroy_complain_button.bind("<Button-1>", destroy_reply_window)

                self.rollno_label = ctk.CTkLabel(self.complain_reply_frame, text = "Roll No: ", font = ("Verdana Pro", 18), text_color="#912BBC")
                self.rollno_label.place(x = 40, y = 50)

                self.rollno_entry = ctk.CTkLabel(self.complain_reply_frame, text = selected_values[0], font = ("Verdana Pro", 18), text_color="black")
                self.rollno_entry.place(x = 125, y = 50)

                self.name_label = ctk.CTkLabel(self.complain_reply_frame, text = "Name: ", font = ("Verdana Pro", 18), text_color="#912BBC")
                self.name_label.place(x = 50, y = 100)

                self.name_entry = ctk.CTkLabel(self.complain_reply_frame, text = selected_values[1], font = ("Verdana Pro", 18), text_color="black")
                self.name_entry.place(x = 125, y = 100)

                self.subject_label = ctk.CTkLabel(self.complain_reply_frame, text = "Subject: ", font = ("Verdana Pro", 18), text_color="#912BBC")
                self.subject_label.place(x = 33, y = 150)

                self.subject_entry = ctk.CTkLabel(self.complain_reply_frame, text = selected_values[2], font = ("Verdana Pro", 18), text_color="black")
                self.subject_entry.place(x = 125, y = 150)

                self.complain_label = ctk.CTkLabel(self.complain_reply_frame, text = "Complain: ", font = ("Verdana Pro", 18), text_color="#912BBC")
                self.complain_label.place(x = 18, y = 200)

                self.complain_entry = ctk.CTkLabel(self.complain_reply_frame, text = selected_values[3], font = ("Verdana Pro", 18), text_color="black")
                self.complain_entry.place(x = 125, y = 200)

                self.complain_answer_label = ctk.CTkLabel(self.complain_reply_frame, text = "Answer: ", font = ("Verdana Pro", 18), text_color="#912BBC")
                self.complain_answer_label.place(x = 35, y = 250)

                self.complain_answer_textbox = ctk.CTkTextbox(self.complain_reply_frame,width=250, height = 70, corner_radius=2, font = ("Verdana Pro", 18), wrap = "word", fg_color = "#D8D9DA", text_color= "black", border_width=0)
                self.complain_answer_textbox.place(x = 125, y = 250)
                FocusColor(entry = self.complain_answer_textbox, border_color="#912BBC")

                self.send_button = ctk.CTkButton(self.complain_reply_frame, text = "Send", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  update_reply_msg, fg_color="#912BBC", text_color="white", hover_color="#8D007B")
                self.send_button.place(x = 125, y = 340)
                self.send_button.bind("<Button-1>", destroy_reply_window)

                self.complain_reply_frame.place(x = 0, y = 0)

                reply_window.lift()
                reply_window.grab_set()

        #=======treeview setting========#
        #add some style
        style = ttk.Style()

        #pick a theme
        style.theme_use("alt")

        #configure the tree view color
        style.configure("Treeview", 
                        background = "#EEF0E5",
                        rowheight = 25,
                        fieldbackground = "#F3FBF1", font = ("Consolas", 14))
                
        style.configure("mystyle.Treeview", font=('Consolas', 15))

        #configure the selected color
        style.map("Treeview", 
        background=[("selected", "#912BBC")],
        foreground=[("selected", "white")])

        #increse the font size of heading
        style.configure("Treeview.Heading", font=("Consolas", 18))

        self.data_frame = tk.Frame(self.complain_page_frame, bg = "lightgrey", borderwidth=0, relief="solid")
        self.data_frame.pack_propagate(False)
        self.data_frame.place(x = 25, y = 170 , height = 200, width = 1300)

        #create a scrollbar
        y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
        x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

        y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
        x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

        #create a treeview
        self.complain_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
        self.complain_tree.pack(fill = "both", expand= True)

        #configure the scrollbar
        x_scroll.config(command = self.complain_tree.xview)
        y_scroll.config(command = self.complain_tree.yview)

        #define our columns
        self.complain_tree["columns"] = ("Roll No", "Student Name", "Subject", "Complain", "Reply")

        #format column
        self.complain_tree.column("Roll No", anchor="center", width = 150, minwidth=150)
        self.complain_tree.column("Student Name", anchor="center", width = 300, minwidth=300)
        self.complain_tree.column("Subject", anchor="center", width = 400, minwidth = 400)
        self.complain_tree.column("Complain", anchor="center", width = 400, minwidth = 400)
        self.complain_tree.column("Reply", anchor="center", width = 400, minwidth = 400)
                
        #create a heading
        self.complain_tree.heading("Roll No", text = "Roll No", anchor = "center")
        self.complain_tree.heading("Student Name", text = "Student Name", anchor = "center")
        self.complain_tree.heading("Subject", text = "Subject", anchor = "center")
        self.complain_tree.heading("Complain", text = "Complain", anchor = "center")
        self.complain_tree.heading("Reply", text = "Reply", anchor = "center")
                
        #Create striped to our tages
        self.complain_tree.tag_configure("evenrow", background="#D875C7")
        self.complain_tree.tag_configure("oddrow", background="white")

        self.total_complain_label = ctk.CTkLabel(self.complain_page_frame, text = "Total Complain = ", font = ("Verdana Pro", 18), text_color="#912BBC")
        self.total_complain_label.place(x = 20, y = 60)

        self.complain_count_label = ctk.CTkLabel(self.complain_page_frame, text = "0", font = ("Verdana Pro", 18), text_color="#912BBC")
        self.complain_count_label.place(x = 180, y = 60)

        self.reply_button = ctk.CTkButton(self.complain_page_frame, text = "Reply", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  complain_reply_func,fg_color="#912BBC", text_color="white", hover_color="#8D007B")
        self.reply_button.place(x = 25, y = 310)

        #=======calling the function==========#
        show_complain_record()

        self.complain_page_frame.place(x=0,y=0)

    def student_leave_frame(self):
        self.leave_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.leave_page_frame,text="Leave", fg_color="#912BBC", text_color="white")

        #======show record of leave===========#
        def student_new_leave_frame():
            #=====inside frame======#
            self.new_leave_frame = ctk.CTkFrame(self.leave_page_frame, width = 1072, height=270, corner_radius=0,  border_width=0, border_color="green", fg_color="white")
        
            #====================function====================#
            def show_new_leave_record():
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #fetch the leave record detail to see status
                    cur.execute("select rollno, student_name, message, no_days, status from student_leave where status = 'Pending'")

                    records = cur.fetchall()
                    total_new_leave_count = len(records)

                    self.count = 0
                    #show record in treeview
                    for record in records:
                        if self.count %2 == 0:
                            self.new_leave_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], record[1], record[2], record[3], record[4]), tags=("evenrow",))
                        else:
                            self.new_leave_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], record[1], record[2], record[3], record[4]), tags=("oddrow",))
                        self.count += 1

                    #=====configure the count label============#
                    self.total_leave_label.configure(text = f"Total New Leave = {total_new_leave_count}")
                    
                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error :", e)

            #=====approve new record ============#
            def approve_new_record():
                selected = self.new_leave_tree.selection()
                selected_values = self.new_leave_tree.item(selected, "values")
                # print(selected_values)

                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #fetch the leave record detail to see status
                    cur.execute("select leave_id, edate from student_leave where rollno = %s and student_name = %s and message = %s and no_days = %s and status = %s", selected_values)

                    pending_record = cur.fetchall()
                
                    for record in pending_record:
                        # #update the leave status
                        cur.execute("update student_leave set status = 'Approve' where leave_id = %s and edate = %s", (record[0], record[1]))

                    # commit the changes
                    con.commit()

                    destroy_new_leave_frame()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error :", e)
            
            #=========reject new record===============#
            def reject_new_record():
                reject_selected = self.new_leave_tree.selection()
                reject_selected_values = self.new_leave_tree.item(reject_selected, "values")
     
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    # #fetch the leave record detail to see status
                    cur.execute("select leave_id, edate from student_leave where rollno = %s and student_name = %s and message = %s and no_days = %s and status = %s", reject_selected_values)

                    pending_record = cur.fetchall()
   
                    for record in pending_record:
                        # #update the leave status
                        cur.execute("update student_leave set status = 'Reject' where leave_id = %s and edate = %s", (record[0], record[1]))

                    #commit the changes
                    con.commit()

                    destroy_new_leave_frame()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error :", e)

            #=====destroy the frame============#
            def destroy_new_leave_frame():
                self.new_leave_frame.destroy()

            #=======treeview setting========#
            #add some style
            style = ttk.Style()

            #pick a theme
            style.theme_use("alt")

            #configure the tree view color
            style.configure("Treeview", 
                                background = "#EEF0E5",
                                rowheight = 25,
                                fieldbackground = "#F3FBF1", font = ("Consolas", 14))
                
            style.configure("mystyle.Treeview", font=('Consolas', 15))

            #configure the selected color
            style.configure("Treeview", background = [("selected", "#347083")])

            #increse the font size of heading
            style.configure("Treeview.Heading", font=("Consolas", 18))

            self.data_frame = tk.Frame(self.new_leave_frame, bg = "lightgrey", borderwidth=0, relief="solid")
            self.data_frame.pack_propagate(False)
            self.data_frame.place(x = 10, y = 5, height = 200, width = 1320)

            #create a scrollbar
            y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
            x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

            y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
            x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

            #create a treeview
            self.new_leave_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
            self.new_leave_tree.pack(fill = "both", expand= True)

            #configure the scrollbar
            x_scroll.config(command = self.new_leave_tree.xview)
            y_scroll.config(command = self.new_leave_tree.yview)

            #define our columns
            self.new_leave_tree["columns"] = ("Roll No", "Student Name", "Subject", "Days","Status")

            #format column
            self.new_leave_tree.column("Roll No", anchor="center", width = 50, minwidth=50)
            self.new_leave_tree.column("Student Name", anchor="center", width = 150, minwidth=150)
            self.new_leave_tree.column("Subject", anchor="center", width = 300, minwidth = 300)
            self.new_leave_tree.column("Days", anchor="center", width = 50, minwidth = 50)
            self.new_leave_tree.column("Status", anchor="center", width = 100, minwidth = 100)
                
            #create a heading
            self.new_leave_tree.heading("Roll No", text = "Roll No", anchor = "center")
            self.new_leave_tree.heading("Student Name", text = "Student Name", anchor = "center")
            self.new_leave_tree.heading("Subject", text = "Subject", anchor = "center")
            self.new_leave_tree.heading("Days", text = "Days", anchor = "center")
            self.new_leave_tree.heading("Status", text = "Status", anchor = "center")
                
            #Create striped to our tages
            self.new_leave_tree.tag_configure("evenrow", background="#D875C7")
            self.new_leave_tree.tag_configure("oddrow", background="white")

            self.approve_button = ctk.CTkButton(self.new_leave_frame, text = "Approve", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  approve_new_record,fg_color="#912BBC", text_color="white", hover_color="#8D007B")
            self.approve_button.place(x=10,y=180)

            self.reject_button = ctk.CTkButton(self.new_leave_frame, text = "Reject", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  reject_new_record,fg_color="#912BBC", text_color="white", hover_color="#8D007B")
            self.reject_button.place(x=150,y=180)

            #=======calling the function==========#
            show_new_leave_record()

            self.new_leave_frame.place(x =10, y = 170)

        def student_approve_leave_frame():
            #=====inside frame======#
            self.approve_leave_frame = ctk.CTkFrame(self.leave_page_frame, width = 1072, height=270, corner_radius=0,  border_width=0, border_color="green", fg_color="white")

            #====================function====================#
            def show_approve_leave_record():
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #fetch the leave record detail to see status
                    cur.execute("select rollno, student_name, message, no_days, status from student_leave where status = 'Approve'")

                    records = cur.fetchall()
                    total_approve_leave_count = len(records)

                    self.count = 0
                    #show record in treeview
                    for record in records:
                        if self.count %2 == 0:
                            self.approve_leave_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], record[1], record[2], record[3], record[4]), tags=("evenrow",))
                        else:
                            self.approve_leave_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], record[1], record[2], record[3], record[4]), tags=("oddrow",))
                        self.count += 1

                    #=====configure the count label============#
                    self.total_leave_label.configure(text = f"Total Approve Leave = {total_approve_leave_count}")
                    
                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error :", e)

            #=========reject new record===============#
            def reject_approve_record():
                reject_selected = self.approve_leave_tree.selection()
                reject_selected_values = self.approve_leave_tree.item(reject_selected, "values")

                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    # #fetch the leave record detail to see status
                    cur.execute("select leave_id, edate from student_leave where rollno = %s and student_name = %s and message = %s and no_days = %s and status = %s", reject_selected_values)

                    pending_record = cur.fetchall()
                    for record in pending_record:
                        # #update the leave status
                        cur.execute("update student_leave set status = 'Reject' where leave_id = %s and edate = %s", (record[0], record[1]))

                    #commit the changes
                    con.commit()

                    destroy_approve_leave_frame()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error :", e)

            #=====destroy the frame============#
            def destroy_approve_leave_frame():
                self.approve_leave_frame.destroy()
            
            #=======treeview setting========#
            #add some style
            style = ttk.Style()

            #pick a theme
            style.theme_use("alt")

            #configure the tree view color
            style.configure("Treeview", 
                            background = "#EEF0E5",
                            rowheight = 25,
                            fieldbackground = "#F3FBF1", font = ("Consolas", 14))
            
            style.configure("mystyle.Treeview", font=('Consolas', 15))

            #configure the selected color
            style.map("Treeview", 
                background=[("selected", "#912BBC")],
                foreground=[("selected", "white")])

            #increse the font size of heading
            style.configure("Treeview.Heading", font=("Consolas", 18))

            self.data_frame = tk.Frame(self.approve_leave_frame, bg = "lightgrey", borderwidth=0, relief="solid")
            self.data_frame.pack_propagate(False)
            self.data_frame.place(x = 10, y = 5, height = 200, width = 1320)

            #create a scrollbar
            y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
            x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

            y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
            x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

            #create a treeview
            self.approve_leave_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
            self.approve_leave_tree.pack(fill = "both", expand= True)

            #configure the scrollbar
            x_scroll.config(command = self.approve_leave_tree.xview)
            y_scroll.config(command = self.approve_leave_tree.yview)

            #define our columns
            self.approve_leave_tree["columns"] = ("Roll No", "Student Name", "Subject", "Days", "Status")

            #format column
            self.approve_leave_tree.column("Roll No", anchor="center", width = 50, minwidth=50)
            self.approve_leave_tree.column("Student Name", anchor="center", width = 150, minwidth=150)
            self.approve_leave_tree.column("Subject", anchor="center", width = 300, minwidth = 300)
            self.approve_leave_tree.column("Days", anchor="center", width = 50, minwidth = 50)
            self.approve_leave_tree.column("Status", anchor="center", width = 100, minwidth = 100)
            
            #create a heading
            self.approve_leave_tree.heading("Roll No", text = "Roll No", anchor = "center")
            self.approve_leave_tree.heading("Student Name", text = "Student Name", anchor = "center")
            self.approve_leave_tree.heading("Subject", text = "Subject", anchor = "center")
            self.approve_leave_tree.heading("Days", text = "Days", anchor = "center")
            self.approve_leave_tree.heading("Status", text = "Status", anchor = "center")
            
            #Create striped to our tages
            self.approve_leave_tree.tag_configure("evenrow", background="#D875C7")
            self.approve_leave_tree.tag_configure("oddrow", background="white")

            self.reject_button = ctk.CTkButton(self.new_leave_frame, text = "Reject", width = 120, height = 38, font = ("Verdana Pro", 17), cursor = "hand2", command =  reject_approve_record,fg_color="#912BBC", text_color="white", hover_color="#8D007B")
            self.reject_button.place(x=10,y=180)

            #======calling the function===============#
            show_approve_leave_record()

            self.approve_leave_frame.place(x =10, y = 170)

        def student_reject_leave_frame():
            #=====inside frame======#
            self.reject_leave_frame = ctk.CTkFrame(self.leave_page_frame, width = 1072, height=270, corner_radius=0,  border_width=0, border_color="green", fg_color="white")

            def show_reject_leave_record():
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    #fetch the leave record detail to see status
                    cur.execute("select rollno, student_name, message, no_days, status from student_leave where status = 'Reject'")

                    records = cur.fetchall()
                    total_reject_leave_count = len(records)

                    self.count = 0
                    #show record in treeview
                    for record in records:
                        if self.count %2 == 0:
                            self.reject_leave_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], record[1], record[2], record[3], record[4]), tags=("evenrow",))
                        else:
                            self.reject_leave_tree.insert(parent = "", index = tk.END, iid = self.count, values=(record[0], record[1], record[2], record[3], record[4]), tags=("oddrow",))
                        self.count += 1

                    self.total_leave_label.configure(text = f"Total Reject Leave = {total_reject_leave_count}")
                    
                    #commit the changes
                    con.commit()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error :", e)
            
            #=======treeview setting========#
            #add some style
            style = ttk.Style()

            #pick a theme
            style.theme_use("alt")

            #configure the tree view color
            style.configure("Treeview", 
                            background = "#EEF0E5",
                            rowheight = 25,
                            fieldbackground = "#F3FBF1", font = ("Consolas", 14))
            
            style.configure("mystyle.Treeview", font=('Consolas', 15))

            #configure the selected color
            style.map("Treeview", 
                background=[("selected", "#912BBC")],
                foreground=[("selected", "white")])

            #increse the font size of heading
            style.configure("Treeview.Heading", font=("Consolas", 18))

            self.data_frame = tk.Frame(self.reject_leave_frame, bg = "lightgrey", borderwidth=0, relief="solid")
            self.data_frame.pack_propagate(False)
            self.data_frame.place(x = 10, y = 5, height = 200, width = 1320)

            #create a scrollbar
            y_scroll = tk.Scrollbar(self.data_frame, orient="vertical")
            x_scroll = tk.Scrollbar(self.data_frame, orient="horizontal")

            y_scroll.pack(side = tk.RIGHT, fill = tk.Y)
            x_scroll.pack(side = tk.BOTTOM, fill = tk.X)

            #create a treeview
            self.reject_leave_tree = ttk.Treeview(self.data_frame, show = "headings",selectmode="extended", xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set, style="mystyle.Treeview")
            self.reject_leave_tree.pack(fill = "both", expand= True)

            #configure the scrollbar
            x_scroll.config(command = self.reject_leave_tree.xview)
            y_scroll.config(command = self.reject_leave_tree.yview)

            #define our columns
            self.reject_leave_tree["columns"] = ("Roll No", "Student Name", "Subject", "Days", "Status")

            #format column
            self.reject_leave_tree.column("Roll No", anchor="center", width = 50, minwidth=50)
            self.reject_leave_tree.column("Student Name", anchor="center", width = 150, minwidth=150)
            self.reject_leave_tree.column("Subject", anchor="center", width = 300, minwidth = 300)
            self.reject_leave_tree.column("Days", anchor="center", width = 50, minwidth = 50)
            self.reject_leave_tree.column("Status", anchor="center", width = 100, minwidth = 100)
            
            #create a heading
            self.reject_leave_tree.heading("Roll No", text = "Roll No", anchor = "center")
            self.reject_leave_tree.heading("Student Name", text = "Student Name", anchor = "center")
            self.reject_leave_tree.heading("Subject", text = "Subject", anchor = "center")
            self.reject_leave_tree.heading("Days", text = "Days", anchor = "center")
            self.reject_leave_tree.heading("Status", text = "Status", anchor = "center")
            
            #Create striped to our tages
            self.reject_leave_tree.tag_configure("evenrow", background="#D875C7")
            self.reject_leave_tree.tag_configure("oddrow", background="white")

            #=========calling the function===========#
            show_reject_leave_record()

            self.reject_leave_frame.place(x =10, y = 170)

        #=======other widgets==========#
        self.new_leave_report_button = ctk.CTkButton(self.leave_page_frame, text = "New Leave Report", width =250, height = 45,font = ("Verdana Pro", 18), cursor = "hand2", command = student_new_leave_frame, fg_color="#912BBC", text_color="white", hover_color="#8D007B", corner_radius=2)
        self.new_leave_report_button.place(x=10,y=80) 

        self.approve_leave_button = ctk.CTkButton(self.leave_page_frame, text = "Approve Leave", width =250, height = 45,font = ("Verdana Pro", 18), cursor = "hand2", command = student_approve_leave_frame, fg_color="#912BBC", text_color="white", hover_color="#8D007B", corner_radius=2)
        self.approve_leave_button.place(x=270,y=80)

        self.reject_leave_report_button = ctk.CTkButton(self.leave_page_frame, text = "Reject Leave", width =250, height = 45,font = ("Verdana Pro", 18), cursor = "hand2", command = student_reject_leave_frame, fg_color="#912BBC", text_color="white", hover_color="#8D007B", corner_radius=2)
        self.reject_leave_report_button.place(x=530,y=80)

        self.total_leave_label = ctk.CTkLabel(self.leave_page_frame, text = "Total Reject Leave = 0", font = ("Verdana Pro", 18), text_color="#912BBC")
        self.total_leave_label.place(x = 15, y = 140)

        #=======calling the function===========#
        student_new_leave_frame()

        self.leave_page_frame.place(x=0,y=0)

    def student_notes_frame(self):
        self.notes_page_frame = ctk.CTkFrame(self.rightside_frame, width = 1092, height=700, corner_radius=0,  border_width=1, border_color="green", fg_color="white")
        ChangeLabel(self.notes_page_frame,text="Upload Materials", fg_color="#912BBC", text_color="white")
        
        #======function for upload notes==========#
        def shared_material_frame():
            #=====inside frame======#
            self.upload_notes_frame = ctk.CTkFrame(self.notes_page_frame, width = 1072, height=585, corner_radius=0,  border_width=0, border_color="violet", fg_color="white")

            def fetch_std_values():
                global cur
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()
                    
                    # fetch std and div
                    cur.execute("select d.std_name , d.div_name from teacher_assignments ta, division d, staff t where t.srno = ta.srno and d.div_id = ta.std_div_id and concat(t.first_name,'@',staff_id) = %s", (teacher_password,))

                    result = cur.fetchall()
                    
                    std_list = []
                    div_list = []

                    for res in result:
                        std_list.append(res[0])
                        div_list.append(res[1])

                    fetch_std_option.configure(values = std_list)
                    fetch_div_option.configure(values = div_list)

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error :", e)

            def check_std_div():
                global cur, records
                std = fetch_std_var.get()
                div = fetch_div_var.get()

                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    #create a cursor instance
                    cur = con.cursor()

                    cur.execute("select d.std_name, d.div_name, d.div_id, s.srno from teacher_assignments ta, division d, staff s where ta.std_div_id = d.div_id and ta.srno = s.srno and d.std_name = %s and d.div_name = %s and concat(s.first_name,'@',s.staff_id) = %s", (std, div, teacher_password))

                    records = cur.fetchone()
                    print(records)

                    if records:
                        open_new_frame()
                    else:
                        messagebox.showerror("Error", "Invalid Selection of std and div.")

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error :", e)

            def open_new_frame():
                upload_frame = ctk.CTkFrame(self.upload_notes_frame, width = 950, height=540, corner_radius=0,  border_width=0, border_color="violet", fg_color="white")
                upload_frame.place(x = 1, y = 50)

                #====function=======#
                def open_file(event = None):
                    global file_path, file_name
                    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("PDF Files", "*.pdf"),("Text Files", "*.txt")], initialdir="C:/Users/vikas/OneDrive/Documents", title="Open File")

                    if os.path.basename(f"{file_path}").endswith(".pdf") or os.path.basename(f"{file_path}").endswith(".txt"):

                        # opening document
                        doc = fitz.open(f"{file_path}")

                        text = ""
                        for page in doc:
                            text += page.get_text()

                        # get basename of file
                        title = os.path.basename(f"{file_path}")
                        file_name = os.path.splitext(title)

                        note_title.delete(0, tk.END)
                        note_content_textbox.delete("0.0", tk.END)
                        note_content_textbox.insert(tk.END, text)
                        note_title.insert(tk.END, title)
                    
                    else:
                        message = "The file type is not supported. Please upload a PDF or Text Document."
                        messagebox.showerror("File Type Check",message=message)

                # function for extract file type from path

                # friendly file type mime
                friendly_mime_type = {
                    'application/pdf': 'PDF Document',
                    'text/plain': 'Text Document',
                }
                def get_file_type(file_path):
                    # Guess the MIME type of the file based on the file extension
                    mime_type, _ = mimetypes.guess_type(file_path)
                    friendly_file_name = friendly_mime_type.get(mime_type, mime_type)
                    return friendly_file_name

                def upload_file():
                    global records
                    try:
                        con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                        #create a cursor instance
                        cur = con.cursor()

                        std_div_id = records[2]
                        teacher_id = records[3]

                        file_type = get_file_type(file_path)

                        #insert this data into database
                        insert_query = "insert into notes(teacher_id, std_div_id, file_name, file_path, file_type) values(%s, %s,%s,%s,%s)"
                        insert_value = (teacher_id, std_div_id,file_name[0],file_path,file_type)

                        cur.execute(insert_query, insert_value)

                        con.commit()

                        messagebox.showinfo("Success", "Your notes have been uploaded successfully!")

                        #close the connection
                        con.close()

                    except Exception as e:
                        print("Error :", e)
                    
                #========textbox===========#
                note_title = ctk.CTkEntry(upload_frame, width = 620, height = 40, corner_radius=5, border_width = 1, border_color="black", placeholder_text="Note Title", font = ("Verdana Pro", 17))
                note_title.place(x = 1, y = 10)

                # upload button
                import_button = ctk.CTkButton(upload_frame, text = "Import Pdf/Text", font = ("Verdana Pro", 17), fg_color="transparent", text_color="black", height = 35, hover_color="#912BBC", command = open_file)
                import_button.place(x = 660, y = 10)
                import_button.bind("<Enter>", lambda e : import_button.configure(fg_color="#912BBC", text_color = "white"))
                import_button.bind("<Leave>", lambda e : import_button.configure(fg_color="white", text_color = "black"))

                # notes frame
                content_frame = tk.Frame(upload_frame)
                content_frame.place(x = 1, y = 85, width=800, height = 480)

                # set scrollbar
                y_scroll= tk.Scrollbar(content_frame)
                y_scroll.pack(side = tk.RIGHT, fill= tk.Y)

                # # content textbox
                note_content_textbox = tk.Text(content_frame, font = ("Verdana Pro", 16), yscrollcommand=y_scroll.set, highlightthickness=2, highlightbackground="violet", wrap = "word",padx = 10, pady = 10)
                note_content_textbox.pack(fill = tk.BOTH, expand = True)
                y_scroll.config(command = note_content_textbox.yview)
    
                # upload button
                upload_button = ctk.CTkButton(upload_frame, text = "Upload", font = ("Verdana Pro", 17), fg_color="#912BBC", text_color="white", height = 38, hover_color="#912BBC", command = upload_file, corner_radius=2)
                upload_button.place(x = 1, y = 480)

            #======std_optionmenu==========#
            fetch_std_var = tk.StringVar(value = "")
            fetch_std_option = ctk.CTkOptionMenu(self.upload_notes_frame, width = 220, height = 30, corner_radius=2, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=fetch_std_var, button_color="#912BBC", button_hover_color="#912BBC")
            fetch_std_option.place(x = 10, y = 10)

            fetch_div_var = tk.StringVar(value = "")
            fetch_div_option = ctk.CTkOptionMenu(self.upload_notes_frame, width = 220, height = 30, corner_radius=2, fg_color="#D8D9DA", text_color="black", dropdown_font=("Verdana Pro", 15), font=("Verdana Pro", 18), variable=fetch_div_var, button_color="#912BBC", button_hover_color="#912BBC")
            fetch_div_option.place(x = 250, y = 10)

            fetch_button = ctk.CTkButton(self.upload_notes_frame, text = "Select", font = ("Verdana Pro", 17), fg_color="#912BBC", text_color="white", height = 38, hover_color="#912BBC", command = check_std_div, width = 120)
            fetch_button.place(x = 570, y = 10)

            #===calling the function=======#
            fetch_std_values()

            self.upload_notes_frame.place(x = 10, y = 105)

        #=====function for viewing notes========#
        def view_material_frame():
            self.view_notes_frame = ctk.CTkFrame(self.notes_page_frame, width = 1072, height=585, corner_radius=0,  border_width=0, border_color="violet", fg_color="white")

            # view notes frame
            table_frame = ctk.CTkScrollableFrame(self.view_notes_frame, width = 900, height = 400, corner_radius=0, border_width=2, border_color="black")
            table_frame.pack(pady = 50)

            #fetch all values of uploaded notes
            def fetch_notes():
                global results
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    # create a cursor instance
                    cur = con.cursor()

                    cur.execute("select file_name, file_type, date(upload_date), concat(d.std_name,' ',d.div_name) from notes n, staff s, division d where n.teacher_id = s.srno and n.std_div_id = d.div_id and CONCAT(s.first_name, '@', s.staff_id) = %s", (teacher_password,))

                    results = cur.fetchall()

                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error :", e)

            # call the function
            fetch_notes()

            column_widths = {
                "NAME":300,
                "TYPE":250,
                "STD-DIV": 150,
                "DATE":200,    
            }

            name_list = []
            type_list = []
            class_list = []
            date_list = []
            for i in results:
                name_list.append(i[0])
                type_list.append(i[1])
                date_list.append(i[2])
                class_list.append(i[3])

            def open_file_in_browser(name):
                try:
                    con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

                    # create a cursor instance
                    cur = con.cursor()

                    cur.execute("select file_path from notes n, staff s where n.file_name = %s and  concat(s.first_name,'@',s.staff_id) = %s", (name, teacher_password,))

                    results = cur.fetchone()
                    
                    #close the connection
                    con.close()

                except Exception as e:
                    print("Error :", e)

                fetched_path = results[0]

                # convert path to url formats
                file_url = "file://" + os.path.abspath(fetched_path)

                # open the file in browser
                webbrowser.open_new(file_url)

            #======uploaded notes button============#
            column_list = ["NAME", "TYPE", "STD-DIV", "DATE"]
            for i, col in enumerate(column_list):
                column_var = tk.StringVar(value = col)
                width = column_widths.get(col, 150)
                column_box = ctk.CTkEntry(table_frame, font = ("Helvetica", 17), border_width=1, border_color = "black", width = width, height = 40, textvariable=column_var, corner_radius=0, justify = "center", state = "readonly", fg_color="#176B87", text_color="white")
                column_box.grid(row = 0, column = i)

            for i, name in enumerate(name_list):
                name_box = ctk.CTkButton(table_frame, font = ("Helvetica", 17), border_width=1, border_color="black", width = 300, height = 42, text = name, corner_radius=0, fg_color="#F6F5F5", text_color = "black", hover = tk.DISABLED, command = lambda n = name: open_file_in_browser(n))
                name_box.grid(row = i+1, column = 0)

            for i, type_file in enumerate(type_list):
                type_var = tk.StringVar(value = type_file)
                type_box = ctk.CTkEntry(table_frame, font = ("Helvetica", 17), border_width=1, border_color = "black", width =250, height = 42, textvariable=type_var, corner_radius=0, state = "readonly", fg_color="#F6F5F5", text_color="black")
                type_box.grid(row = i+1, column = 1)

            for i, class_file in enumerate(class_list):
                class_var = tk.StringVar(value = class_file)
                class_box = ctk.CTkEntry(table_frame, font = ("Helvetica", 17), border_width=1, border_color = "black", width =150, height = 42, textvariable=class_var, corner_radius=0, state = "readonly", fg_color="#F6F5F5", text_color="black")
                class_box.grid(row = i+1, column = 2)

            for i, date_file in enumerate(date_list):
                date_var = tk.StringVar(value = date_file)
                date_box = ctk.CTkEntry(table_frame, font = ("Helvetica", 17), border_width=1, border_color = "black", width =200, height = 42, textvariable=date_var, corner_radius=0, state = "readonly", fg_color="#F6F5F5", text_color="black")
                date_box.grid(row = i+1, column = 3)

            self.view_notes_frame.place(x = 10, y = 105)
            self.view_notes_frame.pack_propagate(False)

        self.upload_notes_button = ctk.CTkButton(self.notes_page_frame, text = "Share Materials", width =250, height = 45,font = ("Verdana Pro", 18), cursor = "hand2", command = shared_material_frame, fg_color="#912BBC", text_color="white", hover_color="#8D007B", corner_radius=2)
        self.upload_notes_button.place(x=10,y=60)

        self.notes_report_button = ctk.CTkButton(self.notes_page_frame, text = "View Materials", width =250, height = 45,font = ("Verdana Pro", 18), cursor = "hand2", command = view_material_frame, fg_color="#912BBC", text_color="white", hover_color="#8D007B", corner_radius=2)
        self.notes_report_button.place(x=280,y=60)

        self.notes_page_frame.place(x=0,y=0)

class AnnouncementWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__(fg_color="#EAFDFC")
        self.geometry("1536x864-10-7")
        self.title("School Management System")
        self.after(200, lambda : self.iconbitmap("image/slogo.ico"))
        #========heading frame=================#
        self.heading_frame = HeadingFrame(self)
        self.heading_frame.place(x = 5, y = 5)

        def return_to_main():
            self.destroy()
            root.deiconify()

        def underline_to_label(event):
            self.underline_label = tk.Label(self,bg="blue")
            self.underline_label.place(x = 69, y = 185, width = 50, height=4)

        def noline_to_label(event):
            self.underline_label = tk.Label(self,bg="#EAFDFC")
            self.underline_label.place(x = 69, y = 185, width = 50, height=4)


        #======back button==========#
        self.back_button = ctk.CTkButton(self, text = "< Back",width = 0, height = 0, font = ("Consolas", 18), text_color="blue", hover = "disabled", cursor = "hand2", fg_color="transparent" , command = return_to_main)
        self.back_button.place(x = 20, y = 120)
        self.back_button.bind("<Enter>", underline_to_label)
        self.back_button.bind("<Leave>", noline_to_label)

        head_label = ctk.CTkLabel(self, text = f"Notice & Events", font = ("Verdana Pro", 30,), text_color="#03346E")
        head_label.place(x = 620, y = 140)

        self.tab_frame = ctk.CTkFrame(self, width = 820, height = 60, fg_color="white", corner_radius=10, border_width=2, border_color="#B0A695")
        self.tab_frame.place(x = 350, y = 200)
        self.tab_frame.grid_propagate(False)

        def button_click(btn):
            notice_image2 = SetImage(image_path="image/sticky_note2.png", width = 25, height = 25)
            event_image2 = SetImage(image_path="image/event_calendar2.png", width = 28, height = 28)
            if btn == 1:
                notice_button.configure(fg_color = "#134B70", text_color = "white", image = notice_image)
                event_button.configure(fg_color = "white", text_color = "black", image = event_image)
                notice_page()
            else:
                notice_button.configure(fg_color = "white", text_color = "black", image = notice_image2)
                event_button.configure(fg_color = "#134B70", text_color = "white", image = event_image2)
                event_page()

        try:
            con = mycon.connect(host = "localhost", username = "root", password = "root", port = 3307, database = "software")

            #create a cursor instance
            cur = con.cursor()

            cur.execute("select announcement_subject, announcement_content, date_format(edate, '%d %M, %Y') as date from announcement where type = 'Notice'")
            notice_data = cur.fetchall()
            
            cur.execute("select announcement_subject, announcement_content, date_format(event_date, '%d %M, %Y') as date from announcement where type = 'Event'")
            event_data = cur.fetchall()
            #close the connection
            con.close()

        except Exception as e:
            print("Error ", e)

        notice_date = [row[2] for row in notice_data]
        notice_title = [row[0] for row in notice_data]
        notice_cont = [row[1] for row in notice_data]
        event_date = [row[2] for row in event_data]
        event_title = [row[0] for row in event_data]
        event_cont = [row[1] for row in event_data]

        def notice_page():
            notice_frame = ctk.CTkScrollableFrame(self, width = 800, height = 500, fg_color="white", corner_radius=2, border_width=2, border_color="#B6C4B6")

            for i, col in enumerate(notice_date):
                frame1 = ctk.CTkFrame(notice_frame,width = 160, height = 70 ,fg_color="#EEEEEE", corner_radius=0)
                image = SetImage(image_path="image/notice_calendar.png", width = 25, height = 25)
                line_image = SetImage(image_path="image/line.png", width = 3, height = 69)
                line_label = ctk.CTkLabel(frame1, text = "", image = line_image)
                line_label.place(x = 0, y = 0)

                image_label = ctk.CTkLabel(frame1, text = "", image = image)
                image_label.grid(row = 0, column = 0, sticky = "w", padx = 7,pady = (5,0))

                date_label = ctk.CTkLabel(frame1, text = f"{col}", font = ("Verdana Pro", 16), text_color="#03346E")
                date_label.grid(row = 1, column = 0, padx = 7)
                frame1.grid(row = i, column = 0, padx = (10,0), pady = 2)

                frame2 = ctk.CTkFrame(notice_frame,width = 620, height = 70 ,fg_color="#EEEEEE",corner_radius=0)
                title_label = ctk.CTkLabel(frame2, text = f"{notice_title[i]}", font = ("Verdana Pro", 20), text_color="black")
                title_label.grid(row = 0, column = 0, sticky = "w", padx = 30,pady = (5,0))

                content_label = ctk.CTkLabel(frame2, text = f"{notice_cont[i]}", font = ("Verdana Pro", 14), text_color="black", wraplength=600, anchor = "w")
                content_label.grid(row = 1, column = 0, padx = 30, sticky = "w")
                frame2.grid(row = i , column = 1, pady = 2)
                frame2.grid_propagate(False)
                frame1.grid_propagate(False)
                
            notice_frame.place(x = 350, y = 280)
        
        def event_page():
            event_frame = ctk.CTkScrollableFrame(self, width = 800, height = 500, fg_color="white", corner_radius=2, border_width=2, border_color="#B6C4B6")

            for i, col in enumerate(event_date):
                frame1 = ctk.CTkFrame(event_frame, width = 160, height = 70 ,fg_color="#EEEEEE", corner_radius=0)
                image = SetImage(image_path="image/notice_calendar.png", width = 25, height = 25)
                line_image = SetImage(image_path="image/line.png", width = 3, height = 69)
                line_label = ctk.CTkLabel(frame1, text = "", image = line_image)
                line_label.place(x = 0, y = 0)

                image_label = ctk.CTkLabel(frame1, text = "", image = image)
                image_label.grid(row = 0, column = 0, sticky = "w", padx = 7,pady = (5,0))

                date_label = ctk.CTkLabel(frame1, text = f"{col}", font = ("Verdana Pro", 16), text_color="#03346E")
                date_label.grid(row = 1, column = 0, padx = 7)
                frame1.grid(row = i, column = 0, padx = (10,0), pady = 2)

                frame2 = ctk.CTkFrame(event_frame,width = 620, height = 70 ,fg_color="#EEEEEE",corner_radius=0)
                title_label = ctk.CTkLabel(frame2, text = f"{event_title[i]}", font = ("Verdana Pro", 20), text_color="black")
                title_label.grid(row = 0, column = 0, sticky = "w", padx = 30,pady = (5,0))

                content_label = ctk.CTkLabel(frame2, text = f"{event_cont[i]}", font = ("Verdana Pro", 14), text_color="black", wraplength=595, anchor = "w")
                content_label.grid(row = 1, column = 0, padx = 30, sticky = "w")
                frame2.grid(row = i , column = 1, pady = 2)
                frame2.grid_propagate(False)
                frame1.grid_propagate(False)
            event_frame.place(x = 350, y = 280)

        notice_page()

        notice_image = SetImage(image_path="image/sticky-note.png", width = 25, height = 25)
        notice_button = ctk.CTkButton(self.tab_frame, text = "Notice",width = 400, height = 51, font = ("Verdana Pro", 20, "bold"), text_color="white", hover = "disabled", cursor = "hand2", fg_color="#134B70", corner_radius=100, command = lambda : button_click(1), image = notice_image)
        notice_button.grid(row = 0, column = 0, pady = 4, padx = (5, 0))

        event_image = SetImage(image_path="image/event_calendar.png", width = 28, height = 28)
        event_button = ctk.CTkButton(self.tab_frame, text = "Upcoming Events",width = 400, height = 51, font = ("Verdana Pro", 20, "bold"), text_color="black", hover = "disabled", cursor = "hand2", fg_color="white", corner_radius=100, command = lambda : button_click(2), image = event_image)
        event_button.grid(row = 0, column = 1, pady = 4,padx = (0, 5))

class ContactUsWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__(fg_color="white")
        self.geometry("1536x864-10-7")
        self.title("School Management System")
        self.after(200, lambda : self.iconbitmap("image/slogo.ico"))

        def return_to_main():
            self.destroy()
            root.deiconify()

        def underline_to_label(event):
            self.underline_label = tk.Label(self,bg="blue")
            self.underline_label.place(x = 69, y = 185, width = 50, height=4)

        def noline_to_label(event):
            self.underline_label = tk.Label(self,bg="white")
            self.underline_label.place(x = 69, y = 185, width = 50, height=4)

        #======back button==========#
        self.back_button = ctk.CTkButton(self, text = "⬅️ Back",width = 0, height = 0, font = ("Consolas", 18), text_color="blue", hover = "disabled", cursor = "hand2", fg_color="transparent" , command = return_to_main)
        self.back_button.place(x = 20, y = 120)
        self.back_button.bind("<Enter>", underline_to_label)
        self.back_button.bind("<Leave>", noline_to_label)

        #======calling heading label class =======#
        self.heading_frame = HeadingFrame(self)
        self.heading_frame.place(x = 5, y = 5)

        self.contact_label = ctk.CTkLabel(self, text = "Connect With Us", width = 670, height =45, font = ("Consolas",25), text_color="white", fg_color="red", anchor = "center")
        self.contact_label.place(x = 350, y = 100)

        self.contact_label = tk.Label(self,bg="black")
        self.contact_label.place(x = 438, y = 180, width = 836, height=4)

        #=======create a frame=========#
        self.contact_frame = ctk.CTkFrame(self, width = 670, height = 620, fg_color="white", corner_radius=2, border_width=2, border_color="green")

        def image_label(image_path, label, image_y, label_y):
            self.contact_us_image = ctk.CTkImage(light_image=Image.open(f"{image_path}"), dark_image=Image.open(f"{image_path}"), size = (40, 40))
                
            self.image_label = ctk.CTkLabel(self.contact_frame, text = "", image = self.contact_us_image, fg_color="transparent")
            self.image_label.place(x = 20, y = image_y)

            #========label===========#
            self.label = ctk.CTkLabel(self.contact_frame, text = label, font = ("Consolas", 17), anchor="w")
            self.label.place(x = 80, y = label_y)
        
        #=========address icon===========#
        self.address_label = "Vivekanand Vidya Bhavan English High School, Aadarsh\n Society,Chembur, Mumbai 400071, India"
        image_label(image_path="image/address.png", label =self.address_label, image_y=43, label_y=45)

        #========contact icon=========#
        self.phone_label = "+91 9619148774 / 7021151536"
        image_label(image_path="image/phone.png", label =self.phone_label, image_y=103, label_y=107)

        #========mail icon=========#
        self.mail_label = "vvb.admin@gmail.com"
        image_label(image_path="image/email.png", label =self.mail_label, image_y=163, label_y=169)

        #===========map frame============#
        self.map_frame1 = tk.LabelFrame(self.contact_frame, width=670, height=370, highlightthickness=0)

        self.map_widget = tkintermapview.TkinterMapView(self.map_frame1, width = 850, height=480, corner_radius=0)

        #=========set cordinates=======#
        self.map_widget.set_position(19.0481, 72.8900, text = "Vivekanand Vidya Bhavan")

        #=======set marker===============#
        self.map_widget.set_marker(19.0481, 72.8900, text = "Vivekanand Vidya Bhavan")

        self.map_widget.pack(fill = "both")
        self.map_frame1.place(x = 0, y = 290)
        self.contact_frame.place(x = 350, y = 190)
                
class AskAQuestionWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__(fg_color="#ff914d")
        self.geometry("1536x864-10-7")
        self.title("School Management System")

        #========heading frame=================#
        self.heading_frame = HeadingFrame(self)
        self.heading_frame.place(x = 5, y = 5)

        def return_to_main():
            self.destroy()
            root.deiconify()

        def underline_to_label(event):
            self.underline_label = tk.Label(self,bg="white")
            self.underline_label.place(x = 69, y = 185, width = 50, height=4)

        def noline_to_label(event):
            self.underline_label = tk.Label(self,bg="#ff914d")
            self.underline_label.place(x = 69, y = 185, width = 50, height=4)

        #======back button==========#
        self.back_button = ctk.CTkButton(self, text = "⬅️ Back",width = 0, height = 0, font = ("Consolas", 18), text_color="white", hover = "disabled", cursor = "hand2", fg_color="transparent" , command = return_to_main)
        self.back_button.place(x = 20, y = 120)
        self.back_button.bind("<Enter>", underline_to_label)
        self.back_button.bind("<Leave>", noline_to_label)

        def send():
            result = wikipedia.summary(self.search_box.get("1.0",tk.END), sentences = 3)
            self.answer_label.configure(text=result)

        def speak():
            engine=pyttsx3.init()
            voices=engine.getProperty('voices')
            engine.setProperty('voice',voices[1].id)
            engine.say(self.answer_label.cget("text"))
            engine.runAndWait()
        
        def mic():
            # Initialize the recognizer
            recognizer = sr.Recognizer()

            # Capture audio from the microphone
            with sr.Microphone() as source:
                audio = recognizer.listen(source)

            # Recognize speech using Google Web Speech API
            try:
                text=recognizer.recognize_google(audio)
                self.search_box.insert(tk.END,text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

        self.main_frame = ctk.CTkFrame(self,width=900,height=700,fg_color="white",corner_radius=5)

        #Heading
        self.heading_label=ctk.CTkLabel(self.main_frame,text="What’s on Your Mind? Ask a Question!",font=("MS Reference Sans Serif",20))
        self.heading_label.place(x=250,y=10)

        #question Frame
        self.question_frame=ctk.CTkScrollableFrame(self.main_frame,width=800,height=400,border_color="black",fg_color="#272829",border_width=2,corner_radius=2, label_text="Response to Your Question", label_font=("Verdana Pro", 18))

        # Answer Label
        self.answer_label=ctk.CTkLabel(self.question_frame,text="",wraplength=700,font=("Verdana Pro",16), text_color="white", anchor="nw")
        self.answer_label.pack()
        self.question_frame.place(x=30,y=50)

        #enter label
        self.enter_label=ctk.CTkLabel(self.main_frame,text="Got a Question? Type it Below!",font=("Verdana Pro",18))
        self.enter_label.place(x=30,y=500)

        # Textbox
        self.search_box = ctk.CTkTextbox(self.main_frame, width = 670, height = 60, border_width=2, border_color="black", corner_radius=6, font = ("Verdana Pro", 18),fg_color="#F6F5F5")
        self.search_box.place(x = 30, y = 530)

        self.send_image = SetImage(image_path="image/send-message.png", width = 15, height=15)
        #buttons
        self.send_ans_button = ctk.CTkButton(self.main_frame,text="Send", width = 120, height = 40, font = ("Verdana Pro", 17), cursor = "hand2",command=send, fg_color="#1679AB", text_color="white", hover_color="#1679AB", image = self.send_image, compound="right")
        self.send_ans_button.place(x=30,y=600)

        self.mic_image = SetImage(image_path="image/microphone.png", width = 50, height=50)
        self.mic_ans = ctk.CTkButton(self.main_frame, width = 0, height=0, fg_color="transparent", text = "", command=mic, image = self.mic_image, hover=tk.DISABLED)
        self.mic_ans.place(x=720,y=530)

        self.speaker_image = SetImage(image_path="image/loud-speaker.png", width = 48, height=48)
        self.speaker_ans = ctk.CTkButton(self.main_frame, width = 0, height=0, fg_color="transparent", text = "", command=speak, image = self.speaker_image, hover=tk.DISABLED)
        self.speaker_ans.place(x=780,y=530)

        self.search_box.bind("<KeyRelease>",lambda e:self.answer_label.configure(text=""))
        self.main_frame.place(x=300,y=110)

if __name__== "__main__":
    root = App()
    root.home_page()
    root.mainloop()
