class Grid:
    def __init__(self,nodes):
        self.nodesdic=nodes
        self.finishingnodes=[]
        self.startingnodes=[]
        self.FindStartingNodes()
        self.firstnode=None
        self.lastnode=None
        self.CheckBreaks()

    def printStartingNodes(self):
        for (node,color,times) in self.startingnodes:
            print(node,color,times,node.BreakConnections())

    def printEndingNodes(self):
        for (node,color,times) in self.finishingnodes:
            print(node,color,times,node.BreakConnections())

    def CheckBreaks(self):
        for node in self.nodesdic.values():
            times=sum([times for (node2, color, times) in self.startingnodes if node==node2 ])
            times+=sum([times for (node2, color, times) in self.finishingnodes if node==node2 ])
            if times!=node.BreakConnections():
                if sum([times for (node2, color, times) in self.startingnodes if node==node2 ])>0 and sum([times for (node2, color, times) in self.finishingnodes if node==node2 ])==0:
                    self.firstnode=node
                if sum([times for (node2, color, times) in self.startingnodes if node==node2 ])==0 and sum([times for (node2, color, times) in self.finishingnodes if node==node2 ])>0:
                    self.lastnode=node
                

    

    
    def StartFinishNodesColor(self,color):
        startnodes=[node for (node,color2,times) in self.startingnodes if color==color2 for i in range(times)]
        finishnodes=[node for (node,color2,times) in self.finishingnodes if color==color2 for i in range(times)]
        return startnodes,finishnodes
    
    #startnodes=[node for (node,color2,times) in self.startingnodes if color==color2 for i in range(times)]
    def FindWordsColorStart(self,color,words,startnodes,finishnodes):

        
        node=startnodes[-1]
        if [connection for connection in node.outcomingconnectionslist if connection.color==color]==[] and node not in finishnodes:
            print("something went wrong")
            raise(RuntimeError)
        
        startnodes.remove(node)
        words[-1].append(node)
        for outcomingconnection in node.outcomingconnectionslist.copy():
            if outcomingconnection.color==color:
                #print(len(node.outcomingconnectionslist.copy()),node.symbol,outcomingconnection.NodeTo,len(words),len(words[-1]), "start")
                node.RemoveOutcomingConnection(outcomingconnection)
                grid.FindWordsColor(outcomingconnection.NodeTo,color,words,startnodes,finishnodes)
                node.AddOutcomingConnection(outcomingconnection)
        startnodes.append(node)
        words[-1].pop().symbol
        #print("popped: ", ,node.symbol)
        if node in startnodes and words[-1]!=[]:
           # if words[-1][-1]!=" ":

                #print("not a space",words[-1][-1])
            #    #raise(RuntimeError)
            if words[-1][-1]==" ":#else:
                words[-1].pop()        
        
        return words
    
    def FindWordsColor(self,node,color,words,startnodes,finishnodes):
        
        words[-1].append(node)
        if [connection for connection in node.outcomingconnectionslist if connection.color==color]==[] and node not in finishnodes:
            print("something went wrong")
            raise(RuntimeError)
        
        if node in finishnodes:
           # print(len(finishnodes),node.symbol)
            finishnodes.remove(node)
            #words.insert(0,words[-1])
            
            if startnodes!=[]:
                words[-1].append(" ")
                grid.FindWordsColorStart(color,words,startnodes,finishnodes)
            else:
                if finishnodes!=[]:
                    print("Something went wrong")
                    raise(RuntimeError)
                
                if [connection for node2 in self.nodesdic.values() for connection in node2.outcomingconnectionslist if connection.color==color]==[]:
                    words[-1].append(" ")
                   # print(len(finishnodes),node.symbol,"here")
                    words.insert(0,words[-1].copy())
                    #print(len(words))
                
            finishnodes.append(node)
        
        for outcomingconnection in node.outcomingconnectionslist.copy():
           if outcomingconnection.color==color:
               # print(len(node.outcomingconnectionslist.copy()),node.symbol,outcomingconnection.NodeTo,len(words),len(words[-1]))
                node.RemoveOutcomingConnection(outcomingconnection)
                grid.FindWordsColor(outcomingconnection.NodeTo,color,words,startnodes,finishnodes)
                node.AddOutcomingConnection(outcomingconnection) 
        
        if node in finishnodes:
        #    if words[-1][-1]!=" ":
         #       print("not a space",words[-1][-1])
          #      raise(RuntimeError)
            if words[-1][-1]==" ":# else:
                 words[-1].pop()
        words[-1].pop()
        #print("popped: ", .symbol,node.symbol)
      #  if len(words[-1])>9:
            #print(words[-1][9].symbol)
        return words




    def FindStartingNodes(self): #this will currently not find all starting nodes, as if a word starts at the same node as it finishes it will not be found
        for node in self.nodesdic.values():
            connectionsdict=node.Connections()
            for color in connectionsdict.keys():
                if connectionsdict[color][0] == connectionsdict[color][1]:
                    continue

                elif connectionsdict[color][0] > connectionsdict[color][1]: 
                    self.finishingnodes.append((node,color,connectionsdict[color][0]-connectionsdict[color][1])) #finishing node
                    
                elif connectionsdict[color][0] < connectionsdict[color][1]:
                    self.startingnodes.append((node,color,connectionsdict[color][1]-connectionsdict[color][0]))  #starting node

                   
class Node:

    def __init__(self,symbol):
        self.symbol=symbol
        self.incomingconnectionslist=[]
        self.outcomingconnectionslist=[]
        self.BreakConnectionslist=[]
        self.translate=symbol

    def __str__(self):
        return self.translate
        #return self.symbol
        #print(self.symbol)
        "^"
    
    def AddIncomingConnection(self,connection):
        self.incomingconnectionslist.append(connection)

    def AddOutcomingConnection(self,connection):
        self.outcomingconnectionslist.append(connection)

    def AddBreakConnection(self,breakconnection):
        self.BreakConnectionslist.append(breakconnection)

    def RemoveIncomingConnection(self,connection):
        self.incomingconnectionslist.remove(connection)

    def RemoveOutcomingConnection(self,connection):
        self.outcomingconnectionslist.remove(connection)

    def RemoveBreakConnection(self,breakconnection):
        self.BreakConnectionslist.remove(breakconnection)

    def Connections(self):
        connectionsdict={color:(0,0) for color in colors}

        for connection in self.incomingconnectionslist:
            connectionsdict.update({connection.color:(connectionsdict[connection.color][0]+1,0)})

        for connection in self.outcomingconnectionslist:
            connectionsdict.update({connection.color:(connectionsdict[connection.color][0],connectionsdict[connection.color][1]+1)})
        
        return connectionsdict
    
    def BreakConnections(self):
        return len(self.BreakConnectionslist)
    


class Connection:

    def __init__(self,color,NodeFrom,NodeTo):
        self.color=color
        self.NodeFrom=NodeFrom
        self.NodeTo=NodeTo


class BreakConnection:

    def __init__(self,NodeFrom,NodeTo):
        self.NodeFrom=NodeFrom
        self.NodeTo=NodeTo

colors=["yellow","green","lightblue","orange","blue","red","pink"]
Calphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
nodelst={letter:Node(letter) for letter in Calphabet}
connections=[("yellow","Y","X"),("yellow", "X","B"),("yellow","B","B"),("yellow","B","U"), \
             ("yellow","S","B"),("yellow","Q","S"),("yellow","Q","B"), \
             ("yellow","V","Q"), ("yellow","V","V"), ("yellow","V","W"), ("yellow","W","V"),\
             ("yellow","W","W"), ("yellow","V","F"), ("yellow","L","V"),\
             ("green","B","R"), ("green","A","B"), ("green","B","L"), ("green","W","B"),\
             ("green","V","V"), ("green","U","V"), ("green","L","W"),("green", "G", "W"), \
             ("orange","A","F"), ("orange","F","B"), ("orange","B","B"),("orange","B","D"),\
             ("orange","T","V"), ("orange", "L", "T"), ("orange","V","L"),("orange","I","V"),\
             ("red","U","C"), ("red","C","V"), ("red","V","N"), ("red","V","N"), ("red","N","L"),\
             ("red","L","N"), ("red","N","P"), ("red","P","T"), ("red","T","M"),("red","M","V"),("red","N","J"),\
             ("lightblue","E","C"), ("lightblue","C","U"), ("lightblue","U","R"),("lightblue","R","L"),\
             ("lightblue","L","N"), ("lightblue","N","P"), ("lightblue","P","K"), ("lightblue","K","W"),\
             ("lightblue", "H","L"), ("lightblue","L","V"), ("lightblue","V","O"),("lightblue","O","V"),\
             ("blue","U","V"), ("blue","V","W"), ("blue","V","S"), ("blue","S","V"), ("blue","J","N"),\
             ("blue","N","W"), ("blue","J","V"),\
             ("pink","P","B"), ("pink","B","B"), ("pink","B","F"), ("pink","F","G"), ("pink","G","W"),\
             ("pink","J","V"), ("pink","V","F"),("pink","T","V")]

breakconnections=[("H","F"),("I","J"),("J","W"),("J","W"),("B","J"),("B","U"),("V","A"),("R","A"),\
                  ("Y","V"),("W","T"),("P","W"),("L","V"),("V","F"),("V","G"),("U","U"),("U","D"),("E","V")]

for connection in connections:
    nodelst[connection[1]].AddOutcomingConnection(Connection(connection[0],nodelst[connection[1]],nodelst[connection[2]]))
    nodelst[connection[2]].AddIncomingConnection(Connection(connection[0],nodelst[connection[1]],nodelst[connection[2]]))
    
for breakconnection in breakconnections:
    nodelst[breakconnection[0]].AddBreakConnection(BreakConnection(breakconnection[0],breakconnection[1]))
    nodelst[breakconnection[1]].AddBreakConnection(BreakConnection(breakconnection[0],breakconnection[1]))

#print(list(nodelst.values()))
grid=Grid(nodelst)

#rood moeilijkheid
translationlst=[('A', 'v'), ('B', 'a'), ('C', 'o'), ('D', 'g'), ('E', 'c'),
                 ('F', 'r'), ('G', 's'), ('H', 'b'), ('I', 'w'), ('J', 'd'),
                   ('K', 'f'), ('L', 'l'), ('M', 'h'), ('N', 'i'), ('O', 'x'),
                     ('P', 'j'), ('Q', 'n'), ('R', 'p'), ('S', 'z'), ('T', 'k'), 
                     ('U', 'm'), ('V', 'e'), ('W', 't'),('Y','q'),('X','u')]
for (symb,trans) in translationlst:
    nodelst[symb].translate=trans


#print(mult)

color="orange"
words=grid.FindWordsColorStart(color,[[]],*grid.StartFinishNodesColor(color))
print(len(words),color)
for word in words:
    for symbol in word:
        print(symbol,end="")

print()
color="lightblue"
words=grid.FindWordsColorStart(color,[[]],*grid.StartFinishNodesColor(color))
print(len(words),color)
for word in words:
    for symbol in word:
        print(symbol,end="")
    print()
print()
color="blue"
words=grid.FindWordsColorStart(color,[[]],*grid.StartFinishNodesColor(color))
print(len(words),color)
for word in words:
    for symbol in word:
        print(symbol,end="")
    print()
print()
color="green"
words=grid.FindWordsColorStart(color,[[]],*grid.StartFinishNodesColor(color))
print(len(words),color)
for word in words:
    for symbol in word:
        print(symbol,end="")
    print()
color="red"
words=grid.FindWordsColorStart(color,[[]],*grid.StartFinishNodesColor(color))
print(len(words),color)
for word in words:
    for symbol in word:
        print(symbol,end="")
    print()
color="pink"
words=grid.FindWordsColorStart(color,[[]],*grid.StartFinishNodesColor(color))
print(len(words),color)
for word in words:
    for symbol in word:
        print(symbol,end="")
    print()

color="yellow"
words=grid.FindWordsColorStart(color,[[]],*grid.StartFinishNodesColor(color))
print(len(words),color)
for word in words:
    strings=""
    for symbol in word:
        if symbol==" ":
            strings+=symbol
        else:
            strings+=symbol.translate          
    if " eenzaam " in strings:
        print(strings)

#woorden: welke vraag blijft complexe met deze dit mee stap valt 
#moeilijkheid kerst jaar de qua eenzaam na
#na deze complexe vraag, blijft de stap qua moeilijkheid mee valt welke letter deze kerst dit jaar eenzaam blijft
#na deze complex stap, valt de vraag mee qua moeilijkheid: welke letter eenzaam met kerst dit jaar blijft