def from_overview_to_bio(url):
    return from_overview_to_extension(url, "bio")

def from_overview_to_playerActivity(url, year):
    return from_overview_to_extension(url, "player-activity?year="+year)

def from_overview_to_extension(url, extension):
    if url[len(url)-1] == "/":
        return url+extension
    else:
        return from_overview_to_extension(url[:len(url)-1], extension)
