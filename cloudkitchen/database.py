import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

products_db = myclient["products"]
order_management_db = myclient["order_management"]
location_db = myclient["location"]


def get_orders(username):
    order_list = []
    orders_coll = order_management_db['orders']
    for o in orders_coll.find({"username": username}):
        order_list.append(o)

    return order_list


def count_orders(username):
    orders_coll = order_management_db["orders"]
    numberoforders = orders_coll.count({"username": username})

    return numberoforders


def create_order(order):
    orders_coll = order_management_db['orders']
    orders_coll.insert(order)


def get_product(code):
    products_coll = products_db["products"]

    product = products_coll.find_one({"code": code})

    return product


def get_products(code):
    product_list = []

    products_coll = products_db["products"]

    for p in products_coll.find({'stall_id': int(code)}):
        product_list.append(p)

    return product_list


def get_stall(code):
    stalls_coll = products_db["stalls"]
    stall = stalls_coll.find_one({"stall_id": code})

    return stall


def get_stalls():
    stall_list = []
    stalls_coll = products_db["stalls"]
    for p in stalls_coll.find({}):
        stall_list.append(p)

    return stall_list


def get_user(username):
    customers_coll = order_management_db['customers']
    user = customers_coll.find_one({"username": username})
    return user


def change_pw(username, user_pw):
    pw_coll = order_management_db['customers']
    customer = {"username": username}
    change = {"$set": {"password": user_pw}}
    pw_coll.find_one_and_update(customer, change)

    return True


def password(username):
    pw_coll = order_management_db['customers']
    user = pw_coll.find_one({"username": username})
    user_pw = user["password"]

    return user_pw


def get_location():
    location_list = []
    location_col1 = location_db["location"]
    for p in location_col1.find({}):
        location_list.append(p)

    return location_list
