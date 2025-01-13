import os
import time
import chess.engine
import psutil

def if_process_is_running_by_exename(exename:str='chrome.exe'):
    '''
    Function to determine is a process is running
    ''' 
    for proc in psutil.process_iter(['pid', 'name']):
        # This will check if there exists any process running with executable name
        if proc.info['name'] == exename:
            return True
    return False

def load_engine(bot_strength:int):
    '''
    Function to iniate chess engine
    '''
    # Construct the path to the Stockfish engine
    script_dir = os.path.dirname(os.path.dirname(__file__))
    stockfish_dir = os.path.join(script_dir, "stockfish")
    # Find the first .exe file in the stockfish directory
    stockfish_path = None
    for file in os.listdir(stockfish_dir):
        if file.endswith(".exe"):
            stockfish_path = os.path.join(stockfish_dir, file)
            break
    if stockfish_path is None:
        raise FileNotFoundError("No .exe file found in the stockfish directory.")
    # Closes any instances of engine already running
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == "stockfish-windows-x86-64-avx2.exe":
            proc.kill()
            print("Killing process")
    # Load the Stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    engine.configure({"UCI_LimitStrength": True})
    engine.configure({"UCI_Elo": bot_strength})  # 1320-3190
    return engine