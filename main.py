#Code By Mayo and Andulana
#IMPORT LIBRARIES

import tkinter as tk
from tkinter import ttk
import TKinterModernThemes as TKMT
import csv
import datetime
import os
import pandas as pd
import shutil
from tkinter import *
#CREATE MAIN CLASS
class App(TKMT.ThemedTKinterFrame):
    title_font = ("Segoe UI Black", 36)
    heading_font = ("Segoe UI Semibold", 24)
    intro_font = ("Segoe UI", 16)
    text_font = ("Segoe UI", 12)
    color_bg = '#FEFFF2'

    #INITIALIZE THE MAIN CLASS
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Final Project", theme, mode, usecommandlineargs, usethemeconfigfile)
        self.master.title("Program Beta")
        self.master.geometry("800x600")
        self.master.config(bg=self.color_bg)
        self.master.resizable(False, False)
        self.startmenu()
        self.run()
        self.username = ""
    def exit_program(self):
            self.master.destroy()

    #START MENU CONTAINS THE FIRST LAYER OF THE PROGRAM WHIHC IS THE WELCOME SCREEN WITH USERNAME INPUT     
    def startmenu(self):
        def check_entry():
            if self.username_entry.get() == "":
                self.button.config(state="disabled")
            else:
                self.username = self.username_entry.get()
                self.button.config(state="normal")

        def username_get():
            self.username = self.username_entry.get()
            self.mainmenu()

        title = tk.Label(self.master, text="CalHealth", font=self.title_font, bg= self.color_bg)
        title.place(relx=0.5, rely=0.35, anchor="center")
        description = tk.Label(
            self.master,
            text="The CalHealth is an application designed to promote healthy living by \nproviding health-conscious people an easy way to calculate he amount of \ncalories eaten per meal and plan succeeding meals based on the results.",
            font=self.intro_font, bg= self.color_bg
        )
        description.place(relx=0.5, rely=0.56, anchor="center")

        Username = tk.Label(self.master, text="Username:", font=self.text_font, bg= self.color_bg)
        Username.place(relx=0.32, rely=0.72, anchor="center")
        self.username_entry = tk.Entry(font=self.text_font, width=30, borderwidth=2, relief="groove")
        self.username_entry.place(relx=0.55, rely=.72, anchor="center")

        self.button = tk.Button(self.master, text="Start Program", command=username_get, state='disabled', font=self.text_font, width= 15, height=1, borderwidth=2, relief="groove")
        self.button.place(relx=0.5, rely=0.87, anchor="center")
        self.username_entry.bind("<KeyRelease>", lambda _: check_entry())


    #MAIN MENU FUNCTION OCNTAINING ALL NAVIGATION AND DISPLAY FUNCTION FOR 2ND LAYER
    def mainmenu(self):

        # Save the username to the user list
        def save_username(): 
            with open('Datafile/USERS/User_list.txt', 'r') as file:
                existing_user_list = [line.strip() for line in file]
            if self.username not in existing_user_list:
                with open('Datafile/USERS/User_list.txt', 'a') as file:
                    file.write('\n'+self.username)

        for widget in self.master.winfo_children():
            widget.destroy()
        print("Main Menu launched!")
        with open('Datafile/USERS/User_list.txt', 'r') as file:
            existing_user_list = [line.strip() for line in file]
        
        def delete_user():
            user_folder = f"Datafile/USERS/{self.username}"
            if os.path.exists(user_folder):
                for file_name in os.listdir(user_folder):
                    file_path = os.path.join(user_folder, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)

                os.rmdir(user_folder)
            
            # Delete user from user list
            with open('Datafile/USERS/User_list.txt', 'r') as file:
                lines = file.readlines()
            with open('Datafile/USERS/User_list.txt', 'w') as file:
                for line in lines:
                    if line.strip() != self.username:
                        file.write(line)
            for widget in self.master.winfo_children():
                widget.destroy()
            self.startmenu()
        def display_bmr_data():
                username_bmr_file = f"Datafile/USERS/{self.username}/{self.username}_BMR.csv"
                try:
                    bmr_data = pd.read_csv(username_bmr_file)
                    
                    latest_results = bmr_data.tail(10)
                    table = ttk.Treeview(self.master, columns=list(latest_results.columns), show="headings")
                    for column in latest_results.columns:
                        table.heading(column, text=column)
                    for row in latest_results.itertuples(index=False):
                        table.insert("" , "end", values=row)
                    table.place(relx=0.65, rely=0.5, anchor='center')
                # If the file is not found, display a message to the user
                except FileNotFoundError:
                    print(f"File {username_bmr_file} not found.")
                    Display_val = tk.Label(self.master, text="No Existing\ndata found", font=self.heading_font, bg= self.color_bg)
                    Display_val.place(relx=0.65, rely=0.4, anchor="center")

        # Checks if user has already entered the application
        if self.username in existing_user_list:
            welcome = tk.Label(self.master, text=f"Welcome back {self.username}", font=self.heading_font, bg= self.color_bg)
            welcome.place(relx=0.06, rely=0.08)
            display_bmr_data()
        else:
            welcome = tk.Label(self.master, text=f"Welcome to CalHealth {self.username}", font=self.heading_font, bg= self.color_bg)
            save_username()
            display_bmr_data()
            welcome.place(relx=0.06, rely=0.08)

        # Main menu options
        user_information = tk.Label(self.master, text="User Information", font=self.intro_font, bg= self.color_bg)
        user_information.place(relx=0.65, rely=0.2, anchor="center")

        option_1 = tk.Button(self.master, text="Calculate Daily \nCaloric Intake", padx=24, pady=6, width=15, command=self.Calculate_Calories)
        option_1.place(relx=0.2, rely=0.3, anchor="center")

        option_2 = tk.Button(self.master, text="Plan Meals", padx=24, pady=6, width=15, command=self.Plan_Meals)
        option_2.place(relx=0.2, rely=0.5, anchor="center")

        option_3 = tk.Button(self.master, text="User History", padx=24, pady=6, width=15, command=self.user_history)
        option_3.place(relx=0.2, rely=0.7, anchor="center")

        return_button = tk.Button(self.master, text="Exit Program", command=self.exit_program)
        return_button.place(relx=0.88, rely=0.9, anchor="center")

        delete_button = tk.Button(self.master, text="Delete User", command=delete_user)
        delete_button.place(relx=0.75, rely=0.9, anchor="center")

    #FUNCTION TO CALCULATE CALORIES
    def Calculate_Calories(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        print("Calculate Calories launched!")
        # Function to check if the user has entered valid data after pressing the calculate button
        def val_check():
            age = self.age_entry.get()
            gender = self.gender_var.get()
            height = self.height_entry.get()
            weight = self.weight_entry.get()

            
            if not age.isdigit():
                self.age_entry.config(bg="red")
            else:
                self.age_entry.config(bg="white")

            if not height.isdigit():
                self.height_entry.config(bg="red")
            else:

                self.height_entry.config(bg="white")

            if not weight.isdigit():
                self.weight_entry.config(bg="red")
            else:
                self.weight_entry.config(bg="white")
                
            if not gender:
                self.invalid_label.config(text="Please indicate gender", font=self.text_font, fg="red")
            else:
                self.invalid_label.config(text="")

            # If all the data is valid, calculate the BMR
            if age.isdigit() or height.isdigit() and weight.isdigit() and gender:
                calculate_bmr()

        # Function to calculate the Basal Metabolic Rate (BMR) and display the results
        def calculate_bmr():
            age = int(self.age_entry.get())
            weight = int(self.weight_entry.get())
            height = int(self.height_entry.get())
            if self.gender_var.get() == "M":
                bmr = (88.4 + 13.4 * weight) + (4.8 * height) - (5.68 * age)
            elif self.gender_var.get() == "F":
                bmr = (447.6 + 9.25 * weight) + (3.10 * height) - (4.33 * age)
                self.bmr_value = tk.Label(self.master, text=f"{round(bmr)}", font=self.text_font, bg=self.color_bg)
                self.bmr_value.place(relx=0.775, rely=0.2, anchor="w")
            try:
                if bmr:
                    proceed_button.config(state="normal")
                    bmr_label = tk.Label(self.master, text="BMR:", font=self.text_font, bg=self.color_bg)
                    bmr_label.place(relx=0.775, rely=0.2, anchor="e")
                    maintain_weight_label = tk.Label(self.master, text="Maintain Weight:", font=self.text_font, bg=self.color_bg)
                    maintain_weight_label.place(relx=0.775, rely=0.3, anchor="e")
                    maintain_weight_calories = round(bmr)
                    maintain_weight_value = tk.Label(self.master, text=f"{maintain_weight_calories} calories/day", font=self.text_font, bg=self.color_bg)
                    maintain_weight_value.place(relx=0.775, rely=0.3, anchor="w")

                    mild_weight_loss_label = tk.Label(self.master, text="Mild Weight Loss:", font=self.text_font, bg=self.color_bg)
                    mild_weight_loss_label.place(relx=0.775, rely=0.4, anchor="e")
                    mild_weight_loss_calories = round(bmr * 0.91)
                    mild_weight_loss_value = tk.Label(self.master, text=f"{mild_weight_loss_calories} calories/day", font=self.text_font, bg=self.color_bg)
                    mild_weight_loss_value.place(relx=0.775, rely=0.4, anchor="w")

                    weight_loss_label = tk.Label(self.master, text="Weight Loss:", font=self.text_font, bg=self.color_bg)
                    weight_loss_label.place(relx=0.775, rely=0.5, anchor="e")
                    weight_loss_calories = round(bmr * 0.82)
                    weight_loss_value = tk.Label(self.master, text=f"{weight_loss_calories} calories/day", font=self.text_font, bg=self.color_bg)
                    weight_loss_value.place(relx=0.775, rely=0.5, anchor="w")

                    extreme_weight_loss_label = tk.Label(self.master, text="Extreme Weight Loss:", font=self.text_font, bg=self.color_bg)
                    extreme_weight_loss_label.place(relx=0.775, rely=0.6, anchor="e")
                    extreme_weight_loss_calories = round(bmr * 0.64)
                    extreme_weight_loss_value = tk.Label(self.master, text=f"{extreme_weight_loss_calories} calories/day", font=self.text_font, bg=self.color_bg)
                    extreme_weight_loss_value.place(relx=0.775, rely=0.6, anchor="w")

                    # Save the BMR data to a CSV file
                    username = self.username
                    folder_path = f"Datafile/USERS/{username}"
                    os.makedirs(folder_path, exist_ok=True)

                    filename = f"{folder_path}/{username}_BMR.csv"
                    with open(filename, 'a', newline='') as file:
                        writer = csv.writer(file)
                        if file.tell() == 0:
                            writer.writerow(["Name", "Value"])
                        writer.writerow(["Date", datetime.date.today()])
                        writer.writerow(["User", username])
                        writer.writerow(["Age", age])
                        writer.writerow(["Weight", weight])
                        writer.writerow(["Height", height])
                        writer.writerow(["Gender", self.gender_var.get()])
                        writer.writerow(["BMR", round(bmr)])
                        writer.writerow(["Maintain Weight", maintain_weight_calories])
                        writer.writerow(["Mild Weight Loss", mild_weight_loss_calories])
                        writer.writerow(["Weight Loss", weight_loss_calories])
                        writer.writerow(["Extreme Weight Loss", extreme_weight_loss_calories])
                        writer.writerow([])
            except NameError:
                pass
        
        # Creates entry fields for the user to enter
        welcome = tk.Label(self.master, text=f"Calorie Calculator", font=self.intro_font, bg=self.color_bg)
        welcome.place(relx=0.5, rely=0.08, anchor="center")
        
        age_label = tk.Label(self.master, text="Age:", font=self.text_font, bg=self.color_bg)
        age_label.place(relx=0.12, rely=0.2, anchor="center")
        self.age_entry = tk.Entry(font=self.text_font, width=20, borderwidth=2, relief="groove")
        self.age_entry.place(relx=0.3, rely=0.2, anchor="center")

        self.gender_var = tk.StringVar()
        gender_label = tk.Label(self.master, text="Gender:", font=self.text_font, bg=self.color_bg)
        gender_label.place(relx=0.12, rely=0.3, anchor="center")
        
        self.male_checkbox = Checkbutton(self.master, variable=self.gender_var, onvalue="M", offvalue="", text = "Male", bg= self.color_bg)
        self.male_checkbox.place(relx=0.23, rely=0.3, anchor="center")

        self.female_checkbox = Checkbutton(self.master, variable=self.gender_var, onvalue="F", offvalue="", text = "Female", bg= self.color_bg)
        self.female_checkbox.place(relx=0.35, rely=0.3, anchor="center")

        self.gender_var.set("")

        height_label = tk.Label(self.master, text="Height (cm):", font=self.text_font, bg=self.color_bg)
        height_label.place(relx=0.12, rely=0.4, anchor="center")
        self.height_entry = tk.Entry(font=self.text_font, width=20, borderwidth=2, relief="groove")
        self.height_entry.place(relx=0.3, rely=0.4, anchor="center")

        weight_label = tk.Label(self.master, text="Weight (kg):", font=self.text_font, bg=self.color_bg)
        weight_label.place(relx=0.12, rely=0.5, anchor="center")
        self.weight_entry = tk.Entry(font=self.text_font, width=20, borderwidth=2, relief="groove")
        self.weight_entry.place(relx=0.3, rely=0.5, anchor="center")

        calculate_button = tk.Button(self.master, text="Calculate BMR", command=val_check)
        calculate_button.place(relx=0.3, rely=0.6, anchor="center")

        
        self.invalid_label = tk.Label(self.master, text="", font=self.text_font, bg=self.color_bg)
        self.invalid_label.place(relx=0.295, rely=0.345, anchor="center")


        proceed_button = tk.Button(self.master, text="Proceed to Meal Plan", command=self.Plan_Meals, state="disabled")
        proceed_button.place(relx=0.68, rely=0.9, anchor="center")
        
        return_button = tk.Button(self.master, text="Return to Main Menu", command=self.mainmenu)
        return_button.place(relx=0.88, rely=0.9, anchor="center")

 
    #FUNCTION TO PLAN MEALS
    def Plan_Meals(self):
        self.total_calories = 0
        for widget in self.master.winfo_children():
            widget.destroy()
        print("Plan Meals launched!")

        # Function to import the dictionary of meals and their calorie counts from a txt file
        def import_dictionary(filename):
            dictionary = {}
            with open(filename, 'r') as file:
                for line in file:
                    key, value = line.strip().split(':')
                    dictionary[key.strip()] = value.strip()
            return dictionary

        imported_dict = import_dictionary('Datafile/meals.txt')

        # Create labels for the listbox and mealbox
        listbox_label = tk.Label(self.master, text="Available Meals:", font=self.intro_font, bg=self.color_bg)
        listbox_label.place(relx=0.22, rely=0.05, anchor="center")

        mealbox_label = tk.Label(self.master, text="Selected Meals:", font=self.intro_font, bg=self.color_bg)
        mealbox_label.place(relx=0.78, rely=0.05, anchor="center")

        # Create a listbox to display the meals
        listbox = tk.Listbox(self.master, width=32, height=10, font=self.text_font, bg= "white", borderwidth=2, relief="groove")
        listbox.place(relx=0.22, rely=0.35, anchor="center")

        for key in imported_dict.keys():
            listbox.insert(tk.END, f"{key}")

        # Create a label to display the calorie count of the selected meal
        value_label = tk.Label(self.master, text="Calories per serving: ", font=self.text_font, bg=self.color_bg)
        value_label.place(relx=0.04, rely=0.57, anchor="w")

        def update_calorie_count():
            try:
                selected_item = listbox.get(listbox.curselection())
                calorie_count = imported_dict[selected_item]
                value_label.config(text=f"Calories per serving: {calorie_count}")
            except:
                value_label.config(text="Calories per serving: N/A")

        # Function to add a meal to the dictionary and the listbox
        def add_meal():
            meal_name = meal_entry.get()
            calorie_count = calorie_entry.get()

            if not meal_name or not calorie_count.isdigit():
                return

            imported_dict[meal_name] = calorie_count

            with open('Datafile/meals.txt', 'a') as file:
                file.write(f'{meal_name}: {calorie_count}\n')

            meal_entry.delete(0, tk.END)
            calorie_entry.delete(0, tk.END)
            listbox.insert(tk.END, f"{meal_name}")

        # Function to add a meal to the mealbox and calculate the total calories
        selected_meal = {}

        def add_mealbox():
            meal_name = meal_pick.get()
            if meal_name in imported_dict:
                calorie_count = imported_dict[meal_name]
            mealbox.insert(tk.END, f"{meal_name} - {calorie_count} Calories")
            self.total_calories += int(calorie_count)
            total_calories_label.config(text=f"Total Calories: {self.total_calories}")
            selected_meal[meal_name] = int(calorie_count)
            selected_meal.update({meal_name: calorie_count})


        # Function to delete a meal from the mealbox and calculate the total calories
        def delete_from_mealbox():
            selected_index = mealbox.curselection()
            if selected_index:
                selected_item = mealbox.get(selected_index)
            meal_name = selected_item.split(" - ")[0]
            calorie_count = selected_item.split(" - ")[1].split(" ")[0]
            mealbox.delete(selected_index)
            self.total_calories -= int(calorie_count)
            total_calories_label.config(text=f"Total Calories: {self.total_calories}")
            del selected_meal[meal_name]
            try:
                selected_meal.pop(meal_name)
            except KeyError:
                pass
        
        # Function to save the meal history to a CSV file
        def save_meal_history():
            directory = f"Datafile/USERS/{self.username}"
            os.makedirs(directory, exist_ok=True)

            file_path = f"{directory}/{self.username}_meals.csv"

            current_datetime = datetime.date.today()

            # Write the data to the CSV file
            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(["Name", "Calorie Count"])
                writer.writerow(["Date",current_datetime])
                for key, value in selected_meal.items():
                    writer.writerow([key, value])
                writer.writerow(["Total Calories", self.total_calories])
                writer.writerow([])

            
            proceed_button.config(state="normal")
        # Function to remove a meal from the dictionary and the listbox
        def remove_meal():
            selected_index = listbox.curselection()
            if selected_index:
                selected_item = listbox.get(selected_index)
                del imported_dict[selected_item]
                listbox.delete(selected_index)
                with open('Datafile/meals.txt', 'w') as file:
                    for key, value in imported_dict.items():
                        file.write(f'{key}: {value}\n')


        
        # Create the labels, entry fields, and buttons for the custom meal
        custom_meal_label = tk.Label(self.master, text="Custom Meal:", font=self.text_font, bg= self.color_bg)
        custom_meal_label.place(relx=0.22, rely=0.68, anchor="center")

        meal_label = tk.Label(self.master, text="Meal Name:", font=self.text_font, bg= self.color_bg)
        meal_label.place(relx=0.04, rely=0.72, anchor="w")

        meal_entry = tk.Entry(self.master, width=18, borderwidth=2, relief="groove")
        meal_entry.place(relx=0.17, rely=0.72, anchor="w")

        calorie_label = tk.Label(self.master, text="Calorie Count:", font=self.text_font, bg= self.color_bg)
        calorie_label.place(relx=0.04, rely=0.77, anchor="w")

        calorie_entry = tk.Entry(self.master, width=18, borderwidth=2, relief="groove")
        calorie_entry.place(relx=0.17, rely=0.77, anchor="w")

        add_button = tk.Button(self.master, text="Add \nMeal", command=add_meal)
        add_button.place(relx=0.37, rely=0.74, anchor="center")
    
        
        meal_button = tk.Button(self.master, text="Add\nto\nMeal", width=12, height=3, command=add_mealbox)
        meal_button.place(relx=0.5, rely=0.32, anchor="center")
        
        meal_pick = tk.Entry(self.master, width=28, borderwidth=2, relief="groove")
        meal_pick.place(relx=0.038, rely=0.12, anchor="w")

        remove_button = tk.Button(self.master, text="Remove Meal", command=remove_meal, height=1)
        remove_button.place(relx=0.29, rely=0.12, anchor="w")

        #removes unmatched items
        def filter_listbox(_):
            try:
                filter_text = meal_pick.get().lower()
                listbox.delete(0, tk.END)
                for key in imported_dict.keys():
                    if filter_text in key.lower():
                        listbox.insert(tk.END, f"{key}")
            except:
                pass

        meal_pick.bind("<KeyRelease>", filter_listbox)
        
        # checks if user selected an item form the listbox
        def select_item(_):
            try:
                selected_item = listbox.get(listbox.curselection())
                meal_pick.delete(0, tk.END)
                meal_pick.insert(tk.END, selected_item)
                update_calorie_countz()
            except:
                pass
        listbox.bind("<<ListboxSelect>>", select_item)

        # Create the mealbox to display the selected meals
        mealbox = tk.Listbox(self.master, width=32, height=10, font=self.text_font, bg="white", borderwidth=2, relief="groove")
        mealbox.place(relx=0.78, rely=0.35, anchor="center")

        
        total_calories_label = tk.Label(self.master, text=f"Total Calories: {self.total_calories}", font=self.text_font, bg=self.color_bg)
        total_calories_label.place(relx=0.78, rely=0.58, anchor="center")

        delete_button = tk.Button(self.master, text="Delete", command=delete_from_mealbox, width=15, height=1, borderwidth=2)
        delete_button.place(relx=0.68, rely=0.12, anchor="center")

        save_button = tk.Button(self.master, text="Save Meal Plan", command=save_meal_history, width=15, height=1, borderwidth=2)
        save_button.place(relx=0.87, rely=0.12, anchor="center")


        proceed_button = tk.Button(self.master, text="Proceed to results", command=self.user_history)
        proceed_button.place(relx=0.68, rely=0.9, anchor="center")
        
        return_button = tk.Button(self.master, text="Return to Main Menu", command=self.mainmenu)
        return_button.place(relx=0.88, rely=0.9, anchor="center")

    #FUNCTION TO DISPLAY USER HISTORY
    def user_history(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        print("User History launched!")
        title_history = tk.Label(self.master, text="User History", font=self.heading_font, bg= self.color_bg)
        title_history.place(relx=0.5, rely=0.1, anchor="center")

        # Display the BMR history in a table
        bmr_filename = f"Datafile/USERS/{self.username}/{self.username}_BMR.csv"
        if os.path.isfile(bmr_filename):
            bmr_data = pd.read_csv(bmr_filename)
            bmr_table = ttk.Treeview(self.master, height = 4)
            bmr_table["columns"] = tuple(bmr_data.columns)
            bmr_table["show"] = "headings"
            for column in bmr_table["columns"]:
                bmr_table.heading(column, text=column)
            for index, row in bmr_data.iterrows():
                bmr_table.insert("", "end", values=tuple(row))
            bmr_table.place(relx=0.5, rely=0.3, anchor="center")
        else:
            Missing_bmr = tk.Label(self.master, text="No BMR data found", font=self.heading_font, bg= self.color_bg)
            Missing_bmr.place(relx=0.5, rely=0.3, anchor="center")

        # Display the meal history in a table
        meals_filename = f"Datafile/USERS/{self.username}/{self.username}_meals.csv"
        if os.path.isfile(meals_filename):
            meals_data = pd.read_csv(meals_filename)
            meals_table = ttk.Treeview(self.master, height = 4)
            meals_table["columns"] = tuple(meals_data.columns)
            meals_table["show"] = "headings"
            for column in meals_table["columns"]:
                meals_table.heading(column, text=column)
            for index, row in meals_data.iterrows():
                meals_table.insert("", "end", values=tuple(row))
            meals_table.place(relx=0.5, rely=0.6, anchor="center")
        else:
            Missing_meals = tk.Label(self.master, text="No meal data found", font=self.heading_font, bg= self.color_bg)
            Missing_meals.place(relx=0.5, rely=0.5, anchor="center")
        
        proceed_button = tk.Button(self.master, text="Return to Main Menu", command=self.mainmenu)
        proceed_button.place(relx=0.71, rely=0.9, anchor="center")
        
        return_button = tk.Button(self.master, text="Exit Program", command=self.exit_program)
        return_button.place(relx=0.88, rely=0.9, anchor="center")
if __name__ == "__main__":
    App("sun-valley", "light")



