def reviews(received):
    # Check to see if a platform was specified
    platforms = [ "movie", "tv", "show", "shows", "360", "ios", "stadia", "gameboy", "gba", "game boy advance", "ds", "3ds",
                  "vita", "n64", "gamecube", "wii", "wii u", "switch", "dreamcast", "ps1", "playstation", "ps2", "ps3",
                  "ps4", "ps5", "xbox", "xbone", "xbox one", "xbone", "xbox series", "series", "xsx", "pc" ]

    matches = []
    for match in platforms:
        if match in received:
            matches.append(match)
    
    response = ""
    received = received.lower()
    size = len(matches)

    if size == 0:
        # return search
        response = "https://www.metacritic.com/search/all/" + received.replace(' ', "%20") + "/results"
        return response
    elif size == 1:
        # return link to game for specific platform
        platforms = {
            "game boy advance": "game-boy-advance",
            "gba": "game-boy-advance",
            "gameboy": "game-boy-advance",
            "360": "xbox-360",
            "xbone": "xbox-one",
            "xsx": "xbox-series-x",
            "ps1": "ps",
            "playstation": "ps",
            "ps2": "playstation-2",
            "ps3": "playstation-3",
            "ps4": "playstation-4",
            "ps5": "playstation-5",
            "movies": "movie",
            "show": "tv",
        }

        caught = matches[0]
        try:
            # Check if the platform matches a special case
            print("try!")
            platform = platforms[caught]
        except:
            print("except!")
            # Does not match a special case, just set directly
            platform = caught

    else:
        # return link to game for specific platform, but there is overlap
        # Whittle down to one platform. Will choose first platform if not recgonized.
        if "xbox" in received:
            # xbox, xbox 360, xbox one, or xbox series
            if "xbox one" in received:
                caught = "xbox one"
                platform = "xbox-one"
            elif "xbox 360" in received:
                caught = "xbox 360"
                platform = "xbox-360"
            elif "xbox series x" in received:
                caught = "xbox series x"
                platform = "xbox-series-x"
            elif "xbox series s" in received:
                caught = "xbox series s"
                platform = "xbox-series-x"
            elif "xbox series" in received:
                caught = "xbox series"
                platform = "xbox-series-x"
            elif "series" in received:
                caught = "series"
                platform = "xbox-series-x"
        if "wii" in received:
            caught = "wii u"
            platform = "wii-u"
        if "show" in received:
            caught = "shows"
            platform = "tv"

    if platform != "tv" and platform != "movie":
        platform = "game/" + platform

    received = received.replace(caught, '')
    response = "https://www.metacritic.com/" + platform + "/" + received[1:].replace(' ', '-')
    return response
