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

armies = {}
roster  = {} #the types of units available
figureStatStream = open("figures.json", 'r')


class Figure:
    def __init__(self, statBlock):
        self.name  = statBlock['name']
        self.hd    = statBlock['hd']
        self.armor = statBlock['armor']
        self.hp = self.hd 
    
    def __str__(self):
        return self.name
        
class Unit:
    def __init__(self, statBlock):
        self.type = 0
        self.figureCount = 0
    
    def __str__(self):
        pass
        #return self.name + " army size = " + str(len(self.figures))
    
    def create(self):
        pass
        #for i in range(random.randint(1,100)):
         #   self.figures.append(lightInfantry)
        #self.figureCount = len(self.figures)

def roll2d6():
    return random.randint(1,6)+ random.randint(1,6)
    
def hit(target):
    roll = random.randint(1,6)
    return roll >= target
    
def combat(armies):
    casualties = 0
    result = ""
    combatHappening = True
    bothSidesWent = False
    
    #initiative
    for army in armies:
        army['initiative'] = roll2d6()

    armies = sorted(units, key=attrgetter('initiative'), reverse=True)
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
print roster
while len(armies) < 2:
    armytoload = raw_input("enter the file name of the army to load: ")
    armyList = json.load(open(armytoload, 'r'))
    armies[armyList['name']] = armyList
    print "loading army:"
    print json.dumps(armyList, indent=4, sort_keys=True)

#combat([goodguys, badguys])

