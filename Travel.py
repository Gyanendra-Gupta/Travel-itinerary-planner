# Travel Itinerary Planner and Trip Cost Estimator is a Python project that helps users plan trips 
# by entering cities, travel dates, and budget. It generates a PDF itinerary, visualizes
# estimated expenses, and sends the plan via email.


import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def generate_itinerary():
    try:
        user_name = entry_name.get()
        city = entry_city.get()
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()
        budget = float(entry_budget.get())

        # Expense breakdown
        accommodation = float(entry_accommodation.get())
        travel = float(entry_travel.get())
        food = float(entry_food.get())
        others = budget - (accommodation + travel + food)

        labels = ['Accommodation', 'Travel', 'Food', 'Others']
        sizes = [accommodation, travel, food, others]

        plt.figure(figsize=(5, 5))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('Trip Expense Breakdown')
        plt.savefig("expenses_pie.png")
        plt.close()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Travel Itinerary Planner", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Name: {user_name}", ln=True)
        pdf.cell(200, 10, txt=f"Destination: {city}", ln=True)
        pdf.cell(200, 10, txt=f"From: {start_date} To: {end_date}", ln=True)
        pdf.cell(200, 10, txt=f"Total Budget: \u20B9{budget}", ln=True)  # Use Unicode for ₹ symbol

        pdf.ln(10)
        pdf.cell(200, 10, txt="Expense Details:", ln=True)
        pdf.cell(200, 10, txt=f"Accommodation: \u20B9{accommodation}", ln=True)  # Use Unicode for ₹ symbol
        pdf.cell(200, 10, txt=f"Travel: \u20B9{travel}", ln=True)  # Use Unicode for ₹ symbol
        pdf.cell(200, 10, txt=f"Food: \u20B9{food}", ln=True)  # Use Unicode for ₹ symbol
        pdf.cell(200, 10, txt=f"Others: \u20B9{others}", ln=True)  # Use Unicode for ₹ symbol

        pdf.image("expenses_pie.png", x=60, y=100, w=90)
        pdf.output("itinerary.pdf")
        sender_email = "sg4463217@gmail.com"
        receiver_email = entry_receiver_email.get()
        password = "psru vast bzna psbr"

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = "Your Travel Itinerary & Budget Report"

        body = "Hi, please find your travel itinerary and budget report attached as a PDF."
        message.attach(MIMEText(body, 'plain'))

        # Attach PDF
        with open("itinerary.pdf", "rb") as file:
            part = MIMEApplication(file.read(), _subtype="pdf")
            part.add_header('Content-Disposition', 'attachment', filename="itinerary.pdf")
            message.attach(part)

        # Send Email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)
        server.quit()

        messagebox.showinfo("Success", "Email sent successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

window = tk.Tk()
window.title("Travel Itinerary Planner and Trip Cost Estimator")

tk.Label(window, text="Enter your name:").grid(row=0, column=0, pady=5)
entry_name = tk.Entry(window)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(window, text="Enter travel city:").grid(row=1, column=0, pady=5)
entry_city = tk.Entry(window)
entry_city.grid(row=1, column=1, pady=5)

tk.Label(window, text="Enter start date (YYYY-MM-DD):").grid(row=2, column=0, pady=5)
entry_start_date = tk.Entry(window)
entry_start_date.grid(row=2, column=1, pady=5)

tk.Label(window, text="Enter end date (YYYY-MM-DD):").grid(row=3, column=0, pady=5)
entry_end_date = tk.Entry(window)
entry_end_date.grid(row=3, column=1, pady=5)

tk.Label(window, text="Enter total budget (INR):").grid(row=4, column=0, pady=5)
entry_budget = tk.Entry(window)
entry_budget.grid(row=4, column=1, pady=5)

tk.Label(window, text="Accommodation cost:").grid(row=5, column=0, pady=5)
entry_accommodation = tk.Entry(window)
entry_accommodation.grid(row=5, column=1, pady=5)

tk.Label(window, text="Travel cost:").grid(row=6, column=0, pady=5)
entry_travel = tk.Entry(window)
entry_travel.grid(row=6, column=1, pady=5)

tk.Label(window, text="Food cost:").grid(row=7, column=0, pady=5)
entry_food = tk.Entry(window)
entry_food.grid(row=7, column=1, pady=5)

tk.Label(window, text="Enter receiver's email:").grid(row=8, column=0, pady=5)
entry_receiver_email = tk.Entry(window)
entry_receiver_email.grid(row=8, column=1, pady=5)

submit_button = tk.Button(window, text="Generate Itinerary and Send Email", command=generate_itinerary)
submit_button.grid(row=9, column=0, columnspan=2, pady=10)
window.mainloop()
