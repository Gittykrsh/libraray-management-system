import datetime
from datetime import datetime, timedelta
import os
import json
from colorama import init, Fore, Style
os.getcwd()

init()  # Initialize colorama

class LMS:
    """
    This class is used to keep records of books library.
    It has total four modules: 'Display Books', 'Lend Books', 'Add Books', 'Return Books'
    'list_of_books' should be txt file. 'library_name' should be string.
    """

    def __init__(self, list_of_books, library_name):
        self.list_of_books = "list_of_books.txt"
        self.library_name = library_name
        self.books_dict = {}
        id = 101
        with open(self.list_of_books) as b:
            content = b.readlines()
        for line in content:
            new_id = str(int(max(self.books_dict, default="100")) + 1)
            self.books_dict.update({new_id: {'books_title': line.strip(), 'lender_name': '', 'lend_date': '', 'status': 'Available'}})
            id += 1

        issued_file = "issued_books.json"
        if os.path.exists(issued_file):
            with open(issued_file, "r") as file:
                content = file.read().strip()
                if content:
                    issued_data = json.loads(content)
                    for book_id, data in issued_data.items():
                        if book_id in self.books_dict:
                            self.books_dict[book_id]['status'] = 'Already Issued'
                            self.books_dict[book_id]['lender_name'] = data.get('lender_name', '')
                            self.books_dict[book_id]['lend_date'] = data.get('issue_date', '')    

    def display_books(self):
        print(f"{Fore.CYAN}------------------------List of Books---------------------{Style.RESET_ALL}")
        print("Books ID","\t", "Title")
        print(f"{Fore.CYAN}----------------------------------------------------------{Style.RESET_ALL}")
        for key, value in self.books_dict.items():
            status = value.get("status")
            color = Fore.GREEN if status == 'Available' else Fore.RED
            print(f"{key:<10}{value.get('books_title'):<30}- [{color}{status}{Style.RESET_ALL}]")

    def issue_books(self):
        books_id = input("Enter Book ID : ")
        current_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        print(f"{Fore.BLUE}Current Date : {current_date}\nDue Date : {due_date}\n{Style.RESET_ALL}")

        if books_id in self.books_dict.keys():
            if self.books_dict[books_id]['status'] != 'Available':
                print(f"{Fore.BLUE}This book is already issued to {self.books_dict[books_id]['lender_name']} on {self.books_dict[books_id]['lend_date']}{Style.RESET_ALL}")
                return
            else:
                print(f"{Fore.GREEN}This book is available for issue. You can issue this book for 7 days. Please return it before {due_date}.\n{Style.RESET_ALL}")
                your_name = input("Enter Your Name : ")
                self.books_dict[books_id]['lender_name'] = your_name
                self.books_dict[books_id]['lend_date'] = current_date
                self.books_dict[books_id]['status']= 'Already Issued'
                print(f"{Fore.GREEN}Book Issued Successfully !!!\n{Style.RESET_ALL}")
                self.log_transaction(f"ISSUED Book ID: {books_id} to {your_name}")

                # Save issued book data to a JSON file
                issued_file = "issued_books.json"
                issued_data = {}

                # Load exisiting data
                if os.path.exists(issued_file):
                    with open(issued_file, "r") as file:
                        content = file.read().strip()
                        if content:
                            issued_data = json.loads(content)

                # Add new issued book data
                issued_data[books_id] = {
                    "lender_name": your_name,
                    "issue_date": current_date,
                    "due_date": due_date
                }

                # Save updated data
                with open(issued_file, "w") as file:
                    json.dump(issued_data, file, indent=4) 
        else:
            print(f"{Fore.RED}Book ID Not Found !!!{Style.RESET_ALL}")
            return self.issue_books()

    def add_books(self):
        try:
            new_books = input("Enter Book's Title : ")
            if new_books == "":
                print(f"{Fore.YELLOW}Book's title cannot be empty !!!{Style.RESET_ALL}")
                return self.add_books()
            elif len(new_books) > 50:
                print(f"{Fore.RED}Book's title length is too long !!! Title length limit is 50 characters{Style.RESET_ALL}")
                return self.add_books()

            with open(self.list_of_books, "a") as b:
                b.writelines(f"{new_books}\n")

            new_id = str(int(max(self.books_dict, default="100")) + 1)
            self.books_dict.update({
                new_id: {
                    'books_title': new_books,
                    'lender_name': '',
                    'lend_date': '',
                    'status': 'Available'
                }
            })
            print(f"{Fore.GREEN}The book '{new_books}' has been added successfully !!!{Style.RESET_ALL}")
            self.log_transaction(f"ADDED Book: '{new_books}'")

        except Exception as e:
            print(f"{Fore.RED}Something went wrong while adding the book. Please check.\nError:{Style.RESET_ALL}", e)

    def return_books(self):
        issued_file = "issued_books.json"

        if not os.path.exists(issued_file) or os.stat(issued_file).st_size == 0:
            print(f"{Fore.YELLOW}No books have been issued yet. Please issue a book first.")
            return

        books_id = input("Enter Book ID (or type 'cancel' to exit): ").strip()
        if books_id.lower() == 'cancel':
            print(f"{Fore.BLUE}Returning process cancelled.{Style.RESET_ALL}")
            return
        
        issued_file = "issued_books.json"

        if books_id in self.books_dict.keys():
            if self.books_dict[books_id]['status'] == 'Available':
                print(f"{Fore.BLUE}This book is already available in library. Please check BOOK ID. !!!{Style.RESET_ALL}")
                return self.return_books()
            else:
                # Load issued book data from JSON file
                if not os.path.exists(issued_file):
                    print(f"{Fore.YELLOW}No issued books found.{Style.RESET_ALL}")
                    return
                with open(issued_file, "r") as file:
                    issued_data = json.load(file)

                if books_id not in issued_data:
                    print(f"{Fore.YELLOW}This book was not issued or does not exist in the issued records.{Style.RESET_ALL}")
                    return

                issue_date_str = issued_data[books_id]['issue_date']
                lender_name = issued_data[books_id]['lender_name']
                print(f"{Fore.BLUE}This book was issued to {lender_name} on {issue_date_str}. Please return it.\n{Style.RESET_ALL}")   
                return_date_str = input("Enter return date (YYYY-MM-DD): ")

                try:
                    issue_date = datetime.strptime(issue_date_str, "%Y-%m-%d")
                    return_date = datetime.strptime(return_date_str, "%Y-%m-%d")
                    days_held = (return_date - issue_date).days

                    if days_held > 7:
                        fine = (days_held - 7) * 5
                        print(f"{Fore.RED}You have returned the book {days_held} days late. Your fine is: Rs.{fine}{Style.RESET_ALL}")
                        self.log_transaction(f"RETURNED Book ID: {books_id} by {lender_name} | Late by {days_held - 7} days | Fine: Rs.{fine}")
                    else:
                        print(f"{Fore.GREEN}You have returned the book on time. No fine.{Style.RESET_ALL}")
                        self.log_transaction(f"RETURNED Book ID: {books_id} by {lender_name} | On time")

                    # Update book status
                    self.books_dict[books_id]['lender_name'] = ''
                    self.books_dict[books_id]['lend_date'] = ''
                    self.books_dict[books_id]['status']= 'Available'
                    print(f"{Fore.GREEN}Successfully Updated !!!\n{Style.RESET_ALL}")

                    # Remove from issued_books.json
                    del issued_data[books_id]
                    with open(issued_file, "w") as file:
                        json.dump(issued_data, file, indent=4)

                except ValueError:
                    print(f"{Fore.RED}Invalid date format. Please enter the date in YYYY-MM-DD format.{Style.RESET_ALL}")
                    return
        else:
            print(f"{Fore.RED}Book ID Not Found !!!{Style.RESET_ALL}")

    def remove_books(self):
        books_id = input("Enter Book ID to remove : ")
        if books_id not in self.books_dict:
            print(f"{Fore.RED}Book ID Not Found !!!{Style.RESET_ALL}")
            return
        
        issued_file = "issued_books.json"
        if os.path.exists(issued_file):
            with open(issued_file, "r") as file:
                content = file.read().strip()
                if content:
                    issued_data = json.loads(content)
                    if books_id in issued_data:
                        print(f"{Fore.BLUE}This book is currently issued and cannot be removed. Please return it first.{Style.RESET_ALL}")
                        return
                    
        book_title = self.books_dict[books_id]['books_title']
        confirm = input(f"{Fore.YELLOW}Are you sure you want to remove '{book_title}'? (yes/no): {Style.RESET_ALL}").strip().lower()
        if confirm != 'yes':
            print(f"{Fore.BLUE}Book removal cancelled.{Style.RESET_ALL}")
            return
        # Remove
        del self.books_dict[books_id]
        print(f"{Fore.BLUE}Book '{book_title}' has been removed successfully.{Style.RESET_ALL}")
        self.log_transaction(f"REMOVED Book ID: {books_id} - '{book_title}'")
        with open(self.list_of_books, "w") as file:
            for book in self.books_dict.values():
                file.write(book['books_title'] + "\n")
        print(f"{Fore.GREEN}Book list updated successfully.\n{Style.RESET_ALL}")
        self.books_dict.clear()
        self.__init__(self.list_of_books, self.library_name)

    def list_issued_books(self):
        import json
        issued_file = "issued_books.json"
        if not os.path.exists(issued_file):
            print(f"{Fore.BLUE}No issued book records found.{Style.RESET_ALL}")
            return
        with open(issued_file, "r") as file:
            content = file.read().strip()
            if not content:
                print(f"{Fore.BLUE}No books are currently issued.{Style.RESET_ALL}")
                return
            issued_data = json.loads(content)
        if not issued_data:
            print(f"{Fore.BLUE}No books are currently issued.{Style.RESET_ALL}")
            return
        print(f"\n{Fore.CYAN}--------------------------  Currently Issued Books  --------------------------{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'Book ID':<10}{'Title':<30}{'Lender':<15}{'Issue Date':<12}{'Due Date'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}------------------------------------------------------------------------------{Style.RESET_ALL}")
        for book_id, info in issued_data.items():
            title = self.books_dict.get(book_id, {}).get('books_title', 'N/A')
            print(f"{book_id:<10}{title:<30}{info['lender_name']:<15}{info['issue_date']:<12}{info['due_date']}")
        print(f"{Fore.CYAN}------------------------------------------------------------------------------\n{Style.RESET_ALL}")

    def search_books(self):
        keyword = input("Enter keyword to search: ").strip().lower()
        print(f"{Fore.YELLOW}\nResults for '{keyword}':{Style.RESET_ALL}")
        found = False
        for book_id, info in self.books_dict.items():
            if keyword in info['books_title'].lower():
                found = True
                print(f"{Fore.GREEN}{book_id:<5} | {info['books_title']:<40} | {info['status']}{Style.RESET_ALL}")
        if not found:
            print(f"{Fore.BLUE}No matching books found.{Style.RESET_ALL}")

    def log_transaction(self, message):
        with open("transaction_log.txt", "a") as logfile:
            from datetime import datetime
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            logfile.write(f"{timestamp} {message}\n")

if __name__ == "__main__":
    try:
        mylms = LMS("list_of_books.txt", "Python's")
        press_key_list = {
            "D": "Display Books",
            "I": "Issue Books",
            "A": "Add Books",
            "R": "Return Books",
            "V": "View Issued Books",
            "X": "Remove Books",
            "S": "Search Books",
            "Q": "Quit"
        }
        key_press = False
        while not (key_press == "q"):
            print(f"\n{Fore.CYAN}----------Welcome To Shakya's Library Management System---------{Style.RESET_ALL}\n")
            for key, value in press_key_list.items():
                print("Press", key, "To", value)
            key_press = input("Press Key : ").lower()
            if key_press == "i":
                print("\nCurrent Selection : ISSUE BOOK\n")
                mylms.issue_books()
            elif key_press == "a":
                print("\nCurrent Selection : ADD BOOK\n")
                mylms.add_books()
            elif key_press == "d":
                print("\nCurrent Selection : DISPLAY BOOKS\n")
                mylms.display_books()
            elif key_press == "r":
                print("\nCurrent Selection : RETURN BOOK\n")
                mylms.return_books()
            elif key_press == "v":
                print("\nCurrent Selection : VIEW ISSUED BOOKS\n")
                mylms.list_issued_books()
            elif key_press == "x":
                print("\nCurrent Selection : REMOVE BOOK\n")
                mylms.remove_books()
            elif key_press == "s":
                print("\nCurrent Selection : SEARCH BOOKS\n")
                mylms.search_books()
            elif key_press == "q":
                print(f"\n{Fore.YELLOW}Thank you for using the Library Management System. Goodbye!{Style.RESET_ALL}\n")
                break
            else:
                continue
    except Exception as e:
        print(f"{Fore.RED}Something went wrong. Please check. !!!\nError:{Style.RESET_ALL}", e)
        print(f"{Fore.RED}Exiting the program.{Style.RESET_ALL}")