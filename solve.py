#!/usr/bin/python
import cgi
import cgitb
#cgitb.enable() 

board=[]
words={}
found=[]

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

#gets words from the formattedWords file
#eval is bad but it makes the program much faster & skips preprocessing
def getWords():
    f=open('formattedWords','r')
    text=f.read()
    f.close()
    return eval(text) #gets python-formatted dictionary from the file, completely safe usage of eval

#gets where the neighbors are from x and y
def getNeighborPositions(x,y):
    ls=[]
    for anX in range(x-1,x+2):
        for aY in range(y-1,y+2):
            #kill invalid positions: x,y doesnt count, and x and y must be from 0 to 3
            if not (anX==x and aY==y) and anX>=0 and anX<=3 and aY>=0 and aY<=3:
                ls.append([anX,aY])
    return ls

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
            #Check if it's a word
            if isWord(newWord) and not newWord in found:
                found.append(newWord)
            recurseThroughBoard(newWord, used+[[nextPos[0],nextPos[1]]],nextPos[0],nextPos[1])
        #oh god. New word is the word plus the letter on the board for next position.
        #New used is old used plus the set of coords.
        #New x and y are next pos x and y.



htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!! 
htmlStr += "<html><head><title> INSERT TITLE HERE </title></head></html>\n"
htmlStr += "<body>"
enteredCorrect=True
try:
    getBoard()
except:
    enteredCorrect=False
if enteredCorrect:
    words=getWords()
    for x in range(4):
        for y in range(4):
            beginRecurse(x,y)
            print 'over'

    htmlStr += "<h3>Your board:<br></h3>"
    htmlStr += str(board)
    htmlStr += "<h3>Your words:<br></h3>"
    for i in found:
        htmlStr+=i+'<br>'
else:
    htmlStr+="The board was not entered correctly, try again."

htmlStr+='<br>Want to<a href="boggle.html">Solve another board?</a>'
htmlStr += "</body></html>"


print htmlStr
