import smtplib
from time import sleep

from ServerComponents.Suppurt.server import execute_all_res_async


def send_email(email, login, code):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login("chess.classic.official@gmail.com", "ChhessClassicc1488")
    msg = "{0}, thank your for authorization on chess classic club.".format(login)
    msg += "Your authentication code is {0}.".format(code)

    server.sendmail("chess.classic.official@gmail.com", email, msg)
    server.quit()

if __name__ == '__main__':
    while True:
        records = execute_all_res_async("select * from chess.get_emails()")
        for rec in records:
            email = rec[0]
            login = rec[1]
            code = rec[2]
            send_email(email, login, code)
        sleep(5)
