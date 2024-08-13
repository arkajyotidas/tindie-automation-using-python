#
# @author [Arkajyoti Das]
# @email [das.arkajyoti@zohomail.in]
# @create date 2024-08-11 13:30:46
# @desc [Automatic Tindie Order Insertion To Database By Arkajyoti Das]
# @website [https://www.arkajyotidas.com]
# 

from dotenv import load_dotenv
import mysql.connector, requests, os, math

i = 0

load_dotenv()

t_db_host = os.getenv("tindie_db_host")
t_db_name = os.getenv("tindie_db_name")
t_db_user = os.getenv("tindie_db_user")
t_db_pass = os.getenv("tindie_db_password")
tindie_APIkey = os.getenv("tindie_APIkey")
tindie_username = os.getenv("tindie_username")


tindie_db = mysql.connector.connect (
    host = t_db_host,
    database = t_db_name,
    user = t_db_user,
    password = t_db_pass
    )

tindie_db_cursor = tindie_db.cursor()

t_order_data = requests.get('https://www.tindie.com/api/v1/order/?format=json&username='+tindie_username+'&api_key='+tindie_APIkey).json()

t_total_orders_pages = math.ceil(t_order_data["meta"]["total_count"] / 50)

for i in range(t_total_orders_pages):
    offset = str(50*i)
    t_order_data = requests.get('https://www.tindie.com/api/v1/order/?format=json&username='+tindie_username+'&api_key='+tindie_APIkey+'&offset='+offset).json()
    t_order_count = 0
    for t_order_count in range(t_order_data["meta"]["total_count"]):
        t_customer_company_name = t_order_data["orders"][t_order_count-1]["company_title"]
        t_placed_date = t_order_data["orders"][t_order_count-1]["date"]
        t_shipped_date = t_order_data["orders"][t_order_count-1]["date_shipped"]
        t_customer_email = t_order_data["orders"][t_order_count-1]["email"]
        t_customer_name = t_order_data["orders"][t_order_count-1]["shipping_name"]
        t_order_number = t_order_data["orders"][t_order_count-1]["number"]
        t_customer_contact = t_order_data["orders"][t_order_count-1]["phone"]
        t_shipping_status = t_order_data["orders"][t_order_count-1]["shipped"]
        t_shipping_city = t_order_data["orders"][t_order_count-1]["shipping_city"]
        t_shipping_country = t_order_data["orders"][t_order_count-1]["shipping_country"]
        t_shipping_state = t_order_data["orders"][t_order_count-1]["shipping_state"]
        t_shipping_street = t_order_data["orders"][t_order_count-1]["shipping_street"]
        t_shipping_postcode = t_order_data["orders"][t_order_count-1]["shipping_postcode"]
        t_order_amount_total = t_order_data["orders"][t_order_count-1]["total"]
        t_order_amount_cc_charge = t_order_data["orders"][t_order_count-1]["total_ccfee"]
        t_order_amount_tindie_charge = t_order_data["orders"][t_order_count-1]["total_tindiefee"]
        t_order_amount_received = t_order_data["orders"][t_order_count-1]["total_seller"]
        t_tracking_code = t_order_data["orders"][t_order_count-1]["tracking_code"]
    
        t_order_search_statement = ("select * from tindie_order_list where order_number = %(t_order_number)s")
        tindie_db_cursor.execute(t_order_search_statement,{'t_order_number' : t_order_number})
        search_results = tindie_db_cursor.fetchall()
        row_count = tindie_db_cursor.rowcount
        if row_count == 0:
            tindie_db_insert_stmt_col = ("insert into tindie_order_list (order_number,order_amount_total,order_amount_cc_charge,"
                                         "order_amount_tindie_charge,order_amount_received,placed_date,shipped_date,customer_company_name,"
                                         "customer_email,customer_contact,customer_name,shipping_country,shipping_state,shipping_city,shipping_street,"
                                         "shipping_postcode,shipping_status,tracking_code) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)") 
            tindie_db_insert_stmt_values = (t_order_number,t_order_amount_total,t_order_amount_cc_charge,t_order_amount_tindie_charge,
                                            t_order_amount_received,t_placed_date,t_shipped_date,t_customer_company_name,t_customer_email,
                                            t_customer_contact,t_customer_name,t_shipping_country,t_shipping_state,
                                            t_shipping_city,t_shipping_street,t_shipping_postcode,t_shipping_status,t_tracking_code)
            tindie_db_cursor.execute(tindie_db_insert_stmt_col,tindie_db_insert_stmt_values)
            tindie_db.commit()
            for i in t_order_data['orders'][t_order_count-1]['items']:
                tindie_db_insert_stmt_col = ("Insert into tindie_order_items (order_number,model_name,model_quantity,model_sku) values (%s,%s,%s,%s)")
                t_product_model_name = i["product"]
                t_product_model_quantity = i["quantity"]
                t_product_model_sku = i["sku"]

                tindie_db_insert_stmt_values = (t_order_number,t_product_model_name,t_product_model_quantity,t_product_model_sku)
                tindie_db_cursor.execute(tindie_db_insert_stmt_col,tindie_db_insert_stmt_values)
                tindie_db.commit()

        else:
            continue
    t_order_count = t_order_count+50