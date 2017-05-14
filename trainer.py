import os
from reverend.thomas import Bayes
trainer = Bayes()
def get_next_lowest_block_ind(y,x,mparr):
    column = ""
    for horiz in mparr:
        column += horiz[x]
    
    for ind, block in enumerate(column[y:]):
        if block != "-":
            return ind
        return 

def get_rel_surfaces(y,x,mparr):
    column = ""
    for horiz in mparr:
        colummn += horiz[x]
    surfaces = []
#    for ind, block in enumerate(column):
#        if block != "-":

def is_jumping(mario):
    if mario["jump"] or mario["ypos"] not in [ind for ind, block in enumerate(mario["curr"][::-1]) if block == "#" or block == "?"]:
        return True
    return False

def train(parsed_ticks): # mario, nextblock, currblock, nbindex):
    global trainer
    prev_xpos = 0
    inp = ""
    keys = ["left", "right", "down", "jumping", "speed"]
    for key in keys:
        inp += str(parsed_ticks[0][key])
    for ticknum, mario in enumerate(parsed_ticks):
        if ticknum == len(parsed_ticks)-1:
            continue
        
        if mario["xpos"] != prev_xpos:
            mario_offset = mario["xpos"] - prev_xpos
            trainer.train(mario["curr"]+":"+str(mario_offset)+":"+str(mario["ypos"]), inp)
            prev_xpos = mario["xpos"]
            inp = ""
        else:
            continue
        for key in keys:
            inp += str(mario[key])



for fn in os.listdir("./"):
    if fn == "trainer.py" or fn == "classifier":
        continue
    cf = ""
    with open(fn,"r") as f:
        cf = f.read()
    ticks = cf.split("\n")
    print fn
    parsed_ticks = []
    for tick in ticks[1:]:
        if tick == "":
            print "empty"
        else:
            tickarr = tick.split("\t")
            mario = {"ticknum":int(tickarr[0]),
                    "left":int(tickarr[1][0]),
                     "right":int(tickarr[1][1]),
                     "down":int(tickarr[1][2]),
                     "jump":int(tickarr[1][3]),
                     "speed":int(tickarr[1][4]),
                     "xpos":int(tickarr[2]),
                     "ypos":int(tickarr[3]),
                     "2prev":tickarr[4],
                     "prev":tickarr[5],
                     "curr":tickarr[6],
                     "next":tickarr[7]}
            mario["jumping"] = int(is_jumping(mario))
            parsed_ticks.append(mario)
    train(parsed_ticks)
trainer.save("classifier")

f = open("astar_01.tsv","r")
sample = f.read().split("\n")
inp = []
for line in sample:
    if line != "":
        inp.append(line.split("\t")[1])
currx = 0
curry = 0
print trainer.guess("01001")
for keym in inp[1:]:
    print keym
    guess = trainer.guess(keym)
    print guess
    guess = guess.split(":")
    print guess[0]



