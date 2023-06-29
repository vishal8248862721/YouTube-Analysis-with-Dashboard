from pymongo import MongoClient
from main_file import main_data

def data_to_MongoDB(channel_id):
    
    
    client = MongoClient(f"mongodb+srv://vishal:vishal123@cluster0.ol1geun.mongodb.net/?retryWrites=true&w=majority")
    
    upload =  main_data(channel_id) 
    
    database = client['project_testing']
    collection = database['channel_data']
    
    try:
        existing_document = collection.find_one({"Channel_Name.Channel_id": channel_id})
        if existing_document:
            print("Channel ID already exist")
        else:
            collection.insert_one(upload)
            print("Data uploaded successfully")
    except Exception as e:
        print(f"Error occurred while uploading data: {str(e)}")
        
    client.close()
    

