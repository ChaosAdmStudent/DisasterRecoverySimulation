import pymysql 

if __name__ == '__main__': 
    conn2 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12')
    cursor2 = conn2.cursor()  

    # Create database 

    cursor2.execute('DROP DATABASE backupdb') 
    cursor2.execute('CREATE DATABASE backupdb') 
    conn2.commit()
    cursor2.close() 
    conn2.close()
    
    conn2 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='backupdb')
    cursor2 = conn2.cursor() 

    # Create the table and fill in the data
    sql = '''
    create table backupbank(
    ids int(20) not null primary key comment 'account ID',
    name varchar(30) not null comment 'name', 
    money int(50) not null comment 'account balance', 
    intruder varchar(30) not null comment 'intrusion status'
    );
    '''
    cursor2.execute(sql)
    conn2.commit()
    cursor2.close() 
    conn2.close()  

    # Create Log Table 

    conn2 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='backupdb')
    cursor2 = conn2.cursor() 

    sql = '''
    create table backuplog(
    sender varchar(30) not null, 
    receiver varchar(30) not null, 
    time_sign_start TIMESTAMP not null comment 'Timestamp of beginning transaction',
    time_sign_end TIMESTAMP not null comment 'Timestamp of end transaction'
    );
    '''
    cursor2.execute(sql)
    conn2.commit()
    cursor2.close() 
    conn2.close() 