'''
 BART station codes
'''

STATION_CODES = {
    "twelfth street oakland city center": "12TH",
    "twelfth street oakland": "12TH",
    "oakland city center": "12th",
    "16th street Mission": "16TH",
    "16th and Mission": "16TH",
    "16th street": "16TH",
    "19th street Oakland": "19TH",
    "24th street mission": "24TH",
    "24th and mission": "24TH",
    "24th street": "24TH",
    "ashby": "ashb",
    "balboa park": "balb",
    "bay fair": "bayf",
    "castro valley": "cast",
    "civic center": "civc",
    "coliseum": "cols",
    "colma": "colm",
    "concord": "conc",
    "daly city": "daly",
    "downtown berkeley": "dbrk",
    "berkeley": "dbrk",
    "dublin pleasanton": "dubl",
    "el cerrito del norte": "deln",
    "el cerrito plaza": "plza",
    "el cerrito": "plza",
    "embarcadero": "embr",
    "fremont": "frmt",
    "fruitvale": "ftvl",
    "glen park": "glen",
    "hayward": "hayw",
    "lafayette": "lafy",
    "Lake Merritt": "lake",
    "macarthur": "mcar",
    "millbrae": "mlbr",
    "montgomery street": "mont",
    "montgomery": "mont",
    "north berkeley": "nbrk",
    "north concord martinez": "ncon",
    "north concord": "ncon",
    "oakland airport": "oakl",
    "oakland international airport": "oakl",
    "orinda": "orin",
    "pittsburg bay point": "pitt",
    "pittsburg": "pitt",
    "pleasant hill contra costa centre": "phil",
    "pleasant hill": "phil",
    "contra costa centre": "phil",
    "powell street": "powl",
    "powell": "powl",
    "richmond": "rich",
    "rockridge": "rock",
    "san bruno": "sbrn",
    "san francisco airport": "sfia",
    "sfo": "sfia",
    "san leandro": "sanl",
    "south hayward": "shay",
    "south san francisco": "ssan",
    "union city": "ucty",
    "walnut creek": "wcrk",
    "west dublin pleasanton": "wdub",
    "west dublin": "wdub",
    "west oakland": "woak"
}

def station_code(station):
    try:
        return STATION_CODES[station.lower()]
    except KeyError:
        return None

