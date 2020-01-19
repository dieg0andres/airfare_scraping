import smtplib
import email
import ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from config import inputs

def email_lowest_fare(df, recipient):
    '''
    df : a pandas DataFrame with pricing data
    recipient : receipients email address

    data frame must already be filtered for desired departure and arrival airports
    '''

    lowest_price = df['prices'].min()
    info = df.loc[df.prices == lowest_price]

    smtp_server = "smtp.gmail.com"
    port = 587

    sender_email = "diego.a.galindo@gmail.com"
    password = "$Carmen19"

    receiver_email = recipient

    body = info.drop(columns=["info_date"]).to_html(index=False, justify='left')

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = "Airfare Info"
        msg.attach(MIMEText(body, 'html'))
        message = msg.as_string()

        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        msg = 'an error ocurred while sending an email\n' + str(e)
        print(msg)
        sms_msg(msg, '8137489298', 'verizon')

    finally:
        server.quit()


def sms_lowest_fare(all_data_df, phone, provider):
    df = all_data_df
    del all_data_df

    lowest_price = df['prices'].min()
    info = df.loc[df.prices == lowest_price]

    smtp_server = "smtp.gmail.com"
    port = 587

    sms_gateway = ''

    if provider == "verizon":
        sms_gateway = phone + '@vtext.com'
    elif provider == "att":
        sms_gateway = phone + '@txt.att.net'
    else:
        print('an error occurred while trying to send SMS: incorrect provider')

    sender_email = "diego.a.galindo@gmail.com"
    password = "$Carmen19"

    body = inputs['dep'] + " -> " + inputs['arr'] + ' : $' + str(lowest_price)

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = sms_gateway
        msg['Subject'] = ""
        msg.attach(MIMEText(body, 'plain'))
        sms = msg.as_string()

        server.sendmail(sender_email, sms_gateway, sms)

    except Exception as e:
        print('An error occurred in sms_lowest_fare function')
        print(e)

    finally:
        server.quit()

def email_with_att(filename):

    subject = "Airfare Plot"
    body = "Interesting plot data\n\n"
    sender_email = "diego.a.galindo@gmail.com"
    receiver_email = "diego.a.galindo@gmail.com"
    password = "$Carmen19"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    try:

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

    except Exception as e:
        print('an error occurred while trying to email with attachment')
        print(e)

def sms_msg(message, phone, provider):
    smtp_server = "smtp.gmail.com"
    port = 587

    sms_gateway = ''

    if provider == "verizon":
        sms_gateway = phone + '@vtext.com'
    elif provider == "att":
        sms_gateway = phone + '@txt.att.net'
    else:
        print('an error occurred while trying to send SMS: incorrect provider')

    sender_email = "diego.a.galindo@gmail.com"
    password = "$Carmen19"

    body = message

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = sms_gateway
        msg['Subject'] = ""
        msg.attach(MIMEText(body, 'plain'))
        sms = msg.as_string()

        server.sendmail(sender_email, sms_gateway, sms)

    except Exception as e:
        print('An error occurred in sms_msg function')
        print(e)

    finally:
        server.quit()
