from Infojobs.DataBase.Mysql_connection import Mysql_Connector
from Infojobs.items import InfojobsItem


class InfojobsPipeline:
    def process_item(self, item, spider):
        
        self.save_mysql(item)

    def save_mysql(self, item):
        connector = Mysql_Connector.Connection()
        cursor = connector[0]
        db_connection = connector[1]

        cursor.execute(
           '''CREATE TABLE IF NOT EXISTS Empregos(
            title VARCHAR(100),
            company_name VARCHAR (100),
            location Varchar(60),
            type_work VARCHAR (50),
            min_salary VARCHAR(20),
            max_salary VARCHAR (20),
            description LONGTEXT
            );''' 
        )

        db_connection.commit()      

        insert_query = """
                        INSERT INTO  Empregos(title, company_name, location, type_work, min_salary, max_salary, description)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""" 
        
        cursor.execute(insert_query, (
            item["title"],
            item["company_name"],
            item["location"],
            item["type_work"],
            item["min_salary"],
            item["max_salary"],
            item["description"]
        ))

        db_connection.commit()
        print("Dados salvos com sucesso!")

        cursor.close()
        db_connection.close()