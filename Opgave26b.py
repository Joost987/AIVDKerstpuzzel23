
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


#counterdict={"m":2,"r":4,"d":1} #van 9: meerdere 
testsentence=[[0,0,0], [0,0,1,0], [1,1,0], [0,"e"], [0,"e",0,"e"], [0,"e",0,1,"e",0], [2,1], ["e","e",1,1,"e",2], [0,"e",1,0,"e",0]]
sentence=[[0,0,0], [0,1,0,0,0,0,0], [2,3,0], [0,0,1,0,1,0,1,1,4], [0,2,1,2,5,1], [0,1], [0,1,1,3,1,2,2,6], \
          [2,7,1,3,1,4,8,2], [2,0,3,4,9,2],[2,10,11,3,1,12,4,13], [0,14,5,0,4,3,15,2,5,3,2,16,4], \
            [1,2,3,6],[3,17], [5,4,18,3,4,19,5]]
actualsentence=[[0,0,0], [0,"e",0,0,0,0,0], ["e","e",0], [0,0,1,0,1,0,1,1,"e"], [0,2,1,2,"e",1], [0,1], [0,1,1,3,1,2,2,"e"], \
          [2,"e",1,3,1,4,"e",2], [2,0,3,4,"e",2],[2,"e","e",3,1,"e",4,"e"], [0,"e",5,0,4,3,"e",2,5,3,2,"e",4], \
            [1,2,3,6],[3,"e"], [5,4,"e",3,4,"e",5]]

#woord8="echter"
woord1="bedacht"
woord2="een"
woord3="grafische"
woord4="manier"
woord5="om" #op, of, om
woord6="logische" #logische of typische
woord7="relaties" #relatief of relaties
woord8="tussen" #guess
woord9="meerdere" #meerdere of zeezieke
woord10="verzamelingen"
woord11="voor" #educated guess
woord12="te" #als 11 voor is, dan deze je of we
woord13="stellen"

#possibilities8=VindWoorden(actualsentence[8],{})
#if woord8 not in possibilities8:
 #   print("wrong word 8")
#counterdict8=PropagateDict(actualsentence[8],woord8,{})
counterdict8={}


possibilities9=VindWoorden(actualsentence[9],counterdict8)
if woord9 not in possibilities9:
    print("wrong word 9")
counterdict9=PropagateDict(actualsentence[9],woord9,counterdict8)

possibilities10=VindWoorden(actualsentence[10],counterdict9)
if woord10 not in possibilities10:
    print("wrong word 10")
counterdict10=PropagateDict(actualsentence[10],woord10,counterdict9)

possibilities11=VindWoorden(actualsentence[11],counterdict10)
if woord11 not in possibilities11:
    print("wrong word 11")
counterdict11=PropagateDict(actualsentence[11],woord11,counterdict10)

possibilities12=VindWoorden(actualsentence[12],counterdict11)
if woord12 not in possibilities12:
    print("wrong word 12")
counterdict12=PropagateDict(actualsentence[12],woord12,counterdict11)


possibilities13=VindWoorden(actualsentence[13],counterdict12)
if woord13 not in possibilities13:
    print("wrong word 13")
counterdict13=PropagateDict(actualsentence[13],woord13,counterdict12)
print(len(VindWoorden(actualsentence[13],counterdict12)))

counterdict12=BackPropagateDict(woord13,counterdict13)
counterdict11=BackPropagateDict(woord12,counterdict12)
counterdict10=BackPropagateDict(woord11,counterdict11) 
counterdict9=BackPropagateDict(woord10,counterdict10)
counterdict8=BackPropagateDict(woord9,counterdict9) 
possibilities8=BackVindWoorden(actualsentence[8],counterdict8)

counterdict7=BackOnlyPropagateDict(actualsentence[8],woord8,counterdict8)
possibilities7=BackVindWoorden(actualsentence[7],counterdict7)

counterdict6=BackOnlyPropagateDict(actualsentence[7],woord7,counterdict7)
possibilities6=BackVindWoorden(actualsentence[6],counterdict6)
print(possibilities6)

counterdict5=BackOnlyPropagateDict(actualsentence[6],woord6,counterdict6)
possibilities5=BackVindWoorden(actualsentence[5],counterdict5)
print(possibilities5)

counterdict4=BackOnlyPropagateDict(actualsentence[5],woord5,counterdict5)
possibilities4=BackVindWoorden(actualsentence[4],counterdict4)
print(possibilities4)

counterdict3=BackOnlyPropagateDict(actualsentence[4],woord4,counterdict4)
possibilities3=BackVindWoorden(actualsentence[3],counterdict3)
print("grafische" in possibilities3,possibilities3)

counterdict2=BackOnlyPropagateDict(actualsentence[3],woord3,counterdict3)
possibilities2=BackVindWoorden(actualsentence[2],counterdict2)
print(possibilities2)



counterdict1=BackOnlyPropagateDict(actualsentence[2],woord2,counterdict2)
possibilities1=BackVindWoorden(actualsentence[1],counterdict1)
print("bedacht" in possibilities1)

counterdict0=BackOnlyPropagateDict(actualsentence[1],woord1,counterdict1)
print(counterdict0)


