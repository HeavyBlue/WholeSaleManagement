import os
import io

from database_manager import DatabaseManager
from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file

db_manager = DatabaseManager()

customerID = 0

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    filtered_data = [item for item in profit if all(x is not None for x in item)]
    return render_template("pages/monthly-profit.html", item=filtered_data)


@app.route("/most_profitable")
def profitable_item():
    item = db_manager.most_profitable()
    return render_template("pages/profit.html", item=item)


@app.route("/customer-list")
def customer_list():
    customers = db_manager.get_customer()
    return render_template("pages/customer-list.html", items=customers)


@app.route("/supplier-list")
def supplier_list():
    suppliers = db_manager.get_supplier()
    return render_template("pages/supplier-list.html", items=suppliers)


@app.route("/payment")
def payment():
    customer_ids = db_manager.get_customer_id_has_unpaid_amount()
    return render_template("pages/payment.html", customer_ids=customer_ids)


@app.route("/buy_item")
def buy_item():
    items = db_manager.get_table_values('suppliers_item')
    return render_template("pages/buy-item-from-suppliers.html", items=items)


@app.route("/sell_item")
def sell_item():
    customer_ids = db_manager.get_customer_id_first_name()
    items = db_manager.get_item_id_name_price()
    return render_template("pages/sell-item-to-customer.html", customer_ids=customer_ids, items=items)


@app.route("/buy_item_from_suppliers")
def buy_item_from_suppliers():
    supp_item_id = request.args.get('supp_item_id')
    item = db_manager.get_suppliers_item_info(int(supp_item_id))
    return render_template("pages/supp-items-buy.html", item=item[0])


@app.route("/inventory_control")
def inventory_control():
    items = db_manager.check_items()
    return render_template("pages/inventory.html", items=items)


@app.route("/get_data", methods=["POST"])
def get_data():
    data = request.json.get("customer_id")
    customer = db_manager.get_customers_has_unpaid_amount(data)
    customer = [list(map(str, row)) for row in customer]
    return jsonify(customer)


@app.route("/update_payment", methods=["POST"])
def update_payment():
    data = request.json
    print(data)
    result = db_manager.payment(data["payment_id"], data["payment_value"])
    if result:
        return jsonify(["success"])
    return jsonify(["error"])


@app.route('/get_customer_data', methods=['POST'])
def get_customer_data():
    data = request.get_data()
    return jsonify({'message': 'success', 'data': data})


@app.route('/update_item_bought', methods=['POST'])
def update_item_bought():
    supp_item_id = request.form.get("supp_item_id")
    quantity = request.form.get("quantity")
    db_manager.buy_item(int(supp_item_id), int(quantity))
    return quantity


@app.route('/create_order', methods=['POST'])
def create_order():
    customer_id = request.form.get("customerSelect")
    item_id = request.form.get("itemSelect")
    quantity = request.form.get("quantity")
    db_manager.sell_item(int(item_id), int(quantity), int(customer_id))
    return render_template('pages/success.html')


@app.route('/photo/<int:item_id>')
def get_photo(item_id):
    photo = db_manager.get_item_image(int(item_id))
    if photo is None:
        return "Fotoğraf bulunamadı", 404
    return send_file(
        io.BytesIO(photo[0]),
        mimetype='image/jpeg',
        as_attachment=False
    )


@app.route('/show-item')
def show_item():
    item_id = request.args.get('item_id')
    item = db_manager.get_items(int(item_id))
    return render_template('pages/show-item.html', item=item)


@app.route('/show-customer')
def show_customer():
    customer_id = request.args.get('customer_id')
    customer = db_manager.get_customer_info(int(customer_id))
    return render_template('pages/show-customer.html', item=customer)


@app.route('/customer-photo/<int:customer_id>')
def customer_photo(customer_id):
    photo = db_manager.get_customer_image(int(customer_id))
    if photo is None:
        return "Fotoğraf bulunamadı", 404
    return send_file(
        io.BytesIO(photo[0]),
        mimetype='image/jpeg',
        as_attachment=False
    )


if __name__ == "__main__":
    app.run(debug=True)
