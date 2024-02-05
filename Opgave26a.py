#f=open("OpenTaal-210G-basis-gekeurd.txt",'r')
f=open("wordlist.txt",'r')
woordenlist=f.read().splitlines()

alfabet=list("abcdefghijklmnopqrstuvwxyz")
alfabetplus=list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
capitalsalfabet=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def CheckKnownNumbers(woord,cryptedword,decryptdict):
    length=len(woord)
    for i in range(length):
        if cryptedword[i] in decryptdict.keys():
            if woord[i] not in decryptdict[cryptedword[i]]:
                return False
        if woord[i] not in alfabetplus:
            return False
    return True
            
def CheckIfLettersSame(woord,cryptedword):
    length=len(woord)
    for i in range(length):
        for j in range(i+1,length):
            if (cryptedword[i]==cryptedword[j] and cryptedword[i] in ["7","8"]) and (woord[i]!=woord[j]):
                return False
            elif cryptedword[i]!=cryptedword[j] and woord[i]==woord[j]:
                return False
    return True
            
def CheckKnownNotNumbers(woord,cryptedword,decryptdict,cryptedNonUniqueness):
    for number in decryptdict.keys():
        if len(decryptdict[number])==cryptedNonUniqueness[number]:
            for i in range(len(woord)):
                if cryptedword[i]!=number and woord[i] in decryptdict[number]:
                    return False
    return True

def DecryptSentence(decryptdict,cryptedNonUniqueness,sentence):
    newdecrypdict=decryptdict.copy()
    biglist=[[] for i in range(len(sentence))]
    for (n,cryptedword) in enumerate(sentence):
        length=len(cryptedword)
        for woord in woordenlist:
            if len(woord)!=length:
                continue
            if not CheckKnownNumbers(woord,cryptedword,decryptdict):
                continue
            if not CheckIfLettersSame(woord,cryptedword):
                continue
            if not CheckKnownNotNumbers(woord,cryptedword,decryptdict,cryptedNonUniqueness):
                continue
            biglist[n].append(woord)
    return biglist






#the one before last word gives 7:e by using CheckWord(6,[(0,1,5)],[2,3,4])
#58 2741 3335 4831582 2541741 148531 5483278 1538 775237 8417415532
sentence=[58,2741,3335,4831582,2541741,148531,5483278,1538,775237,8417415532]
cryptedNonUniqueness={"1":7*2,"2":3*2,"3":3*2,"4":2*2,"5":2*2,"7":1*2,"8":1*2}
sentence=[str(word) for word in sentence]
decryptdict={"1":"kvzbpKVZBP","2":"wsgWSG","3":"jatJAT","4":"olOL","5":"irIR","7":"eE","8":"nN"} #ezclap
biglist=DecryptSentence(decryptdict,cryptedNonUniqueness,sentence)

for i in range(len(biglist)):
    print(biglist[i])
