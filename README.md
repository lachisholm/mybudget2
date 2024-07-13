# mybudget2

## A continuation and rethink of the first version

## Overview

This project I am working on is a Python-based Budget Tracker designed for single parents or single mothers to help users efficiently manage their finances by tracking income and expenses, setting up different types of budgets, and providing detailed transaction summaries. This is currently a work in progress.

The MyBudget2 Tracker allows users to add, deduct, and transfer funds between categories, keep a record of transactions with timestamps, and view both budget summaries and detailed transaction logs. The purpose of this project is to create a user-friendly application that aids users in achieving better financial management and planning, helping to track additional flows of help outside of job-related income.

**Software Demo Video** - Under Construction

## Development Environment

To develop this software, I utilized the following tools and programming languages:

- **Development Tools**: Visual Studio Code (VSCode), Git
- **Programming Language**: Python 3.x
- **Libraries**: None required; the application relies on Python's standard library, particularly datetime, json, decimal, and collections.
- **Version Control**: Git and GitHub for tracking changes and collaborating with other developers.
- **Testing Framework**: PyTest for automated testing to ensure code quality and reliability.

These tools provided a robust and efficient environment for coding, testing, and version control. Visual Studio Code offers a wide range of extensions and integrations that facilitated a seamless development experience. Using Git ensured that the code was versioned and collaborated upon efficiently. Automated testing with PyTest helped maintain code integrity throughout the development process.

## Useful Websites

The following websites were instrumental in the development of this project. They provided valuable resources, tutorials, and documentation that guided me through various aspects of Python programming and application development:

- **[Python Official Documentation](https://docs.python.org/3/)**: Comprehensive documentation on Python, including detailed explanations of modules, libraries, and language features. It is an indispensable resource for understanding Python's capabilities and best practices.
- **[Real Python](https://realpython.com/)**: Offers a wealth of tutorials and articles on Python programming. The practical examples and in-depth discussions helped me to understand complex concepts and apply them effectively in my project.
- **[W3Schools](https://www.w3schools.com/)**: Known for its easy-to-follow tutorials, W3Schools was a great resource for quick references and learning Python syntax and basic programming techniques.
- **[GeeksforGeeks](https://www.geeksforgeeks.org/)**: Offers a variety of coding tutorials and algorithm explanations. It was particularly helpful for understanding the logic and structure required for developing robust Python applications.
- **[Programiz](https://www.programiz.com/)**: Provides clear and concise tutorials with examples, making it easier to grasp Python programming concepts and apply them to real-world scenarios.
- **[Stack Overflow](https://stackoverflow.com/)**: A community-driven question-and-answer site that provided solutions to specific coding problems and facilitated discussions on best practices.
- **[Medium](https://medium.com/)**: Contains articles and tutorials on Python programming and software development, written by experienced developers.
- **[Towards Data Science](https://towardsdatascience.com/)**: Offers insights and tutorials on Python programming, data analysis, and machine learning, which were valuable for implementing advanced features.
- **[Coursera](https://www.coursera.org/)**: Provided access to courses on Python programming and software development, helping to enhance my skills and knowledge.
- **[Kaggle](https://www.kaggle.com/)**: A platform for data science competitions and projects, offering datasets and kernels that were useful for testing and refining the budget tracker.

## Future Work

There are several enhancements and features planned for future versions of this project. These improvements aim to expand the functionality and user experience of the mybudget Tracker:

- **Implement a Graphical User Interface (GUI)**: Using libraries like Tkinter or PyQt to make the application more user-friendly and visually appealing. This will allow users to interact with the budget tracker through a more intuitive interface.
- **Data Visualization Tools**: Integrate data visualization tools using libraries such as Matplotlib or Plotly to help users better understand their financial data. Graphs and charts illustrating income and expense trends would provide valuable insights and aid in financial planning.
- **Exporting and Importing Data**: Enable the export and import of data to/from CSV files to make data management more flexible. Users could back up their data, share it with others, or import data from other financial management tools.
- **User Authentication and Profile Management**: Adding features for user authentication would allow multiple users to use the application with their personalized settings. Each user could have their own budget categories, transaction history, and preferences.
- **Mobile Version**: Developing a mobile version of the application using frameworks like Kivy would allow users to manage their finances on the go. A mobile app would offer convenience and accessibility, making the Budget Tracker a versatile tool for financial management.
- **Budget Recommendations**: Implementing an AI-driven feature to provide users with personalized budget recommendations based on their spending habits and financial goals.
- **Integration with Financial APIs**: Integrate with financial APIs to automatically import transactions from bank accounts and credit cards, reducing manual data entry.
- **Multi-Currency Support**: Enhancing the currency conversion feature to support real-time exchange rates and automatic updates.
- **Expense Categorization**: Implementing machine learning algorithms to automatically categorize expenses based on transaction descriptions.
- **Notifications and Alerts**: Adding features to send notifications and alerts to users when they approach or exceed their budget goals.

## Code Explanation

The core functionality of the MyBudget2 Tracker is implemented in the `BudgetTracker` class. Below is a detailed explanation of its components:

### Class: BudgetTracker

#### Attributes:

- `categories`: A dictionary to store category names and their balances. This allows for easy tracking and updating of financial categories.
- `transactions`: A list to store transaction records. Each record includes the date, category, type (add or deduct), amount, and currency, providing a comprehensive transaction history.
- `budget_type`: Stores the type of budget chosen (Real or Projected). This helps customize the budget setup based on the user's preference.
- `budget_goals`: A dictionary to store budget goals for each category.
- `base_currency`: The base currency for all transactions.
- `exchange_rates`: A dictionary to store exchange rates for different currencies.
- `undo_stack`: A deque to store the previous states for undo functionality.
- `redo_stack`: A deque to store the next states for redo functionality.

#### Methods:

- `__init__()`: Initializes the tracker with default values including categories, transactions, budget type, budget goals, base currency, exchange rates, undo stack, and redo stack.

- `add_category(category_name)`: Adds a new category if it doesn't exist.

- `add_income(category_name, amount, currency="USD", date=None)`: Adds income to a category. It updates the balance, converts the amount to the base currency if necessary, logs the transaction, and checks the budget goal.

- `deduct_expense(category_name, amount, currency="USD", date=None)`: Deducts an expense from a category. It adjusts the balance, converts the amount to the base currency if necessary, logs the transaction, and checks the budget goal.

- `move_money(from_category, to_category, amount, currency="USD", date=None)`: Transfers money between categories. This method combines deduction and addition operations to facilitate fund transfer.

- `view_summary(start_date=None, end_date=None)`: Prints a summary of all categories and their balances within a specified date range. This provides a quick overview of the financial status.

- `view_details(start_date=None, end_date=None)`: Prints all transactions within a specified date range. This offers a detailed log of all financial activities.

- `filter_transactions(start_date=None, end_date=None)`: Filters transactions based on a specified date range.

- `is_within_date_range(date, start_date, end_date)`: Checks if a date is within a specified date range.

- `calculate_balance(category, start_date=None, end_date=None)`: Calculates the balance for a category within a specified date range.

- `setup_budget()`: Sets up the budget type (Real or Projected). This method guides the user through the initial budget setup process.

- `handle_real_budget()`: Handles the setup for a real budget. It prompts the user to enter actual income details.

- `handle_projected_budget()`: Handles the setup for a projected budget.

- `collect_income()`: Prompts the user to enter income details for various predefined categories.

- `run()`: Main loop to run the application and handle user inputs for different budget management actions.

- `get_valid_amount(prompt)`: Prompts the user to enter a valid amount and converts it to Decimal.

- `get_currency()`: Prompts the user to enter a valid currency.

- `get_date()`: Prompts the user to enter a date or defaults to the current date.

- `get_date_range()`: Prompts the user to enter a date range.

- `convert_currency(amount, from_currency, to_currency)`: Converts an amount from one currency to another using predefined exchange rates.

- `format_currency(amount, currency)`: Formats an amount as a string with the specified currency.

- `set_budget_goal()`: Sets a budget goal for a specified category.

- `check_budget_goal(category)`: Checks if the current amount in a category exceeds the budget goal.

- `change_base_currency()`: Changes the base currency and converts all balances and goals to the new base currency.

- `save_to_file(filename='budget_data.json')`: Saves the current budget data to a JSON file.

- `load_from_file(filename='budget_data.json')`: Loads budget data from a JSON

## For Further information

### Contact me @

#### Lora Chisholm

#### loraperrychisholm@gmail.com
