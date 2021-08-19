def steam(received):
    # substitute spaces for url space character
    response = "https://store.steampowered.com/search/?term=" + received.replace(' ', "%20")
    return response
