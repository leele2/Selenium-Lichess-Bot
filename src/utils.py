import os
import configparser
import sys

def initialise_config():
    # Path to the .ini file
    if getattr(sys, 'frozen', False):  # Running as .exe
        directory = os.path.dirname(sys.executable)  # directory of the .exe
    else:  # Running as a script
        directory = os.path.dirname(os.path.dirname(__file__))
    config_file = os.path.join(directory, 'config.ini')

    # Check if the file exists
    if not os.path.exists(config_file):
        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Add default sections and settings
        config['settings'] = {
            'engine_thinking_time': 0.1,
            'pause_before_turn': 0.25,
            'pause_after_turn': 0.1,
            'UCI_Elo' : 3190,
            'automove': True,
            'chrome_dir' : ''
        }

        # Write to the .ini file
        with open(config_file, 'w') as file:
            config.write(file)

        print(f"'{config_file}' created with default settings.")
    else:
        print(f"'{config_file}' already exists.")
    
    # Return config values
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        t0 = config.getfloat('settings', 'engine_thinking_time')
        t1 = config.getfloat('settings', 'pause_before_turn')
        t2 = config.getfloat('settings', 'pause_after_turn')
        bot_strength = config.getint('settings', 'UCI_Elo')
        automove = config.getboolean('settings', 'automove')
        chrome_dir = config.get('settings','chrome_dir')
    except:
        os.remove(config_file)
        raise Exception("Config file is corrupted and has been deleted. Rerun to create new config file")
        sys.exit()
    return (t0, t1, t2), automove, bot_strength, chrome_dir


def filt(text: str, begining: str, end: str):
    '''
    Function which filters a string between two substrings
    '''
    return text[text.index(begining) + len(begining) :
                text.index(end)]