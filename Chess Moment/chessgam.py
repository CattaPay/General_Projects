

# fen consists of position, to move, castling, en passant, half moves since pawn/cap, move num
fena = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
pieces = [" ","p","r","n","b","q","k","P","R","N","B","Q","K"]
files = ["a", "b", "c", "d", "e", "f", "g", "h"]
castledirs = ["K", "Q", "k", "q"]
fenb = "rnbqkbnr/pppp1pp1/8/4p2p/4P3/5Q2/PPPP1PPP/RNB1KBNR w KQkq - 0 3"
horsychange = [[2,1], [1,2], [-1,2], [-2,1], [1,-2], [2,-1], [-1,-2], [-2,-1]]
kingchange = [[1,0], [0,1], [-1,0], [0,-1], [1,1], [-1,1], [1,-1], [-1,-1]]


def alptonum(alp):
   return([8-int(alp[1]), ord(alp[0]) - ord('a')], [8-int(alp[3]), ord(alp[2]) - ord('a')])

def nametonum(startsq, endsq): #converts square names to move
   outbox = [0,0]
   outbox[0] = (8-int(startsq[1]), files.index(startsq[0]))
   outbox[1] = (8-int(endsq[1]), files.index(endsq[0]))
   return(outbox)

EMPTYCHAR = " "
def fentomap(fen):
   outpos = []
   row = []
   bois = fen.split(" ")[0]
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

def horseyadd(arra, rank, file):
   outbox = []
   for square in arra:
       outrank = rank + square[0]
       outfile = file + square[1]
       if outrank >= 0 and outrank <= 7 and outfile >= 0 and outfile <= 7:
           outbox.append([outrank, outfile])
   return(outbox)

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

class square:
   def __init__(self, letter, rank, file):
       self.isempty = letter == EMPTYCHAR
       if not self.isempty: #self.piece only defined if square occupied
           self.piece = piece(letter)
       self.rank = rank #might be important later
       self.file = file #might be important later
   def print(self):
       if self.isempty:
           print(EMPTYCHAR, end = " ")
       else:
           self.piece.print()

   def code(self):
       if self.isempty:
           return(EMPTYCHAR)
       else:
           return(self.piece.rep)

class board:
   def __init__(self, fen):
       self.posmap = fentomap(fen)
       self.position = []
       for rank in range(8):
           row = []
           for file in range(8):
               row.append(square(self.posmap[rank][file], rank, file))
           self.position.append(row)
       self.whitetomove = fen.split(" ")[1] == "w"
              
  
   def print(self):
       for rank in range(8):
           for file in range(8):
               self.position[rank][file].print()
           print()
       if self.whitetomove:
           print("White to move.")
       else:
           print("Black to move.")

   def checkdir(self, rank, file, rankinc, fileinc):
       count = 0
       piece = self.position[rank][file].piece
       whiteness = piece.iswhite
       for squaredif in range(1,8):
           checkrank = rank + squaredif*rankinc
           checkfile = file + squaredif*fileinc
           if checkrank >= 0 and checkrank <= 7 and checkfile >= 0 and checkfile <= 7:
               box = self.position[checkrank][checkfile]
               if box.isempty:
                   count += 1
               else:
                   if box.piece.iswhite != whiteness:
                       count += 1
                       return(count)
                   else:
                       return(count)
           else:
               return(count)
       return(count)
  
   def flipboard(self):
       newpos = []
       for i in range(8):
           newpos.append(self.position[7-i])
       self.position = newpos

   def genmoves(self, current):
       movebox = []
       for rank in range(8):
           for file in range(8):
               box = self.position[rank][file]
               if not box.isempty:
                   boi = box.piece
                   if boi.iswhite == self.whitetomove:
                       if boi.isrook:
                           # check right
                           dirx = 1
                           diry = 0
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))

                           # check left
                           dirx = -1
                           diry = 0
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))
                          
                           # check down
                           dirx = 0
                           diry = 1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))

                           # check up
                           dirx = 0
                           diry = -1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))

                       elif boi.isbishop:
                           # check northwest
                           dirx = 1
                           diry = -1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))

                           # check southwest
                           dirx = 1
                           diry = 1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))
                          
                           # check southeast
                           dirx = -1
                           diry = 1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))

                           # check northeast
                           dirx = -1
                           diry = -1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))
                      
                       elif boi.isqueen:
                           # check right
                           dirx = 1
                           diry = 0
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))

                           # check left
                           dirx = -1
                           diry = 0
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))
                          
                           # check down
                           dirx = 0
                           diry = 1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))

                           # check up
                           dirx = 0
                           diry = -1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))

                           # check northwest
                           dirx = 1
                           diry = -1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))

                           # check southwest
                           dirx = 1
                           diry = 1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))
                          
                           # check southeast
                           dirx = -1
                           diry = 1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))

                           # check northeast
                           dirx = -1
                           diry = -1
                           for i in range(1,self.checkdir(rank, file, dirx, diry)+1):
                               endbox = self.position[rank+dirx*i][file+diry*i]
                               movebox.append(move([rank, file], [rank+dirx*i, file+diry*i], endbox.code()))
                          
                       elif boi.isknight:
                           horsemoves = horseyadd(horsychange, rank, file)
                           for endsquare in horsemoves:
                               squareto = self.position[endsquare[0]][endsquare[1]]
                               if squareto.isempty:
                                   movebox.append(move([rank, file], endsquare, squareto.code()))
                               elif squareto.piece.iswhite != boi.iswhite:
                                   movebox.append(move([rank, file], endsquare, squareto.code()))
                      
                       elif boi.isking:
                           kingmoves = horseyadd(kingchange, rank, file)
                           for endsquare in kingmoves:
                               squareto = self.position[endsquare[0]][endsquare[1]]
                               if squareto.isempty:
                                   movebox.append(move([rank, file], endsquare, squareto.code()))
                               elif squareto.piece.iswhite != boi.iswhite:
                                   movebox.append(move([rank, file], endsquare, squareto.code()))

                       elif boi.ispawn:
                           # set up pawn jank
                           pawnrank = rank
                           pawnfile = file
                           whiteness = boi.iswhite
                           pawnmoves = []
                           if whiteness:
                               pawnrank = rank
                               pawnfile = file
                           else:
                               pawnrank = 7-pawnrank
                               pawnfile = 7-pawnfile
                               self.flipboard()

                           # find pawn moves
                           if self.position[pawnrank-1][pawnfile].isempty:
                               pawnmoves.append([pawnrank-1,pawnfile])
                               if pawnrank == 6 and self.position[pawnrank-2][pawnfile].isempty:
                                   pawnmoves.append([pawnrank-2,pawnfile])
                          
                           if pawnfile-1 >= 0:
                               if not self.position[pawnrank-1][pawnfile-1].isempty:
                                   if self.position[pawnrank-1][pawnfile-1].piece.iswhite != whiteness:
                                       pawnmoves.append([pawnrank-1,pawnfile-1])
                           if pawnfile+1 <= 7:
                               if not self.position[pawnrank-1][pawnfile+1].isempty:
                                   if self.position[pawnrank-1][pawnfile+1].piece.iswhite != whiteness:
                                       pawnmoves.append([pawnrank-1,pawnfile+1])
                          
                           # fixing pawn jank
                           if not whiteness:
                               self.flipboard()
                               for i in range(len(pawnmoves)):
                                   pawnmoves[i][0] = 7-pawnmoves[i][0]
                                   pawnmoves[i][1] = 7-pawnmoves[i][1]
                          
                           for endsquare in pawnmoves:
                               squareto = self.position[endsquare[0]][endsquare[1]]
                               movebox.append(move([rank, file], endsquare, squareto.code()))
       if current:
           self.possiblemoves = movebox
       else:
           return(movebox)


   def findkingpos(self):
       for rank in range(8):
           for file in range(8):
               box = self.position[rank][file]
               if not box.isempty:
                   if box.piece.isking and box.piece.iswhite != self.whitetomove:
                       return[rank, file]
                      
   def checkiflegal(self, move): # checks if a move from generatemoves is actually legal
       self.makemove(move)
       kingsquare = self.findkingpos()
       nextmoves = self.genmoves(False)
       for nextmove in nextmoves:
           if nextmove.endpos == kingsquare:
               self.unmakemove(move)
               return(False)
       self.unmakemove(move)
       return(True)
      
   def checkifalllegal(self):
       self.legalmoves = []
       for move in self.possiblemoves:
           if self.checkiflegal(move):
               self.legalmoves.append(move)

   def makemove(self, move):
       startsquare = self.position[move.startpos[0]][move.startpos[1]]
       endsquare = self.position[move.endpos[0]][move.endpos[1]]
       endsquare.isempty = False
       endsquare.piece = startsquare.piece
       startsquare.piece = piece("")
       startsquare.isempty = True
       self.whitetomove = not self.whitetomove
  
   def unmakemove(self, move):
       startsquare = self.position[move.startpos[0]][move.startpos[1]]
       endsquare = self.position[move.endpos[0]][move.endpos[1]]
       startsquare.isempty = False
       startsquare.piece = endsquare.piece
       endsquare.isempty = move.piecetaken == EMPTYCHAR
       endsquare.piece = piece(move.piecetaken)
       self.whitetomove = not self.whitetomove
  
   def movefromalp(self, alp):
       startsq, endsq = alptonum(alp)
       captured = self.position[endsq[0]][endsq[1]].code()
       return(move(startsq, endsq, captured))
  
   def makealpmove(self, alp):
       self.makemove(self.movefromalp(alp))

class move:
   def __init__(self, startpos, endpos, piecetaken): # startpos/endpos are of the form [rank, file]
       self.startpos = startpos
       self.endpos = endpos
       self.piecetaken = piecetaken
  
   def print(self):
       print(self.startpos, self.endpos)

   def printalp(self):
       print(files[self.startpos[1]] + str(8-self.startpos[0]) + files[self.endpos[1]] + str(8-self.endpos[0]))
game = board(fena)

game.print()








# game.makemove(game.possiblemoves[1])

# game.print()

# game.genmoves(True)
# game.checkifalllegal()
# print()

# for move in game.possiblemoves:
#     game.makemove(move)
#     game.print()
#     print()
#     game.unmakemove(move)


gameb = board(fenb)
#gameb.print()
#gameb.print()
#gameb.genmoves()
#for move in gameb.possiblemoves:
#    move.printalp()

"""
game.print()
game.genmoves()
for move in game.possiblemoves:
   move.printalp()
"""

"""
for i in range(10):
   game.print()
   print("Enter your move: ", end = "")
   inmove = input()
   boi = alptonum(inmove)
   game.makemove(move(boi[0], boi[1], False))
   print()
"""

#print(gameb.checkdir(5,7,0,1))

# thing that lets u type moves



""" class board():
   def __init__(self, fen):
       self.posmap = fentopos(fen)
       self.box = fen.split(" ")
       self.whitetomove = self.box[1] == "w"
       # set up castling
       self.castling = [False, False, False, False]
       for i in self.box[2]:
           if i in castledirs:
               self.castling[castledirs.index(i)] = True
       self.enpassant = self.box[3]
       self.movecount = int(self.box[5])
       self.halfmove = int(self.box[4])
   def print(self):
       for row in self.position:
           for piece in row:
               print(pieces[piece], end = " ")
           print()
       if self.whitetomove:
           print("White to Move")
       else:
           print("Black to Move")
       print("Castling: " + str(self.castling))
       print()
   def move(self, squares): # squares is [x1, y1, x2, y2]
       # move piece
       x1, y1 = squares[0]
       x2, y2 = squares[1]
       self.capped = self.position[x2][y2]
       self.position[x2][y2] = self.position[x1][y1]
       self.position[x1][y1] = 0
       # change move num
       if not self.whitetomove:
           self.movecount += 1
       # change turn
       self.whitetomove = not self.whitetomove
       # change castling
       if squares[0] == (7,0) or squares[1] == (7,0):
           self.castling[2] = False
       if squares[0] == (7,7) or squares[1] == (7,7):
           self.castling[1] = False
       if squares[0] == (7,4) or squares[1] == (7,4):
           self.castling[1] = False
           self.castling[2] = False
       if squares[0] == (0,0) or squares[1] == (0,0):
           self.castling[4] = False
       if squares[0] == (0,7) or squares[1] == (0,7):
           self.castling[3] = False
       if squares[0] == (0,4) or squares[1] == (0,4):
           self.castling[3] = False
           self.castling[4] = False
       #
   def genmoves(self):
       self.possiblemoves = []
       if self.whitetomove:
           for rank in range(8):
               for file in range(8):
                   if self.position[rank][file] == 1: # if pawn
                       if rank == 0 or rank == 7:
                           print("bruh how tf a pawn get here")
                       elif self.position[rank+1][file] == 0:
                           self.movelist.append([(rank, file), (rank+1, file)])
                           if self.position[rank+2][file] == 0 and rank == 1:
                               self.movelist.append([(rank, file), (rank+2, file)])
                       if self.position[rank+1][file+1]:
                           print("Hi")
                   # if self.position[rank][file] == 2: #if rook
                   #     count = 0
                   #     for i in range(7):
                   #         count += 1
                   #         if rank + count <= 7:
                   #             #print
#possible movelist
# Initialize movelist
#                       
gameboard = board(fena)
game = board(fena)
game.print()
game.move(nametonum("d2", "d4"))
game.print()
# game.move(nametonum("d7", "d5"))
# game.print()
# game.move(nametonum("c2", "c4"))
# game.print()
# print(nametonum("a1", "h1"))   
"""
