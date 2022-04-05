#https://github.com/wintun-devop
#https://www.youtube.com/channel/UCz9ebjc-_3t3p49gGpwyAKA (Please subscribe my channel.Thank You!)

import boto3
import aws_config as awsdata
import datetime

#declare dynamodb as aws resource api
awsResource=boto3.resource("dynamodb",region_name=awsdata.aws_region,aws_access_key_id=awsdata.aws_access_key,
                   aws_secret_access_key=awsdata.aws_secret_key
                    )

#define dynamodb table creating and must erase attribe according to desire table
def create_table(table_name):
    #define datble to create using resource method
    tranactionTable=awsResource.create_table(
    TableName=table_name,
    KeySchema=[
        {
            "AttributeName": "userEmail",
            "KeyType": "HASH"
        },
        {
            "AttributeName": "userName",
            "KeyType": "RANGE"
        }
    ],
    AttributeDefinitions=[
        {
            "AttributeName": "userEmail",
            "AttributeType": "S"
        },
        {
            "AttributeName": "userName",
            "AttributeType": "S"
        },
    ],
    ProvisionedThroughput={
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }
    )
    # Wait until the table exists.
    tranactionTable.wait_until_exists()
    print(f"Dynamodb table named {table_name}  has been created successfully!")

def create_item():
    current_datetime=datetime.datetime.utcnow()
    current_datetime=current_datetime.strftime("%m-%d-%Y %H:%M:%S")
    user_table = awsResource.Table("userdata")
    user_table.put_item(
        Item={
            "userEmail":"wintun.edu@gmail.com",
            "userName":"Win Tun Hlaing",
            "password":"password@123!@#",
            "registerTime": current_datetime
        }
    )
    
create_item()
    