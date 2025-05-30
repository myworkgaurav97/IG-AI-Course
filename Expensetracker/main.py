import csv
''' ========EXPENSE TRACKER=====
Operations: Add Expense, View Expenses, Set Budgte, Track Your Monthly Budget, Save Expenses
 '''
def main():
#Global
    expenseFileToPerformOps = 'expenses.csv'
    newExpensesToAdd = []
    previousExpenses = []
    budgets= {} #year,month,budgetAmount
    from datetime import datetime

    

    # === Add New Expense =====
    def addNewExpense():
        print("===Add you Expense===")
        # Initilizing balnk dictionary
        expense = {}
        info = ['date','category','amount','description']
        for i in info:
            if i == 'date':
                keyInfo = input(f"{i} (YYYY-MM-DD):")
                # Validate date format
                while True:
                    try:
                        #Attmept to parse data value
                        expense[i] = datetime.strptime(keyInfo, '%Y-%m-%d').date()  # Store as date object
                        break  # If successful, exit the loop
                    except ValueError:
                        # If ValueError occurs, prompt user again
                        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                        keyInfo = input(f"{i} (YYYY-MM-DD):")
            elif i == 'amount':
                keyInfo = input(f"{i}:")
                while True:
                    try: 
                        expense[i] = float(keyInfo)
                        break
                    except ValueError:
                        print('Amount must be number')
                        keyInfo = input(f"{i}:")
            else:
                keyInfo = input(f"{i}:")
                expense[i] = keyInfo
        #push the expense on newExpenses
        newExpensesToAdd.append(expense)
        print('Expenses', newExpensesToAdd)
        trackBudgetStatusOfTheMonth(expense['date'])

    #===== ADD EXPENS CLOSED ===#

    #Option selction
    def selectOperationToPerform(ops):
        print(ops)
        opsToGoahead = input('Enter Operation Number: ')
        #Perform operation as per user selection
        match int(opsToGoahead):
            case 1: 
                print('=== ADD NEW EXPENSE ===')
                addNewExpense()
                selectOperationToPerform(opsToshow)
            case 2: 
                print('=== VIWE ADDED EXPENSES ===')
                viewAddedExpenses()
                selectOperationToPerform(opsToshow)
            case 3:
                print('=== SET BUDGET ===')
                setMonthlyBudget()
                selectOperationToPerform(opsToshow)
            case 4:
                print('=== YOUR BUDGET STATUS ===')
                trackBudgetStatusOfTheMonth()
                selectOperationToPerform(opsToshow)
            case 5:
                saveAddedExpenses()
                selectOperationToPerform(opsToshow)
            case 6:
                print('Exit')
                newExpensesToAdd.clear()
                previousExpenses.clear()
            case _:
                print('default')

     #==== VIEW EXPENSES ====#
    #Transform and store on CSV
    def transfromAndStoreOnCSV(data):
        file = open(expenseFileToPerformOps, 'a')
        dataSetTOadd = []
        for data in newExpensesToAdd:
            line = f"\n{data['date']},{data['category']},{data['amount']},{data['description']}"
            dataSetTOadd.append(line)
        file.writelines(dataSetTOadd)
        file.close()

    #Transform CSV data to store on expense list
    def transformCSVDataToStoreOnExpenseList(CSVRecord):
        if all(key != '' for key in CSVRecord):
            return {
                'date': datetime.strptime(CSVRecord[0], '%Y-%m-%d').date(),  # Convert to date object
                'category': CSVRecord[1],
                'amount': CSVRecord[2],
                'description': CSVRecord[3]
            }
        else:
            return 'incomplete'
    
    #view added expenses
    def viewAddedExpenses():
        #Check if newExpensesToAdd is empty
        if len(previousExpenses) == 0:
            print('No Expense Record available!')
            return 'No Expense Record available!'
        #If having records
        collectiveRecordsToShow = previousExpenses + newExpensesToAdd
        for expense in collectiveRecordsToShow:
            if type(expense) == str and expense == 'incomplete':
                print('Incomplete record found, skipping...')
                continue
            # Print each expense in a formatted way
            print(f"Date: {expense['date']}, Category: {expense['category']}, Amount: {expense['amount']}, Description: {expense['description']}")

    def loadExpensesFromCSV():
        #Load CSV file and show all stored expenses
        #Check any of the key is missing on any record skip and show a message that it is incomplete
        #Read file
        expensesFile = open(expenseFileToPerformOps, 'r')
        records = list(csv.reader(expensesFile))
        if len(records[1:]) == 0:
            print('No Expense Record available!')
            return 'No Expense Record available!'
            
        #with map
        transFormdRecordPrevious = (list(map(transformCSVDataToStoreOnExpenseList, records[1:])))
        if transFormdRecordPrevious != []:
            previousExpenses.extend(transFormdRecordPrevious)
    #====VIEW EXPENSES CLOSED===#

    #====SAVE EXPENSES====#
    def saveAddedExpenses():
        if len(newExpensesToAdd) == 0:
            print('No new records to save')
            return 'No new Expesne has been added to save'
        #If having records
        file = open(expenseFileToPerformOps,'r')
        contentInFile = list(csv.reader(file))
        #check if header exists
        file.close()
        if len(contentInFile) == 0:
            fileTowrite = open(expenseFileToPerformOps, 'w')
            header = "date,category,amount,description\n"
            fileTowrite.write(header)
            fileTowrite.close()
            transfromAndStoreOnCSV(newExpensesToAdd)
        else:
            transfromAndStoreOnCSV(newExpensesToAdd)
        print('Expenses saved successfully!')
        #Clear newExpensesToAdd after saving
        newExpensesToAdd.clear()
        previousExpenses.clear()
        loadExpensesFromCSV()

#SET and TRACK Monthly Budget
    def setMonthlyBudget():
        print('===SET and TRACK BUDGET ===')
        year = input('Enter Buget Year (YYYY): ')
        month = input ('Enter Budget Month (1-12): ')
        budgetAmount = input('Enter Budget amount: ')
        
        budget_key = (year, month) #using touple, immutable and ordered
        if budget_key not in budgets:
            budgets[budget_key] = {} #taking empty dictionary to store amount, key value pair

        #add and update bugets
        budgets[budget_key]['budgetAmount'] = budgetAmount #setting a new object inside bugtes for respective month 
        print(f"Budget for month/year {month}/{year} is set {budgetAmount}")


    def trackBudgetStatusOfTheMonth(expenseDate = None):
        if not expenseDate:
            year = input('Enter the Year: ')
            month = input('Enter the month: ')
        else: 
            year = expenseDate.year
            month = expenseDate.month
            

        budget_key = (str(year),str(month))
        if budget_key not in budgets:
            print('No budget available for the same year month, please set it first..')
            setMonthlyBudget()
        
        #Collective expenses (old + newwly added)
        collectiveEpenses = list(filter(lambda x: x != 'incomplete' and x['date'].year == int(year) and x['date'].month == int(month), previousExpenses + newExpensesToAdd))
        # print('collectiveEpenses', collectiveEpenses)
        if len(collectiveEpenses) > 0:
            total = sum(float(expense['amount']) for expense in collectiveEpenses)
            print('total', total)
            remaining = float(budgets[budget_key]['budgetAmount']) - total
            if remaining < 0:
                print('===OOPs!! You have exceeded your budget for the month!===')
            else:
                print('You are within your budget for the this month!','\nRemaining:', remaining) 
        else:
            print('No expenses found for the month')
            return 'No expenses found for the month'
            
        
        #else====

#main function calling
    loadExpensesFromCSV()
    ops = [{"opsId": 1, "opsName": 'Add Expense'},{"opsId": 2, "opsName": 'View Expenses'},{"opsId": 3, "opsName": 'Set Budget'},{"opsId": 4, "opsName": 'View Budget Status'},{"opsId": 5, "opsName": 'Save Expenses'}, {"opsId": 6, "opsName": 'Exit'}]
    operationNames = []
    for operation in ops:
        name = f"{operation['opsId']}. {operation['opsName']}\n"
        operationNames.append(name)
    opsToshow = ''.join(operationNames)
    print(f"=======Welcome To Expense Tracker!!=========' '\nSelect Choice by giving input as 1 to {len(ops)} \nOperations:")
    selectOperationToPerform(opsToshow)
main()
