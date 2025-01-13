from src.utils import filt

def piece_notation(text: str):
    '''
    Function to convert piece locations to FEN naming convenction
    '''
    pmap = {
        "bishop" : "b",
        "king" : "k",
        "knight" : "n",
        "pawn" : "p",
        "queen" : "q",
        "rook" : "r"}
    split = text.split(" ")
    # if black keep notation lower case as per FEN
    if split[0] == "black":
        return pmap[split[1]]
    # Otherwise make it upper case for white
    return pmap[split[1]].upper()

def locate_pieces(board: str, dx: int, dy: int):
    '''
    Locate all pieces on the board and export them as a list of tuples
    '''
    # (x,y) map used to inverse [px] location to integer [1-8]
    xmap = {dx*(i):i for i in range(8)}
    ymap = {dy*(i):i for i in range(8)}
    # This comprehension finds the starting index of each instance of '<piece class='
    N = [n for n in range(len(board)) if board.find('<piece class=', n) == n]
    # raw will now store each <piece class /> tag
    raw = []
    for i in range(len(N)-1):
        raw.append(board[N[i]:N[i + 1]]) 
    pieces = []
    # Here we use the filt function to extract the (x,y) location [px]
    # and extract the piece type
    # then store in a list of tuples ([piece],[1-8],[1-8])
    for row in raw:
        x = round(float(filt(row, "late(", "px,")))
        y = round(float(filt(row, "px, ", "px);")))
        pieces.append( 
            (piece_notation(filt(row, '="', '" st')), 
             xmap[x], ymap[y]))
    return pieces

def my_turn(is_black:bool, html:str):
    '''
    Logical function to determine if its our turn
    '''
    turn = whose_turn(html)
    if is_black and (turn == " b"):
        return True
    if (not is_black) and (turn == " w"):
        return True
    return False

def whose_turn(html:str):
    '''
    Function to determine whose turn it is
    '''
    # look at last row of moves
    text = filt(html, "<l4x>", "</l4x>")[::-1] #reversing order to get bottom
    text = filt(text, ">", ">z5i<")[::-1]
    # if 4 kwdb tags then two moves made > white to go
    if text.count("kwdb") == 4:
        return " w"
    return " b"

def last_move(html:str):
    '''
    Function to detect changes in the last move
    '''
    text = filt(html, '</square><square class="last-move"',"</piece>")
    if '</square><square class="last-move"' in text:
        text = filt(text, '</square><square class="last-move"', '<piece')
    text = filt(text, "translate(", ")")
    # print(f"Last move found is {text}")
    return text

def chess_notation_to_pixel(chess_move:str, width:int, height:int, areBlack: bool):
    """
    Convert a chess move like 'h4h6' into pixel coordinates (x, y).
    Adjusts for black's inverted perspective.
    """
    if areBlack:
        # Reverse the mapping for black
        xmap = {chr(97 + i): (7 - i) * (width / 8) for i in range(8)}
        ymap = {str(i): (i - 1) * (height / 8) for i in range(1, 9)}
    else:
        # Normal mapping for white
        xmap = {chr(97 + i): i * (width / 8) for i in range(8)}
        ymap = {str(i): (8 - i) * (height / 8) for i in range(1, 9)}

    # Get start and end positions from the chess move
    start_file, start_rank = chess_move[2:4]
    end_file, end_rank = chess_move[2:]

    # Convert to pixel coordinates
    start_x = int(xmap[start_file])
    start_y = int(ymap[start_rank])
    end_x = int(xmap[end_file])
    end_y = int(ymap[end_rank])

    return start_x, start_y, end_x, end_y

def creat_ASCII(pieces:tuple, areBlack:bool):
    '''
    Function to create ASCII board
    '''
    board = ["."*8 for i in range(8)]
    for i in pieces:
        (x, y) = [i[1], i[2]]
        if areBlack:
            # Flip coordinates when playing as black
            x = 7 - x
            y = 7 - y
        board[y] = board[y][:x] + i[0] + board[y][x + 1:]
    return board

def ASCII_to_FEN(board:list):
    '''
    Function to convert ascii board into FEN
    '''
    FEN = []
    for row in board:
        store = [] #temporary list to collect FEN parts for a row
        num = 0 #count empty squares in row
        for column in row:
            # element is a . at 1 to count of empty squares
            if column == ".":
                num = num + 1
                continue
            # otherwise append piece and its number of empty squares
            # if number of empty squares is not 0
            else:
                if not num == 0:
                    store.append(str(num))
                store.append(column)
                num = 0
        # append number of empty squares to the end of row
        if not num == 0:
            store.append(str(num))
        # save row info as list element
        FEN.append("".join(store))
    #join all elements by a / to indicate a break in the rows per FEN
    return "/".join(FEN)