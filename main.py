# importing required modules
import os
import pandas as pd
import random
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

# Load the CSV file and create a DataFrame
df = pd.read_csv('restaurants.csv', encoding='latin-1')


# Define the decision tree based on user preferences
def recommend_restaurant(city, price, cuisine):
    # Filter restaurants based on user preferences
    filtered_df = df[(df['CITY'] == city.upper()) &
                     (df['PRICE'] <= price) &
                     (df['CUISINE_CATEGORY'].str.contains(cuisine.upper()))]

    # Sort restaurants by rating and overall score
    sorted_df = filtered_df.sort_values(['RATING', 'OVERALL'], ascending=False)

    # Return the top 5 recommended restaurants
    if sorted_df.empty:
        return "Sorry, no restaurants were found that match your preferences in {}.".format(city)
    else:
        recommended_restaurants = sorted_df.head(5)
        return recommended_restaurants[['NAME', 'URL', 'RATING', 'PRICE', 'CUISINE_CATEGORY', 'REGION']]


# Define a function to print 5 new restaurants in the city
def new_restaurant(city, cuisine):
    # Filter all the new restaurants based on user preferences
    filtered_dfnew = df[(df['CITY'] == city.upper()) &
                        (df['RATING'] == 0.1) &
                        (df['CUISINE_CATEGORY'].str.contains(cuisine.upper()))]

    # Shuffle the filtered restaurants
    shuffled_values = filtered_dfnew.values
    random.shuffle(shuffled_values)
    shuffled_dfnew = pd.DataFrame(shuffled_values, columns=filtered_dfnew.columns)

    # Return the top 5 recommended restaurants
    if shuffled_dfnew.empty:
        return "Sorry, no new restaurants based on your preference were found in {}.".format(city)
    else:
        new_restaurants = shuffled_dfnew.head(5)
        return new_restaurants[['NAME', 'URL', 'RATING', 'PRICE', 'CUISINE_CATEGORY', 'REGION']]


# Define function for clear button
def clear_entries():
    city_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    cuisine_entry.delete(0, tk.END)


# define function for exit button
def exit():
    app.destroy()


# Define a function to handle the search button click
def search():
    # Get user preferences
    city = city_entry.get().strip()
    price = float(price_entry.get())
    cuisine = cuisine_entry.get().strip()

    # Get recommended restaurants
    recommended_restaurants = recommend_restaurant(city, price, cuisine)
    new_restaurants = new_restaurant(city, cuisine)

    # create a separate window for list of restaurants
    out = ctk.CTk()
    out.geometry("1000x600")
    out.title("RECOMMENDATIONS")

    # Define the columns for the treeview
    columns = ('Name', 'Cuisine', 'Rating', 'Region', 'Price', 'URL')

    # Create the recommended label
    recommended_label = ctk.CTkLabel(master=out, text="", font=('Century Gothic', 16))
    recommended_label.pack()
    recommended_label.configure(
        text="\nHere are the top 5 restaurants that match your preferences in {}: \n".format(city))

    # Create the treeview for recommended restaurants
    tv1 = ttk.Treeview(master=out, columns=columns, show='headings')
    tv1.pack()

    # Set the column headings for recommended restaurants
    for col in columns:
        tv1.heading(col, text=col)

    # Insert the recommended restaurants into the treeview
    if isinstance(recommended_restaurants, str):
        recommended_label = ctk.CTkLabel(master=out, text="", font=('Century Gothic', 16))
        recommended_label.pack()
        recommended_label.configure(text="\nsorry no data available for {}. \n".format(city))
    else:
        for restaurant in recommended_restaurants.itertuples():
            tv1.insert('', tk.END, values=(
            restaurant[1], restaurant[5], restaurant[3], restaurant[6], restaurant[4], restaurant[2]))

    # Create the new label
    new_label = ctk.CTkLabel(master=out, text="", font=('Century Gothic', 16))
    new_label.pack()
    new_label.configure(text="\nHere are some new restaurants that match your preferences in {}: \n".format(city))

    # Create the treeview for new restaurants
    tv2 = ttk.Treeview(master=out, columns=columns, show='headings')
    tv2.pack()

    # Set the column headings for new restaurants
    for col in columns:
        tv2.heading(col, text=col)

    # Insert the new restaurants into the treeview
    # Insert the recommended restaurants into the treeview
    if isinstance(new_restaurants, str):
        new_label = ctk.CTkLabel(master=out, text="", font=('Century Gothic', 16))
        new_label.pack()
        new_label.configure(text="\nsorry no data available for {}. \n".format(city))
    else:
        for restaurant in new_restaurants.itertuples():
            tv2.insert('', tk.END, values=(
            restaurant[1], restaurant[5], restaurant[3], restaurant[6], restaurant[4], restaurant[2]))

    out.mainloop()


# Main Application
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()  # creating Window
app.geometry("600x600")
app.title('Resturant Recommender')

# background
img1 = ImageTk.PhotoImage(Image.open("BG.png"))
l1 = ctk.CTkLabel(master=app, image=img1)
l1.pack()

# center frame
frame = ctk.CTkFrame(master=app, width=400, height=400, corner_radius=20)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# header
l2 = ctk.CTkLabel(master=frame, text="Enter your Prefrences here.", font=('Century Gothic', 28))
l2.place(x=20, y=50)

# City row
lcity = ctk.CTkLabel(master=frame, text="Enter preffred city:", font=('Century Gothic', 12))
lcity.place(x=10, y=115)
city_entry = ctk.CTkEntry(master=frame, width=220, placeholder_text="Enter City")
city_entry.place(x=170, y=115)

# Price row
lprice = ctk.CTkLabel(master=frame, text="Average price for 2:", font=('Century Gothic', 12))
lprice.place(x=10, y=165)
price_entry = ctk.CTkEntry(master=frame, width=220, placeholder_text="Maximum amount")
price_entry.place(x=170, y=165)

# Cuisine row
lcuisine = ctk.CTkLabel(master=frame, text="Cuisine you want to eat:", font=('Century Gothic', 12))
lcuisine.place(x=10, y=215)
cuisine_entry = ctk.CTkEntry(master=frame, width=220, placeholder_text="Enter Cuisine")
cuisine_entry.place(x=170, y=215)

# Search button
search_button = ctk.CTkButton(master=frame, width=180, text="Search", corner_radius=6, hover_color="#EC3232",
                              command=search)
search_button.place(x=205, y=265)

# Clear button
clear_button = ctk.CTkButton(master=frame, width=180, text="Clear", corner_radius=6, hover_color="#EC3232",
                             command=clear_entries)
clear_button.place(x=15, y=265)

# Exit button
exit_button = ctk.CTkButton(master=frame, width=200, text="Exit", corner_radius=6, hover_color="#EC3232", command=exit)
exit_button.place(x=100, y=315)

app.mainloop()