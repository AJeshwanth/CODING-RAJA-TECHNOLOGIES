import matplotlib.pyplot as plt
import time
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['BUDGET_TRACKER']
budget = db['Budget']
def analyze(categories, expenses, duration):
    plt.figure(figsize=(6, 4))
    bars = plt.bar(categories, expenses, color=['red', 'green', 'blue'], width=0.3)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'₹{round(yval, 2)}', ha='center', va='bottom')
    plt.title(f'{duration} Expenditure-{sum(expenses)}₹')
    plt.xlabel('Categories')
    plt.ylabel('Expense (in ₹)')
    plt.show()
def expen(id):
    income=int(input("Enter your income per month: "))
    data={
        "ID":id,
        "Income":income
    }
    totexp=0
    print("....Provide all the expenses per day....")
    while True:
        category=input("Enter the category (1 to exit): ")
        if category == "1": break
        expense=int(input("Enter the Expense Amount: "))
        data[category]=expense
        totexp+=expense*30
    data["Total Expenditure"]= totexp
    print("Your savings are: ", income-totexp)
    time.sleep(1)
    return data
def analyzeexpen():
    while True:
        print("1: Per Day")
        print("2: Per Month")
        print("3: Per Year")
        print("4: Menu")
        cat=[]
        exp=[]
        achoice=int(input("Enter your choice: "))
        for key, value in data.items():
            cat.append(key)
            exp.append(value)
        cat=cat[3:-1]
        exp=exp[3:-1]
        if achoice==1:
            analyze(cat, exp, "Daily")
        elif achoice==2:
            monexp=[]
            for j in exp:
                monexp.append(j*30)
            analyze(cat, monexp, "Monthly")
        elif achoice==3:
            yearexp=[]
            for j in exp:
                yearexp.append(j*365)
            analyze(cat, yearexp, "Yearly")
        else:
            return
while True:
    print("1: To calculate Budget")
    print("2: Analyze Expenses")
    print("3: Modify Expenses")
    print("4: Delete Your Expenses")
    print("5: Exit")
    choice=int(input("Enter your choice: "))
    if choice==1:
        while True:
            id=int(input("create your ID: "))
            valid=budget.find_one({"ID": id})
            if valid:
                print("Already Exists")
                continue
            else:
                data=expen(id)
                budget.insert_one(data)
                print("Your expenses have been stored.")
                break
    elif choice == 2:
        id=int(input("Enter your ID: "))
        data=budget.find_one({"ID": id})
        if data:
            analyzeexpen()
        else:
            print("Wrong ID, Please provide correct ID")
        time.sleep(1)
    elif choice==3:
        id=int(input("Enter your ID: "))
        data=budget.find_one({"ID": id})
        if data:
            budget.delete_one({"ID" : id})
            upd=expen(id)
            budget.insert_one(upd)
            print("Your expenses have been modified successfully")
        else:
            print("Wrong ID, Please provide correct ID")
        time.sleep(1)
    elif choice==4:
        id=int(input("Enter your ID: "))
        data=budget.find_one({"ID": id})
        if data:
            budget.delete_one({"ID" : id})
            print("Your expenses have been deleted successfully")
        else:
            print("Wrong ID, Please provide correct ID")
        time.sleep(1)
        
    else:
        print("Exited...")
        break