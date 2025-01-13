import re
import time

import chess

from src.browser_functions import draw_arrow, iniate_browser, move_to_coordinates_and_click
from src.chess_functions import ASCII_to_FEN, creat_ASCII, last_move, locate_pieces, my_turn, whose_turn
from src.engine_functions import if_process_is_running_by_exename, load_engine
from src.utils import filt, initialise_config

def cheat(driver, engine, last:str, times:tuple, automove:bool):
    global totalTime, move_time
    pause_before_turn = times[1]
    pause_after_turn = times[2]
    # thinking_limit = move_time / 3
    thinking_limit = times[0]
    # Capture html
    html = driver.page_source
    # Check if last move has changed
    current = last_move(html)
    if current == last:
        # print("No new moves since last calculation")
        return last
    # Determine if the board is orientated for white or black
    if re.search(r'<coords class="ranks black">.*</coords>', html):
        areBlack = True
    else:
        areBlack = False
    time.sleep(pause_before_turn)
    html = driver.page_source
    # End if not our turn
    if not my_turn(areBlack, html):
        return last
    # Calculate how long it took for opponent to move
    move_time = time.time() - totalTime
    # Filter for board info
    board = html[html.index("<cg-container"):html.index("</cg-container>")]
    # Get current dimensions
    width  = int(filt(board, 'style="width: ', 'px'))
    height = int(filt(board, 'height: ', 'px;"'))
    dx = width/8
    dy = height/8
    # Get current positions returns [piece,x[1-8],y[1-8]]
    pieces = locate_pieces(board, dx, dy)
    # Create ascii board
    board = creat_ASCII(pieces, areBlack)
    # Convert ASCII to FEN
    FEN = ASCII_to_FEN(board)
    # Iniate chess board
    Board = chess.Board(fen=FEN + whose_turn(html))
    # Ask engine for best move
    result = engine.play(Board, chess.engine.Limit(time=thinking_limit))
    print(Board)
    print(result.move)
    draw_arrow(driver, width, height, result.move,areBlack)  
    # Make the move
    if automove:
        move_to_coordinates_and_click(driver, str(result.move), width, height, areBlack)
        time.sleep(pause_after_turn)
    # Reset global timer
    totalTime = time.time()
    return current
    
if __name__ == "__main__":
    times, automove, bot_strength, chrome_dir = initialise_config()
    driver = iniate_browser(chrome_dir)
    engine = load_engine(bot_strength)
    totalTime = time.time()
    move_time = 0
    arrows = False
    last = ""
    while if_process_is_running_by_exename():
        try:
            last = cheat(driver, engine, last, times, automove)
            arrows = True
        except Exception as e:
            print(e)
            if "engine event loop dead" in str(e):
                engine = load_engine(bot_strength)
                continue
            # always reload engine on failure, todo: add more exceptions
            engine = load_engine(bot_strength)
            totalTime = time.time()