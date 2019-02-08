import math

numSlut = 8
begintimework = 8
endtimework = 16
lunchDuration = .25
beginLunch = 11
endLunch = 2
A = [.1, .3, .5, .7, 1]
output = open("outputsim.txt", 'a')

class task:
    def __init__(self, day, typeTask, slot, comingTime, startingTime):
        self.day = day
        self.typeTask = typeTask
        self.slot = slot
        self.comingTime = comingTime
        self.startingTime = startingTime

    def setTime(self, t):
        self.startingTime = t
        self.finishingTime = A[self.typeTask] + self.startingTime

    def print(self, file):

        file.write(self.day)
        file.write(self.slot)
        file.write(self.typeTask)
        file.write(self.comingTime)
        file.write(self.startingTime)
        file.write(self.finishingTime)
        

class employee:
    def __init__(self, number, start, end):
        self.number = number
        self.start = start
        self.freeTime = start
        self.end = end

    def setFreeTime(self, t):
        self.freeTime = t

    def setFreeTime(self):
        self.freeTime = systemTime + lunchDuration

    def checkAvailablity(self):
        if (self.start <= math.floor(systemTime)) and (math.floor(systemTime) <= (self.end + 1)):
            return 1
        else:
            return 0
    def checkStaylunch(self):
        if (beginLunch - begintimework +1 <= self.end) and (beginLunch - begintimework +1 >= self.start):
            return 1
        else:
            return 0


class lunchEvent:
    def __init__(self, employeeNumber, lunchTime):
        self.employeeNumber = employeeNumber
        self.lunchTime = lunchTime


f = open ( 'dataSimSchedule.txt' , 'r')
data = [[int(num) for num in line.split()] for line in f ]
f.close()
#print(data)
employeearray = []  # list of employee object
luncharray = []  # list of lunchEvent object

day = 1
dataindex = 0
t = 0
while data[dataindex][0] == day:
    x = employee(data[dataindex][1], data[dataindex][2] + begintimework - 1, data[dataindex][3] + begintimework - 1)
    employeearray.append(x)
    if x.checkStaylunch():
        l = lunchEvent(x.number, beginLunch + t/4.0)
        t = (t + 1) % (4*(endLunch - beginLunch))
        luncharray.append(l)
    dataindex += 1

beginLunch - begintimework +1
taskindex = 0
lunchindex = 0
taskarray = []  # sorted list of task object

i = 0



systemTime = 0

while (taskindex < len(taskarray)) or (lunchindex < len(luncharray)):
    minserverfreeindex = -1
    minserverfreevalue = 25
    while i < len(employeearray):
        if (systemTime < employeearray[i].freeTime) and (minserverfreevalue > employeearray[i].freeTime):
            minserverfreeindex = i
            minserverfreevalue = employeearray[i].freeTime
        i += 1
    systemTime = minserverfreevalue

    for l in luncharray:
        if l.lunchTime <= systemTime:
            if employee[l.employeeNumber].freeTime <= systemTime:
                employee[l.employeeNumber].setFreeTime()
                luncharray.remove(l)

    while taskarray[taskindex].startingTime <= systemTime:
        mn, idx = min((employeearray[j].freeTime, j) for j in range(len(employeearray)))
        taskarray[taskindex].setTime(systemTime)
        taskarray[taskindex].print()
        employeearray[idx].setFreeTime(taskarray[taskindex].finishingTime)
        if employeearray[idx].checkAvailablity() == 0 and employeearray[idx].end < endtimework:
            employeearray[idx].freeTime = 25
        taskindex += 1

output.close()
