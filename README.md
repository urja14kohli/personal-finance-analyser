# 💰 Personal Finance Analyzer (CSV Upload)

Analyze your bank statements (CSV format) and visualize where your money is going – food, rent, travel, shopping, etc. This beginner-friendly project helps you understand your expenses using simple charts.

---

## 🧠 Why This Project?

Learning to build this will teach you:

- How to read and clean data from CSV files
- How to visualize your data with charts
- How to use Streamlit to create web apps in Python
- How to categorize expenses and analyze trends

---

## 🔧 Tech Stack

| Part            | Tool / Library                                       | Why Used                                                   |
| --------------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| Web App UI      | [Streamlit](https://streamlit.io)                    | Easiest way to build web apps in Python                    |
| Data Processing | [Pandas](https://pandas.pydata.org/)                 | Powerful tool for analyzing and cleaning data              |
| Charts / Plots  | [Plotly](https://plotly.com/python/) or `matplotlib` | To show your spending visually                             |
| IDE             | Cursor Pro                                           | To help you write and debug Python code with AI assistance |

---

## 📦 Features

- [x] Upload bank statement in `.csv` format
- [x] Automatically clean and read your file
- [x] Categorize expenses (Food, Rent, Travel, etc.)
- [x] Show total spending by category
- [x] Month-over-month comparison chart
- [ ] Export analyzed data (coming soon!)

---

## 📁 Folder Structure

```
personal-finance-analyzer/
├── app.py                # Main Streamlit app
├── requirements.txt      # List of Python libraries to install
├── sample_statement.csv  # Sample input CSV for testing
└── README.md             # You are here!
```

---

## 🖼️ UI Overview

A simple and clean layout like this:

```
+------------------------------------------------------+
| 📤 Upload Your Bank Statement (CSV)                  |
|  [ Choose File ]                                     |
+------------------------------------------------------+

+------------------------------------------------------+
| 📊 Total Expenses by Category                        |
|  - Food: ₹2,000 | Rent: ₹10,000 | Travel: ₹1,500 ... |
+------------------------------------------------------+

+------------------------------------------------------+
| 📆 Monthly Expense Trend                              |
|  [Chart showing monthly spend for each category]     |
+------------------------------------------------------+

+------------------------------------------------------+
| 📥 Download Cleaned CSV (Optional)                   |
+------------------------------------------------------+
```

---

## 🧪 Sample CSV Format

Your CSV should look something like:

| Date       | Description      | Amount | Type  |
| ---------- | ---------------- | ------ | ----- |
| 2024-05-01 | Zomato           | 450    | Debit |
| 2024-05-03 | Rent - Apartment | 10000  | Debit |
| 2024-05-04 | Uber             | 300    | Debit |

**Note:** You may need to clean and rename columns depending on your bank's format.

---

## 🚀 How to Run (Step-by-Step)

1. **Clone this project**

```
git clone https://github.com/yourusername/personal-finance-analyzer.git
cd personal-finance-analyzer
```

2. **Install dependencies**

```
pip install -r requirements.txt
```

3. **Run the app**

```
streamlit run app.py
```

4. **Open in browser** – You'll see the app at `http://localhost:8501`

---

## 🧠 Tips for Beginners (with Cursor Pro)

- Ask Cursor: "Create a Streamlit file uploader and read CSV using Pandas"
- Then: "Make a bar chart of total amount grouped by category"
- Try debugging one feature at a time, and use `st.write()` to check what's working

---

## ✅ What's Next?

- [ ] Let users assign categories to uncategorized rows
- [ ] Add login system to save sessions
- [ ] Export final report as PDF
- [ ] Link with Google Sheets for real-time updates

---

## 📬 Connect

Made with ❤️ by **Urja Kohli**  
For questions or improvements, drop a mail at: `your.email@example.com`
