from fastapi import FastAPI, Request
import mariadb
import sys
import json

conn = mariadb.connect(
            user = "test",
            password = "12345abc",
            host = "localhost",
            port = 3306,
            database = "ninjaRun"
         )
cur = conn.cursor();

app = FastAPI(
    title="NinjaRun API",
    description='Super cool API used by Ninjaneers',
    version="1.0.0"
        )

@app.get("/test/")
async def test():
    cur.execute('DESCRIBE User;')
    return list(cur)

@app.get("/update_user/")
async def update_user(var_uid: int, var_dist: float,var_cal: int):    
    query = ('UPDATE User' + 
                ' SET total_distance = (total_distance + '+  str(var_dist) + ')' +
                ' WHERE user_id = ' + str(var_uid) + ';')
    cur.execute(query)
    query = ('UPDATE User' + 
                ' SET total_calories = (total_calories + '+  str(var_cal) + ')' +
                ' WHERE user_id = ' + str(var_uid) + ';')
    cur.execute(query)

    try:
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"

@app.get("/send_route")
async def send_route(var_lat_start: float, var_long_start: float, var_lat_end: float, var_long_end: float, var_town: str, var_dist: float, var_uid: int, var_routf: str):
    query = ('INSERT INTO Routes' +
                ' (town,distance,user_id,lat_start,long_start,lat_end,long_end,route_f)' +
                ' VALUES' + 
                ' ("' + var_town + '",' + str(var_dist) +  ',' + str(var_uid) + ',' + str(var_lat_start) + ',' + str(var_long_start) + ',' + str(var_lat_end) + ',' + str(var_long_end) + ',"' + var_routf +  '");')
    cur.execute(query)
    try:
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"

@app.get("/user_info/")
async def user_info(username: str):
    query = ('SELECT * FROM User u' + 
                ' INNER JOIN History h' + 
                ' ON u.user_id = h.user_id' + 
                ' WHERE u.username = "' + username + '";')
    cur.execute(query)
    columns = [column[0] for column in cur.description]
    results = []
    for row in cur.fetchall():
        results.append(dict(zip(columns,row)))
    query = ('SELECT * FROM User u WHERE u.username = "' + username + '";')
    cur.execute(query)
    columns = [column[0] for column in cur.description]
    results2 = []
    for row in cur.fetchall():
        results2.append(dict(zip(columns,row)))
    res = {"user":results2,"history":results}
    return res

@app.get("/new_user/")
async def new_user(var_un: str, var_pw: str, var_lb: float, var_ft: int, var_in: float, var_pts: int, var_cals: int, var_dist: float,var_nam: str, var_adm: int):
    query = ('INSERT INTO User ' +
                '(username,password,weight,height_ft,height_in,points,total_calories,total_distance,Name,IsAdmin)' +
                ' VALUES ("' + var_un + '","' + var_pw + '",' + str(var_lb) + ',' + str(var_ft) + ',' + str(var_in) + ',' + str(var_pts) + ',' + str(var_cals) + ',' + str(var_dist) + ',"' + var_nam + '",' + str(var_adm) + ');')

    try:
        cur.execute(query)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"

@app.get("/user_stats/")
async def user_stats(user_id: int):
    cur.execute('SELECT * FROM User ' + 
                'WHERE user_id = ' + str(user_id) + ';')
    results = list(cur)
    return results  

@app.get("/user_login/")
async def user_login(username: str,password: str):
    cur.execute('SELECT user_id FROM User ' + 
                'WHERE username = "' + username + '" AND password = "'+ password +'";')
    results = list(cur)
    return results   

