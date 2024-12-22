from database_manager import DatabaseManager

from flask import Flask, render_template, redirect,url_for, request
db_manager = DatabaseManager()

customerID=0

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def index():
    global customerID
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        x = db_manager.login(customer_id)
        if x:
            customerID=customer_id
            return redirect(url_for("home"))
        else:
            return render_template("login.html")
    else:
        if(customerID!=0):
            return redirect(url_for("home"))
        else:
          return render_template("login.html")
    
@app.route('/home')
def home():
    return render_template("home.html")

@app.route("/exit")
def exit():
    global customerID
    customerID=0
    return redirect(url_for("index"))

@app.route("/customer_debts")
def customer_debts():
    customers = db_manager.check_customer_debts()
    return render_template("profitable_item.html",customers=customers)

@app.route("/monthly_profit")
def  monthly_profit():
    profit = db_manager.monthly_profit()
    return render_template("profit.html",profit=profit)
@app.route("/most_profitable")
def profitable_item():
    item = db_manager.most_profitable()
    return render_template("profitable_item.html",item=item)

if __name__ == "__main__":
    app.run(debug=True)
