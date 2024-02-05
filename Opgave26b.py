
f=open("wordlist.txt",'r')

woordenlist=f.read().splitlines()

alfabet=list("abcdefghijklmnopqrstuvwxyz")
alfabetplus=list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
capitalsalfabet=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

deletedwords=['Be', 'Ee', 'Fe', 'ge', 'he', 'He', 'ie', 'Le',  'ne', 'Ne', 're', 'se', 'Te', 'Ye', \
              'Meerbeke','CCCV','CCCX','CCLV','CCXV','CMLV', 'CMXV', 'DXXV','CCCI','CCLX','CCXI',"CDLI"]
for woord in deletedwords:
    woordenlist.remove(woord)


def CheckAlreadyFilledInAndE(cryptedword,woord):
    for i in range(len(cryptedword)):
        if cryptedword[i] in alfabet and cryptedword[i]!=woord[i]:
            return False
        if woord[i].lower()=="e" and not cryptedword[i]=="e": #not correct for first two words
            return False
        if woord[i] not in alfabetplus:
            return False
    return True

def CheckCounterdict(cryptedword,woord,counterdictcopy):
    counterdict=counterdictcopy.copy()
    for i in range(len(cryptedword)):
        if woord[i].lower() in counterdict.keys():
            if cryptedword[i]!=counterdict[woord[i].lower()]+1:
                return False
            else:
                counterdict.update({woord.lower()[i]:cryptedword[i]})
        elif cryptedword[i] not in alfabetplus:
            counterdict.update({woord.lower()[i]:cryptedword[i]})
    
    return True

def BackCheckCounterdict(cryptedword,woord,counterdictcopy):
    counterdict=counterdictcopy.copy()
    for i in range(len(cryptedword)):
        if woord[len(woord)-i-1].lower() in counterdict.keys():
            if cryptedword[len(woord)-i-1]!=counterdict[woord[len(woord)-i-1].lower()]:
                return False
            else:
                counterdict.update({woord[len(woord)-i-1].lower():cryptedword[len(woord)-i-1]-1})
        elif cryptedword[len(woord)-i-1] not in alfabetplus:
            counterdict.update({woord[len(woord)-i-1].lower():cryptedword[len(woord)-i-1]-1})
    return True

def PropagateDict(cryptedword,woord,counterdictcopy):
    counterdict=counterdictcopy.copy()
    for i in range(len(cryptedword)):
        if woord[i].lower() in counterdict.keys():
            if cryptedword[i]!=counterdict[woord[i].lower()]+1:
                print("Word is not correct")
                raise(RuntimeError)
            else:
                counterdict.update({woord[i].lower():cryptedword[i]})
        elif cryptedword[i] not in alfabetplus:
            counterdict.update({woord[i].lower():cryptedword[i]})
    
    return counterdict

def BackPropagateDict(woord,counterdict):
    counterdict=counterdict.copy()
    for i in range(len(woord)):
        if woord[len(woord)-i-1].lower()=="e":
            continue
        if woord[len(woord)-i-1].lower() in counterdict.keys():
            counterdict.update({woord[len(woord)-i-1].lower():counterdict[woord[len(woord)-i-1].lower()]-1})
        else:
            print(woord[len(woord)-i-1])
            print("Counterdict did not derive from this word")
            raise(RuntimeError)
    return counterdict

def BackOnlyPropagateDict(cryptedword,woord,counterdict):
    counterdict=counterdict.copy()
    for i in range(len(woord)):
        try:
            a=cryptedword[len(woord)-i-1]
        except:
            print(woord,cryptedword,i,'fail')
        if woord[len(woord)-i-1].lower()=="e":
            continue
        if woord[len(woord)-i-1].lower() in counterdict.keys():
            counterdict.update({woord[len(woord)-i-1].lower():counterdict[woord[len(woord)-i-1].lower()]-1})

        elif cryptedword[len(woord)-i-1] not in alfabetplus:
            counterdict.update({woord[len(woord)-i-1].lower():cryptedword[len(woord)-i-1]-1})

    return counterdict


def VindWoorden(cryptedword,counterdict):
    length=len(cryptedword)
    possibilities=[]
    for woord in woordenlist:
        if len(woord)!=length:
            continue
        if not CheckAlreadyFilledInAndE(cryptedword,woord):
            continue
        if not CheckCounterdict(cryptedword,woord,counterdict):
            continue
        possibilities.append(woord)
    return possibilities

def BackVindWoorden(cryptedword,counterdict):
    length=len(cryptedword)
    possibilities=[]
    for woord in woordenlist:
        if len(woord)!=length:
            continue
        if not CheckAlreadyFilledInAndE(cryptedword,woord):
            continue
        if not BackCheckCounterdict(cryptedword,woord,counterdict):
            continue
        possibilities.append(woord)
    return possibilities

def TryHardForward(actualsentence):
    counterdictlst=[("",{})]
    for i in range(9,14):
        counterdictlstnew=[]
        for (translation,counterdict) in counterdictlst:
            possibilities=VindWoorden(actualsentence[i],counterdict)
            for possibility in possibilities:
                counterdictlstnew.append((translation+" "+possibility,PropagateDict(actualsentence[i],possibility,counterdict)))
        counterdictlst=counterdictlstnew
    return counterdictlst

def TryHardBackward(actualsentence,counterdictlst):
    for i in range(9,14):
        index=14-i-1+9
        counterdictlstnew=[]
        for (translation,counterdict) in counterdictlst:
            woord=translation.split(" ")[index-9]
            counterdictlstnew.append((translation,BackPropagateDict(woord,counterdict)))
        counterdictlst=counterdictlstnew
    for (translation,counterdict) in counterdictlst:
        possibilities=BackVindWoorden(actualsentence[8],counterdict)
        if len(possibilities)!=0:
            print(len(possibilities))


testsentence=[[0,0,0], [0,0,1,0], [1,1,0], [0,"e"], [0,"e",0,"e"], [0,"e",0,1,"e",0], [2,1], ["e","e",1,1,"e",2], [0,"e",1,0,"e",0]]
sentence=[[0,0,0], [0,1,0,0,0,0,0], [2,3,0], [0,0,1,0,1,0,1,1,4], [0,2,1,2,5,1], [0,1], [0,1,1,3,1,2,2,6], \
          [2,7,1,3,1,4,8,2], [2,0,3,4,9,2],[2,10,11,3,1,12,4,13], [0,14,5,0,4,3,15,2,5,3,2,16,4], \
            [1,2,3,6],[3,17], [5,4,18,3,4,19,5]]
actualsentence=[[0,0,0], [0,"e",0,0,0,0,0], ["e","e",0], [0,0,1,0,1,0,1,1,"e"], [0,2,1,2,"e",1], [0,1], [0,1,1,3,1,2,2,"e"], \
          [2,"e",1,3,1,4,"e",2], [2,0,3,4,"e",2],[2,"e","e",3,1,"e",4,"e"], [0,"e",5,0,4,3,"e",2,5,3,2,"e",4], \
            [1,2,3,6],[3,"e"], [5,4,"e",3,4,"e",5]]




