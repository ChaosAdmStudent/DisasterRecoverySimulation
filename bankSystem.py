# Bank Client
from tabulate import tabulate 
import pymysql 
from datetime import datetime 
from time import sleep 


class Bank(): 
    def __init__(self, conn, cursor, banktype):
        self.conn = conn 
        self.cursor = cursor 
        self.banktype = banktype
    
    def make_account(self, ids, name, amount): 
        try:
            sql = f"INSERT INTO {self.banktype} (ids, name,money, intruder) VALUES(%s,%s,%s,%s)"
            self.cursor.execute(sql, (ids, name, amount,'No')) 
            self.conn.commit() 
            print('Your account was successfully made! ')  
            
        except Exception as e: 
            print(f'There was an error making your account: {e}') 
            self.conn.rollback() 
    
    def get_account(self, ids): 
        try: 
            self.cursor.execute(f'SELECT * FROM {self.banktype} WHERE ids={ids}')
            result_set = self.cursor.fetchone()
            return result_set
                
        except Exception as e: 
            print(f'There was some error displaying your account: {e}')
    
    def show_all_accounts(self):
        try: 
            self.cursor.execute(f'SELECT name,money FROM {self.banktype}')
            result_set = self.cursor.fetchall()
            mydata = [] 
            for row in result_set:
                mydata.append([row[0], row[1]]) 

            head = ["Name", "Money"]
            print(tabulate(mydata, headers=head, tablefmt="grid"))
            print()
                
        except Exception as e: 
            print(f'There was some error displaying your account: {e}')
            
    def show_database(self): 
        try: 
            self.cursor.execute(f'SELECT * FROM {self.banktype}')
            result_set = self.cursor.fetchall()
            mydata = [] 
            for row in result_set:
                mydata.append([row[0], row[1], row[2],row[3]]) 

            head = ["ID", "Name", "Money", "Intrusion Status"]
            print(tabulate(mydata, headers=head, tablefmt="grid"))
            print()
                
        except Exception as e: 
            print(f'There was some error displaying your account: {e}')
    
    def get_database(self): 
        try: 
            self.cursor.execute(f'SELECT * FROM {self.banktype}')
            result_set = self.cursor.fetchall()
            mydata = [] 
            for row in result_set:
                mydata.append([row[0], row[1], row[2],row[3]]) 

            head = ["ID", "Name", "Money", "Intrusion Status"]
            return tabulate(mydata, headers=head, tablefmt="grid")
              
        except Exception as e: 
            print(f'There was some error displaying your account: {e}')
        
            
    def show_logs(self): 
        try: 
            if self.banktype == 'mainbank': 
                self.cursor.execute('SELECT * from mainlog') 
            elif self.banktype == 'backupbank':
                self.cursor.execute('SELECT * from backuplog') 
                
            result_set = self.cursor.fetchall()
            mydata = [] 
            for row in result_set: 
                mydata.append([row[0], row[1], row[2], row[3]])
            
            head = ["Sender", "Receiver", "T_Start","T_End"]
            print(tabulate(mydata, headers=head, tablefmt="grid"))
            print()
        
        except Exception as e: 
            print(f'There was an error: {e}')

# Transfer Client

class TransferMoney():
    def __init__(self,conn,cursor,A,B,money):
        self.conn = conn
        self.cursor = cursor
        self.A = A
        self.B = B
        self.num = money
        self.intruder_flag = False
        
    def transfer(self):
        try:
            self.cursor.execute('select money from mainbank where ids=(%s)',(self.A))
            a = int(self.cursor.fetchone()[0])
            self.cursor.execute('select money from mainbank where ids=(%s)',(self.B))
            b = int(self.cursor.fetchone()[0])
            
            #Insufficient Balance
            if a<self.num:
                print('Insufficient balance, transfer failed')
                
            #Intruder Check
            self.cursor.execute('SELECT ids FROM mainbank WHERE Intruder=(%s)', ('Yes'))  
            intrusion_results = self.cursor.fetchall()
            n = len(intrusion_results) 
        
            if n>0:         
                for intruder in intrusion_results: 
                    print('Intruder ID: ',intruder[0])
                    if intruder[0] == self.A: 
                        print('SENDER IS AN INTRUDER! TRANSACTION BLOCKED') 
                        self.intruder_flag = True
                        break 
                    if intruder[0] == self.B: 
                        print('RECEIVER IS AN INTRUDER! TRANSACTION BLOCKED') 
                        self.intruder_flag = True
                        break 
                    else: 
                        self.intruder_flag = False 
                   
            if not self.intruder_flag:
                #T his is A transfer operation. Subtract the transfer amount from A's money and add the transfer amount to B's money
                # If there is an error, enter except to perform data rollback
                # It reflects the atomicity of the transaction. Either all or none of the transaction operations are done. 
                # If one of the statements is wrong, all of them will be rolled back         
                
                
                # To get name of the person and store it in logs 
                self.cursor.execute(f'SELECT name,money FROM mainbank WHERE ids={self.A}')
                result_set = self.cursor.fetchone()
                sender = result_set[0] 

                # Make timestamp 
                now = datetime.now() 
                timestamp_start = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f'{sender} sent money at:', timestamp_start)
                
                self.cursor.execute(f'SELECT name,money FROM mainbank WHERE ids={self.B}')
                result_set = self.cursor.fetchone()
                receiver = result_set[0] 
                
                sleep(1.5)
                now = datetime.now() 
                timestamp_end = now.strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute('update mainbank set money=(%s) where ids=(%s)',(a-self.num,self.A))
                self.cursor.execute('update mainbank set money=(%s) where ids=(%s)', (b + self.num, self.B))
                self.cursor.execute("INSERT INTO mainlog (sender, receiver, time_sign_start, time_sign_end) VALUES(%s,%s,%s, %s)", (sender, receiver,timestamp_start, timestamp_end))
                self.conn.commit() 
                print(f'{receiver} received money from {sender} at:', timestamp_end)
                print('Successful transfer')
                
        except Exception as e:
            print(f'Transfer failed, transaction rolled back,Error: {e}')
            self.conn.rollback()
