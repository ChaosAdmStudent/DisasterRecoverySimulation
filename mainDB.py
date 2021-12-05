import pymysql
if __name__ == '__main__':
    conn1 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12')
    cursor1 = conn1.cursor() 

    # Create database 

    cursor1.execute('DROP DATABASE db') 
    cursor1.execute('CREATE DATABASE db') 
    conn1.commit()
    cursor1.execute('USE db')

    # Create the table and fill in the data
    sql = '''
    create table mainbank(
    ids int(20) not null primary key comment 'account ID',
    name varchar(30) not null comment 'name', 
    money int(50) not null comment 'account balance', 
    intruder varchar(30) not null comment 'intrusion status'
    );
    '''
    cursor1.execute(sql)
    conn1.commit()

    # Create Log Table 

    sql = '''
    create table mainlog(
    sender varchar(30) not null, 
    receiver varchar(30) not null, 
    time_sign_start TIMESTAMP not null comment 'Timestamp of beginning transaction',
    time_sign_end TIMESTAMP not null comment 'Timestamp of end transaction'
    );
    '''
    cursor1.execute(sql)
    conn1.commit()
    cursor1.close() 
    conn1.close() 