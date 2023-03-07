import json

def populate_database(populate=True, base_json="./develop_database.json"):
    if(populate):
        print("\nPopulating batabase...")
        print("File ' "+ str(base_json) +"' will be used to populate.")

        file = open_json_handler(base_json)
        if (file == None):
            return None
        
        data = json.loads(file)
        print("Number of games that will be use to populate: " + str(len(data)))


def open_json_handler(base_json,encoding="utf-8"):
    try:
        with open(base_json, "r", encoding=encoding) as file:
            print("The file has been opened successfully")
            return file.read()
    except:
        print("File '" + str(base_json) +"' not found, aborting action.")