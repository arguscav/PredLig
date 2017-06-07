'''
Created on 29 de set de 2015

@author: CarlosPM
'''
import mysql.connector
from datetime import datetime


if __name__ == '__main__':
    data = datetime.today()
    print 'executando...'
    cnx = mysql.connector.connect(user='root', password='1234',
                              host='127.0.0.1',
                              database='calculos')
    add_employee = ("INSERT INTO resultadopesos "
               "(no1, no2, resultados) "
               "VALUES (%s, %s, %s)")
    cursor = cnx.cursor()
    for i in range(200):
        data_employee = (1, i, 0.1)
        cursor.execute(add_employee, data_employee)
    cnx.commit()
    cursor.close()
    cnx.close()
    print 'terminou!', datetime.today() - data