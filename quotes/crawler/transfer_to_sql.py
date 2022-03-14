import pymysql.cursors
import getpass
import re

SPLIT_PATTERN = re.compile("[-—－]+")

INSERT_SQL = "INSERT INTO `crawler` (`quote`, `lang`, `man`) " \
             "VALUES (%s, %s, %s)"

password = getpass.getpass("请输入密码")

connection = pymysql.connect(host="localhost",
                             user="qza2468",
                             password=password,
                             database="scraped")
if __name__ == "__main__":
    quotes = []
    f = open("quotes_cn.txt", "r")
    while True:
        man = ""
        quote = f.readline()
        if not quote:
            break
        quote = quote.strip()

        quote_splited = re.split(SPLIT_PATTERN, quote)
        if len(quote_splited) > 2:
            continue
        elif len(quote_splited) == 2:
            man = quote_splited[1].strip()
        
        quote = quote.strip()
        if not quote:
            continue

        with connection.cursor() as cursor:
            cursor.execute(INSERT_SQL, [quote, "cn", man])

    f.close()
    f = open("quotes_en.txt")
    while True:
        man = ""
        quote = f.readline()
        if not quote:
            break
        quote = quote.strip()

        quote_splited = re.split(SPLIT_PATTERN, quote)
        if len(quote_splited) > 1:
            man = quote_splited[-1]
        quote = "".join(quote_splited[:-1])

        quote = quote.strip()
        if not quote:
            continue

        with connection.cursor() as cursor:
            cursor.execute(INSERT_SQL, [quote, "en", man])

connection.commit()
connection.close()