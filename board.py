#!/usr/bin/python
print 'Content-Type: text/html'
print ""
import cgi
import cgitb
cgitb.enable()
import random
first='aaeegn'
dice=["abbjoo", "achops", "affkps",
    "aoottw", "cimotu", "deilrx", "delrvy",
    "distty", "eeghnw", "eeinsu", "ehrtvw",
    "eiosst", "elrtty", "himnqu", "hlnnrz"]
#got this list from https://github.com/BR903/boggle

def generate():
    rolls=[random.choice(first)]
    for i in dice:
        of=len(rolls)
        num=random.randrange(of+1)
        if num == of:
            rolls.append(random.choice(i))
        else:
            rolls.insert(num,random.choice(i))
    board=[rolls[0:4],rolls[4:8],rolls[8:12],rolls[12:16]]
    return board

def printBoard(bord):
    html=''
    for row in bord:
        for lett in row:
            html+= lett + ' '
        html+= '<br>'
    return html
generatedmeme = generate()

def getstring(bord):
    html = '?'
    for i in range(4):
        for j in range(4):
            letter = bord[i][j]
            html += str(i + 1) + str(j + 1) + '=' + letter
    return html


htmlStr = "<html><head><title> Random Boggle Board</title></head></html>\n"
htmlStr += "<body>"
htmlStr += '<h3>Your Board:</h3><br><br>'
htmlStr += printBoard(generatedmeme)
htmlStr += '<br>Want to <a href="board.py">get another board?</a><br>'
htmlStr += 'Or <a href="solve.py'+getstring(generatedmeme)+'">solve this board?</a>'
htmlStr += 'Or <a href="boggle.html">go back?</a><br>'
htmlStr += "</body></html>"



print htmlStr
