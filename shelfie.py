import json
import sys

DATA_FILE = "books.json"

#--- Data type
class Book:
  def __init__(self, title, author, genre, intention, color, status="Not Started", reflection=""):
    self.title = title
    self.author = author
    self.genre = genre
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
def safe_input(prompt, book_list = None):
  #takes user input, exits program if user types 'exit'
  user_input = input(prompt).strip()
  if user_input.lower() == "exit":
    if book_list is not None:
      save_books(book_list) #auto save
    print("Books saved. Exiting Shelfie.")
    sys.exit()
  return user_input
    
def display_books(book_list):
  if not book_list:
    print("\nYour Shelfie list is empty.\n")
    return

  print("\nYour Books:")
  for index, book in enumerate(book_list, start=1):
    print(f"{index}. {book.title} by {book.author} | {book.status} | {book.genre} | {book.intention}")

def filter_books(book_list):
  if not book_list:
    print("\nYour Shelfie list is empty.\n")
    return
  print("\nFilter options:")
  print("1. By Status (Not Started, In Progress, Finished)")
  print("2. By Reading Intention")
  print("3. By Genre")
  print("4. Return to main menu")

  choice = safe_input("Choose an option: ")

  if choice == "1":
    status = safe_input("Enter status to filter: ").strip().lower()
    filtered = [b for b in book_list if b.status.lower() == status]
  elif choice == "2":
    intention = safe_input("Enter reading intention to filter: ").strip().lower()
    filtered = [b for b in book_list if b.intention.lower() == intention.lower()]
  elif choice == "3":
    genre = safe_input("Enter book genre to filter: ").strip().lower()
    filtered = [b for b in book_list if b.genre.lower() == genre.lower()]
  else:
    return

  display_books(filtered)

def add_book(book_list):
  #title cannot be empty
  while True:
    title = safe_input("\nEnter book title: ", book_list).strip()
    if title:
      break
    print("Title cannot be empty. Please enter a valid book title.")
    
  author = safe_input("Enter author: ", book_list)
  genre = safe_input("Enter book genre: ", book_list)
  intention = safe_input("Enter reading intention: ", book_list)
  color = safe_input("Enter color: ", book_list)

  new_book = Book(title, author, genre, intention, color)
  book_list.append(new_book)
  save_books(book_list) #auto save

  print("\nBook added successfully.\n")

def edit_book(book_list):
  if not book_list:
    print("\nYour Shelfie list is empty. There is nothing to edit.\n")
    return  # go back to menu immediately
    
  display_books(book_list)

  try:
    choice = int(safe_input("Enter the number of the book to edit: ")) - 1

    #check if book choice is valid
    if choice < 0 or choice >= len(book_list):
      print("Invalid selection. Please enter a valid book number.\n")
      return
    
    book = book_list[choice]

    #title cannot be empty
    while True:
      new_title = safe_input(f"New title (leave blank to keep '{book.title}'): ", book_list).strip()
      if new_title: 
        #update title
        book.title = new_title
        break
      elif new_title == "":
        #keep original title
        break
        
    book.author = safe_input(f"New author (leave blank to keep '{book.author}'): ", book_list) or book.author
    book.genre = safe_input("New book genre (leave blank to keep '{book.genre}'): ", book_list) or book.genre
    book.intention = safe_input("New reading intention (leave blank to keep '{book.intention}'): ", book_list) or book.intention
    book.color = safe_input("New color tag (leave blank to keep '{book.color}'): ", book_list) or book.color

    save_books(book_list) #auto save
    
    print("\nBook updated.\n")

  except ValueError:
    print("Invalid selection.")

def delete_book(book_list):
  if not book_list:
    print("\nYour Shelfie list is empty. There is nothing to delete.\n")
    return  # go back to menu immediately
    
  display_books(book_list)

  try:
    choice = int(safe_input("Enter the number of the book to delete: ")) - 1

    #check if book choice is valid
    if choice < 0 or choice >= len(book_list):
      print("Invalid selection. Please enter a valid book number.\n")
      return
      
    removed_book = book_list.pop(choice)

    save_books(book_list) #auto save
    
    print(f"\n{removed_book.title} removed.\n")

  except ValueError:
    print("Invalid selection.")

def update_status(book_list):
  if not book_list:
    print("\nYour Shelfie list is empty. There is nothing to update.\n")
    return  # go back to menu immediately
    
  display_books(book_list)

  try:
    choice = int(safe_input("Enter the number of the book to change status: ")) - 1

    #check if book choice is valid
    if choice < 0 or choice >= len(book_list):
      print("Invalid selection. Please enter a valid book number.\n")
      return
      
    new_status = safe_input("Enter new status (Not Started, In Progress, Finished): ", book_list)

    book_list[choice].status = new_status

    if new_status.lower() == "finished":
      reflection = safe_input("Enter your reflection of the book: ", book_list)
      book_list[choice].reflection = reflection
    
    save_books(book_list) #auto save

    print("\nStatus updated.\n")

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
    print("6. Filter books")
    print("7. Save and exit")
    
    user_choice = safe_input("Choose an option: ")

    if user_choice in ["1", "2", "3", "4", "5", "6", "7"]:
      return user_choice
    else:
      print("\nInvalid option. Please enter a number between 1-7.\n")
      
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
      filter_books(book_list)

    elif user_choice == "7":
      save_books(book_list)
      print("Books saved. Goodbye.")
      break

  else:
    print("Invalid option. Please try again.")

#--- Run program
if __name__ == "__main__":
  menu()
  
    
