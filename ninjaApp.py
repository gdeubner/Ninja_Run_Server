from fastapi import FastAPI, Request, Body
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

@app.post("/send_route")
async def send_route(var_lat_start: float, var_long_start: float, var_lat_end: float, var_long_end: float, var_town: str, var_dist: float, var_uid: int, var_routf: str = Body(...)):
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

@app.get("/update_userprofile/")
async def update_userprofile(user_id:int, username:str, password:str, weight:float, height_ft:int, height_in:float):
    query = ('UPDATE User SET username = "'+username+'", password = "'+password
            +'", weight = "'+str(weight)+ '", height_ft = "'+str(height_ft)+'", height_in = "'
            +str(height_in) + '" where user_id = "'+ str(user_id) +'";')
    try:
        cur.execute(query)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"


@app.get("/route_info/")
async def route_info(user_id : int):
    query = ('SELECT * FROM Routes ' + 
                'WHERE user_id = ' + str(user_id) + ';')
    cur.execute(query)
    columns = [column[0] for column in cur.description]
    results = []
    for row in cur.fetchall():
        results.append(dict(zip(columns,row)))
    return results

@app.get("/shared_routes/")
async def shared_routes(user_id : int):
    query = ('SELECT r.route_id,r.town,r.distance,s.shared_username FROM Routes r ' + 
            'LEFT JOIN Shared s ON s.route_id = r.route_id WHERE s.user_id = ' + str(user_id) + ';')
    cur.execute(query)
    columns = [column[0] for column in cur.description]
    results = []
    for row in cur.fetchall():
        results.append(dict(zip(columns,row)))
    return results

@app.get("/route_history/")
async def route_history(user_id : int):
    query = ('SELECT h.route_id,h.datetime_of_run,h.calories,h.duration_of_run,h.distance_run, r.town FROM History h LEFT JOIN Routes r ON r.route_id = h.route_id WHERE h.user_id = ' + str(user_id) + ';')

    cur.execute(query)
    columns = [column[0] for column in cur.description]
    results = []
    for row in cur.fetchall():
        results.append(dict(zip(columns,row)))
    return results

@app.get("/add_history/")
async def add_history(user_id:int, datetime_of_run:str, calories:int, duration_of_run:str, distance_run:float):
    cur.execute('SELECT route_id FROM Routes ' +
            'WHERE user_id = "' + str(user_id) + ' order by route_id DESC limit 1";')
    result = list(cur)
    route_id =[r[0] for r in result]
    print(route_id[0])
    query = ('INSERT INTO History'+
            '(user_id,route_id, datetime_of_run, calories, duration_of_run, distance_run) Values ("'
            +str(user_id) + '","'+str(route_id[0])+'","'+datetime_of_run +'","'+str(calories)+'","'+duration_of_run+'","'+ str(distance_run)+ '");')
    try:
        cur.execute(query)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"

@app.get("/add_request/")
async def add_request(user_id:int,toAdd_username:str, username:str):
    cur.execute('SELECT user_id FROM User ' +
            'WHERE username = "' + toAdd_username + '";')
    result = list(cur)
    Addto_id =[r[0] for r in result]
    print(Addto_id[0])
    query = ('INSERT INTO Request'+
            '(user_id,username, toAdd_id, toAdd_username) Values ("'
            +str(user_id) + '","'+username +'","'+ str(Addto_id[0])+ '","' +
            toAdd_username + '");')
    try:
        cur.execute(query)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"

@app.get("/check_friend/")
async def check_friend(user_id:int, toAdd_username: str):
    cur.execute('SELECT * FROM Friend ' +
                'WHERE user_id = ' + str(user_id) + ' and friend_username = "'+ toAdd_username +'";')
    results = list(cur)
    if results:
        return "Already Friends"
    else:
        return "Not Friends Yet"
 
@app.get("/check_request/")
async def check_request(user_id:int, toAdd_username: str):
    cur.execute('SELECT * FROM Request ' +
                'WHERE user_id = ' + str(user_id) + ' AND toAdd_username = "'+ toAdd_username +'";')
    results = list(cur)
    if results:
        return "Request already made"
    else:
        return "No request made"
  
@app.get("/show_requestlist/")
async def show_requestlist(user_id:int):
    cur.execute('SELECT toAdd_username, toAdd_id FROM Request ' +
                'WHERE user_id = "' + str(user_id)+ '";')
    columns = [column[0] for column in cur.description]
    results = []
    for row in cur.fetchall():
        results.append(dict(zip(columns,row)))
    return results

@app.get("/delete_request/")
async def delete_request(user_id:int, toAdd_username: str):
    query = ('DELETE FROM Request WHERE user_id = '
            + str(user_id) + ' AND toAdd_username = "'+ toAdd_username +'";')
    try:
        cur.execute(query)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"


@app.get("/show_friendlist/")
async def show_friendlist(user_id: int):
    cur.execute('SELECT friend_username, friend_id FROM Friend WHERE user_id = ' + str(user_id) + ';')
    columns = [column[0] for column in cur.description]
    results = []
    for row in cur.fetchall():
        results.append(dict(zip(columns,row)))
    return results

@app.get("/delete_friend/")  
async def delete_friend(user_id:int, friend_username: str):
    query = ('DELETE FROM Friend WHERE user_id = '
            + str(user_id) + ' AND friend_username = "'+ friend_username +'";')
    try:
        cur.execute(query)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"

@app.get("/add_friend/")
async def add_friend(user_id:int,friend_id:int, friend_username:str, username:str):
    query = ('INSERT INTO Friend'+
            '(user_id, friend_id, friend_username, username) Values ("'
            +str(user_id) + '","'+str(friend_id) +'","'+friend_username + '","' +
            username + '");')
    try:
        cur.execute(query)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"

@app.get("/share_route")
async def share_route(user_id: int, shared_username: str, route_id: int):
    query1 = ('SELECT * FROM User WHERE username = "' + shared_username + '";')
    cur.execute(query1)
    results = list(cur)
    if len(results) == 0:
        return "no user"

    query2 = ('SELECT * FROM Shared WHERE route_id = ' + str(route_id) + ' AND shared_username = "' + shared_username + '";')
    cur.execute(query2)
    results = list(cur)
    if len(results) != 0:
        return "duplicate" 

    query3 = ('INSERT INTO Shared (user_id,username,shared_id,shared_username,route_id) ' + 
                'VALUES (' + str(user_id) + ',(SELECT u1.username FROM User u1 WHERE u1.user_id = ' + str(user_id) +
                '), (SELECT u2.user_id FROM User u2 WHERE u2.username = "' + shared_username + '"),"' + shared_username + 
                '",' + str(route_id) + ');')
    try:
        cur.execute(query3)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"

@app.get("/add_follow/")
async def add_follow(user_id:int,username:str,follow_username:str):
    cur.execute('SELECT user_id FROM User ' +
            'WHERE username = "' + follow_username + '";')
    result = list(cur)
    if not result:
        return "No Username"
    follow_id =[r[0] for r in result]
    print(follow_id[0])
    query = ('INSERT INTO Follow'+
            '(user_id,username, follow_id, follow_username) Values ("'
            +str(user_id) + '","'+username +'","'+ str(follow_id[0])+ '","' +
            follow_username + '");')
    try:
        cur.execute(query)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"
 

@app.get("/show_followinglist/")
async def show_followinglist(user_id: int):
    cur.execute('SELECT follow_username, follow_id FROM Follow WHERE user_id = ' + str(user_id) + ';')
    columns = [column[0] for column in cur.description]
    results = []
    for row in cur.fetchall():
        results.append(dict(zip(columns,row)))
    return results

@app.get("/show_followerlist/")
async def show_followerlist(user_id: int):
    cur.execute('SELECT username, user_id FROM Follow WHERE follow_id = ' + str(user_id) + ';')
    columns = [column[0] for column in cur.description]
    results = []
    for row in cur.fetchall():
        results.append(dict(zip(columns,row)))
    return results


@app.get("/delete_follow/")
async def delete_follow(user_id:int, follow_username: str):
    query = ('DELETE FROM Follow WHERE user_id = '
            + str(user_id) + ' AND follow_username = "'+ follow_username +'";')
    try:
        cur.execute(query)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
        return "fail"
    return "success"


