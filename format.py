#this file is for pre-processing the words:
#formatWords(): turns a file with a bunch of words to a dictionary in this format:
#{<num letters>:{"<first letter>":{list of words with num letters & given first letter},...},...}
#i use sets because sets are fast
#this will make finding if a word is a word faster, bc we have to search through less
#outputs plaintext dict. to the file formattedWords, to be used with eval
pref = {}
def formatWords():
    f=open('words','r')
    lst=f.readlines()
    f.close()
    theDict={}
    for lin in lst:
        word=lin.strip()
        #1. eliminate fake words, remember boggle words have >2 chars, but double letters exist
        if word.isalpha() and word==word.lower() and len(word) >= 3:
            leng=len(word)
            first=word[0]
            if leng in theDict:
                partial=theDict[leng]
                if first in partial: #both are present, just append to list
                    partial[first].add(word)
                else: #words of same length but none of same letter yet
                    partial[first]={word}
            else: #no words of this length
                theDict[leng]={first:{word}} #this length starts with one entry
    out=open('formattedWords','w')
    out.write(str(theDict))
    out.close()

def prefix():
    pref={}
    form = open('formattedWords', 'r')
    largememe = form.read()
    form.close()
    dictio = eval(largememe)
    
    for number in dictio:
        for letter in dictio[number]:
            for word in dictio[number][letter]:
                if not letter in pref:
                    pref[letter]={number:set()}
                for i in range(2,number):
                    if i in pref[letter]:
                        pref[letter][i].add(word[:i])
                    else:
                        pref[letter][i]=set()
    outpref = open('prefixes','w')
    outpref.write(str(pref))
    outpref.close()
                   
        
formatWords()
prefix()
