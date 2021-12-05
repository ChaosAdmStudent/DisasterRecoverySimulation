'''
This script allows you to conveniently make transactions in the database
''' 

import bankSystem  
import pymysql 


def transfer_money(sender, receiver, amount, conn1, cursor1): 

    transferClient = bankSystem.TransferMoney(conn1, cursor1, sender, receiver, amount)
    transferClient.transfer()

if __name__ == '__main__': 

    conn1 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='db')
    cursor1 = conn1.cursor() 

    bankClient = bankSystem.Bank(conn1, cursor1, 'mainbank') 
    bankClient.show_database() 

    sender = int(input('Please enter ID of sender: ')) 
    receiver = int(input('Please enter ID of receiver: ')) 
    amount = int(input('Please enter amount to be sent: '))
    transfer_money(sender, receiver, amount, conn1, cursor1) 