#! /usr/bin/env python
#source hex and market hex.
#to be a source hex must have a merchant
#wealth of a town is based on the stronghold
#function of length of existence strength of leaders and resources.
#length of existence and quality of resources 
#strongholds are primarily self sufficient.
#income that they generate.
#if i want to have an auction i need to calculate size of city
#somer sort of elite average class level.
#baron 10gp per person in barony
#patriarch 20gp per year
#Within each territory there will be from 2-8 villages of from 100-400 inhabitants
#But towns don't really exist until someone creates a stronghold and clears the wilderness
#subjugation and surrender rules.
#how you accumulate population.- hire mercenaries.
# load army
# load figures
# handle combat

from operator import itemgetter, attrgetter, methodcaller
import random, json

armies = [] #nicer if ordered for initiative so not a dict
roster  = {} #the types of units available
figureStatStream = open("figures.json", 'r')

def roll2d6():
    return random.randint(1,6)+ random.randint(1,6)
    
def hit(target):
    roll = random.randint(1,6)
    return roll >= target

class Figure:
    def __init__(self, statBlock):
        self.name  = statBlock['name']
        self.hd    = statBlock['hd']
        self.armor = statBlock['armor']
        self.hp    = self.hd 
    
    def __str__(self):
        return self.name
        
class Unit:
    def __init__(self, statBlock):
        self.type = roster[statBlock['type']]
        self.figureCount = statBlock['figureCount']
        self.figures = self.muster()
        self.casualties = 0
        self.rateOfLoss = 0
        self.morale = "ok"
    
    def __str__(self):
        pass
        #return self.name + " Unit Count = " + str(len(self.figures))
    
    def muster(self):
        figs = []
        for fig in range(self.figureCount):
           figs.append(self.type)
        return figs
    
    def checkMorale(self):
        pass

class Army:
    def __init__(self, statBlock):
        self.name = statBlock['name']
        self.units = []
        for unit in statBlock['units']:
            self.units.append(Unit(statBlock['units'][unit]))
        self.initiative = 0
    
    def rollInitiative(self):
        self.initiative = roll2d6()
        
def combat(armies):
    casualties = 0
    result = ""
    combatHappening = True
    bothSidesWent = False
    
    #initiative
    while armies[0].initiative is armies[1].initiative:
        for army in armies:
            army.rollInitiative()
    armies.sort(key = attrgetter('initiative'), reverse=True)
    print armies[0].initiative
    print armies[1].initiative
    #attack
    for unit in army['units'].keys():
        if len(units[1].figures) > 0 and hit(units[1].figures[0].armor):
            units[1].figures.pop(0)
            units[1].figureCount -= 1
            casualties += 1
    #morale
    if len(units[1].figures) is 0:
        result = units[0].name + " triumphed"
        combatHappening = False
    elif casualties > 0:
        rateOfLoss = units[1].figureCount / float(casualties)
        if roll2d6() + units[1].figures[0].hd + rateOfLoss >= 10:
            result = "battle continues"
        else:
            result = units[0].name + " routed the other army"
            combatHappening = False 
    else:
        result = "nothing happened"
    print result

unitList = json.load(figureStatStream)
  
for statBlock in unitList.keys():
    roster[statBlock] = Figure(unitList[statBlock])

while len(armies) < 2:
    armytoload = raw_input("enter the file name of the army to load: ")
    try: 
        armyList = json.load(open(armytoload, 'r'))
    except:
        if 'Good Guys' not in armies:
            armyList = json.load(open('goodguys.json', 'r'))
        else:
            armyList = json.load(open('badguys.json', 'r'))
    print "army list type"
    print type(armyList)
    armies.append(Army(armyList))
    print "object"
    print "loading army: "
    print json.dumps(armyList, indent=4, sort_keys=True)
print "done"

combat(armies)