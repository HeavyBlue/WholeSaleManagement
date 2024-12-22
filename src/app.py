from database_manager import DatabaseManager
from flask import Flask, render_template, redirect, url_for, request, jsonify

db_manager = DatabaseManager()

customerID = 0

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    global customerID
    if request.method == 'POST':
        customer_id = int(request.form['customer_id'])
        x = db_manager.login(customer_id)
        if x:
            customerID = customer_id
            return redirect(url_for("home"))
        else:
            return render_template("pages/login.html")
    else:
        if customerID != 0:
            return redirect(url_for("home"))
        else:
            return render_template("pages/login.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route("/exit")
def logout():
    global customerID
    customerID = 0
    return redirect(url_for("index"))


@app.route("/customer_debts")
def customer_debts():
    customers = db_manager.check_customer_debts()
    return render_template("pages/customer-debt.html", customers=customers)


@app.route("/monthly_profit")
def monthly_profit():
    profit = db_manager.monthly_profit()
    return render_template("pages/monthly-profit.html", item=profit)


@app.route("/most_profitable")
def profitable_item():
    item = db_manager.most_profitable()
    return render_template("pages/profit.html", item=item)


@app.route("/create_customer")
def create_customer():
    return render_template("pages/create-customer.html")


@app.route("/create_supplier")
def create_supplier():
    return render_template("pages/create-supplier.html")


@app.route("/payment")
def payment():
    customer_ids = db_manager.get_customer_id_has_unpaid_amount()
    return render_template("pages/payment.html", customer_ids=customer_ids)


@app.route("/buy_item")
def buy_item():
    return render_template("pages/buy-item-from-suppliers.html")


@app.route("/sell_item")
def sell_item():
    return render_template("pages/create-customer.html")


@app.route("/inventory_control")
def inventory_control():
    return render_template("pages/inventory.html")


@app.route("/get_data", methods=["POST"])
def get_data():
    data = request.json.get("customer_id")
    customer = db_manager.get_customers_has_unpaid_amount(data)
    customer = [list(map(str, row)) for row in customer]
    print(customer)
    return jsonify(customer)


@app.route("/update_payment", methods=["POST"])
def update_payment():
    data = request.json
    result = db_manager.payment(data["payment_id"], data["payment_value"])

    if result:
        return jsonify(["success"])
    return jsonify(["error"])


if __name__ == "__main__":
    app.run(debug=True)
