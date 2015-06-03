#!/usr/bin/python
#dan and gabe r kuhl
import cgi
import cgitb
cgitb.enable() 

#Converts cgi.FieldStorage() return value into a standard dictionary
def FStoD():

    d = {}
    formData = cgi.FieldStorage()
    for k in formData.keys():
        d[k] = formData[k].value
    return d

#Takes the GET dictionary and turns it into a 2d list representing the board
def getBoard():
    board=[[],[],[],[]]
    dictGET=FStoD()
    #probably should have made the front end with 0-3 instead of 1-4, oops
    for y in range(4):
        for x in range(4):
            elem=dictGET[str(y+1)+str(x+1)]
            board[y].append(elem)
    return board
htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!! 
htmlStr += "<html><head><title> INSERT TITLE HERE </title></head></html>\n"
htmlStr += "<body>"

htmlStr += "<h3>Your board:<br></h3>"
htmlStr += str(getBoard())


htmlStr += "</body></html>"


print htmlStr
