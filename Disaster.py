from random import randint
import pymysql 
import bankSystem

class Disaster(): 
    def __init__(self, conn1, conn2, cursor1, cursor2):
        self.conn1 = conn1 
        self.conn2 = conn2 
        self.cursor1 = cursor1 
        self.cursor2 = cursor2 
        self.bankClient = bankSystem.Bank(conn1, cursor1, 'mainbank')
        self.backupClient = bankSystem.Bank(conn2, cursor2, 'backupbank')
    
    def backup(self, severity): 
        try:
            self.cursor2.execute("DELETE FROM backupbank")
            self.cursor1.execute("SELECT COUNT(*) from mainbank")
            n = int(self.cursor1.fetchone()[0])

            for i in range(n):
                sql = "INSERT INTO backupbank (ids, name,money,intruder) VALUES(%s,%s,%s,%s)"
                self.cursor2.execute(sql, self.bankClient.get_account(i)) 
                self.conn2.commit() 
                if severity == 'high': 
                    self.cursor1.execute("DELETE FROM mainbank WHERE ids=(%s)", (i))
            
            if severity == 'low': 
                self.cursor1.execute("DELETE FROM mainbank WHERE ids=(%s)", (randint(0,n)))
                
            print('All data was successfully backed up!')  

        except Exception as e: 
            print(f'There was an error backing up the server: {e}') 
            self.conn2.rollback() 
        
    def recover(self): 
        try:
            self.cursor2.execute("SELECT COUNT(*) from backupbank")
            n = int(self.cursor2.fetchone()[0]) 
            self.cursor1.execute("DELETE FROM mainbank")
            
            for i in range(n):
                sql = "INSERT INTO mainbank (ids, name,money, intruder) VALUES(%s,%s,%s,%s)"
                self.cursor1.execute(sql, self.backupClient.get_account(i)) 
                self.conn1.commit() 
            print('All data was successfully recovered!')  
            
        except Exception as e: 
            print(f'There was an error recovering from backup site: {e}') 
            self.conn1.rollback()  
    
    def simulate_earthquake(self, severity): 
        print('THERE WAS AN EARTHQUAKE!') 
        Disaster.backup(self, severity)  
        
    def simulate_breach(self, intruder): 
        self.cursor1.execute('SELECT name from mainbank WHERE ids=(%s)',(intruder)) 
        intruder_name = self.cursor1.fetchone() 
        print('THERE WAS AN INFORMATION BREACH by: ',intruder_name)
        self.cursor1.execute('update mainbank set intruder=(%s) where ids=(%s)',('Yes',intruder))
        self.cursor2.execute('update backupbank set intruder=(%s) where ids=(%s)',('Yes',intruder))
        