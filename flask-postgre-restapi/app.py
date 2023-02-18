from crypt import methods
from urllib import response
from flask import Flask,request,jsonify
from databse_manage import ManageDatabase
import psycopg2
from psycopg2 import connect,extensions,sql


app = Flask(__name__)
app.config['SECRET_KEY']="@MY-KEY"

#databse connection
# db_connection = connect(
#             database="flask_api", 
#             user="dbadmin",
#             password="Abc123Abc123",
#             host="localhost",
#             port= '5432'
# )

db_connection = ManageDatabase().database_connection("flask_api", "dbadmin", "Abc123Abc123", "172.18.0.2")


#default end-point
@app.route("/")
def index():
    return jsonify(
        {'code': 200,
        'stats': 'API is working well.'})

#get method
@app.route("/test",methods=["GET"])
def test_get():
    return jsonify({
        'Product':'Liquor',
        'Price':300,
        'Remark':'Heigh Demand'
    })

#delete method
@app.route("/api/v1/item",methods=["DELETE"])
def delete_item():
    params = request.args
    id=params["id"]
    try:
        if id:
            response={}
            db_cursor=db_connection.cursor()
            delete_query="DELETE from items where id=\'{id}\'".format(id=id)
            db_cursor.execute(delete_query)
            response["id"]=id
            response["message"]="Success"
            response["Operation"]="Deleted"
            response["status"]=204
            return jsonify(response)

    except:
        response = {"message":f"User id {id} not found","status":404}
        return jsonify(response)




#path method
@app.route("/api/v1/item",methods=["PATCH"])
def update_item():
    params = request.args
    id=params["id"]
    updateKey = params["updateKey"]
    updateValue = params["updateValue"]
    try:
        if id:
            response = {}
            db_cursor=db_connection.cursor()
            update_query = "UPDATE items SET {updateKey}=\'{updateValue}\' where id=\'{id}\'".format(updateKey=updateKey,updateValue=updateValue,id=id)
            db_cursor.execute(update_query)
            response["id"]=id
            response["updateKey"]=updateKey
            response["updateValue"]=updateValue
            response["message"]="success"
            response["Operation"]="Update"
            response["status"]=204
            return jsonify(response )
    except:
        response = {"message":f"User id {id} not found","status":404}
        return jsonify(response)
 

#post method
@app.route("/api/v1/item",methods=["POST"])
def create_item():
        #database connection
        db_cursor=db_connection.cursor()
        data = request.get_json()
        name=data["name"]
        vendor=data["vendor"]
        model=data["model"]
        remark=data["remark"]
        try:
            insert_query = "INSERT INTO items (name,vendor,model,remark) VALUES (%s,%s,%s,%s) RETURNING id,name,vendor,model,remark"
            record = (name,vendor,model,remark)
            db_cursor.execute(insert_query,record)
            # response = db_cursor.fetchone()
            # print(response)
            id = db_cursor.fetchone()[0]
            if id is not None:
                return jsonify({
                        "id":id,
                        "name":name,
                        "vendor":vendor,
                        "model":model,
                        "remark":remark,
                        "message":"Success",
                        "status":201
                })
        except:
            return jsonify({
                    "message":"Not success",
                    "status":401
                })
       

#get single
@app.route("/api/v1/item",methods=['GET'])
def get_item():
    params = request.args
    id = params['id']
    try:
        if id:
            response = {}
            db_cursor=db_connection.cursor()
            select_query = "SELECT  id,name,vendor,model,remark FROM items where id=\'{id}\'".format(id=id)
            db_cursor.execute(select_query)
            results=db_cursor.fetchone()
            response['id']=results[0]
            response['name']=results[1]
            response['vendor']=results[2]
            response['model']=results[3]
            response['remark']=results[4]
            response['status']=200
            return jsonify(response)
    except:
        response = {"message":f"User id {id} not found","status":404}
        return jsonify(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80,Deubug=True)

