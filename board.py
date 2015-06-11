#!/usr/bin/python
import random
print 'Content-Type: text/html'
print ""
first='aaeegn'
dice=["abbjoo", "achops", "affkps",
    "aoottw", "cimotu", "deilrx", "delrvy",
    "distty", "eeghnw", "eeinsu", "ehrtvw",
    "eiosst", "elrtty", "himnqu", "hlnnrz"]
#got this list from https://github.com/BR903/boggle

def generate():
    rolls=[choice(first)]
    for i in dice:
        of=len(rolls)
        num=random.randrange(of+1)
        if num == of:
            rolls.append(choice(i))
        else:
            rolls.insert(num,choice(i))
    board=[rolls[0:4],rolls[4:8],rolls[8:12],rolls[12:16]]
    return board


                               
