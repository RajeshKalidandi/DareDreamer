import sqlite3
from sqlite3 import Error
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_FILE = 'job_search.db'

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        logger.info(f"Connected to SQLite version: {sqlite3.version}")
    except Error as e:
        logger.error(f"Error connecting to database: {e}")
    return conn

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                url TEXT UNIQUE,
                description TEXT,
                salary TEXT,
                date_posted TEXT,
                date_scraped TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        logger.info("Table created successfully")
    except Error as e:
        logger.error(f"Error creating table: {e}")

def insert_job(conn, job):
    sql = '''INSERT OR REPLACE INTO jobs(title, company, location, url, description, salary, date_posted)
             VALUES(?,?,?,?,?,?,?)'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (job['title'], job['company'], job['location'], job['url'],
                          job['description'], job['salary'], job['date_posted']))
        conn.commit()
        logger.info(f"Job inserted successfully: {job['title']}")
        return cur.lastrowid
    except Error as e:
        logger.error(f"Error inserting job: {e}")
        return None

def get_all_jobs(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM jobs")
        return cur.fetchall()
    except Error as e:
        logger.error(f"Error fetching jobs: {e}")
        return []

if __name__ == '__main__':
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        logger.error("Error! Cannot create the database connection.")