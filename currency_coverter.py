import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class RealTimeCurrencyConverter():
    def __init__(self,url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency] 

        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

class App(tk.Tk):
    def __init__(self, converter):
        super().__init__()
        self.title('Currency Converter')
        self.currency_converter = converter
        self.geometry("510x200")
        
        self.background_image = Image.open("background.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.intro_label = tk.Label(
            self, text='REAL TIME CURRENCY CONVERTER', 
            fg='black', relief=tk.RAISED, borderwidth=3, justify='center',
            font=('Arial', 15, 'bold')
        )
        self.intro_label.place(x=75, y=15)

        exchange_rate = self.currency_converter.convert('INR', 'USD', 1)
        date = self.currency_converter.data['date']
        self.date_label = tk.Label(
            self, text=f"1 Indian Rupee = {exchange_rate} USD \n Date : {date}",
            borderwidth=3, font= ('Arial', 9,'bold')
        )
        self.date_label.place(x=175, y=60)

        valid = (self.register(self.restrictNumberOnly), '%d', '%P')
        self.amount_field = tk.Entry(
            self, bd=3, relief=tk.RIDGE, justify=tk.CENTER, 
            validate='key', validatecommand=valid
        )
        self.amount_field.place(x=36, y=150)

        self.converted_amount_field_label = tk.Label(
            self, text='', fg='black', bg='white', relief=tk.RIDGE, 
            justify=tk.CENTER, width=17, borderwidth=3
        )
        self.converted_amount_field_label.place(x=346, y=150)

        font = ("Courier", 12, "bold")
        self.from_currency_variable = tk.StringVar(self)
        self.from_currency_variable.set("INR")
        self.to_currency_variable = tk.StringVar(self)
        self.to_currency_variable.set("USD")

        self.from_currency_dropdown = ttk.Combobox(
            self, textvariable=self.from_currency_variable, 
            values=list(self.currency_converter.currencies.keys()), 
            font=font, state='readonly', width=12, justify=tk.CENTER
        )
        self.from_currency_dropdown.place(x=30, y=120)

        self.to_currency_dropdown = ttk.Combobox(
            self, textvariable=self.to_currency_variable, 
            values=list(self.currency_converter.currencies.keys()), 
            font=font, state='readonly', width=12, justify=tk.CENTER
        )
        self.to_currency_dropdown.place(x=340, y=120)
        
        self.convert_button = tk.Button(
            self, text="CONVERT", fg="black", command=self.perform, 
            font=('Arial', 10, 'bold')
        ) 
        self.convert_button.place(x=220, y=135)

    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 2)

        self.converted_amount_field_label.config(text=str(converted_amount))
    
    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or (string.count('.') <= 1 and result is not None))

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)

    app = App(converter)
    app.mainloop()