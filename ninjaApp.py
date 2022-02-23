from fastapi import FastAPI, File, UploadFile
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
    cur.execute('UPDATE User' + 
                'SET total_distance = (total_distance + '+  str(var_dist) + '),' +
                'total calories = (total_calories + ' + str(var_cal) + ')' + 
                'WHERE user_id = ' + str(var_uid) + ';')
    return "success" 

@app.get("/send_route")
async def send_route(var_start: float, var_end: float, var_town: str, var_dist: float, var_uid: int, var_routf: bytes = File(...)):
    cur.execute('INSERT INTO Routes' +
                '(start,end,town,distance,route_f,user_id)' +
                'VALUES' + 
                '(' + str(var_start) + ',' + str(var_end) + ',"' + var_town + '",' + str(var_dist) + ',' + str(var_routf) + ',' + str(var_uid) + ');')
    return "success"

@app.get("/user_info/")
async def user_info(user_id: int):
    cur.execute('SELECT * FROM User u' + 
                'INNER JOIN History h' + 
                'ON u,user_id = h.user_id' + 
                'WHERE u,user_id = "' + str(user_id) + '";')
    results = list(cur)
    return results

@app.get("/new_user/")
async def new_user(var_un: str, var_pw: str, var_lb: float, var_ft: int, var_in: float, var_pts: int, var_cals: int, var_dist: float):
    query = ('INSERT INTO User ' +
                '(username,password,weight,height_ft,height_in,points,total_calories,total_distance,Name,IsAdmin)' +
                ' VALUES ("' + var_un + '","' + var_pw + '",' + str(var_lb) + ',' + str(var_ft) + ',' + str(var_in) + ',' + str(var_pts) + ',' + str(var_cals) + ',' + str(var_dist) + ',"joe",0);')
    try:
        cur.execute(query)
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")
    return "success"



