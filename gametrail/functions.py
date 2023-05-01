import json
from . import models
from datetime import datetime

def populate_users(base_json = "./src/population/users/users.json"):
    file = open_json_handler(base_json,encoding="utf-8")
    data = json.loads(file)
    for user in data:
        models.User.objects.create_user(
            email= str(user.get("email")),
            username = str(user.get("username")),
            avatar= str(user.get("avatar")),
            password=str(user.get("password"))
        )
    return True

def populate_gameLists(base_json = "./src/population/gameList/gameList.json"):
    file = open_json_handler(base_json,encoding="utf-8")
    data = json.loads(file)
    for gameList in data:
        models.GameInList.objects.create(
            gameList_id = int(gameList.get("gameList")),
            game_id = int(gameList.get("game")),
            status = str(gameList.get("status"))
        )
    return True

def populate_comments(base_json = "./src/population/comments/comment.json"):
    file = open_json_handler(base_json,encoding="utf-8")
    data = json.loads(file)
    for comment in data:
        models.Comment.objects.create(
            userWhoComments_id = int(comment.get("userWhoComments")),
            userCommented_id = int(comment.get("userCommented")),
            commentText = str(comment.get("commentText"))
        )
    return True

def populate_ratings(base_json = "./src/population/ratings/rating.json"):
    file = open_json_handler(base_json,encoding="utf-8")
    data = json.loads(file)
    for rating in data:
        models.Rating.objects.create(
            ratedUser_id = int(rating.get("ratedUser")),
            userWhoRate_id = int(rating.get("userWhoRate")),
            type = str(rating.get("type")),
            rating = int(rating.get("rating")),
        )
    return True

def populate_trails(base_json = "./src/population/trails/trail_copy.json"):
    file = open_json_handler(base_json,encoding="utf-8")
    data = json.loads(file)
    for conjunto in data:
        trail = conjunto.get("trail")
        new_trail = models.Trail.objects.create(
            name = str(trail.get("name")),
            description = str(trail.get("description")),
            startDate = str(trail.get("startDate")),
            finishDate = str(trail.get("finishDate")),
            maxPlayers = int(trail.get("maxPlayers")),
            owner_id = int(trail.get("owner"))
        )
        trail_id = new_trail.id
        games = conjunto.get("games")
        for game in games:
            models.GameInTrail.objects.create(
                game_id = str(game.get("game")),
                message = str(game.get("message")),
                priority = int(game.get("priority")),
                status = str(game.get("status")),
                trail_id = trail_id
            )
        users = conjunto.get("users")
        for user in users:
            models.UserInTrail.objects.create(
                user_id = int(user.get("user")),
                trail_id = trail_id
            )
    return True

def populate_sabias_que(base_json="./src/population/sabiasque.json"):
    file = open_json_handler(base_json,encoding="utf-8")
    data = json.loads(file)
    for d in data.get("sabias que"):
        models.SabiasQue.objects.create(
            curiosity= str(d.get("curiosity"))
        )
    return True

def populate(populate=True, base_json="./src/population/database0.json"):
    #Change database.json to database.json to have all games 
    
    return(populate_database(base_json="./src/population/database0.json"))

def populate_generes_and_platforms(populate=True, base_json="./src/population/database0.json"):
    #Change database.json to database.json to have all games 
    return(populate_genres(base_json="./src/population/develop_database_genres.json") & populate_platforms(base_json="./src/population/develop_database_platforms.json"))


def populate_database(populate=True, base_json="./src/population/database.json"):
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
                    if float(str(releaseDate)) < 0:
                        dreleaseDate = datetime.fromtimestamp(float(str(1))).strftime('%Y-%m-%d')
                    else:
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
            try:

            
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
                print('este juego no se ha añadido porque ya existe')
                
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