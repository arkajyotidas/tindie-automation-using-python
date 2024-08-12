#
# @author [Arkajyoti Das]
# @email [das.arkajyoti@zohomail.in]
# @create date 2024-08-11 13:30:46
# @modify date 2024-08-11 13:30:46
# @desc [Tindie Order Automation By Arkajyoti Das]
# @website [https://www.arkajyotidas.com]
# 

from dotenv import load_dotenv
import mysql.connector, requests, os, math

i = 0

load_dotenv()

tindie_db_host = os.getenv("tindie_db_host")
tindie_db_name = os.getenv("tindie_db_name")
tindie_db_user = os.getenv("tindie_db_user")
tindie_db_password = os.getenv("tindie_db_password")
tindie_APIkey = os.getenv("tindie_APIkey")
tindie_username = os.getenv("tindie_username")


tindie_db = mysql.connector.connect (host = tindie_db_host,database = tindie_db_name,user = tindie_db_user,password = tindie_db_password)
tindie_db_cursor = tindie_db.cursor()

tindie_total_order_data = requests.get('https://www.tindie.com/api/v1/order/?format=json&username='+tindie_username+'&api_key='+tindie_APIkey).json()

tindie_total_orders_pages = math.ceil(tindie_total_order_data["meta"]["total_count"] / 50)

for i in range(tindie_total_orders_pages):
    offset = str(50*i)
    tindie_order_data = requests.get('https://www.tindie.com/api/v1/order/?format=json&username='+tindie_username+'&api_key='+tindie_APIkey+'&offset='+offset).json()
    tindie_order_count = 0
    for tindie_order_count in range(tindie_total_order_data["meta"]["total_count"]):
        tindie_order_data_customer_company_name = tindie_order_data["orders"][tindie_order_count-1]["company_title"]
        tindie_order_data_order_placed_date = tindie_order_data["orders"][tindie_order_count-1]["date"]
        tindie_order_data_order_shipped_date = tindie_order_data["orders"][tindie_order_count-1]["date_shipped"]
        tindie_order_data_customer_email = tindie_order_data["orders"][tindie_order_count-1]["email"]
        tindie_order_data_customer_name = tindie_order_data["orders"][tindie_order_count-1]["shipping_name"]
        tindie_order_data_order_number = tindie_order_data["orders"][tindie_order_count-1]["number"]
        tindie_order_data_customer_contact = tindie_order_data["orders"][tindie_order_count-1]["phone"]
        tindie_order_data_order_shipping_status = tindie_order_data["orders"][tindie_order_count-1]["shipped"]
        tindie_order_data_shipping_city = tindie_order_data["orders"][tindie_order_count-1]["shipping_city"]
        tindie_order_data_shipping_country = tindie_order_data["orders"][tindie_order_count-1]["shipping_country"]
        tindie_order_data_shipping_state = tindie_order_data["orders"][tindie_order_count-1]["shipping_state"]
        tindie_order_data_shipping_street = tindie_order_data["orders"][tindie_order_count-1]["shipping_street"]
        tindie_order_data_shipping_postcode = tindie_order_data["orders"][tindie_order_count-1]["shipping_postcode"]
        tindie_order_data_order_amount_total = tindie_order_data["orders"][tindie_order_count-1]["total"]
        tindie_order_data_order_amount_cc_charge = tindie_order_data["orders"][tindie_order_count-1]["total_ccfee"]
        tindie_order_data_order_amount_tindie_charge = tindie_order_data["orders"][tindie_order_count-1]["total_tindiefee"]
        tindie_order_data_order_amount_received = tindie_order_data["orders"][tindie_order_count-1]["total_seller"]
        tindie_order_data_order_tracking_code = tindie_order_data["orders"][tindie_order_count-1]["tracking_code"]
        if tindie_order_data["orders"][tindie_order_count-1]["payment"]== "complete": 
            tindie_order_data_order_status = "completed"
        else:
            tindie_order_data_order_status = "new"

        tindie_search_statement = ("select * from tindie_orders where order_number = %(tindie_order_number)s")
        tindie_db_cursor.execute(tindie_search_statement,{'tindie_order_number' : tindie_order_data_order_number})
        search_results = tindie_db_cursor.fetchall()
        row_count = tindie_db_cursor.rowcount
        if row_count == 0:
            tindie_db_insert_stmt_col = ("insert into tindie_orders (order_number,order_amount_total,order_amount_cc_charge,"
                                         "order_amount_tindie_charge,order_amount_received,order_placed_date,order_shipped_date,customer_company_name,"
                                         "customer_email,customer_contact,customer_name,shipping_country,shipping_state,shipping_city,shipping_street,"
                                         "shipping_postcode,order_shipping_status,order_tracking_code,order_status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)") 
            tindie_db_insert_stmt_values = (tindie_order_data_order_number,tindie_order_data_order_amount_total,
                                            tindie_order_data_order_amount_cc_charge,tindie_order_data_order_amount_tindie_charge,
                                            tindie_order_data_order_amount_received,tindie_order_data_order_placed_date,tindie_order_data_order_shipped_date,
                                            tindie_order_data_customer_company_name,tindie_order_data_customer_email,
                                            tindie_order_data_customer_contact,tindie_order_data_customer_name,
                                            tindie_order_data_shipping_country,tindie_order_data_shipping_state,
                                            tindie_order_data_shipping_city,tindie_order_data_shipping_street,
                                            tindie_order_data_shipping_postcode,tindie_order_data_order_shipping_status,tindie_order_data_order_tracking_code,
                                            tindie_order_data_order_status)
            tindie_db_cursor.execute(tindie_db_insert_stmt_col,tindie_db_insert_stmt_values)
            tindie_db.commit()
            for i in tindie_order_data['orders'][tindie_order_count-1]['items']:
                tindie_db_insert_stmt_col = ("Insert into tindie_order_items (order_number,model_number,model_name,quantity,model_sku) values (%s,%s,%s,%s,%s)")
                tindie_order_product_model_number = i["model_number"]
                tindie_order_product_model_name = i["product"]
                tindie_order_product_quantity = i["quantity"]
                tindie_order_product_sku = i["sku"]

                tindie_db_insert_stmt_values = (tindie_order_data_order_number,tindie_order_product_model_number,tindie_order_product_model_name,tindie_order_product_quantity,tindie_order_product_sku)
                tindie_db_cursor.execute(tindie_db_insert_stmt_col,tindie_db_insert_stmt_values)
                tindie_db.commit()

        else:
            continue
    tindie_order_count = tindie_order_count+50