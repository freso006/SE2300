import json

DATA_FILE = "books.json"

#--- Data type
class Book:
  def __init__(self, title, author, intention, color, status="Not Started", reflection=""):
    self.title = title
    self.author = author
    self.intention = intention
    self.color = color
    self.status = status
    self.reflection = reflection

  def to_dict(self):
    return self.__dict__

  @staticmethod
  def from_dict(data):
    return Book(**data)

#--- Data Storage
def load_books():
  try:
    with open(DATA_FILE, "r") as file:
      data = json.load(file)
      return [Book.from_dict(book) for book in data]

  except FileNotFoundError:
    return []

def save_books(book_list):
  with open(DATA_FILE, "w") as file:
    json.dump([book.to_dict() for book in book_list], file, indent=4)

#--- Core Functions
def display_books(book_list):
  if not book_list:
    print("\nYour Shelfie list is empty.\n")
    return

  print("\nYour Books:")
  for index, book in enumerate(book_list, start=1):
    print(f"{index}. {book.title} by {book.author} | {book.status} | {book.intention}")

def add_book(book_list):
  title = input("Enter book title: ")
  author = input("Enter author: ")
  intention = input("Enter reading intention: ")
  color = input("Enter color tag: ")

  new_book = Book(title, author, intention, color)
  book_list.append(new_book)

  print("Book added successfully.")

def edit_book(book_list):
  if not book_list:
    print("\nYour Shelfie list is empty. There is nothing to edit.\n")
    return  # go back to menu immediately
    
  display_books(book_list)

  try:
    choice = int(input("Enter the number of the book to edit: ")) - 1

    #check if book choice is valid
    if choice < 0 or choice >= len(book_list):
      print("Invalid selection. Please enter a valid book number.\n")
      return
    
    book = book_list[choice]

    book.title = input("New title: ")
    book.author = input("New author: ")
    book.intention = input("New reading intention: ")
    book.color = input("New color tag: ")

    print("Book updated.")

  except ValueError:
    print("Invalid selection.")

def delete_book(book_list):
  if not book_list:
    print("\nYour Shelfie list is empty. There is nothing to delete.\n")
    return  # go back to menu immediately
    
  display_books(book_list)

  try:
    choice = int(input("Enter the number of the book to delete: ")) - 1

    #check if book choice is valid
    if choice < 0 or choice >= len(book_list):
      print("Invalid selection. Please enter a valid book number.\n")
      return
      
    removed_book = book_list.pop(choice)

    print(f"{removed_book.title} removed.")

  except ValueError:
    print("Invalid selection.")

def update_status(book_list):
  if not book_list:
    print("\nYour Shelfie list is empty. There is nothing to update.\n")
    return  # go back to menu immediately
    
  display_books(book_list)

  try:
    choice = int(input("Enter the number of the book to change status: ")) - 1

    #check if book choice is valid
    if choice < 0 or choice >= len(book_list):
      print("Invalid selection. Please enter a valid book number.\n")
      return
      
    new_status = input("Enter new status (Not Started, In Progress, Finished): ")

    book_list[choice].status = new_status

    if new_status.lower() == "finished":
      reflection = input("Enter your reflection of the book: ")
      book_list[choice].reflection = reflection

    print("Status updated.")

  except ValueError:
    print("Invalid selection.")

#--- UI
def get_menu_choice():
  while True:
    print("\nMenu:")
    print("1. Display books")
    print("2. Add book")
    print("3. Edit book")
    print("4. Delete book")
    print("5. Update status")
    print("6. Save and exit")
    
    user_choice = input("Choose an option: ")

    if user_choice in ["1", "2", "3", "4", "5", "6"]:
      return user_choice
    else:
      print("\nInvalid option. Please enter a number between 1-6.\n")
      
def menu():
  book_list = load_books()

  while True:
    user_choice = get_menu_choice()

    if user_choice == "1":
      display_books(book_list)

    elif user_choice == "2":
      add_book(book_list)

    elif user_choice == "3":
      edit_book(book_list)

    elif user_choice == "4":
      delete_book(book_list)

    elif user_choice == "5":
      update_status(book_list)

    elif user_choice == "6":
      save_books(book_list)
      print("Books saved. Goodbye.")
      break

  else:
    print("Invalid option. Please try again.")

#--- Run program
if __name__ == "__main__":
  menu()
  
    
