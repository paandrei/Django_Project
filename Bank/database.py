import sqlite3

class AccouuntDatabase():
    def __init__(self):
        self.db_file = '../Project/db.sqlite3'

    def create_connection(self):
        '''Create a conection to database'''
        try:
            self.conn = sqlite3.connect(self.db_file)
            return self.conn
        except Exception as e:
            print(e)

    def read_from_database(self, iban):
        task = [iban]
        command = '''SELECT * FROM accounts where IBAN = ?'''
        conn = self.create_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(command, task)
            return cursor.fetchall()
        
    def update_balance_in_db(self, IBAN, balance):
        task = [IBAN, balance]
        con =self.create_connection()
        command = '''UPDATE accounts 
                    SET 
                        'Balance_RON' = ?
                    WHERE 
                        IBAN = ?'''
        with con:
            cursor = con.cursor()
            cursor.execute(command,task)

    def read_balance_from_db(self, IBAN):
        command = '''SELECT Balance_RON FROM accounts WHERE IBAN = ?'''
        conn = self.create_connection()
        task = [IBAN]
        with conn:
            cursor = conn.cursor()
            cursor.execute(command, task)
            return cursor.fetchall()   
         
    def read_IBAN_from_db(self):
        password = ''
        command = '''SELECT IBAN FROM accounts WHERE password = ?'''
        conn = self.create_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(command,password)
            return cursor.fetchall()
        
    def read_password_from_db(self, username):
        task = [username]
        command = '''SELECT password FROM accounts WHERE username = ?'''
        conn = self.create_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(command,task)
            return cursor.fetchall()
        
    def read_country_from_db(self, username):
        task = [username]
        command = '''SELECT country FROM accounts WHERE username = ?'''
        conn = self.create_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(command,task)
            return cursor.fetchall()

class AccountRegister():
    def __init__(self, db_file):
        self.db_file = db_file

    def create_connection(self):
        '''Create a conection to database'''
        try:
            self.conn = sqlite3.connect(self.db_file)
            return self.conn
        except Exception as e:
            print(e,'---------')

    def create_table(self):
        command = """CREATE TABLE IF NOT EXISTS Register (
                Action TEXT NOT NULL,
                Amount NUM NOT NULL,
                Currency TEXT NOT NULL,
                Date TEXT NOT NULL
        )"""
        conn =  self.create_connection()

        with  conn:

            cursor = conn.cursor()
            cursor.execute(command)

    def write_in_database(self, action, amount, date, currency):
        characteristics = [action, amount,currency, date ]
        command = '''INSERT INTO Register 
                     (Action, Amount, Date, Currency) VALUES
                     (?,?,?,?)'''
        conn = self.create_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(command, characteristics)

    def read_from_database(self):
        command = '''SELECT * FROM Register'''
        conn = self.create_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(command)
            return cursor.fetchall()
        
    