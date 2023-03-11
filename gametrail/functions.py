import json
from . import models
from datetime import datetime

def populate(populate=True, base_json="./src/population/develop_database.json"):
    return(populate_genres() & populate_platforms() & populate_database(base_json="./src/population/develop_database_little.json"))


def populate_database(populate=True, base_json="./src/population/develop_database.json"):
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
                dimage = "https://images.igdb.com/igdb/image/upload/t_original/nocover.png"
            else:
                dimage = d.get("cover").get("url")
                dimage = str(dimage).replace("t_thumb","t_original")
            if d.get("screenshots") == None:
                dphotos = ""
            else:
                screenshots = d.get("screenshots")
                dphotos = ""
                for screenshot in screenshots:
                    parsedScreenshot = screenshot.get("url")
                    parsedScreenshot = str(parsedScreenshot).replace("t_thumb", "t_original")
                    dphotos = dphotos + str(parsedScreenshot) + ", "
            if d.get("summary") == None:
                ddescription = ""
            else:
                ddescription = d.get("summary")           
            
            game = models.Game.objects.create(
            name = dname, releaseDate=dreleaseDate, image=dimage, photos=dphotos, description=ddescription)

            if d.get("platforms") == None:
                pplatforms = []
            else:
                pplatforms = d.get("platforms")
                if pplatforms != None:
                    for platform in pplatforms:
                        parsedPlatform = platform.get("name")
                        if parsedPlatform != None:
                            ePlatform = models.Platform.objects.get(platform=parsedPlatform)
                            ePlatform.game.add(game)
            
            if d.get("genres") == None:
                ggenres = []
            else:
                ggenres = d.get("genres")
                if ggenres != None:
                    for genre in ggenres:
                        parsedGenre = genre.get("name")
                        if parsedGenre != None:
                            eGenre = models.Genre.objects.get(genre=parsedGenre)
                            eGenre.game.add(game)

    except:
        print("Data was not stored successfully")
        return False

    print("Database population finished!")
    return True

def populate_genres(populate=True, base_json="./src/population/develop_database_genres.json"):
    if(populate):
        print("\nPopulating batabase...")
        print("File ' "+ str(base_json) +"' will be used to populate.")

        file = open_json_handler(base_json)
        if (file == None):
            return None
        
        try:
            data = json.loads(file)
            print("Number of genres that will be use to populate: " + str(len(data)))
        except:
            print("Invalid json, aborting action.")
            return None

        return parse_genres(data)
    
def parse_genres(data):
    try:
        for d in data:
            if d.get("name") == None:
                dname = ""
            else:
                dname = str(d.get("name"))

            genre = models.Genre.objects.create(
                genre = dname)
    except:
        print("Genres were not stored successfully")
        return False

    print("Genres population finished!")
    return True

def populate_platforms(populate=True, base_json="./src/population/develop_database_platforms.json"):
    if(populate):
        print("\nPopulating batabase...")
        print("File ' "+ str(base_json) +"' will be used to populate.")

        file = open_json_handler(base_json)
        if (file == None):
            return None
        
        try:
            data = json.loads(file)
            print("Number of platforms that will be use to populate: " + str(len(data)))
        except:
            print("Invalid json, aborting action.")
            return None

        return parse_platforms(data)
    
def parse_platforms(data):
    try:
        for d in data:
            if d.get("name") == None:
                dname = ""
            else:
                dname = str(d.get("name"))

            platform = models.Platform.objects.create(
                platform = dname)
    except:
        print("Platforms were not stored successfully")
        return False

    print("Platforms population finished!")
    return True