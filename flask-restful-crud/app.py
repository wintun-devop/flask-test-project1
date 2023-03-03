""" 
https://www.youtube.com/channel/UCz9ebjc-_3t3p49gGpwyAKA (Please subscribe my channel.Thank You!)

"""
from flask import Flask,request,jsonify
from flask_restful import Api,Resource,reqparse,abort
from database_manage import ManageDatabase


my_app = Flask(__name__)
my_app.config['SECRET_KEY']="@MY-KEY"
my_api = Api(my_app)

# database setup
db_connection = ManageDatabase().database_connection("flask_restful", "dbadmin", "Abc123Abc123", "172.18.0.2")

#Api for health check
class Health(Resource):
    def get(self):
        response = {"message":"Api is healthly."}
        return response

#
class Item(Resource):
    def post(self):
        ''' 
        #Request from params
        name=request.args.get("name",type=str)
        price = request.args.get("price",type=float)
        qty = request.args.get("qty",type=int)
         '''
        #Request from body
        data = reqparse.RequestParser()
        data.add_argument("name",type=str,help="Name is required.",required=True)
        data.add_argument("price",type=float,help="Price is required.",required=True)
        data.add_argument("qty",type=int,help="Qunity is required.",required=True)
        response = data.parse_args()
        name = response["name"]
        price = response["price"]
        qty = response["qty"]
        try:
            db_cursor=db_connection.cursor()
            insert_query = "INSERT INTO items (name,price,qty) VALUES (%s,%s,%s) RETURNING id,name,price,qty"
            record = (name,price,qty)
            db_cursor.execute(insert_query,record)
            # response = db_cursor.fetchone()
            # print(response)
            id = db_cursor.fetchone()[0]
            if id is not None:
                response["id"]=id
                response["operation"]="Created"
                response["Status"]="Success"
                return response,201
        except:
            abort(404, message="Operation was not success.")

    def get(self):
        #Request from params
        id=request.args.get("id",type=str)
        try:
            if id:
                response = {}
                db_cursor=db_connection.cursor()
                select_query = "SELECT  id,name,price,qty FROM items where id=\'{id}\'".format(id=id)
                db_cursor.execute(select_query)
                results=db_cursor.fetchone()
                response['id']=results[0]
                response['name']=results[1]
                response['price']=results[2]
                response['qty']=results[3]
                response["operation"]="Query"
                response["Status"]="Success"
                return jsonify(response)
        except:
            abort(404, message="ID {} do not exist".format(id))
        
    def put(self):
        response = {}
        id=request.args.get("id",type=str)
        updateKey=request.args.get("updateKey",type=str)
        if updateKey == "name":
            updateValue=request.args.get("updateValue",type=str)
        if updateKey == "price":
            updateValue=request.args.get("updateValue",type=float)
        if updateKey == "qty":
            updateValue=request.args.get("updateValue",type=int)
        try:
            if id:
                response = {}
                db_cursor=db_connection.cursor()
                update_query = "UPDATE items SET {updateKey}=\'{updateValue}\' where id=\'{id}\'".format(updateKey=updateKey,updateValue=updateValue,id=id)
                db_cursor.execute(update_query)
                response["id"]=id
                response["updateKey"]=updateKey
                response["updateValue"]=updateValue
                response["Status"]="Success"
                response["Operation"]="Updated"
                return jsonify(response)
        except:
            abort(404, message="ID {} do not exist".format(id))

    def delete(self):
        response = {}
        id=request.args.get("id",type=str)
        try:
            if id:
                response={}
                db_cursor=db_connection.cursor()
                delete_query="DELETE from items where id=\'{id}\'".format(id=id)
                db_cursor.execute(delete_query)
                response["id"]=id
                response["Operation"]="Deleted"
                response["status"]="Success"
                return response,204
        except:
            abort(404, message="ID {} do not exist".format(id))



my_api.add_resource(Health,"/","/health")
my_api.add_resource(Item,"/item")

