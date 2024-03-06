from flask import Flask, render_template, request, session, redirect,url_for,jsonify
import sqlite3
import webbrowser
import json
import random,string

class Database:
    def __init__(self) -> None:
        pass
    def all_user(self):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.execute("SELECT * FROM user")
        data = cursor.fetchall()
        self.conn.close()
        return data
    def all_shopping_car(self):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.execute("SELECT * FROM shopping_car")
        data = cursor.fetchall()
        self.conn.close()
        return data
    def add_shopping_car(self,shopping_car):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO shopping_car (`username`, `product`,`price`,`amount`) VALUES (?,?,?,?)", (shopping_car["username"],shopping_car["product"],shopping_car["price"], shopping_car["amount"]))
        self.conn.commit()
        self.conn.close()
        return 0
    def add_user(self,user):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO user ('username', 'password','email')\
                        VALUES (?,?,?)", (user["username"], user["password"],user["email"]))
        self.conn.commit()
        self.conn.close()
    def all_product(self):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.execute("SELECT * FROM product")
        data = cursor.fetchall()
        self.conn.close()
        return data
    def add_product(self,product):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO product (product_img, product_name,product_price,\
                       product_description_1,product_description_2,product_description_3,\
                       product_description_4) VALUES (?,?,?,?,?,?,?)", (product["product_img"],\
                        product["product_name"],product["product_price"], product["product_description_1"],\
                        product["product_description_2"],product["product_description_3"],\
                        product["product_description_4"]))
        self.conn.commit()
        self.conn.close()
    def all_order(self):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.execute("SELECT * FROM orders")
        data = cursor.fetchall()
        self.conn.close()
        return data
    def add_order(self,orders):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.cursor()
        if "credit_card" in orders:
            cursor.execute("INSERT INTO orders (`username`, `product`,`price`,`amount`,`total_price`,`address`,`how_to_pay`,`credit_card`) VALUES (?,?,?,?,?,?,?,?)", (orders["username"],orders["product"],orders["price"], orders["amount"],orders["total_price"],orders["address"],orders["how_to_pay"],orders["credit_card"]))
        else:
            cursor.execute("INSERT INTO orders (`username`, `product`,`price`,`amount`,`total_price`,`address`,`how_to_pay`) VALUES (?,?,?,?,?,?,?)", (orders["username"],orders["product"],orders["price"], orders["amount"],orders["total_price"],orders["address"],orders["how_to_pay"]))
        self.conn.commit()
        self.conn.close()
    def updata_order_state(self,orders):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.cursor()
        cursor.execute("UPDATE orders SET state=? WHERE username=? AND product=?", (orders["state"],orders["username"],orders["product"]))
        self.conn.commit()
        self.conn.close()
    def remove_shopping_car(self,orders):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM shopping_car WHERE username=? AND product=?", (orders["username"],orders["product"]))
        self.conn.commit()
        self.conn.close()
    def updata_product(self,product):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.cursor()
        cursor.execute("UPDATE product SET product_img=?,product_name=?,product_price=?,\
                       product_description_1=?,product_description_2=?,product_description_3=?,\
                       product_description_4=? WHERE rowid=?", (product["product_img"],\
                        product["product_name"],product["product_price"], product["product_description_1"],\
                        product["product_description_2"],product["product_description_3"],\
                        product["product_description_4"],product["id"]))
        self.conn.commit()
        self.conn.close()
    def remove_product(self,product):
        self.conn = sqlite3.connect('account.db')
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM product WHERE rowid=? ", (product["id"],))
        self.conn.commit()
        self.conn.close()


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
def login_state():
    if not session:
        session["login_state"] = "False"
        return "False"
def login_test():
    username = request.form["username"]
    password = request.form["password"]
    user_data = database.all_user()
    for user in user_data:
        if username == user[0]:
            if password == user[1]:
                return_msg = "登入成功"
                session["login_state"] = "True"
                session["username"] = user[0]
                session["password"] = user[1]
                session["email"] = user[2]
                if username == "admin":
                    return_msg = "管理員登入成功"
                    return redirect(url_for('admin_index_msg', msg=return_msg))
                return redirect(url_for('index_msg', msg=return_msg))
            else:
                return_msg = "密碼錯誤"
                return redirect(url_for('login_msg', msg=return_msg))
    else:
        return_msg = "使用者名稱錯誤"
        return redirect(url_for('login_msg', msg=return_msg))
def register_test():
    user = {}
    print(request.form)
    user["username"] = request.form["username"]
    user["password"] = request.form["password"]
    user["email"] =request.form["email"]
    database.add_user(user)
    return_msg = "註冊成功"
    return redirect(url_for('login_msg', msg=return_msg))
def order_deal_with():
    print("|||||||||||||||||||||")
    print(request.form)
    product_values = request.form.getlist("product")
    print(product_values)
    for item in product_values:
        product = {}
        product = (json.loads(item))
        print(product)
        orders = {}
        orders["username"] = product["username"]
        orders["product"] = product["product"]
        orders["price"] = int(product["price"])
        orders["amount"] = int(product["amount"])
        orders["total_price"] = int(product["total_price"])
        orders["address"] = request.form["address"]
        orders["how_to_pay"] = request.form["how_to_pay"]
        if "credit_card" in request.form:
            orders["credit_card"] = request.form["credit_card"]
        print(orders)
        database.add_order(orders)
        database.remove_shopping_car(orders)
def credit_card_deal_with():
    credit_card_ = request.get_json(force=True)
    value = credit_card_["value"]
    value_ =value
    list_value = list(value)
    list_value_ =[]
    total = 0
    # print(list_value)
    for i in range(16):
        list_value_ .append (int(list_value[i]))
        if i%2 == 0:
            list_value_[i] = 2*(list_value_[i])
            if list_value_[i] > 9:
                x = list_value_[i]%10
                y = list_value_[i]//10
                list_value_[i] = x + y
        total += list_value_[i]
    # print(total)
    if total %10 == 0:
        return "True"
    else:
        return "False"
def order_state_deal_with():
    print("\\\\\\")
    print(request.form)
    state_list = request.form.getlist("state")
    print(state_list)
    data = database.all_order()
    for i in range(len(data)):
        orders = {}
        orders["username"] = data[i][0]
        orders["product"] = data[i][1]
        orders["state"] = state_list[i]
        print(orders)
        database.updata_order_state(orders)
def updata_product_data_deal_with():
    data = request.get_json(force=True)
    print(",,,,")
    print(data)
    conn = sqlite3.connect('account.db')
    cursor = conn.execute("SELECT rowid FROM product")
    rowid_list = cursor.fetchall()
    conn.close()
    print(rowid_list)
    i = 0
    for key in data.keys():
        product = {}
        item = data[key]
        product["product_img"] = item[0]
        product["product_name"] = item[1]
        product["product_price"] = item[2]
        product["product_description_1"] = item[3]
        product["product_description_2"] = item[4]
        product["product_description_3"] = item[5]
        product["product_description_4"] = item[6]
        product["id"] = int(rowid_list[i][0])
        print(product)
        database.updata_product(product)
        i += 1
def add_shopping_car_data_deal_with():
    pass
app = Flask(__name__)
app.secret_key = generate_random_string(20)
print(app.secret_key)

database = Database()


# 首頁頁面
@app.route('/',methods=['GET'])
def index():
    login_state()
    print(session)
    return render_template("index.html")
# 首頁 (傳訊息)
@app.route("/<msg>", methods=["GET"])
def index_msg(msg):
    login_state()
    return render_template("index.html", message=msg)

# 登入頁面
@app.route('/login',methods=['GET', 'POST'])
def login():
    login_state()
    if request.method == "POST":
        return login_test()
    return render_template("login.html")
# 登入 (傳訊息)
@app.route("/login/<msg>", methods=["GET"])
def login_msg(msg):
    login_state()
    return render_template("login.html", message=msg)

# 註冊頁面
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        return register_test()
    return render_template("register.html")

# 網路商店頁面
@app.route("/store", methods=["GET"])
def store():
    login_state()
    return render_template("store.html")

# 購物車頁面
@app.route("/shopping_car", methods=["GET"])
def shopping_car_():
    login_state()
    return render_template("shopping_car.html")

# 管理員首頁
@app.route("/admin_index", methods=["GET"])
def admin_index():
    login_state()
    return render_template("admin_index.html")

# 管理員首頁(傳訊息)
@app.route("/admin_index/<msg>", methods=["GET"])
def admin_index_msg(msg):
    login_state()
    return render_template("admin_index.html", message=msg)

# 查看/更新訂單狀態頁面
@app.route("/admin_order", methods=["GET"])
def admin_order():
    login_state()
    return render_template("admin_order.html")

# 修改商品頁面
@app.route("/admin_product_change", methods=["GET"])
def admin_product_change():
    login_state()
    return render_template("admin_product_change.html")

# 預覽商店頁面
@app.route("/admin_product_page", methods=["GET"])
def admin_product_page():
    return render_template("admin_product_page.html")

# ----------------------------------------------------

# 登出
@app.route('/logout',methods=['GET'])
def logout():
    session.clear()
    login_state()
    return render_template("index.html")

# 信用卡規則
@app.route("/shopping_car/credit_card", methods=["POST"])
def credit_card():
    return_msg = credit_card_deal_with()
    return jsonify(return_msg)



@app.route("/admin_order_state", methods=["GET","POST"])
def admin_order_state():
    login_state()
    if request.method == "POST":
        order_state_deal_with()
    return render_template("admin_order.html")
@app.route("/login/check", methods=["GET"])
def login_check():
    if session["login_state"] == "True":
        session_dict = dict(session)
        return jsonify(session_dict) 
    else:
        return jsonify("False") 


@app.route("/add_shopping_car", methods=["POST"])
def store_add_shopping_car():
    product_list = request.get_json(force=True)
    shopping_car = {}
    all_product_data = database.all_product()
    product_id = int(product_list["product_id"])
    amount = product_list["amount"]
    shopping_car["username"] = session["username"]
    shopping_car["product"] = all_product_data[product_id][1]
    if ',' in str(all_product_data[product_id][2]):
        shopping_car["price"] = int(all_product_data[product_id][2].replace(',', ''))
    else:
        shopping_car["price"] = int(all_product_data[product_id][2])
    
    shopping_car["amount"] = int(amount)
    print(shopping_car)
    data = []
    data = database.all_shopping_car()
    for item in data:
        if item[0] == shopping_car["username"] and item[1] == shopping_car["product"]:
            shopping_car["amount"] = item[3]+shopping_car["amount"]
            conn = sqlite3.connect("account.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE shopping_car SET amount=? WHERE username=? AND product=?", (shopping_car["amount"], shopping_car["username"], shopping_car["product"]))
            conn.commit()
            conn.close()
            return jsonify("successful")
    else:
        database.add_shopping_car(shopping_car)
    return jsonify("successful")
@app.route("/get_product_data", methods=["GET"])
def get_product_data():
    data = database.all_product()
    return jsonify(data)



@app.route("/get_shopping_car_data", methods=["GET"])
def get_shopping_car_data():
    print("------")
    data = database.all_shopping_car()
    print(data)
    return jsonify(data)

@app.route("/shopping_car/order", methods=["POST"])
def order():
    login_state()
    order_deal_with()
    return render_template("shopping_car.html")
@app.route("/get_order_data", methods=["GET"])
def get_order_data():
    login_state()
    data = database.all_order()
    print(data)
    return jsonify(data)
@app.route("/remove_shopping_car", methods=["POST"])
def remove_shopping_car():
    login_state()
    credit_card_ = request.get_json(force=True)
    print(credit_card_)
    database.remove_shopping_car(credit_card_)
    return jsonify("successful")
    



@app.route("/updata_product_data", methods=["POST"])
def updata_product_data():
    login_state()
    updata_product_data_deal_with()
    return jsonify("successful")





@app.route("/get_all_user_data", methods=["POST"])
def get_all_user_data():
    data = database.all_user()
    print(data)
    return jsonify(data)
@app.route("/add_product_data", methods=["POST"])
def add_product_data():
    # tmp = request.get_json(force=True)
    tmp_list = ["產品圖片","產品名稱","0","描述_1","描述_2","描述_3","描述_4"]
    product = {}
    product["product_img"] = tmp_list[0]
    product["product_name"] = tmp_list[1]
    product["product_price"] = tmp_list[2]
    product["product_description_1"] = tmp_list[3]
    product["product_description_2"] = tmp_list[4]
    product["product_description_3"] = tmp_list[5]
    product["product_description_4"] = tmp_list[6]
    database.add_product(product)
    return jsonify("successful")

        
@app.route("/remove_product_data", methods=["POST"])
def remove_product_data():
    data = request.get_json(force=True)
    print(",,,,")
    print(data["id"])
    tmp = int(data["id"])
    product = {}
    conn = sqlite3.connect('account.db')
    cursor = conn.execute("SELECT rowid FROM product")
    rowid_list = cursor.fetchall()
    conn.close()
    print(rowid_list)
    id = int(rowid_list[tmp][0])
    product["id"] = id
    database.remove_product(product)
    return jsonify("successful")


if __name__ == "__main__":
    app.run(debug=True)
    # url = 'http://localhost:5000/'
    # webbrowser.open_new(url)