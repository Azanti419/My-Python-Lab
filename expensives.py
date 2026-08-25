import csv
import os
from datetime import date

BUDGET = 20000
CATEGORIES = ['Food', 'Transport', 'Shopping', 'Bills', 'Health', 'Entertainment', 'Others']
FILE_NAME = 'expenses.csv'


def create_expense(expense_date, category, description, amount):
	return {'date': expense_date, 'category': category, 'description': description, 'amount': amount}


# summarizes expense by category
def view_summary():
	summary = {}
	for expense in expenses:
		category = expense['category']
		amount = expense['amount']
		summary[category] = summary.get(category, 0) + amount
	print('===== Summary =====')

	for category, total in summary.items():
		totals = f'{category}: ₦{total:,.2f}'
		print(totals)
	print('========================')

	# summarizes expense by amount and gives budget warning
	grand_total = sum(expense['amount'] for expense in expenses)
	print(f'Total Spent: ₦{grand_total:,.2f}')

	if grand_total > BUDGET:
		print(f'⚠️ You have exceeded your budget of ₦{BUDGET:,.2f}!')
	else:
		print(f'✅ You are within the budget of ₦{BUDGET:,.2f}')


def view_chart():
	chart = {}
	for expense in expenses:
		category = expense['category']
		amount = expense['amount']
		chart[category] = chart.get(category, 0) + amount
	print('===== Chart =====')

	grand_total = sum(expense['amount'] for expense in expenses)

	for category, total in chart.items():
		percentage = (total / grand_total) * 100
		filled = int((percentage / 100) * 30)
		empty = 30 - filled
		filled_bar = ('█' * filled)
		empty_bar = ('░' * empty)
		print(f'{category}: {filled_bar}{empty_bar} {percentage:.1f}%')


# gives options to pick categories
def pick_category():
	for index, item in enumerate(CATEGORIES, start=1):
		print(index, item)
	choice = int(input('Choose category: '))
	return CATEGORIES[choice - 1]


def get_expenses():
	expense_date = date.today()
	category = pick_category()
	description = input('Enter place/description: ')
	amount = float(input('Enter amount: '))
	expense = create_expense(expense_date, category, description, amount)
	return expense


def save_expenses():
	with open(FILE_NAME, 'w', newline='') as file:
		fieldnames = ['date', 'category', 'description', 'amount']
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(expenses)


def load_expenses():
	loaded = []
	if not os.path.exists(FILE_NAME):
		return loaded
	else:
		with open(FILE_NAME, 'r') as file:
			reader = csv.DictReader(file)
			for row in reader:
				row['amount'] = float(row['amount'])
				loaded.append(row)
		return loaded


def delete_expenses():
	for index, expense in enumerate(expenses, start=1):
		print(f"{index}. {expense['category']} - {expense['description']} - ₦{expense['amount']:,.2f}")
	choice = int(input('Pick option to delete: '))
	expenses.pop(choice - 1)
	save_expenses()
	print('Expenses deleted ✅')


# main menu interface where all functions come into place
def main_menu():
	while True:
		print('''
	==================================
   ║ 💲 📋   EXPENSES TRACKER   💲 📋  ║
	==================================
     1. Add an Expense ⏬
     2. View all Expenses 👀 
     3. View Summary 📃
     4. View Chart 📊
     5. Delete an Expense ❌
     6. Quit 👋
    ========================''')

		choice = input('Choose Option: ')

		if choice == '1':
			expense = get_expenses()
			expenses.append(expense)
			save_expenses()
			print('Expenses added ✅')

		elif choice == '2':
			print(expenses)

		elif choice == '3':
			view_summary()

		elif choice == '4':
			view_chart()

		elif choice == '5':
			delete_expenses()

		elif choice == '6':
			print('Goodbye 👋')
			break

		else:
			print('option not found 🙄')


expenses = load_expenses()
main_menu()