from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql import querySomething, queryAllthing

# Configure the database
hostname = 'localhost'
port = '3306'
database = 'db01'
username = 'root'
pwd = ''
dburl = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(username, pwd, hostname, port, database)

# create engine and session
engine = create_engine(dburl, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# login interface
def login(idNum, password):
    truepassword = ''
    rs1 = querySomething(engine, 'user', idNum, "userId", "*")
    if rs1 is None:
        return 'flase'
    else:
        rs2 = querySomething(engine, 'user', idNum, "userId", "password")
        for row in rs2:
             truepassword = str(row[0])

    if password == truepassword:
        return 'success'
    else:
        return 'false'


# register interface
def signup(id,password):
    sql = 'insert into user(userId, password, isAdmin) values ({},\'{}\',0)'.format(id,password)
    # sql = 'insert into user() values ({},{},0)'.format(id,password)
    session.execute(sql)
    session.commit()
    session.close()
    return "true"

# Delete Interface
def deleteUser(userid):
    sql = "delete from user where userId = {}".format(str(userid))
    session.execute(sql)
    session.commit()
    session.close()
    return "true"

# Judgment permission interface
def judgeAdmin(idNum):
    global isAdmin
    rs = querySomething(engine, 'user', idNum, "userId", "isAdmin")
    for row in rs:
        isAdmin = str(row[0])

    if isAdmin == '1':
        return "true"
    else:
        return "false"

# Person query
def selectAllUser():
    rs = queryAllthing(engine, 'user', 'userId')
    allUser = []
    for row in rs:
        allUser.append(row[0])

    print(allUser)
    return allUser


