settings = {}
prefix = ""
desc = ""
joinsound = ""
channel = {}

def read_settings():
    os.chdir(sys.path[0])
    with open("settings.json", "r") as settings_file:
        global settings 
        global prefix
        global desc
        global joinsound
        
        settings = json.load(settings_file)
        prefix = settings["prefix"]
        desc = settings["desc"]
        joinsound = settings["joinsound"]


def print_settings():
    print("Prefix: " + prefix + "\tdesc: " + desc)


def set_bot_settings():
    bot.command_prefix = commands.when_mentioned_or(prefix)
    bot.description = desc


def update_game():
    yield from bot.change_presence(game=discord.Game(name="Use me: " + prefix + "help"))
