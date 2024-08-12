#
# @author [Arkajyoti Das]
# @email [das.arkajyoti@zohomail.in]
# @create date 2024-08-11 13:30:46
# @modify date 2024-08-11 13:30:46
# @desc [Tindie Order Automation By Arkajyoti Das]
# @website [https://www.arkajyotidas.com]
# 

from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

tindie_db_host = os.getenv("tindie_db_host")
tindie_db_name = os.getenv("tindie_db_name")
tindie_db_user = os.getenv("tindie_db_user")
tindie_db_password = os.getenv("tindie_db_password")

tindie_create_db_stmt = ("Create Database if not exists "+ tindie_db_name +" ;")

tindie_create_tindie_order_items = ("CREATE TABLE tindie_order_items ("
                                    "order_number bigint NOT NULL,"
                                    "model_number varchar(50) NOT NULL,"
                                    "model_name varchar(100) NOT NULL,"
                                    "quantity tinyint NOT NULL,"
                                    "model_sku varchar(50) NOT NULL);")

tindie_create_tindie_orders_table = ("CREATE TABLE tindie_orders ("
                            "order_id int NOT NULL AUTO_INCREMENT,"
                            "order_number varchar(50) NOT NULL,"
                            "order_amount_total float NOT NULL,"
                            "order_amount_cc_charge float NOT NULL,"
                            "order_amount_tindie_charge float NOT NULL,"
                            "order_amount_received float NOT NULL,"
                            "order_placed_date date NOT NULL,"
                            "order_shipped_date date NOT NULL,"
                            "customer_company_name varchar(255) NOT NULL,"
                            "customer_email varchar(255) NOT NULL,"
                            "customer_contact varchar(255) NOT NULL,"
                            "customer_name varchar(255) NOT NULL,"
                            "shipping_country varchar(255) NOT NULL,"
                            "shipping_state varchar(255) NOT NULL,"
                            "shipping_city varchar(255) NOT NULL,"
                            "shipping_street varchar(255) NOT NULL,"
                            "shipping_postcode varchar(255) NOT NULL,"
                            "order_shipping_status tinyint(1) NOT NULL,"
                            "order_tracking_code varchar(255) NOT NULL,"
                            "order_status enum('new','shipped','completed') NOT NULL DEFAULT 'new',"
                            "PRIMARY KEY (order_id));")
                   

tindie_db_first = mysql.connector.connect (
    host = tindie_db_host,
    user = tindie_db_user,
    password = tindie_db_password
    )

if(tindie_db_first):
    tindie_db_first_cursor=tindie_db_first.cursor()
    tindie_db_first_cursor.execute(tindie_create_db_stmt)
    tindie_db_first_cursor.close()

    tindie_db = mysql.connector.connect (
        host = tindie_db_host,
        database = tindie_db_name,
        user = tindie_db_user,
        password = tindie_db_password
    )
    tindie_db_cursor= tindie_db.cursor()
    tindie_db_cursor.execute(tindie_create_tindie_order_items)
    tindie_db_cursor.execute(tindie_create_tindie_orders_table)
    tindie_db_cursor.close()
else:
    print("Failed To Create Database")
