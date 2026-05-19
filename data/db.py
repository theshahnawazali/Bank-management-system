# pyright: reportMissingImports=false
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="password",
    database="bank"
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
               user_id INT AUTO_INCREMENT PRIMARY KEY,
               full_name VARCHAR(100),
               username VARCHAR(100) UNIQUE,
               password VARCHAR(100),
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
               account_id INT PRIMARY KEY AUTO_INCREMENT,
               user_id INT,

               FOREIGN KEY (user_id) REFERENCES users(user_id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
               
               account_number BIGINT UNIQUE DEFAULT 0.00,
               account_type ENUM('Saving Account','Current Account'),
               balance DECIMAL(12,2),
               status VARCHAR(20) DEFAULT 'Active',
               created_at DATETIME DEFAULT CURRENT_TIMESTAMP
               );
               """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
               transaction_id INT PRIMARY KEY,
               account_id INT,
               FOREIGN KEY (account_id) REFERENCES accounts(account_id)
                    ON UPDATE CASCADE
                    ON DELETE SET NULL,
               
               transaction_type ENUM('Deposits','Withdraw','Transfer'),
               amount DECIMAL(12,2),
               transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
               description TEXT
               );
    """)
