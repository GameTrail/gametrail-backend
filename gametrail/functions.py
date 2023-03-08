import json
from . import models
from datetime import datetime

def populate_database(populate=True, base_json="./develop_database.json"):
    if(populate):
        print("\nPopulating batabase...")
        print("File ' "+ str(base_json) +"' will be used to populate.")

        file = open_json_handler(base_json)
        if (file == None):
            return None
        
        try:
            data = json.loads(file)
            print("Number of games that will be use to populate: " + str(len(data)))
        except:
            print("Invalid json, aborting action.")
            return None

        return parse_data(data)


def open_json_handler(base_json,encoding="utf-8"):
    try:
        with open(base_json, "r", encoding=encoding) as file:
            print("The file has been opened successfully.")
            return file.read()
    except:
        print("File '" + str(base_json) +"' not found, aborting action.")

def parse_data(data):
    try:
        for d in data:
            if d.get("name") == None:
                dname = ""
            else:
                dname = str(d.get("name"))
            if d.get("release_dates") == None:
                dreleaseDate = ""
            else:
                if d.get("release_dates")[0].get("date") != None:
                    releaseDate = d.get("release_dates")[0].get("date")
                    dreleaseDate = datetime.fromtimestamp(float(str(releaseDate))).strftime('%Y-%m-%d')
            if d.get("cover") == None:
                dimage = "https://images.igdb.com/igdb/image/upload/t_cover_big/nocover.png"
            else:
                dimage = d.get("cover").get("url")
                dimage = str(dimage).replace("t_thumb","t_cover_big")
            if d.get("screenshots") == None:
                dphotos = ""
            else:
                screenshots = d.get("screenshots")
                dphotos = ""
                for screenshot in screenshots:
                    parsedScreenshot = screenshot.get("url")
                    parsedScreenshot = str(parsedScreenshot).replace("t_thumb", "t_cover_big")
                    dphotos = dphotos + str(parsedScreenshot) + ", "
            if d.get("summary") == None:
                ddescription = ""
            else:
                ddescription = d.get("summary")
            
            game = models.Game.objects.create(
            name = dname, releaseDate=dreleaseDate, image=dimage, photos=dphotos, description=ddescription)
            game.save()
    except:
        print("Data was not stored successfully")
        return False

    print("Database population finished!")
    return True