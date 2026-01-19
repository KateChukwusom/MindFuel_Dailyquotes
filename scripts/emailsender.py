"""Import Built-in python library to connect to an email server and send mail,
fetch user and quote into from our local database, record what happens, format email properly and
 deliver successsfully
"""
import os
import smtplib
import sqlite3
import logging
from email.utils import formataddr 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
import time
from dotenv import load_dotenv

#load environment variables
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")


"""Set up logging, this ensures every event are recorded in a file called emailsender.log"""
logging.basicConfig(
    filename='emailsender.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
#Check whether everything loaded correctly and logs a warning if something is missing
if not all([SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD]):
    logging.error("Missing email configuration in .env file")
else:
    logging.info("Email Configuration loaded sucessfully")

#Connect to database to get quote from quote table and users from users table
try:
    connection = sqlite3.connect('/home/kate/Dailyquotes/scripts/storage.db')
    cur = connection.cursor()
    logging.info("Connected to SQLite database")
except Exception as e:
    logging.error("Database connection failed")
    connection = None


#Get today's quote
today = date.today().isoformat()
quote = None
author = None

if connection:
    cur.execute("SELECT id, quote, author FROM quotes WHERE date_fetched = ?", (today,))
    quote_row = cur.fetchone()
    if quote_row:
        _, quote, author = quote_row
        logging.info("Found today's quote")
    else:
        logging.warning("No quote found!")
else:
    logging.error("No database connection, cannot fetch quote")

#Get Active Users, we only send to active subscribers
users = []
if connection:
    cur.execute("SELECT name, email FROM users WHERE status = 'active' AND frequency = 'daily'")
    users = cur.fetchall()

    if users:
        logging.info("Active users found")
    else:
        logging.warning("No active daily users found")
else:
    logging.warning("Skipping user fetch")

#Open a secure TLS SMTP connection, connect your email credentials
#TLS(Transport Layer Security) ensures the email content and credentials cannot be read or modified in transit
#We use port 465 with SMTP_SSL for a secure direct connection

if quote and author and users:
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            logging.info("Logged into SMTP server successfully.")


#For each user, create a subject and body that includes their name
            for name, email in users:
                subject = "Your Daily Dose of Inspiration"
                body = f"Dear {name}, Great one, \n\n \"{quote}\"\n-- {author} \n\nGo conquer the world!"


#Construct the email message using MIME
                """MIME-Multipurpose Internet Mail Extensions: It is a standard that defines how email
                messages are formatted so they can include plain text, attachments and special characters safely"""

                msg = MIMEMultipart()
                msg["From"] = formataddr(("MindFuel", SENDER_EMAIL)) 
                msg["To"] = email
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                try:
                    server.send_message(msg)
                    logging.info(f"Email sent successfully to {email}")
                    cur.execute(
                                "INSERT INTO email_logs (email, quote, author, status) VALUES(?, ?, ?,?)",
                                  (email, quote, author, 'success')
                                  )
                    connection.commit()
                except Exception as e:
                    logging.error("Failed to send email to user")
    except Exception as e:
        logging.error(f"SMTP connection error: {e}")
else:
    logging.warning("No quotes or users found")

#close connection
if connection:
    connection.close()
    logging.info("Database connection closed")

logging.info("Email sent successfully")












