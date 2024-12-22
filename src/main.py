import psycopg2
from flask import Flask, request, jsonify, render_template
from database_manager import DatabaseManager
import random
from datetime import datetime
import time
db_manager = DatabaseManager()
def addi(table_name,path):
    with open(path ,"r") as datas:
        datas = datas.read().split("\n")
        lenght = len(datas[0])
        for i in datas[1:]:
            values=[]
            i=i.split(",")
            for k in range(3):
                if(k==1):
                    number = random.randint(40000, 50000)
                    values.append(number)
                else:
                    values.append(i[k])
            values.append("1")  
            db_manager.add_to_table(table_name,values)

def add(table_name,path):
    with open(path ,"r") as datas:
        datas = datas.read().split("\n")
        lenght = len(datas[0])
        for i in datas[1:]:
            values=[]
            i=i.split(",")
            for k in i[1:]:
                if(k==""):
                    values.append("1")
                else:
                    values.append(k)
            db_manager.add_to_table(table_name,values)

def add2(table_name,path):
    with open(path ,"r") as datas:
        datas = datas.read().split("\n")
        lenght = len(datas[0])
        for i in datas[1:]:
            time.sleep(0.1)
            values=[]
            i=i.split(",")
            for k in i[1:]:
                if(k==""):
                    number = random.randint(1, 100)
                    values.append(number)
                else:
                    if("/" in k):
                        date_obj = datetime.strptime(k, "%m/%d/%Y")
                        k = date_obj.strftime("%Y/%m/%d")
                    values.append(k)
            db_manager.add_to_table(table_name,values)

addi("Item","/home/heavyblue/Desktop/dbms/WholeSaleManagement/Data/item.csv")
add("Supplier","/home/heavyblue/Desktop/dbms/WholeSaleManagement/Data/Supplier Table.csv")
add2("Suppliers_Item","/home/heavyblue/Desktop/dbms/WholeSaleManagement/Data/Suppliers_Item.csv")
add2("Inbound_Items","/home/heavyblue/Desktop/dbms/WholeSaleManagement/Data/Inbound_Items Table.csv")
add("Customer","/home/heavyblue/Desktop/dbms/WholeSaleManagement/Data/Customer Table.csv")
add2("Orders","/home/heavyblue/Desktop/dbms/WholeSaleManagement/Data/Orders Table.csv")