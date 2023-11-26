
from codecs import escape_encode
from math import inf


EMPTYCHAR = " "
fena = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
pieces = [EMPTYCHAR,"p","r","n","b","q","k","P","R","N","B","Q","K"]
files = ["a", "b", "c", "d", "e", "f", "g", "h"]
castledirs = ["K", "Q", "k", "q"]
fenb = "rnbqkbnr/pppp1pp1/8/4p2p/4P3/5Q2/PPPP1PPP/RNB1KBNR w KQkq - 0 3"
nmoves = [[2,1], [1,2], [-1,2], [-2,1], [1,-2], [2,-1], [-1,-2], [-2,-1]]
kmoves = [[1,0], [0,1], [-1,0], [0,-1], [1,1], [-1,1], [1,-1], [-1,-1]]
rookdirs = [(0,1), (1,0), (0,-1), (-1,0)]
bishopdirs = [(1,1), (1,-1), (-1,1), (-1,-1)]
castledict = {"K": 0, "Q": 1, "k": 2, "q": 3}
promotionpieces = [["n", "b", "r", "q"], ["N", "B", "R", "Q"]]

def alptonum(alp): # takes alp of move such as a2b4 and converts to coordinates
    return([8-int(alp[1]), ord(alp[0]) - ord('a')], [8-int(alp[3]), ord(alp[2]) - ord('a')])

def nametonum(box): #converts square names to move
    return(8-int(box[1]), files.index(box[0]))

def coordstoalp(coords): # takes coordinates of a square and converts to alp
    return(files[coords[1]] + str(8-coords[0]))

def checkwhichranksame(checksquare, squares): # takes a checksquare and a list of squares and checks which ones have the same ranks
    samerankbox = []
    for i in range(len(squares)):
        if checksquare[0] == squares[i][0]:
            samerankbox.append(squares[i])
    return(samerankbox)

def checkwhichfilesame(checksquare, squares): # takes a checksquare and a list of squares and checks which ones have the same files
    samefilebox = []
    for i in range(len(squares)):
        if checksquare[1] == squares[i][1]:
            samefilebox.append(squares[i])
    return(samefilebox)

def whichnum(arra, value):
    for i in range(len(arra)):
        if arra[i] == value:
            return(i)

def copymovelist(moves): # makes deep copy of list of moves
    newlist = []
    for i in moves:
        newlist.append(i.copy())
    return(newlist)

def printmovelist(moves):
    outstr = ""
    outstr += "["
    for i in moves:
        outstr += i.print()
        outstr += ", "
    outstr = outstr[:-2]
    outstr += "]"
    return(outstr)


def maxandmoves(evalmoves1,evalmoves2): # compares two (eval, moves) pairs
    if evalmoves1[0] >= evalmoves2[0]:
        return(evalmoves1[0], evalmoves1[1])
    newbest = []
    for i in evalmoves2[1]:
        newbest.append(i)
    return(evalmoves2[0], newbest)

def minandmoves(evalmoves1,evalmoves2):
    if evalmoves1[0] <= evalmoves2[0]:
        return(evalmoves1[0], evalmoves1[1])
    newbest = []
    for i in evalmoves2[1]:
        newbest.append(i)
    return(evalmoves2[0], newbest)


def fentomap(bois):
    outpos = []
    row = []
    for cha in bois:
        if cha in pieces:
            row.append(cha)
        elif cha == "/":
            outpos.append(row)
            row = []
        else:
            for i in range(int(cha)):
                row.append(EMPTYCHAR)
    outpos.append(row)
    return(outpos)

def kandnmoves(arra, rank, file):
    outbox = []
    for square in arra:
        outrank = rank + square[0]
        outfile = file + square[1]
        if outrank >= 0 and outrank <= 7 and outfile >= 0 and outfile <= 7:
            outbox.append([outrank, outfile])
    return(outbox)

def partitionkeyval(vals, keys, start, end, white):
    if white:
        pivot = vals[end]
        i = start - 1
        for j in range(start, end):
            if vals[j] > pivot:
                i += 1
                swap(vals, i, j)
                swap(keys, i, j)
        i += 1
        swap(vals, i, end)
        swap(keys, i, end)
        return(i)
    else:
        pivot = vals[end]
        i = start - 1
        for j in range(start, end):
            if vals[j] <= pivot:
                i += 1
                swap(vals, i, j)
                swap(keys, i, j)
        i += 1
        swap(vals, i, end)
        swap(keys, i, end)
        return(i)


def swap(arra, i, j):
    bruh = arra[i]
    arra[i] = arra[j]
    arra[j] = bruh

def quicksortkeyval(vals, keys, start, end, white): # if max is true, large values first
    if start >= end or start < 0:
        return()
    else:
        p = partitionkeyval(vals, keys, start, end, white)
        quicksortkeyval(vals, keys, start, p-1, white)
        quicksortkeyval(vals, keys, p+1, end, white)

def contains(ordered, boi): # checking if a move is in the ordered list
    for i in ordered:
        if i.equals(boi):
            return(True)
    return(False)

def addmissingtoend(ordered, allbois):
    newlist = copymovelist(ordered)
    for boi in allbois:
        if not contains(ordered, boi):
            newlist.append(boi.copy())
    return(newlist)

def movelisttokey(arra):
    box = []
    for i in arra:
        box.append(i.print())
    return(tuple(box))


class piece:
    def __init__(self, letter):
       self.rep = letter
       uplet = letter.upper()
       self.iswhite = uplet == letter
       self.ispawn = uplet == "P"
       self.isrook = uplet == "R"
       self.isknight = uplet == "N"
       self.isbishop = uplet == "B"
       self.isqueen = uplet == "Q"
       self.isking = uplet == "K"

    def print(self):
       print(self.rep, end = " ")

    def copy(self):
        return(piece(self.rep))

    def issamepiece(self, checkpiece): # checks if two pieces are some colour and type
        return(self.iswhite == checkpiece.iswhite and self.rep.lower() == checkpiece.rep.lower())

class square:
    def __init__(self, letter, rank, file):
        self.isempty = letter == EMPTYCHAR
        self.piece = None
        if not self.isempty: #self.piece only defined if square occupied
            self.piece = piece(letter)
        self.rank = rank #might be important later
        self.file = file #might be important later
    
    def print(self):
        if self.isempty:
            print(EMPTYCHAR, end = " ")
        else:
            self.piece.print()

    def copy(self):
        return(square(EMPTYCHAR, self.rank, self.file))

    def code(self):
       if self.isempty:
           return(EMPTYCHAR)
       else:
           return(self.piece.rep)

    def removepiece(self):
        self.isempty = True
        self.piece = None

    def placepiece(self, letter):
        self.isempty = False
        self.piece = piece(letter)

class board:
    def __init__(self, fen):
        splitfen = fen.split(" ")
        self.posmap = fentomap(splitfen[0])
        self.position = []
        for rank in range(8):
            row = []
            for file in range(8):
                row.append(square(self.posmap[rank][file], rank, file))
            self.position.append(row)
        self.whitetomove = splitfen[1] == "w"
        self.castlerights = [False] * 4
        castlefen = splitfen[2]
        if castlefen != "-":
            for char in castlefen:
                self.castlerights[castledict[char]] = True
        if splitfen[3] == "-":
            self.enpassant = None
        else:
            self.enpassant = nametonum(splitfen[3])
        self.movecount = int(splitfen[5]) # move counter
        self.nocap = int(splitfen[4]) # count towards 50 move rule

    def print(self, rowfile = False):
        for rank in range(8):
            for file in range(8):
                self.position[rank][file].print()
            if rowfile:
                print(8-rank, end = "")
            print()
        if rowfile:
            print("a b c d e f g h")
        if self.whitetomove:
            print("White to move.")
        else:
            print("Black to move.")

    def checkdir(self, rank, file, rankinc, fileinc): #takes a rank+file and a direction, returns the moves the piece can make in given direction
        movebox = []
        piece = self.position[rank][file].piece
        whiteness = piece.iswhite
        for squaredif in range(1,8): # iterates over up to 7 moves in straight line
            checkrank = rank + squaredif*rankinc
            checkfile = file + squaredif*fileinc
            if checkrank >= 0 and checkrank <= 7 and checkfile >= 0 and checkfile <= 7: # checks if within board
                box = self.position[checkrank][checkfile]
                if box.isempty: # if square is empty, add as potential move
                    movebox.append(move([rank, file], [checkrank, checkfile]))
                else:
                    if box.piece.iswhite != whiteness: # if square is occupied and can be captured, add as potential move and return
                        movebox.append(move([rank, file], [checkrank, checkfile], captured = box.piece.rep))
                        return(movebox)
                    else:
                        return(movebox)
            else:
                return(movebox)
        return(movebox)

    def flipboard(self):
        newpos = []
        for i in range(8):
            newpos.append(self.position[7-i])
        self.position = newpos

    def checkrookdirs(self, rank, file):
        movebox = []
        for dirx,diry in rookdirs:
            movebox += self.checkdir(rank, file, rankinc = dirx, fileinc = diry)
        return(movebox)
    
    def checkbishopdirs(self, rank, file):
        movebox = []
        for dirx,diry in bishopdirs:
            movebox += self.checkdir(rank, file, rankinc = dirx, fileinc = diry)
        return(movebox)

    def checkNorKmoves(self, rank, file, testarr): # where testarr is either kmoves or nmoves
        movebox = []
        whiteness = self.position[rank][file].piece.iswhite
        for dx, dy in testarr:
            newx = rank + dx
            newy = file + dy
            if newx >= 0 and newx <= 7 and newy >= 0 and newy <= 7:
                newsquare = self.position[newx][newy]
                if newsquare.isempty: # if square is empty, can move
                    movebox.append(move([rank, file], [newx, newy]))
                elif newsquare.piece.iswhite != whiteness: # if piece on square is opposite colour, can move
                    movebox.append(move([rank, file], [newx, newy], captured = newsquare.piece.rep))
        return(movebox)

    def checkPawnMoves(self, rank, file):
        movebox = []
        whiteness = self.position[rank][file].piece.iswhite
        movedir = 1 - 2 * whiteness # -1 for white, 1 for black
        doublerank = 1 + 5 * whiteness # 1 for black, 6 for white
        promorank = 7 - 7 * whiteness # 7 for black, 0 for white

        checkrank = rank + movedir
        if checkrank >= 0 and checkrank <= 7: # not off board
            if self.position[checkrank][file].isempty:
                if checkrank == promorank: # if promotion
                    for piecename in promotionpieces[whiteness]: # iterates over all pieces pawn can promote to (based on colour)
                        movebox.append(move([rank, file], [checkrank, file], promotion = piecename))
                else: # if not promotion
                    movebox.append(move([rank, file], [checkrank, file]))

                    if rank == doublerank: # if 2nd or 7th rank
                        checkrank = rank + 2*movedir
                        if self.position[checkrank][file].isempty: # check if can move 2
                            movebox.append(move([rank, file], [checkrank, file], doublepawn = True))

            checkrank = rank + movedir
            for i in [1, -1]: # check captures
                checkfile = file + i
                if checkfile >= 0 and checkfile <= 7: # if within board
                    checksquare = self.position[checkrank][checkfile]
                    if not checksquare.isempty: # check that square is occupied
                        cappiece = checksquare.piece
                        if cappiece.iswhite != whiteness: # check that piece is opposite colour
                            if checkrank == promorank: # if capture and promotion
                                for piecename in promotionpieces[whiteness]: # iterates over all pieces pawn can promote to (based on colour)
                                    movebox.append(move([rank, file], [checkrank, checkfile], promotion = piecename, captured = cappiece.rep))
                            else:
                                movebox.append(move([rank, file], [checkrank, checkfile], captured = cappiece.rep))
                    else: # if square is empty, check for en passant
                        if self.enpassant == (checkrank, checkfile):
                            movebox.append(move([rank, file], [checkrank, checkfile], enpassant = True))
        return(movebox)

    def squaresattacked(self, whiteattack): # returns the squares attacked by a colour, whiteattack true if checking what white can attack
        attacksquares = set()
        for rank in range(8):
            for file in range(8):
                checksquare = self.position[rank][file]
                if not checksquare.isempty:
                    checkpiece = checksquare.piece
                    if checkpiece.iswhite == whiteattack:
                        attacksquares = attacksquares.union(self.cansee(rank, file))
        return(attacksquares)

    def checkpawncaps(self, rank, file): # returns the squares a pawn attacks
        attacksquares = set()
        whiteness = self.position[rank][file].piece.iswhite
        movedir = 1 - 2 * whiteness # -1 for white, 1 for black
        checkrank = rank + movedir
        for i in [-1, 1]:
            checkfile = file + i
            if checkrank >= 0 and checkrank <= 7 and checkfile >= 0 and checkfile <= 7:
                attacksquares.add((checkrank, checkfile))
        return(attacksquares)

    def cansee(self, rank, file): # returns the squares a piece can see
        attacksquares = set()
        checkpiece = self.position[rank][file].piece
        if checkpiece.ispawn:
            return(self.checkpawncaps(rank, file)) #pawn things (just check diagonals)
        elif checkpiece.isrook:
            moveset = self.checkrookdirs(rank, file)
            for boi in moveset: # iterate over the moves and extract the endsquares
                attacksquares.add(boi.getendsquare())
        elif checkpiece.isbishop:
            moveset = self.checkbishopdirs(rank, file)
            for boi in moveset: # iterate over the moves and extract the endsquares
                attacksquares.add(boi.getendsquare())
        elif checkpiece.isknight:
            moveset = self.checkNorKmoves(rank, file, nmoves)
            for boi in moveset: # iterate over the moves and extract the endsquares\
                attacksquares.add(boi.getendsquare())
        elif checkpiece.isking:
            moveset = self.checkNorKmoves(rank, file, kmoves)
            for boi in moveset: # iterate over the moves and extract the endsquares
                attacksquares.add(boi.getendsquare())
        elif checkpiece.isqueen:
            moveset = self.checkbishopdirs(rank, file) + self.checkrookdirs(rank, file)
            for boi in moveset: # iterate over the moves and extract the endsquares
                attacksquares.add(boi.getendsquare())
        return(attacksquares)

    def allempty(self, squares): #returns true if all squares empty
        for box in squares:
            if not self.position[box[0]][box[1]].isempty: # if square contains a piece
                return(False)
        return(True)

    def allsafe(self, squares, attacked): #returns true if all squares empty
        for box in squares:
            if box in attacked:
                return(False)
        return(True)

    def checkcastling(self, whitemove): # returns legal castling moves
        castlemoves = []
        backrank = whitemove * 7
        unsafesquares = self.squaresattacked(not whitemove)
        ksempty = [(backrank, 5), (backrank, 6)] # squares that have to be empty to castle kingside
        kssafe = [(backrank, 4), (backrank, 5), (backrank, 6)] # squares that have to be safe to castle kingside
        qsempty = [(backrank, 1), (backrank, 2), (backrank, 3)] # empty queenside
        qssafe = [(backrank, 2), (backrank, 3), (backrank, 4)] # safe queenside

        if self.castlerights[2 - 2*whitemove]: # kingside potentially legal
            if self.allsafe(kssafe, unsafesquares) and self.allempty(ksempty):
                if whitemove:
                    castlemoves.append(move(castle = "K"))
                else:
                    castlemoves.append(move(castle = "k"))
        
        if self.castlerights[3 - 2*whitemove]: # queenside potentially legal
            if self.allsafe(qssafe, unsafesquares) and self.allempty(qsempty):
                if whitemove:
                    castlemoves.append(move(castle = "Q"))
                else:
                    castlemoves.append(move(castle = "q"))

        return(castlemoves)

    def genmovesfromsquare(self, rank, file, whitemove): # naively generates moves from a given square, whitemove true if white to move
        movesquare = self.position[rank][file]
        if not movesquare.isempty:
            movepiece = movesquare.piece
            if movepiece.iswhite == whitemove: # checks if piece is same colour as next move
                if movepiece.ispawn:
                    return(self.checkPawnMoves(rank, file))
                elif movepiece.isrook:
                    return(self.checkrookdirs(rank, file))
                elif movepiece.isbishop:
                    return(self.checkbishopdirs(rank, file))
                elif movepiece.isknight:
                    return(self.checkNorKmoves(rank, file, nmoves))
                elif movepiece.isking:
                    return(self.checkNorKmoves(rank, file, kmoves))
                elif movepiece.isqueen:
                    return(self.checkbishopdirs(rank, file) + self.checkrookdirs(rank, file))
        return([])

    def genmoves(self, whitemove): #naively generates moves over board, whitemvoe true if white to move
        allmoves = []
        for rank in range(8):
            for file in range(8):
                squaremoves = self.genmovesfromsquare(rank, file, whitemove)
                allmoves += squaremoves
        allmoves += self.checkcastling(whitemove)
        return(allmoves)
    
    def getkingpos(self, whiteness):
        for rank in range(8):
            for file in range(8):
                checksquare = self.position[rank][file]
                if not checksquare.isempty:
                    if checksquare.piece.isking and checksquare.piece.iswhite == whiteness: # if piece is king of right colour return position as tuple
                        return((rank, file))
        return("where the homie at")

    def makemovelite(self, movea): # makes a move without adjusting FEN and is reversable... for making sure move doesn't lead to check
        if sum(movea.castle) == 0 and not movea.enpassant and movea.promotion == None: # if normal move...
            movepiece = self.position[movea.startsq[0]][movea.startsq[1]].piece.rep # movepiece is the rep for the piece that is getting moved
            self.position[movea.startsq[0]][movea.startsq[1]].removepiece() # removes the piece from the square it was on
            self.position[movea.endsq[0]][movea.endsq[1]].placepiece(movepiece) # places the piece on the new square
        elif sum(movea.castle) > 0: # castle in right direction
            if movea.castle[0]:
                self.position[7][4].removepiece()
                self.position[7][7].removepiece()
                self.position[7][6].placepiece("K")
                self.position[7][5].placepiece("R")
            elif movea.castle[1]:
                self.position[7][4].removepiece()
                self.position[7][0].removepiece()
                self.position[7][2].placepiece("K")
                self.position[7][3].placepiece("R")
            elif movea.castle[2]:
                self.position[0][4].removepiece()
                self.position[0][7].removepiece()
                self.position[0][6].placepiece("k")
                self.position[0][5].placepiece("r")
            elif movea.castle[3]:
                self.position[0][4].removepiece()
                self.position[0][0].removepiece()
                self.position[0][2].placepiece("k")
                self.position[0][3].placepiece("r")

        elif movea.enpassant:
            movepiece = self.position[movea.startsq[0]][movea.startsq[1]].piece.rep # movepiece is the rep for the piece that is getting moved
            self.position[movea.startsq[0]][movea.startsq[1]].removepiece() # removes the piece from the square it was on
            self.position[movea.endsq[0]][movea.endsq[1]].placepiece(movepiece) # places the piece on the new square
            self.position[movea.startsq[0]][movea.endsq[1]].removepiece() # remove en passant captured piece

        elif movea.promotion != None:
            self.position[movea.startsq[0]][movea.startsq[1]].removepiece() # removes the piece from the square it was on
            self.position[movea.endsq[0]][movea.endsq[1]].placepiece(movea.promotion) # places the piece on the new square
            
    def unmakemovelite(self, movea): # unmakes move that makemovelite made
        if sum(movea.castle) == 0 and not movea.enpassant and movea.promotion == None: # normal move
            movepiece = self.position[movea.endsq[0]][movea.endsq[1]].piece.rep # movepiece is the rep for the piece that got moved
            self.position[movea.startsq[0]][movea.startsq[1]].placepiece(movepiece) # places the piece on the square where it started
            self.position[movea.endsq[0]][movea.endsq[1]].removepiece() # removes the piece from the new square
            if movea.captured != None: # if a piece was captured
                self.position[movea.endsq[0]][movea.endsq[1]].placepiece(movea.captured) # add the piece back to the square
        elif sum(movea.castle) > 0: # uncastle pieces
            if movea.castle[0]:
                self.position[7][6].removepiece()
                self.position[7][5].removepiece()
                self.position[7][4].placepiece("K")
                self.position[7][7].placepiece("R")
            elif movea.castle[1]:
                self.position[7][2].removepiece()
                self.position[7][3].removepiece()
                self.position[7][4].placepiece("K")
                self.position[7][0].placepiece("R")
            elif movea.castle[2]:
                self.position[0][6].removepiece()
                self.position[0][5].removepiece()
                self.position[0][4].placepiece("k")
                self.position[0][7].placepiece("r")
            elif movea.castle[3]:
                self.position[0][2].removepiece()
                self.position[0][3].removepiece()
                self.position[0][4].placepiece("k")
                self.position[0][0].placepiece("r")
        elif movea.enpassant:
            movepiece = self.position[movea.endsq[0]][movea.endsq[1]].piece.rep # movepiece is the rep for the piece that got moved
            self.position[movea.startsq[0]][movea.startsq[1]].placepiece(movepiece) # adds the piece to the square it started from
            self.position[movea.endsq[0]][movea.endsq[1]].removepiece() # removes the piece from the new square
            if movepiece == "P": # if white, replace black pawn
                self.position[movea.startsq[0]][movea.endsq[1]].placepiece("p") # replace en passant captured piece
            if movepiece == "p": # if black, replace white pawn
                self.position[movea.startsq[0]][movea.endsq[1]].placepiece("P") # replace en passant captured piece
        elif movea.promotion != None:
            if self.position[movea.endsq[0]][movea.endsq[1]].piece.iswhite: # movepiece is the rep for the piece that got moved
                movepiece = "P"
            else:
                movepiece = "p"
            self.position[movea.startsq[0]][movea.startsq[1]].placepiece(movepiece) # places the piece on the square where it started
            self.position[movea.endsq[0]][movea.endsq[1]].removepiece() # removes the piece from the new square
            if movea.captured != None: # if a piece was captured
                self.position[movea.endsq[0]][movea.endsq[1]].placepiece(movea.captured) # add the piece back to the square

    def checksinglelegal(self, movea, whitemove): # checks if moving into check
        self.makemovelite(movea)
        res = self.medloop(whitemove)
        # kingpos = self.getkingpos(whitemove)
        # attackedsquares = self.squaresattacked(not whitemove)
        self.unmakemovelite(movea)
        # return(kingpos not in attackedsquares)
        return(res)
    
    def checkalllegal(self, movelist, whitemove):
        legalmoves = []
        for movea in movelist:
            if self.checksinglelegal(movea, whitemove):
                legalmoves.append(movea)
        return(legalmoves)

    def genlegalmoves(self): # generates legal moves for the person who's turn it is
        whitemove = self.whitetomove
        possiblemoves = self.genmoves(whitemove)
        return(self.checkalllegal(possiblemoves, whitemove))

    def makemove(self, movea): # makes move and updates fen
        whiteness = self.whitetomove
        movepiece = None
        startsq = movea.getstartsquare()
        endsq = movea.getendsquare()

        # case 1 - castling... switch pieces and update castling rights
        if sum(movea.castle) > 0: # castle in right direction
            if movea.castle[0]:
                self.position[7][4].removepiece()
                self.position[7][7].removepiece()
                self.position[7][6].placepiece("K")
                self.position[7][5].placepiece("R")
                self.castlerights[0] = False
                self.castlerights[1] = False

            elif movea.castle[1]:
                self.position[7][4].removepiece()
                self.position[7][0].removepiece()
                self.position[7][2].placepiece("K")
                self.position[7][3].placepiece("R")
                self.castlerights[0] = False
                self.castlerights[1] = False

            elif movea.castle[2]:
                self.position[0][4].removepiece()
                self.position[0][7].removepiece()
                self.position[0][6].placepiece("k")
                self.position[0][5].placepiece("r")
                self.castlerights[2] = False
                self.castlerights[3] = False

            elif movea.castle[3]:
                self.position[0][4].removepiece()
                self.position[0][0].removepiece()
                self.position[0][2].placepiece("k")
                self.position[0][3].placepiece("r")
                self.castlerights[2] = False
                self.castlerights[3] = False
            
            # reset en passant
            self.enpassant = ()
        
        # case 2 - double pawn move... add en passant square (as is pawn moved one square)
        elif movea.doublepawn:
            movepiece = self.position[startsq[0]][startsq[1]].piece.rep # movepiece is the rep for the piece that is getting moved
            self.position[startsq[0]][startsq[1]].removepiece() # removes the piece from the square it was on
            self.position[endsq[0]][endsq[1]].placepiece(movepiece) # places piece on the new square

            # set up en passant for next move
            self.enpassant = ((startsq[0] + endsq[0]) // 2, startsq[1]) # en passant square is between startrank and endrank
        
        # case 3 - en passant
        elif movea.enpassant:
            movepiece = self.position[startsq[0]][startsq[1]].piece.rep # movepiece is the rep for the piece that is getting moved
            self.position[startsq[0]][startsq[1]].removepiece() # removes the piece from the square it was on
            self.position[endsq[0]][endsq[1]].placepiece(movepiece) # places the piece on the new square
            self.position[startsq[0]][endsq[1]].removepiece() # remove en passant captured piece

            # reset en passant
            self.enpassant = ()
        
        # case 4 - pawn promotion
        elif movea.promotion != None:
            movepiece = self.position[startsq[0]][startsq[1]].piece.rep # movepiece is the rep for the piece that is getting moved
            self.position[startsq[0]][startsq[1]].removepiece() # removes the piece from the square it was on
            self.position[endsq[0]][endsq[1]].placepiece(movea.promotion) # places the piece on the new square

            # reset en passant
            self.enpassant = ()
        
        # case 5 - normal move (contains captures)
        else:
            movepiece = self.position[startsq[0]][startsq[1]].piece.rep # movepiece is the rep for the piece that is getting moved
            self.position[startsq[0]][startsq[1]].removepiece() # removes the piece from the square it was on
            self.position[endsq[0]][endsq[1]].placepiece(movepiece) # places the piece on the new square
        
            # reset en passant
            self.enpassant = ()

            # check if castling changes
            if startsq == (7,4) or startsq == (7,7) or endsq == (7,4) or endsq == (7,7):
                self.castlerights[0] = False
            if startsq == (7,4) or startsq == (7,0) or endsq == (7,4) or endsq == (7,0):
                self.castlerights[1] = False
            if startsq == (0,4) or startsq == (0,7) or endsq == (0,4) or endsq == (0,7):
                self.castlerights[2] = False
            if startsq == (0,4) or startsq == (0,0) or endsq == (0,4) or endsq == (0,0):
                self.castlerights[3] = False

        # change move count
        if not whiteness:
            self.movecount += 1
        
        # update 50 move rule
        if sum(movea.castle) == 0 or movepiece in ["P", "p"] or movea.captured != None:
            self.nocap = 0
        else:
            self.nocap += 1
        
        # flip turn
        self.whitetomove = not whiteness
    
    def getshortmove(self, movea): # returns the move in SAN... not perfect bc doesn't check if moves are all legal for fancy stuff
        # check if castle
        if sum(movea.castle) == 1:
            return(movea.print())

        outstr = ""
        seensquares = [] # squares that can be seen
        onsquares = [] # squares that pieces see from
        movestart = movea.getstartsquare()
        moveend = movea.getendsquare()
        movepiece = self.position[movestart[0]][movestart[1]].piece

        # build first part of SAN
        if movepiece.rep.upper() == "P": # if it's a pawn... nothing funny, do seperately
            if movea.captured != None:
                outstr += coordstoalp(movestart)[0]
        else:
            outstr += movepiece.rep.upper()
            # loop over all squares
            for rank in range(8):
                for file in range(8):
                    if not (rank == movestart[0] and file == movestart[1]): # if piece isn't the one being moved
                        if not self.position[rank][file].isempty:
                            checkpiece = self.position[rank][file].piece
                            if movepiece.issamepiece(checkpiece):
                                seensquares.append(self.cansee(rank, file)) # stores the squares the piece can see
                                onsquares.append((rank, file)) # stores the square the piece is on
            seeendsquare = []
            for i in range(len(seensquares)):
                if moveend in seensquares[i]:
                    seeendsquare.append(onsquares[i])

            
            # some logic based on the ranks and files that can see square
            if len(seeendsquare) > 0:
                samefile = checkwhichfilesame(movestart, seeendsquare) # list squares that can move to end and share file
                if len(samefile) == 0:
                    outstr += coordstoalp(movestart)[0]
                else:
                    samerankfile = checkwhichranksame(movestart, seeendsquare)
                    if len(samerankfile) == 0:
                        outstr += coordstoalp(movestart)[1]
                    else:
                        outstr += coordstoalp(movestart)

        # build last part of SAN
        if movea.captured != None:
            outstr += "x"
        outstr += coordstoalp(moveend)

        # check if promotion
        if movea.promotion != None:
            outstr += "=" + movea.promotion.upper()
        return(outstr)

    def listmoves(self, width, allmoves): # lists allmoves in nice form
        nmoves = len(allmoves)
        for i in range(nmoves):
            if i % width == 0:
                print()
            outstr = str(i) + ". " + self.getshortmove(allmoves[i])
            if len(outstr) <= 7:
                outstr += "\t\t"
            else:
                outstr += "\t"
            
            print(outstr, end = "")
        print()

    def moveprompt(self, n): # list all legal moves (in rows of n) and takes input then makes move
        allmoves = self.genlegalmoves()
        self.listmoves(n, allmoves)
        print()
        boi = input("What move u finna make: ")
        movetomake = allmoves[int(boi)]
        self.makemove(movetomake)

    def resetposmap(self):
        for rank in range(8):
            for file in range(8):
                self.posmap[rank][file] = self.position[rank][file].code()

    def generatefen(self, full):
        posfen = "" # fen of the board position
        emptycount = 0
        for rank in range(8):
            for file in range(8):
                cha = self.posmap[rank][file]
                if cha == EMPTYCHAR:
                    emptycount += 1
                else:
                    if emptycount > 0:
                        posfen += str(emptycount)
                        posfen += cha
                        emptycount = 0
                    else:
                        posfen += cha
            if emptycount > 0:
                posfen += str(emptycount)
            if rank != 7:
                posfen += "/"
            emptycount = 0

        if self.whitetomove:
            movefen = "w"
        else:
            movefen = "b"

        castlefen = ""
        if sum(self.castlerights) == 0:
            castlefen += "-"
        else:
            for i in range(4):
                if self.castlerights[i]:
                    castlefen += castledirs[i]
        
        if self.enpassant == () or self.enpassant == None:
            croissant = "-"
        else:
            croissant = coordstoalp(self.enpassant)

        nocaps = str(self.nocap)
        
        movecount = str(self.movecount)

        if full:
            return(posfen + " " + movefen + " " + castlefen + " " + croissant + " " + nocaps + " " + movecount)
        else:
            return(posfen + " " + movefen + " " + castlefen + " " + croissant)
        
    def makecopy(self):
        self.resetposmap()
        return(board(self.generatefen(True)))

    def checkres(self): # returns 0 for game still going, 1 for white win, 2 for draw, 3 for black win
        # check 50 move rule
        if self.nocap >= 100:
            return(2)
        allmoves = self.genlegalmoves()
        if len(allmoves) > 0:
            return(0) 
        else:
            whitemove = self.whitetomove
            attacked = self.squaresattacked(not whitemove)
            kingpos = self.getkingpos(whitemove)
            if kingpos in attacked:
                if whitemove:
                    return(3)
                else:
                    return(1)
            else:
                return(2)

    def medloop(self, whiteness): # returns true if king in other colour attacked squares
        attackedsquares = set()
        kingpos = ()
        for rank in range(8):
            for file in range(8): # iterate over all squares
                checksquare = self.position[rank][file]
                if not checksquare.isempty: #if checksquare has a piece on it
                    if checksquare.piece.iswhite != whiteness: # if piece wrong colour
                        attackedsquares = attackedsquares.union(self.cansee(rank, file)) # check what squares it can attack
                    elif checksquare.piece.isking: # if piece same colour king 
                            kingpos = (rank, file) # set as king position
                        
        return(kingpos not in attackedsquares)

    def bigloop(self): # 
        # gets naive moves, attacked squares, and empty squares to check what moves are legal
        whitemove = self.whitetomove
        potentialmoves = []
        emptysquares = set()
        attackedsquares = set()
        for rank in range(8):
            for file in range(8): # iterate over all squares
                checksquare = self.position[rank][file]
                if checksquare.isempty: # if square is empty, add it to empty move list
                    emptysquares.add((rank, file))
                else: #otherwise...
                    if checksquare.piece.iswhite == whitemove: # if piece same colour
                        potentialmoves += self.genmovesfromsquare(rank, file, whitemove) # generate moves from square
                        if checksquare.piece.isking: # if piece is king, set as king position
                            kingpos = (rank, file)
                    
                    else: # if piece opposite colour
                        attackedsquares = attackedsquares.union(self.cansee(rank, file)) # check what squares it can attack

        # potential moves is moves before checking if illegal
        # empty squares
        # attacked squares
        # kingpos

        # check which moves legal

        return(potentialmoves, emptysquares, attackedsquares, kingpos)
            

class move:
    def __init__(self, startsq = None, endsq = None, captured = None, castle = None, promotion = None, enpassant = False, doublepawn = False):
        self.startsq = startsq
        self.endsq = endsq
        self.captured = captured
        self.castle = [x == castle for x in castledirs]
        self.promotion = promotion
        self.enpassant = enpassant
        self.doublepawn = doublepawn

    def copy(self):
        newmove = move()
        newmove.startsq = self.startsq
        newmove.endsq = self.endsq
        newmove.captured = self.captured
        newmove.castle = self.castle
        newmove.promotion = self.promotion
        newmove.enpassant = self.enpassant
        newmove.doublepawn = self.doublepawn
        return(newmove)
    
    def getstartsquare(self): # get start square as tuple
        if self.startsq != None:
            return(tuple(self.startsq))
        return(None)

    def getendsquare(self): # get end square as tuple
        if self.endsq != None:
            return(tuple(self.endsq))
        return(None)

    def print(self): # returns the string of the move
        if sum(self.castle) == 1:
            if self.castle[0] or self.castle[2]:
                outstr = "0-0"
            elif self.castle[1] or self.castle[3]:
                outstr = "0-0-0"
        else:
            outstr = ""
            outstr += coordstoalp(self.startsq)
            if self.captured != None: 
                outstr += "x"
            else:
                outstr += " "
            
            outstr += coordstoalp(self.endsq)

            if self.promotion != None:
                outstr += "=" + self.promotion
            if self.enpassant:
                outstr += " EN PASSANTANTNLDNFLdF"
        return(outstr)

    def equals(self, moveb):
        return(moveb.startsq == self.startsq and moveb.endsq == self.endsq and moveb.captured == self.captured and moveb.castle == self.castle and moveb.promotion == self.promotion and moveb.enpassant == self.enpassant and moveb.doublepawn == self.doublepawn)

class game: # game is a current position and a list of moves + boardstates
    def __init__(self, startfen):
        self.moves = []
        self.sans = []
        self.boardstates = [] # array of boards
        self.fenstarts = [] # array of fen states (just in case)
        self.currentboard = board(startfen)

        self.boardstates.append(self.currentboard.makecopy()) # add initial to boardstates
        self.fenstarts.append(self.currentboard.generatefen(False)) # add initial to fenbox... only first 3 parts tho for threefold checking

    def print(self):
        print("Current Position: ")
        self.currentboard.print(False)
        print()
        print("All fens:")
        for i in self.boardstates:
            print(i.generatefen(True))
        print()
        print("All moves:")
        for i in range(len(self.moves)):
            print(self.boardstates[i].getshortmove(self.moves[i]))

    def performmove(self, movea):
        self.currentboard.makemove(movea)
        self.moves.append(movea) # add move to movelist
        self.boardstates.append(self.currentboard.makecopy()) # add board to boardstates
        self.fenstarts.append(self.currentboard.generatefen(False)) # add fen to fenbox... only first 3 parts tho for threefold checking
    
    def undomove(self):
        self.boardstates.pop() # remove last boardstate 
        self.moves.pop() # remove last move 
        self.fenstarts.pop()  # remove last fen 
        self.currentboard = self.boardstates[-1].makecopy()  # make currentboard a copy of the last board in boardstates

    def playermove(self):
        self.currentboard.print()
        moves = self.currentboard.genlegalmoves()
        self.currentboard.listmoves(5, moves)
        movetomake = moves[int(input("Pick a move, dumbass: "))]
        self.performmove(movetomake)

    def playergame(self):
        while(True): # LOOP
            self.playermove()
            currentres = self.checkresult()
            if currentres > 0:
                break
        print()
        print()
        if currentres == 3:
            print("Black wins")
        elif currentres == 2:
            print("Draw")
        elif currentres == 1:
            print("White wins")
        else:
            print("What happn?")
    
    def checkresult(self):
        currentres = self.currentboard.checkres()
        threefold = self.checkthreefold()
        if threefold:
            return(2)
        else:
            return(currentres)

    def checkthreefold(self): # returns true if threefold repetition has occured
        allfens = self.fenstarts
        samecount = 0
        for i in allfens:
            for j in allfens:
                if i == j:
                    samecount += 1
            if samecount >= 3:
                return(True)
            samecount = 0
        return(False)

    def getpgnmoves(self):
        movepgns = []
        for i in range(len(self.moves)):
            movepgns.append(self.boardstates[i].getshortmove(self.moves[i]))

        pgnstr = ""
        for i in range(len(movepgns)):
            if i % 2 == 0:
                pgnstr += str(i // 2 + 1) + ". "
            pgnstr += movepgns[i] + " "
        return(pgnstr)

    def getpgn(self):
        startpos = self.boardstates[0].generatefen(True)
        return("[FEN \"" + startpos + "\"]\n" + self.getpgnmoves())
    
    def makemoves(self, moves):
        for boi in moves:
            self.performmove(boi)

    def enginegame(self):
        sigma = sigmafish()
        while(True): # LOOP
            if self.currentboard.whitetomove:
                self.playermove()
            else:
                eval, movetoplay = sigma.searchtodepth(self, 3)
                print(self.currentboard.getshortmove(movetoplay[0]))
                self.performmove(movetoplay[0])  
             
            currentres = self.checkresult()
            if currentres > 0:
                break
        print()
        print()
        if currentres == 3:
            print("Black wins")
        elif currentres == 2:
            print("Draw")
        elif currentres == 1:
            print("White wins")
        else:
            print("What happn?")


import random
class rnchessus:
    def pickmove(gamea):
        movelist = gamea.currentboard.genlegalmoves()
        return(movelist[random.randint(0, len(movelist)-1)])

poscount = 0
pieces = [EMPTYCHAR,"p","r","n","b","q","k","P","R","N","B","Q","K"]

class chessfish:
    def eval(boarda): # simple eval function... adds up white and black piece
        score = 0
        piecevals = [1, 5, 3, 3, 9, 0] # values of pawn, rook, knight, bishop, queen, and king
        boarda.resetposmap()
        boardmap = boarda.posmap
        for rank in range(8):
            for file in range(8):
                let = boardmap[rank][file]
                letnum = whichnum(pieces, let) - 1
                if letnum >= 6:
                    score += piecevals[letnum - 6]
                else:
                    score -= piecevals[letnum]
                
                # if rank in [3,4]:
                #     letnum = whichnum(pieces, let) - 1
                #     if letnum >= 6:
                #         score += piecevals[letnum - 6] * 0.25
                #     else:
                #         score -= piecevals[letnum] * 0.25
        return(score)

    def gameeval(gamea): # returns eval of a game position
        # if it's over return score
        LARGE = 100000
        currentres = gamea.currentboard.checkres()
        if gamea.checkthreefold() or currentres == 2:
            return(0)
        elif currentres == 1:
            return(LARGE)
        elif currentres == 3:
            return(-LARGE)
        else: # otherwise, return eval board
            return(chessfish.eval(gamea.currentboard))

    def search(gamea, depth, whiteness, moves = []):
        if depth == 0:
            global poscount
            poscount += 1
            return(chessfish.gameeval(gamea), moves)
        if gamea.checkresult() > 0:
            return(chessfish.gameeval(gamea), moves)
        else:
            movelist = gamea.currentboard.genlegalmoves()
            if whiteness:
                bestscore = -inf
                bestmoves = []
                for movea in movelist:
                        gamea.performmove(movea)
                        moves.append(movea)
                        bestscore, bestmoves = maxandmoves((bestscore, bestmoves), chessfish.search(gamea, depth-1, not whiteness, moves))
                        moves.pop()
                        gamea.undomove()
            else:
                bestscore = inf
                bestmoves = []
                for movea in movelist:
                        gamea.performmove(movea)
                        moves.append(movea)
                        bestscore, bestmoves = minandmoves((bestscore, bestmoves), chessfish.search(gamea, depth-1, not whiteness, moves))
                        moves.pop()
                        gamea.undomove()
            return(bestscore, bestmoves)

    def alphabeta(gamea, depth, alpha, beta, whiteness, moves):
        if depth == 0 or gamea.checkresult() > 0:
            global poscount
            poscount += 1
            if poscount % 100 == 0:
                print(poscount)
            return(chessfish.gameeval(gamea), moves)
        
        movelist = gamea.currentboard.genlegalmoves()
        bestmoves = []
        if whiteness:
            score = -inf  
            for movea in movelist:
                gamea.performmove(movea)
                moves.append(movea)
                score, bestmoves = maxandmoves((score, bestmoves), chessfish.alphabeta(gamea, depth-1, alpha, beta, False, moves))
                alpha = max(alpha, score)
                moves.pop()
                gamea.undomove()
                if score >= beta:
                    break
            return(score, bestmoves)
        else:
            score = inf
            for movea in movelist:
                gamea.performmove(movea)
                moves.append(movea)
                score, bestmoves = minandmoves((score, bestmoves), chessfish.alphabeta(gamea, depth-1, alpha, beta, False, moves))
                beta = min(alpha, score)
                
                gamea.undomove()
                if score >= alpha:
                    break
            return((score, bestmoves))


    def pickmove(gamea, depth):
        dats = chessfish.search(gamea, depth, gamea.currentboard.whitetomove, [])
        return(dats[1][0])

class sigmafish:
    def __init__(self):
        self.movedict = {}

    def eval(self, boarda): # simple eval function... adds up white and black piece
        score = 0
        piecevals = [1, 5, 3, 3, 9, 0] # values of pawn, rook, knight, bishop, queen, and king
        boarda.resetposmap()
        boardmap = boarda.posmap
        for rank in range(8):
            for file in range(8):
                let = boardmap[rank][file]
                letnum = whichnum(pieces, let) - 1
                if letnum >= 6:
                    score += piecevals[letnum - 6]
                else:
                    score -= piecevals[letnum]
                
                if rank in [3,4]: # bonus points for piece near middle of board
                    letnum = whichnum(pieces, let) - 1
                    if letnum >= 6:
                        score += piecevals[letnum - 6] * 0.25
                    else:
                        score -= piecevals[letnum] * 0.25    
        return(score)
    
    def gameeval(self, gamea): # returns eval of a game position
        # if it's over return score
        LARGE = 100000
        currentres = gamea.currentboard.checkres()
        if gamea.checkthreefold() or currentres == 2:
            return(0)
        elif currentres == 1:
            return(LARGE)
        elif currentres == 3:
            return(-LARGE)
        else: # otherwise, return eval board
            return(self.eval(gamea.currentboard))

    def getevalandmoves(self, gamea, depth, alpha, beta, whiteness, moves): 
        if depth == 0 or gamea.checkresult() > 0:
            global poscount
            poscount += 1
            if poscount % 100 == 0:
                print(poscount)
            return(self.gameeval(gamea), moves)
        
        loopevals = []
        loopmoves = []
        if movelisttokey(moves) in self.movedict: # if prior moves exist, check those first in order of best to move
            premoves = self.movedict[movelisttokey(moves)]
        else:
            premoves = []
        allmoves = gamea.currentboard.genlegalmoves()
        movelist = addmissingtoend(premoves, allmoves)
        bestmoves = []
        if whiteness:
            score = -inf  
            for movea in movelist:
                gamea.performmove(movea)
                moves.append(movea)
                newscore, nextmove = self.getevalandmoves(gamea, depth-1, alpha, beta, False, moves)
                score, bestmoves = maxandmoves((score, bestmoves), (newscore, nextmove))
                loopevals.append(newscore) # adds eval to loopevals
                loopmoves.append(nextmove[-depth].copy()) # adds the first move after the key to loopmoves
                moves.pop()
                gamea.undomove()
                if score >= beta:
                    break
                alpha = max(alpha, score)

            quicksortkeyval(loopevals, loopmoves, 0, len(loopevals)-1, True) # sorts loopmoves by eval
            self.movedict[movelisttokey(moves)] = copymovelist(loopmoves)
            return(score, bestmoves)
        else:
            score = inf
            for movea in movelist:
                gamea.performmove(movea)
                moves.append(movea)
                newscore, nextmove = self.getevalandmoves(gamea, depth-1, alpha, beta, True, moves)
                score, bestmoves = minandmoves((score, bestmoves), (newscore, nextmove))
                loopevals.append(newscore) # adds eval to loopevals
                if len(nextmove) < depth:
                    printmovelist(nextmove)
                loopmoves.append(nextmove[-depth].copy()) # adds the first move after the key to loopmoves
                moves.pop()
                gamea.undomove()
                if score <= alpha:
                    break
                beta = min(beta, score)
            quicksortkeyval(loopevals, loopmoves, 0, len(loopevals)-1, False) # sorts loopmoves by eval
            self.movedict[movelisttokey(moves)] = copymovelist(loopmoves)
            return(score, bestmoves)
    
    def searchtodepth(self, gamea, depth):
        self.movedict = {}
        for i in range(depth):
            eval, bestline = self.getevalandmoves(gamea, i+1, -inf, inf, gamea.currentboard.whitetomove, [])
            print("Depth:", i+1, "Eval:", eval, printmovelist(bestline))
        return(eval, bestline)

    def actualalphabeta(self, gamea, depth, alpha, beta):
        if depth == 0 or gamea.checkresult() > 0:
            global poscount
            poscount += 1
            if poscount % 100 == 0:
                print(poscount)
            return(-self.gameeval(gamea))
        
        movelist = gamea.currentboard.genlegalmoves()
        for movea in movelist:
            gamea.performmove(movea)
            score = -self.actualalphabeta(gamea, depth-1, -beta, -alpha)
            gamea.undomove()
            if score >= beta:
                return(beta)
            alpha = max(alpha, score)
        return(alpha)

    def searchmoves(self, gamea, depth):
        movelist = gamea.currentboard.genlegalmoves()
        evals = []
        for movea in movelist:
            gamea.performmove(movea)
            evals.append(-self.actualalphabeta(gamea, depth-1, -inf, inf))
            gamea.undomove()
        return(movelist, evals)

    def scoremove(self, movea): # quickly scores if it thinks a move is good or not
        movea

# class movetrees: # plan is to create two 2d arrays
# array 1 contains the moves searched at each level
# array 2 contains the next iteration's moves in order from highest to lowest eval
#     def __init__(self):



fenc = "rnbqk1nr/ppp2ppp/4p3/3p4/1bPP4/5N2/PP2PPPP/RNBQKB1R w KQkq - 2 4"

fend = "4k2r/6P1/5r2/1Pp5/8/r7/6K1/r7 w k c6 0 2"

fene = "rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/2N2N2/PP2PPPP/R1BQKB1R b KQkq - 3 4"

fenf = "7k/8/8/1N3N2/8/1N6/8/7K w k - 0 1"

dragonfen = "rnbqk2r/pp2ppbp/3p1np1/8/3NP3/2N1B3/PPP2PPP/R2QKB1R w KQkq - 2 7"

feng = "rnbqk2r/ppp1bppp/4pn2/3p4/2PP4/2N2N2/PP2PPPP/R1BQKB1R w KQkq - 4 5"

fenh = "r3kbnr/4p1p1/n6q/ppppPQNp/3P1P2/2P3P1/PP5P/RNB1KB1R w KQkq - 0 1"

gamea = game(fena)

sigma = sigmafish()

moves, scores = sigma.searchmoves(gamea, 3)

for i in range(len(moves)):
    print(moves[i].print(), scores[i])


# print(printmovelist(outmoves))

# for i in sigma.movedict:
#     print(i, printmovelist(sigma.movedict[i]))

# for i in outmoves:
#     gamea.performmove(i)




# sigma.ordermoves(False)
# for i in range(len(sigma.allscores)):
#     print(sigma.allscores[i], printmovelist(sigma.allmoves[i]))




# sigma.allmoves = []
# sigma.allscores = []



# sigma.ordermoves(False)
# for i in range(len(sigma.allscores)):
#     print(sigma.allscores[i], printmovelist(sigma.allmoves[i]))




#italian = [move((6,4),(4,4)), move((1,4),(3,4)), move((7,6),(5,5)), move((0,1),(2,2)), move((7,5),(4,2)), move((0,5),(3,2))]

# princefen = "rnbqkbnr/pp3ppp/7P/2ppp3/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 4"

# gamea = game(princefen)

# gamea.print()

# gamea.enginegame()

# fname = "princefen"
# boi = open(fname + ".txt", "w")
# boi.write(gamea.getpgn())
# boi.close


# gamea.currentboard.print()

# for boi in gamea.moves:
#     boi.print()


# for i in range(20):
#     game.print(True)
#     game.moveprompt()

# gamea = game(fena)
# print(alptonum("f8c5"))

# italian = [move((6,4),(4,4)), move((1,4),(3,4)), move((7,6),(5,5)), move((0,1),(2,2)), move((7,5),(4,2)), move((0,5),(3,2))]

# gamea.makemoves(italian)

# gamea.print()

# print(chessfish.search(gamea, 1, True))

# print(poscount)





# checking time stuff
import time

# boarda = board(fene)

# bruh = time.perf_counter_ns()

# loops = 10000

# for i in range(loops):
#     for rank in range(8):
#         for file in range(8):
#             checksquare = boarda.position[rank][file]
#             if not checksquare.isempty:
#                 boarda.cansee(rank, file)


# ayy = time.perf_counter_ns() - bruh

# print(ayy / loops)

#each loop over board for pieces about 10-20us

# loop over functions closer to 150us


# gamea = game(fena)

# italian = [move((6,4),(4,4)), move((1,4),(3,4)), move((7,6),(5,5)), move((0,1),(2,2)), move((7,5),(4,2)), move((0,5),(3,2))]

# gamea.makemoves(italian)


# poscount = 0
# bruh = time.perf_counter_ns()


# print(chessfish.alphabeta(gamea, 3, -inf, inf, True, []))

# ayy = time.perf_counter_ns() - bruh

# print(ayy)
# print(poscount)

# print(ayy / poscount)

#about 3.7ms per position searched

#medloop brings it down to 3.55ms per position

