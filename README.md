# 📖 Library Book Management System (Console-based)

A Python-based console project for managing a library system. You can issue, return, add, remove, view, and search books easily. It also keeps track of transaction logs and late return fines — everything stored locally via file I/O.

---

## 🚀 Features

| Feature             | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| 📚 Display Books     | List all books with status (Available / Already Issued)                    |
| 📤 Issue Book        | Issue a book to a user with auto due-date generation (7 days from issue)   |
| 📥 Return Book       | Return a book and auto-calculate fine if returned after due date           |
| ➕ Add Book          | Add new book to library with auto-generated ID                             |
| ➖ Remove Book       | Delete book from library (only if not currently issued)                    |
| 👀 View Issued Books | View all currently issued books with lender name, issue and due date       |
| 🔍 Search Book       | Keyword-based title search                                                  |
| 🧾 Transaction Logs  | All transactions are stored in `transaction_log.txt`                       |
| 🧠 Auto ID Handling  | Automatically assigns unique book IDs                                      |
| ❌ Cancel Return     | Allows typing 'cancel' to exit from return loop                            |

---

## 🧱 Project Structure

```
📁 Library-Management-System/
├── LMS.py                  # Main program
├── list_of_books.txt       # Text file containing available books
├── issued_books.json       # JSON file for tracking issued books
├── transaction_log.txt     # Log of all operations
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🧑‍💻 Tech Stack

- Python 3.10+
- `colorama` — for colored terminal outputs
- JSON, TXT — for file storage
- Basic OOP & date-time modules

---

## 📦 Installation

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## 🛠️ How to Run

```bash
python LMS.py
```

Choose from the menu:

| Key | Operation          |
|-----|--------------------|
| D   | Display Books      |
| I   | Issue Book         |
| R   | Return Book        |
| A   | Add Book           |
| X   | Remove Book        |
| V   | View Issued Books  |
| S   | Search Book        |
| Q   | Quit the Program   |

---

## 🧮 Fine Calculation

| Days Late | Fine (Rs.)    |
|-----------|---------------|
| 0 - 7     | No fine        |
| > 7 Days  | ₹5 per day     |

---

## 📂 File Examples

**📘 list_of_books.txt:**
```
Python
Java
C Programming
```

**📄 issued_books.json:**
```json
{
  "106": {
    "lender_name": "Dinga",
    "issue_date": "2025-06-12",
    "due_date": "2025-06-19"
  }
}
```

**🧾 transaction_log.txt:**
```
[2025-06-12 10:42:00] ISSUED Book ID: 106 to Dinga
[2025-06-19 11:05:13] RETURNED Book ID: 106 by Dinga | On time
```

---

## 🧪 Sample Use Case

```bash
Enter Book ID : 106
Current Date : 2025-06-12
Due Date : 2025-06-19

This book is available for issue...
Enter Your Name : Dinga
Book Issued Successfully !!!

# Later...
Enter return date (YYYY-MM-DD): 2025-06-22
You have returned the book 10 days late. Your fine is: Rs.15
```

---

## 💡 Future Suggestions (Add-ons)

- GUI using Tkinter / PyQt
- Student login system
- Search filters (status/category)
- Backup/restore JSON records
- Integration with SQLite or MongoDB

---

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 👏 Credits

Made with ❤️ by **Shakya**  
Guided by **Dinga (ChatGPT)**