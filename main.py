import requests
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import webbrowser
import datetime

url = "https://sky-scanner3.p.rapidapi.com/"

book_url = "https://www.skyscanner.net/transport/flights"

headers = {
    "x-rapidapi-key": "004359d3f2msh392fcea5cfe0b50p1b738djsnc4eace725973",
    "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
}

df = pd.DataFrame()

def get_airports(city: str) -> dict:
    params = {"query":city}
    response = requests.get(url+"flights/auto-complete", headers=headers, params=params).json()["data"]
    airports = {}
    for i in response:
        name = f'{i["presentation"]["suggestionTitle"], i["presentation"]["subtitle"]}'
        id = i["presentation"]["skyId"]
        airports[name] = id
    return airports

def search_flights(AP1:str, AP2:str = None, depart:str = None, year:int = None, month:int = None, adults:int = None, children:int = 0, cabin_class:str = None) -> list:

    params = {"fromEntityId": AP1}
    if cabin_class:
        params["cabinClass"] = cabin_class
    if children:
        params["children"] = children
    if adults:
        params["adults"] = adults
    if year:
        params["year"] = year
    if month:
        params["month"] = month
    if depart:
        params["departDate"] = depart
    if AP2:
        params["toEntityId"] = AP2
        response = requests.get(url + "flights/cheapest-one-way", headers=headers, params=params)
        try:
            return response.json()["data"]
        except:
            return False
    else:
        params["type"] = "oneway"
        response = requests.get(url + "flights/search-everywhere", headers=headers, params=params)
        flights = []
        r = response.json()["data"]["everywhereDestination"]["results"]
        for i in r:
            try:
                price = i["content"]["flightQuotes"]["cheapest"]["price"]
                direct = i["content"]["flightQuotes"]["cheapest"]["direct"]
                location = i["content"]["location"]["name"]
            except:
                continue
            flights.append((location,price,"Direct" if direct else "Not Direct"))
        return flights

def search_airports():
    airport = airport_entry.get()
    if not airport:
        messagebox.showerror("Input Error", "Please enter a airport name.")
        return
    try:
        airports = get_airports(airport)
        airport_list.delete(0, tk.END)
        airport_codes.clear()
        if airports:
            for airport in airports.keys():
                airport_list.insert(tk.END, airport)
                airport_codes[airport] = airports[airport]
        else:
            messagebox.showinfo("Results", "No airports found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def search_airports2():
    airport2 = airport_entry2.get()
    if not airport2:
        messagebox.showerror("Input Error", "Please enter a airport name.")
        return
    try:
        airports2 = get_airports(airport2)
        airport_list2.delete(0, tk.END)
        airport_codes2.clear()
        if airports2:
            for airport2 in airports2.keys():
                airport_list2.insert(tk.END, airport2)
                airport_codes2[airport2] = airports2[airport2]
        else:
            messagebox.showinfo("Results", "No airports found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_airport():
    selected_airport = airport_list.get(airport_list.curselection())
    airport_code = airport_codes[selected_airport]
    if airport_selection_var.get() == "Departure":
        departure_airport_entry.delete(0, tk.END)
        departure_airport_entry.insert(0, airport_code)
    else:
        arrival_airport_entry.delete(0, tk.END)
        arrival_airport_entry.insert(0, airport_code)

def select_airport2():
    selected_airport2 = airport_list2.get(airport_list2.curselection())
    airport_code2 = airport_codes2[selected_airport2]
    departure_airport_entry2.delete(0, tk.END)
    departure_airport_entry2.insert(0, airport_code2)

def search_flight1():
    global df
    departure_airport = departure_airport_entry.get()
    arrival_airport = arrival_airport_entry.get()
    if not departure_airport:
        messagebox.showerror("Input Error", "Please enter a departure airport.")
        return
    
    if not arrival_airport:
        messagebox.showerror("Input Error", "Please enter a arival airport.")
        return

    try:
        results = search_flights(
                AP1=departure_airport,
                AP2=arrival_airport,
                depart=datetime.datetime.today().strftime('%Y-%m-%d')
            )
        if results:
            df = pd.DataFrame(results)
            current_flights = df.sort_values(by="day").values.tolist()
            results_text1.delete(1.0, tk.END)
            for result in current_flights:
                for i in result:
                    results_text1.insert(tk.END, f"{i} ")
                results_text1.insert(tk.END, f"\n")
        else:
            messagebox.showinfo("Results", "No flights found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def search_flight2():
    departure_airport = departure_airport_entry2.get()
    month = None
    year = None

    try:
        if year_entry2.get(): year = int(year_entry2.get())
        if year < datetime.datetime.now().year:
            messagebox.showerror("Input Error", "Please enter a valid year.")
            return
    except:
        messagebox.showerror("Input Error", "Please enter a valid year.")
        return
    
    try:
        if month_entry2.get(): 
            month = int(month_entry2.get())
        if month > 12 or month <= datetime.datetime.now().month:
            messagebox.showerror("Input Error", "Please enter a valid month.")
            return
    except:
        messagebox.showerror("Input Error", "Please enter a valid month.")
        return

    

    if not departure_airport:
        messagebox.showerror("Input Error", "Please enter a departure airport.")
        return

    

    
    
    try:
        results = search_flights(
                AP1=departure_airport,
                year=str(year),
                month=str(month).zfill(2)
        )
        if results:
            results_text2.delete(1.0, tk.END)
            for result in results:
                for i in result:
                    results_text2.insert(tk.END, f"{i} ")
                results_text2.insert(tk.END, "\n")
        else:
            messagebox.showinfo("Results", "No flights found.")
    except Exception as e:
        messagebox.showinfo("Results", "No flights found.")


def sortPrice():
    global df
    if not df.empty:
        try:
            current_flights = df.sort_values(by="price").values.tolist()
            results_text1.delete(1.0, tk.END)
            for result in current_flights:
                for i in result:
                    results_text1.insert(tk.END, f"{i} ")
                results_text1.insert(tk.END, f"\n")
        except Exception as e:
            print(e)

def sortDay():
    global df
    if not df.empty:
        try:
            current_flights = df.sort_values(by="day").values.tolist()
            results_text1.delete(1.0, tk.END)
            for result in current_flights:
                for i in result:
                    results_text1.insert(tk.END, f"{i} ")
                results_text1.insert(tk.END, f"\n")
        except Exception as e:
            print(e)

def bookflight():
    departure_airport = departure_airport_entry.get()
    arrival_airport = arrival_airport_entry.get()
    if departure_airport and arrival_airport:
        url = f"{book_url}/{departure_airport}/{arrival_airport}"
        webbrowser.open(url)

root = tk.Tk()
root.title("Flight Finder")

# Dictionary to store airport codes
airport_codes = {}

# Airport Search GUI
airport_search_frame = tk.Frame(root)
airport_search_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

tk.Label(airport_search_frame, text="Airport Search").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')
tk.Label(airport_search_frame, text="Airport").grid(row=1, column=0, padx=10, pady=5, sticky='e')
airport_entry = tk.Entry(airport_search_frame)
airport_entry.grid(row=1, column=1, padx=10, pady=5)
search_airport_button = tk.Button(airport_search_frame, text="Search Airports", command=search_airports)
search_airport_button.grid(row=1, column=2, padx=10, pady=5)

airport_list = tk.Listbox(airport_search_frame, height=6, width=50)
airport_list.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

tk.Label(airport_search_frame, text="Use selected airport as:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
airport_selection_var = tk.StringVar(value="Departure")
tk.Radiobutton(airport_search_frame, text="Departure", variable=airport_selection_var, value="Departure").grid(row=3, column=1, padx=10, pady=5, sticky='w')
tk.Radiobutton(airport_search_frame, text="Arrival", variable=airport_selection_var, value="Arrival").grid(row=3, column=2, padx=10, pady=5, sticky='w')

select_airport_button = tk.Button(airport_search_frame, text="Select Airport", command=select_airport)
select_airport_button.grid(row=4, column=0, columnspan=3, pady=5)

# Flight Search 1 GUI (Left)
flight_search_frame1 = tk.Frame(root)
flight_search_frame1.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

tk.Label(flight_search_frame1, text="Flight Search").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')
tk.Label(flight_search_frame1, text="Departure Airport Code").grid(row=1, column=0, padx=10, pady=5, sticky='e')
departure_airport_entry = tk.Entry(flight_search_frame1)
departure_airport_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(flight_search_frame1, text="Arrival Airport Code").grid(row=2, column=0, padx=10, pady=5, sticky='e')
arrival_airport_entry = tk.Entry(flight_search_frame1)
arrival_airport_entry.grid(row=2, column=1, padx=10, pady=5)

search_button1 = tk.Button(flight_search_frame1, text="Search Flights", command=search_flight1)
search_button1.grid(row=9, column=0, columnspan=2, pady=10)

sort_button1 = tk.Button(flight_search_frame1, text="Sort By Date", command=sortDay)
sort_button1.grid(row=10, column=0, columnspan=2, pady=10)

sort_button2 = tk.Button(flight_search_frame1, text="Sort By Price", command=sortPrice)
sort_button2.grid(row=11, column=0, columnspan=2, pady=10)

book_button = tk.Button(flight_search_frame1, text="Book Flight", command=bookflight)
book_button.grid(row=12, column=0, columnspan=2, pady=10)

results_text1 = tk.Text(root, height=10, width=40)
results_text1.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

# Airport Search 2 GUI
airport_codes2 = {}

airport_search_frame2 = tk.Frame(root)
airport_search_frame2.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

tk.Label(airport_search_frame2, text="Airport Search").grid(row=0, column=2, columnspan=2, padx=10, pady=5, sticky='w')
tk.Label(airport_search_frame2, text="Airport").grid(row=1, column=2, padx=10, pady=5, sticky='e')
airport_entry2 = tk.Entry(airport_search_frame2)
airport_entry2.grid(row=1, column=3, padx=10, pady=5)
search_airport_button2 = tk.Button(airport_search_frame2, text="Search Airports", command=search_airports2)
search_airport_button2.grid(row=1, column=4, padx=10, pady=5)

airport_list2 = tk.Listbox(airport_search_frame2, height=6, width=50)
airport_list2.grid(row=2, column=2, columnspan=3, padx=10, pady=5)

select_airport_button2 = tk.Button(airport_search_frame2, text="Select Airport", command=select_airport2)
select_airport_button2.grid(row=4, column=2, columnspan=3, pady=5)


# Flight Search 2 GUI (Right)
flight_search_frame2 = tk.Frame(root)
flight_search_frame2.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

tk.Label(flight_search_frame2, text="Flight Search Everywhere").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='w')
tk.Label(flight_search_frame2, text="Departure Airport Code").grid(row=1, column=0, padx=10, pady=5, sticky='e')
departure_airport_entry2 = tk.Entry(flight_search_frame2)
departure_airport_entry2.grid(row=1, column=1, padx=10, pady=5)

tk.Label(flight_search_frame2, text="Year(2024)").grid(row=3, column=0, padx=10, pady=5, sticky='e')
year_entry2 = tk.Entry(flight_search_frame2)
year_entry2.grid(row=3, column=1, padx=10, pady=5)

tk.Label(flight_search_frame2, text="Month(04)").grid(row=4, column=0, padx=10, pady=5, sticky='e')
month_entry2 = tk.Entry(flight_search_frame2)
month_entry2.grid(row=4, column=1, padx=10, pady=5)

search_button2 = tk.Button(flight_search_frame2, text="Search Flights", command=search_flight2)
search_button2.grid(row=9, column=0, columnspan=2, pady=10)

results_text2 = tk.Text(root, height=10, width=40)
results_text2.grid(row=1, column=3, padx=10, pady=10, sticky='nsew')

root.mainloop()