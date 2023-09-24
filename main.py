import sqlite3
from datetime import datetime
def connect_db():
    return sqlite3.connect('library_management.db')

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books
                      (BookID TEXT PRIMARY KEY, Title TEXT, Author TEXT, ISBN TEXT, Status TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users
                      (UserID TEXT PRIMARY KEY, Name TEXT, Email TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations
                      (ReservationID TEXT PRIMARY KEY, BookID TEXT, UserID TEXT, ReservationDate TEXT)''')
    conn.commit()

def add_book(conn):
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = "Available"   # when adding a book, the status is set to be “Available”
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Books VALUES (?, ?, ?, ?, ?)", (book_id, title, author, isbn, status))
    conn.commit()
    print(f"Book {title} added successfully!")

def find_book(conn):
    book_id = input("Enter BookID: ")
    cursor = conn.cursor()
    cursor.execute('''SELECT Books.*, Users.Name, Users.Email, Reservations.ReservationDate 
                      FROM Books 
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID 
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID 
                      WHERE Books.BookID = ?''', (book_id,))
    result = cursor.fetchone()
    if result:
        print(f"BookID: {result[0]}, Title: {result[1]}, Author: {result[2]}, ISBN: {result[3]}, Status: {result[4]}")
        if result[5]:
            print(f"Reserved by: {result[5]}, User Email: {result[6]}, Reservation Date: {result[7]}")
    else:
        print("Book not found!")

def search_by_identifier(conn):
    identifier = input("Enter Identifier (BookID/Title/UserID/ReservationID): ")

    if identifier.startswith("LB"):
        table, column = "Books", "BookID"
    elif identifier.startswith("LU"):
        table, column = "Users", "UserID"
    elif identifier.startswith("LR"):
        table, column = "Reservations", "ReservationID"
    else:
        table, column = "Books", "Title"

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE {column} = ?", (identifier,))
    result = cursor.fetchone()
    if result:
        print(result)
    else:
        print(f"No record found for {identifier}")

def view_all_books(conn):
    cursor = conn.cursor()
    cursor.execute('''SELECT Books.*, Users.Name, Users.Email, Reservations.ReservationDate 
                      FROM Books 
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID 
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    results = cursor.fetchall()
    for result in results:
        print(result)

def modify_book(conn):
    book_id = input("Enter BookID to modify: ")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books WHERE BookID = ?", (book_id,))
    book = cursor.fetchone()
    if not book:
        print("Book not found!")
        return

    print("Enter new details (leave blank to keep unchanged):")
    title = input(f"Title (Current: {book[1]}): ") or book[1]
    author = input(f"Author (Current: {book[2]}): ") or book[2]
    isbn = input(f"ISBN (Current: {book[3]}): ") or book[3]
    status = input(f"Status (Current: {book[4]}): ") or book[4]

    cursor.execute("UPDATE Books SET Title = ?, Author = ?, ISBN = ?, Status = ? WHERE BookID = ?",
                   (title, author, isbn, status, book_id))
    conn.commit()
    print("Book details updated successfully!")

def delete_book(conn):
    book_id = input("Enter BookID to delete: ")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
    cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    conn.commit()
    print("Book and related things deleted successfully!")

def main():
    conn = connect_db()
    create_tables(conn)

    while True:
        print(
            "\n1. Add a new book\n2. Find a book's detail\n3. Find a book's reservation status\n4. View all books\n5. Modify book details\n6. Delete a book\n7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_book(conn)
        elif choice == '2':
            find_book(conn)
        elif choice == '3':
            search_by_identifier(conn)
        elif choice == '4':
            view_all_books(conn)
        elif choice == '5':
            modify_book(conn)
        elif choice == '6':
            delete_book(conn)
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please enter again.")

    conn.close()

if __name__ == "__main__":
    main()
