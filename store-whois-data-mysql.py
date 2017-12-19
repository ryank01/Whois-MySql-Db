import whois
import requests
import MySQLdb


def Whois():
    # returns whois data for given domain
    w = whois.whois('hackerrank.com')
    if isinstance(w.domain_name, list):
        Domain_Name = w.domain_name[0]
    else:
        Domain_Name = w.domain_name
    if isinstance(w.org, list):
        Org_Name = w.org[0]
    else:
        Org_Name = w.org
    if isinstance(w.whois_server, list):
        Whois_Server = w.whois_server[0]
    else:
        Whois_Server = w.whois_server
    if isinstance(w.address, list):
        if w.address[0] == 'null':
            print 'No Address'
        else:
            Address = w.address[0]
    elif w.address == 'null':
        print 'No Address'
    else:
        Address = w.address
    return Domain_Name, Org_Name, Whois_Server, Address


def InsertIpInfo(cursor, db, Domain_Name):
    # api returns owner, location and date last seen of ip for domain passed in
    # inserts these values into the database
    r = requests.get(
        """https://api.viewdns.info/iphistory/?domain=hackerrank.com&apikey=89f94f2c39609baf16ab25dca31e9076ae7a69b6&output=json"""
    )
    data = r.json()
    response = data['response']['records']
    for value in response:
        owner = value['owner']
        ip = value['ip']
        location = value['location']
        lastseen = value['lastseen']

        sql = """INSERT INTO WHOIS_INFO(DOMAIN_NAME,
                 OWNER, IP, LOCATION, LAST_SEEN)
                 VALUES('%s', '%s', '%s', '%s', '%s' )""" % (Domain_Name,
                                                             owner, ip,
                                                             location,
                                                             lastseen)
        try:
            cursor.execute(sql)
            db.commit()
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            db.rollback()
            db.close()
            print e


def ConnectToDb():
    # connect to database
    db = MySQLdb.connect("localhost", "****", "****", "WHOIS")
    cursor = db.cursor()
    return cursor, db


def CreateTable(cursor, db):
    # creates a table in databse
    cursor.execute("DROP TABLE IF EXISTS WHOIS_INFO")
    sql = """CREATE TABLE WHOIS_INFO(
             DOMAIN_NAME CHAR(255) NOT NULL,
             ORG_NAME CHAR(255),
             WHOIS_SERVER CHAR(255),
             ADDRESS CHAR(255),
             OWNER CHAR(255),
             IP CHAR(255),
             LOCATION CHAR(255),
             LAST_SEEN CHAR(255))"""
    cursor.execute(sql)
    db.close()


def InsertWhoisInformation(cursor, db, Domain_Name, Org_Name, Whois_Server,
                           Address):
    # inserts who is info
    sql = """INSERT INTO WHOIS_INFO(
             DOMAIN_NAME, ORG_NAME,
             WHOIS_SERVER, ADDRESS)
             VALUES('%s', '%s', '%s', '%s')""" % (Domain_Name, Org_Name,
                                                  Whois_Server, Address)
    try:
        cursor.execute(sql)
        db.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        db.rollback()
        db.close()
        print e


def main():
    # main function
    cursor, db = ConnectToDb()
    CreateTable(cursor, db)
    Domain_Name, Org_Name, Whois_Server, Address = Whois()
    InsertWhoisInformation(cursor, db, Domain_Name, Org_Name, Whois_Server,
                           Address)
    InsertIpInfo(cursor, db, Domain_Name)


if __name__ == "__main__":
    main()
