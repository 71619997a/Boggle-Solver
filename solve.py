#!/usr/bin/python
print "Content-Type: text/html"
print ""
import cgi
import cgitb
cgitb.enable() 

board=[]
words={}
found={}
prefs={}
#Converts cgi.FieldStorage() return value into a standard dictionary
def FStoD():
    d = {}
    formData = cgi.FieldStorage()
    for k in formData.keys():
        d[k] = formData[k].value
    return d
    
#Takes the GET dictionary and turns it into a 2d list representing the board
def getBoard():
    boar=[[],[],[],[]]
    dictGET=FStoD()
    #probably should have made the front end with 0-3 instead of 1-4, oops

    for y in range(4):
        for x in range(4):
            elem=dictGET[str(y+1)+str(x+1)]
            boar[y].append(elem)
    #if you set somthing to a slice it will retain its value outside the function
    board[:]=boar

def printBoard(bord):
    html='<tt>'
    for row in bord:
        for lett in row:
            s=lett.find('>')
            if s == -1:
                if len(lett)==2:
                    html+= lett
                else:
                    html+= lett + ' '
            else:
                e=lett.find('<',s)
                space=e-s-1 #if there are tags, this willfind the actual leng of letter
                if space==2:
                    html+= lett
                else:
                    html+= lett + ' '
        html+= '<br>'
    return html+'</tt>'

#gets words from the formattedWords file
#eval is bad but it makes the program much faster & skips preprocessing
def getWords():
    f=open('formattedWords','r')
    text=f.read()
    f.close()
    return eval(text) #gets python-formatted dictionary from the file, completely safe usage of eval

def getPrefixes():
    pre=open('prefixes','r')
    text=pre.read()
    pre.close()
    return eval(text)

#gets where the neighbors are from x and y
def getNeighborPositions(x,y):
    ls=[]
    for anX in range(x-1,x+2):
        for aY in range(y-1,y+2):
            #kill invalid positions: x,y doesnt count, and x and y must be from 0 to 3
            if not (anX==x and aY==y) and anX>=0 and anX<=3 and aY>=0 and aY<=3:
                ls.append([anX,aY])
    return ls

def isPrefix(pref):
    leng=len(pref)
    if leng>=2:
        first=pref[0]
        if first in prefs:
            if leng in prefs[first]:
                return pref in prefs[first][leng]

def isWord(word):
    leng=len(word)
    if leng>=3:
        first=word[0]
        if leng in words:
            if first in words[leng]:
                return word in words[leng][first]
def beginRecurse(x,y):
    recurseThroughBoard(board[x][y],[[x,y]],x,y)

#the most important function! it goes through the board using recursion, finding every word.
def recurseThroughBoard(word,used,x,y): #word is the word so far, including (x,y), used is the positions used, including (x,y), x and y are coords of current pos
    for nextPos in getNeighborPositions(x,y):
        if not nextPos in used: #if we havent used this pos already
            newWord=word+board[nextPos[0]][nextPos[1]]
            newUsed=used+[[nextPos[0],nextPos[1]]]
            #Check if it's a word
            if isWord(newWord) and not newWord in found:
                found[newWord]=newUsed
            #Check if prefix or word (which dont count as prefs)
            if isPrefix(newWord):
                recurseThroughBoard(newWord, newUsed,nextPos[0],nextPos[1])
        #oh god. New word is the word plus the letter on the board for next position.
        #New used is old used plus the set of coords.
        #New x and y are next pos x and y.

def showOnBoard(word):
    pos=found[word]
    showBoard=[]
    #i tried copying the board with other methods, but they didnt work
    #so i had to resort to this :(
    for x in range(4):
        showBoard.append([])
        for y in range(4):
            showBoard[x].append(board[x][y])
    #first letter is green
    showBoard[pos[0][0]][pos[0][1]]='<font style="background-color: green">' \
                       +showBoard[pos[0][0]][pos[0][1]]+'</font>'
    #last is red
    showBoard[pos[-1][0]][pos[-1][1]]='<font style="background-color: red">' \
                        +showBoard[pos[-1][0]][pos[-1][1]]+'</font>'
    #the other ones are yellow
    for i in pos[1:-1]:
        showBoard[i[0]][i[1]]='<font style="background-color: yellow">' \
                      +showBoard[i[0]][i[1]]+'</font>'
    return showBoard

def negLen(a):
    return -len(a)

def sortedWords():
    return sorted(found,key=negLen)
    
htmlStr = "<html><head><title> Boggle Solver Results </title></head></html>\n"
htmlStr += "<body>"
enteredCorrect=True
try:
    getBoard()
except:
    enteredCorrect=False
if enteredCorrect:
    prefs=getPrefixes()
    words=getWords()
    for x in range(4):
        for y in range(4):
            beginRecurse(x,y)
    htmlStr += "<h3>Your board:<br></h3>"
    htmlStr += printBoard(board)
    htmlStr += "<h3>Your words:<br></h3>"
    for i in sortedWords():
        htmlStr+=i+'<br>'+printBoard(showOnBoard(i))+'<br><br>'

else:
    htmlStr+="The board was not entered correctly, try again."

htmlStr+='<br>Want to <a href="boggle.html">solve another board?</a>'
htmlStr += "</body></html>"


print htmlStr
