#
# @author [Arkajyoti Das]
# @email [das.arkajyoti@zohomail.in]
# @create date 2024-08-11 13:30:46
# @desc [Automatic Tindie Order Insertion To Database By Arkajyoti Das]
# @website [https://www.arkajyotidas.com]
# 

from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

t_db_host = os.getenv("tindie_db_host")
t_db_name = os.getenv("tindie_db_name")
t_db_user = os.getenv("tindie_db_user")
t_db_pass = os.getenv("tindie_db_password")

t_c_db_stmt = ("Create Database if not exists "+ t_db_name +" ;")


t_c_tb_tindie_order_list = ("CREATE TABLE tindie_order_list ("
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

t_c_tb_tindie_order_items = ("CREATE TABLE tindie_order_items ("
                                    "order_number bigint NOT NULL,"
                                    "model_name varchar(100) NOT NULL,"
                                    "quantity tinyint NOT NULL,"
                                    "model_sku varchar(50) NOT NULL);")
                   

t_db_init = mysql.connector.connect (
    host = t_db_host,
    user = t_db_user,
    password = t_db_pass
    )

if(t_db_init):
    t_db_init_cursor=t_db_init.cursor()
    t_db_init_cursor.execute(t_c_db_stmt)
    t_db_init_cursor.close()

    tindie_db = mysql.connector.connect (
        host = t_db_host,
        database = t_db_name,
        user = t_db_user,
        password = t_db_pass
    )
    tindie_db_cursor= tindie_db.cursor()
    tindie_db_cursor.execute(t_c_tb_tindie_order_list)
    tindie_db_cursor.execute(t_c_tb_tindie_order_items)
    tindie_db_cursor.close()
else:
    print("Failed To Create Database")
