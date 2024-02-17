from pymongo import MongoClient
from prettytable import PrettyTable
import time
client = MongoClient('mongodb://localhost:27017/')
db = client['TODO_DATABASE']
taskrel = db['TASK']
completTask=db['COMPTASK']
sno=0
marcompc=0

def storetask(data):
    taskrel.insert_one(data)
    print("Your Task Has been stored")
def removetask(index):
    query = {"SNo": index}
    result=taskrel.delete_one(query)
    cresult=completTask.delete_one({'SNo' : index})
    if result.deleted_count > 0 or cresult.deleted_count > 0:
        print("Your task has been removed.")
    else:
        print("Task not found.")
def changetask(index, data):
    fibyind = {'SNo': index}
    newdata = {'$set': data}
    taskrel.update_one(fibyind, newdata)
    print("Your Task has been modified")
def markcomp(index, marcompc):
    query={"SNo" : index}
    getrec=taskrel.find_one(query)
    taskrel.delete_one(query)
    getrec['SNo']=marcompc
    completTask.insert_one(getrec)
    print("Your Task has been Marked as Completed")
def compTask():
    allrecords=completTask.find()
    print("Displaying your completed Tasks....")
    displaytable(allrecords)
def exisTask():
    allrecords=taskrel.find()
    print("Displaying your Existing Tasks....")
    displaytable(allrecords)
def displaytable(tasks):
    table = PrettyTable(["SNo", "Task", "Due Date"])
    for task in tasks:
        table.add_row([task["SNo"], task["Task"], task["Due Date"]])
    print(table)
while True:
    print("1: Add Task")
    print("2: Remove Task")
    print("3: Modify Task")
    print("4: Mark Task as Completed")
    print("5: Display Task")
    print("6: EXIT")
    choice=int(input("Enter your choice: "))
    if choice ==1:
        sno+=1
        task=input("Enter your task: ")
        duedate=input("Enter the due date in format (DD/MM/YYYY): ")
        data={
            "SNo":sno,
            "Task": task,
            "Due Date": duedate
        }
        storetask(data)
        time.sleep(1)
    elif choice ==2:
        index=int(input("Enter your Removing Task index: "))
        removetask(index)
        time.sleep(1)
    elif choice == 3:
        index=int(input("Enter the index to change your task: "))
        newtask=input("Enter your New Task:  ")
        duedate=input("Enter Due Date in format (DD/MM/YYYY): ")
        data={
            "SNo" : index,
            "Task" : newtask,
            "Due Date": duedate
        }
        changetask(index, data)
        time.sleep(1)
    elif choice == 4:
        index=int(input("Enter the index of the task to mark as completed: "))
        marcompc+=1
        markcomp(index, marcompc)
    elif choice == 5:
        print("1: Completed Tasks")
        print("2: Existing Tasks")
        dispchoice=int(input("Enter your choice: "))
        if dispchoice == 1:
            compTask()
        else:
            exisTask()
        time.sleep(1)
    else:
        client.close()
        print("Exited...")
        break
