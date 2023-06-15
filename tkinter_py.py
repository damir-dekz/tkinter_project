import csv
import tkinter as tk
from tkinter import messagebox

# User dictionary for authentication
user_dict = {
    "admin": "admin123",
    "user1": "password1",
    "user2": "password2"
}
# Function to search for a book
def search_book():
    book_name = book_entry.get()
    with open('books.csv', 'r') as file:
        reader = csv.DictReader(file)
        found_books = []
        for row in reader:
            if book_name.lower() in row['name'].lower():
                found_books.append(row)

    if found_books:
        messagebox.showinfo("Search Results", f"Found {len(found_books)} book(s).\n\n{format_book_list(found_books)}")
    else:
        messagebox.showinfo("Search Results", "No books found.")


# Function to borrow a book
def borrow_book():
    book_name = book_entry.get()
    with open('books.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames  # Store the fieldnames

        books = list(reader)

    found_book = None
    for book in books:
        if book_name.lower() == book['name'].lower() and book['availability'] == 'available':
            found_book = book
            break

    if found_book:
        found_book['availability'] = 'borrowed'
        found_book['borrower'] = current_user.get()

        with open('books.csv', 'w', newline='') as file:
            fieldnames = ['author', 'name', 'year', 'publisher', 'availability', 'borrower']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books)

        messagebox.showinfo("Borrow Book", f"You have successfully borrowed the book:\n\n{format_book(found_book)}")
    else:
        messagebox.showinfo("Borrow Book", "The book is not available for borrowing.")




# Function to return a book
def return_book():
    book_name = book_entry.get()
    with open('books.csv', 'r') as file:
        reader = csv.DictReader(file)
        books = list(reader)

    found_book = None
    for book in books:
        if book_name.lower() == book['name'].lower() and book['availability'] == 'borrowed' and book[
            'borrower'] == current_user.get():
            found_book = book
            break

    if found_book:
        found_book['availability'] = 'available'
        found_book.pop('borrower')
        with open('books.csv', 'w', newline='') as file:
            fieldnames = ['author', 'name', 'year', 'publisher', 'availability', 'borrower']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books)

        messagebox.showinfo("Return Book", f"You have successfully returned the book:\n\n{format_book(found_book)}")
    else:
        messagebox.showinfo("Return Book", "You have not borrowed this book or it is not available for return.")


# Function to format book details
def format_book(book):
    return f"Author: {book['author']}\nName: {book['name']}\nYear: {book['year']}\nPublisher: {book['publisher']}"


# Function to format book list
def format_book_list(books):
    book_list = ""
    for book in books:
        book_list += format_book(book) + "\n\n"
    return book_list


# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if username and password match
    if username in user_dict and user_dict[username] == password:
        current_user.set(username)
        messagebox.showinfo("Login", "Login successful.")
        main_menu()
    else:
        messagebox.showerror("Login Error", "Invalid username or password.")


# Function to display the main menu
def main_menu():
    login_frame.pack_forget()

    main_frame = tk.Frame(window)
    main_frame.pack(pady=20)

    tk.Label(main_frame, text="Library Management System", font=("Helvetica", 16)).grid(row=0, columnspan=2)

    tk.Label(main_frame, text="Enter Book Name:").grid(row=1, column=0)
    global book_entry
    book_entry = tk.Entry(main_frame)
    book_entry.grid(row=1, column=1)

    tk.Button(main_frame, text="Search Book", command=search_book).grid(row=2, column=0, pady=10)
    tk.Button(main_frame, text="Borrow Book", command=borrow_book).grid(row=2, column=1, pady=10)
    tk.Button(main_frame, text="Return Book", command=return_book).grid(row=3, column=0, pady=10)


# Create the main window
window = tk.Tk()
window.title("Library Management System")

# Login page
login_frame = tk.Frame(window)
login_frame.pack(pady=50)

tk.Label(login_frame, text="Login", font=("Helvetica", 16)).grid(row=0, columnspan=2)

tk.Label(login_frame, text="Username:").grid(row=1, column=0)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=1, column=1)

tk.Label(login_frame, text="Password:").grid(row=2, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=2, column=1)

tk.Button(login_frame, text="Login", command=login).grid(row=3, columnspan=2, pady=10)

# Variable to store the current user
current_user = tk.StringVar()

# Run the application
window.mainloop()
