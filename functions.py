from datetime import datetime

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.checked_out = False

    #Check out books
    def check_out(self):
        if not self.checked_out:
            self.checked_out = True
            return True
        else:
            return False
    
    #Return books
    def check_in(self):
        self.checked_out = False
    
    def __str__(self):
        return f"'{self.title}' by {self.author}"

class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.books_checked_out = []
    
    def check_out_book(self, book):
        if book.check_out():
            self.books_checked_out.append(book)
            print(f"{book.title} has been checked out by {self.name}.")
        else:
            print(f"{book.title} is already checked out.")

    def return_book(self, book):
        book.check_in()
        self.books_checked_out.remove(book)
        print(f"{book.title} has been returned by {self.name}.")

    def list_books(self):
        return self.books_checked_out

class Library:
    def __init__(self):
        self.books = []
        self.members = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def add_member(self, member):
        self.members.append(member)
    
    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None
    
    def check_out_book(self, member_id, book_title):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = self.find_book(book_title)
        
        if member and book:
            member.check_out_book(book)
        else:
            print("Member or book not found.")
    
    def check_in_book(self, member_id, book_title):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in member.books_checked_out if b.title == book_title), None)
        
        if member and book:
            member.return_book(book)
        else:
            print("Member or book not found.")

