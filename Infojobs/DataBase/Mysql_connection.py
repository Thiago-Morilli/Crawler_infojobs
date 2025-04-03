import mysql.connector
import os


class Mysql_Connector:
    def Connection():
        db_connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="998674629Th.",
        database="Infojobs"
        )

        if db_connection.is_connected():
            print("Conexão com o banco de dados está ativa.")
        else:
            print("Conexão com o banco de dados falhou.")

        cursor = db_connection.cursor()
        
        return [cursor, db_connection]