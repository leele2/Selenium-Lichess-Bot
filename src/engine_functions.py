import os
import sys
import chess.engine
import psutil
import subprocess

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
    if getattr(sys, 'frozen', False):  # Check if the script is frozen by pyinstaller
       script_dir = os.path.dirname(sys.executable) #.exe directory
    else:
        script_dir = os.path.dirname(os.path.dirname(__file__))
    stockfish_dir = os.path.join(script_dir, "stockfish")
    # Find the first .exe file in the stockfish directory
    stockfish_path = None
    for file in os.listdir(stockfish_dir):
        if file.endswith(".exe"):
            stockfish_path = os.path.join(stockfish_dir, file)
            engine_exe = file
            break
    if stockfish_path is None:
        raise FileNotFoundError("No .exe file found in the stockfish directory.")
    # Closes any instances of engine already running
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == engine_exe:
            proc.kill()
            print("Killing process")
    # Load the Stockfish engine
    creationflags = 0
    if os.name == 'nt':  # Windows
        creationflags = subprocess.CREATE_NO_WINDOW
    
    engine = chess.engine.SimpleEngine.popen_uci(
        stockfish_path,
        creationflags=creationflags
    )
    engine.configure({"UCI_LimitStrength": True})
    engine.configure({"UCI_Elo": bot_strength})  # 1320-3190
    return engine