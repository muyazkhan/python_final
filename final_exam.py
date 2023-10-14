class User:
    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = None
        self.balance = 0
        self.loan = 0
        self.transactions = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited ${amount}")
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrew ${amount}")
            print(
                f"Withdrawal successful. ${amount} withdrawn. New balance: ${self.balance}")

        elif amount <= self.total_balance:
            print('The bank is bankrupt')
        else:
            print("Withdrawal amount exceeded.")

    def check_balance(self):
        print(f"Available Balance: ${self.balance}")

    def check_transaction_history(self):
        return self.transactions

    def take_loan(self, amount, bank):
        if bank.loan_enabled:
            if self.loan < 2 and 0 < amount <= self.balance:
                self.balance += amount
                self.loan += 1
                bank.total_loans += amount
                self.transactions.append(f"Took a loan of ${amount}")
                print(f"Loan approved. ${amount} added to your account.")
            else:
                print("Loan not approved.")
        else:
            print("Loan feature is currently disabled by the bank.")

    def transfer(self, recipient, amount, bank):
        if recipient is not None:
            if 0 < amount <= self.balance:
                self.balance -= amount
                recipient.balance += amount
                self.transactions.append(
                    f"Transferred ${amount} to {recipient.name}")
                recipient.transactions.append(
                    f"Received ${amount} from {self.name}")
                print("Transfer successful.")
            else:
                print("Insufficient balance for the transfer.")
        else:
            print("Account does not exist.")


class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def delete_user_account(self, user, bank):
        bank.users.remove(user)
        print(f"Account {user.account_number} deleted successfully.")

    def list_user_accounts(self, bank):
        print("List of User Accounts:")
        for user in bank.users:
            print(f"Account Number: {user.account_number}, Name: {user.name}")

    def see_all_user_accounts(self, bank):
        for user in bank.users:
            print(f"Account Number: {user.account_number}")
            print(f"Name: {user.name}")
            print(f"Email: {user.email}")
            print(f"Address: {user.address}")
            print(f"Account Type: {user.account_type}")
            print(f"Available Balance: ${user.balance}")


class Bank:
    def __init__(self):
        self.users = []
        self.admins = []
        self.total_loans = 0
        self.loan_enabled = True

    def create_admin_account(self, username, password):
        admin = Admin(username, password)
        self.admins.append(admin)
        print("Admin account created successfully.")

    def create_user_account(self, name, email, address, account_type):
        new_user = User(name, email, address, account_type)
        self.users.append(new_user)
        new_user.account_number = len(self.users)+3
        print(
            f"Account created successfully. Your account number is: {new_user.account_number}")

    def get_user_by_account_number(self, account_number):
        for user in self.users:
            if user.account_number == account_number:
                return user
        return None

    def get_total_balance(self):
        total_balance = sum(user.balance for user in self.users)
        print(f"Total Balance: ${total_balance}")

    def get_total_loan_amount(self):
        print(f"Total Loan Amount: ${self.total_loans}")

    def toggle_loan_feature(self):
        self.loan_enabled = not self.loan_enabled
        status = "enabled" if self.loan_enabled else "disabled"
        print(f"Loan feature is now {status}")


bank = Bank()

while True:
    print("\n----Welcome to the National Bank ----")
    print("1. Register a new user account")
    print("2. Register a new admin account")
    print("3. Login as a user")
    print("4. Login as an admin")
    print("5. Exit")

    option = input("Enter your choice: ")

    if option == '1':
        name = input("Enter user's name: ")
        email = input("Enter user's email: ")
        address = input("Enter user's address: ")
        account_type = input("Enter account type (sav/cur): ")
        if account_type == 'sav':
            bank.create_user_account(name, email, address, 'Savings')
        elif account_type == 'cur':
            bank.create_user_account(name, email, address, 'Current')

    if option == "2":
        name = input("Name: ")
        password = input("Password: ")
        bank.create_admin_account(name, password)

    elif option == '3':
        account_number = int(input("Enter your account number: "))
        user = bank.get_user_by_account_number(account_number)
        if user is None:
            print("Account not found.")

        while True:
            print("Select an operation:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Check Transaction History")
            print("5. Take Loan")
            print("6. Transfer Money")
            print("7. Exit")
            operation = input("Enter your choice: ")

            if operation == '1':
                amount = float(input("Enter the deposit amount: $"))
                user.deposit(amount)

            elif operation == '2':
                amount = float(input("Enter the withdrawal amount: $"))
                user.withdraw(amount)

            elif operation == '3':
                user.check_balance()

            elif operation == '4':
                transactions = user.check_transaction_history()
                for transaction in transactions:
                    print(transaction)

            elif operation == '5':
                if bank.loan_enabled:
                    amount = float(input("Enter the loan amount: $"))
                    user.take_loan(amount, bank)
                else:
                    print("Loan feature is currently disabled by the bank.")

            elif operation == '6':
                recipient_account_number = int(
                    input("Enter the recipient's account number: "))
                recipient = bank.get_user_by_account_number(
                    recipient_account_number)
                if recipient:
                    amount = float(
                        input(f"Enter the amount to transfer to {recipient.name}: $"))
                    user.transfer(recipient, amount, bank)
                else:
                    print("Recipient account not found.")

            elif operation == '7':
                break

    elif option == '4':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        authenticated = False

        for admin in bank.admins:
            if admin.username == username and admin.password == password:
                authenticated = True
                break

        if authenticated:
            while True:
                print("Admin Menu:")
                print("1. Create New User Account")
                print("2. Delete User Account")
                print("3. List User Accounts")
                print("4. Bank Balance")
                print("5. Total Loans")
                print("6. Loan Feature")
                print("7. Exit")
                admin_option = input("Enter your choice: ")

                if admin_option == '1':
                    name = input("Enter user's name: ")
                    email = input("Enter user's email: ")
                    address = input("Enter user's address: ")
                    account_type = input("Enter account type (sav/cur): ")
                    if account_type == 'sav':
                        bank.create_user_account(
                            name, email, address, 'Savings')
                    elif account_type == 'cur':
                        bank.create_user_account(
                            name, email, address, 'Current')

                elif admin_option == '2':
                    account_number = int(
                        input("Enter the account number to delete: "))
                    user_to_delete = bank.get_user_by_account_number(
                        account_number)
                    if user_to_delete:
                        admin.delete_user_account(user_to_delete, bank)
                    else:
                        print("Account not found.")

                elif admin_option == '3':
                    admin.list_user_accounts(bank)

                elif admin_option == '4':
                    bank.get_total_balance()

                elif admin_option == '5':
                    bank.get_total_loan_amount()

                elif admin_option == '6':
                    bank.toggle_loan_feature()

                elif admin_option == '7':
                    break
        else:
            print("Authentication failed. Invalid username or password.")

    elif option == '5':
        break

    else:
        print("Invalid choice. Please select a valid option.")
