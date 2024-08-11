from dotenv import load_dotenv
import mysql.connector
import requests
import os
import math

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
        tindie_order_data_number = tindie_order_data["orders"][tindie_order_count-1]["number"]
        tindie_order_data_email = tindie_order_data["orders"][tindie_order_count-1]["email"]
        tindie_search_statement = ("select * from tindie_orders where order_number = %(tindie_order_number)s")
        tindie_db_cursor.execute(tindie_search_statement,{'tindie_order_number' : tindie_order_data_number})
        search_results = tindie_db_cursor.fetchall
        row_count = tindie_db_cursor.rowcount
        if row_count == 0:
            tindie_db_insert_stmt_col = ("insert into tindie_orders (order_number, customer_email) values (%s,%s)") 
            tindie_db_insert_stmt_values = (tindie_order_data_number,tindie_order_data_email)
            tindie_db_cursor.execute(tindie_db_insert_stmt_col,tindie_db_insert_stmt_values)
            tindie_db.commit()
        else:
            continue
    tindie_order_count = tindie_order_count+50