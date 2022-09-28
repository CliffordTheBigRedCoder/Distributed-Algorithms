class Process:
    def __init__(self,pid,neighbours,activation_time):
        self.pid = pid
        self.neighbours = neighbours
        self.neighbour_signals = [0] * len(neighbours)
        self.silent_neighbour = None
        self.activation_time = activation_time
        self.activated = False
        self.waiting_signals = []
        self.decider = True

    def signal_received(self,sender):
        print(str(sender)+"'s signal for "+self.pid+" received")
        
        if self.activated == False:
            self.waiting_signals.append(sender)
            print(str(sender)+"'s signal for "+self.pid+" put in waiting signals to process upon activation")
        else:
            for i in range(0,len(self.neighbours)):
                if self.neighbours[i] == sender:
                    print(str(sender)+"'s signal for "+self.pid+" processed")
                    self.neighbour_signals[i] = 1

            self.silent_neighbour_check()

    def activate(self):
        print(str(self.pid)+" activated")
        self.activated = True
        self.silent_neighbour_check()
        for i in self.waiting_signals:
            self.signal_received(i)
        self.waiting_signals = []

    def silent_neighbour_check(self):
        
        if len(self.neighbour_signals) == self.neighbour_signals.count(1)+1:
            receiver = self.neighbours[self.neighbour_signals.index(0)]
            print(self.pid+"'s signal for "+str(receiver)+" sent")
            new_stack.append([receiver,int(self.pid)])
        elif len(self.neighbour_signals) == self.neighbour_signals.count(1):
            self.decider = True
            deciders.append(self.pid)
            print(self.pid+" is one of the decider's")
            if len(deciders) == 2:
                new_stack.append("end")

processes = []

f = open("processes.txt", "r")
for i in f:
    details = i.split(":")
    details[1] = details[1].split(",")
    for i in range(0,len(details[1])):
        details[1][i] = int(details[1][i])
    details[2] = int(details[2])
    new_process = Process(details[0],details[1],details[2])
    processes.append(new_process)
f.close()

stack = []
new_stack = []
t = 0
deciders = []
decision = False

while decision == False:
    print("\nTime: "+str(t))
    for i in processes:
        if i.activation_time == t:
            i.activate()
    while len(stack) > 0:
        event = stack.pop(0)
        if event == "end":
            decision = True
        else:
            processes[event[0]].signal_received(event[1])
    stack = new_stack
    new_stack = []
    t += 1
print("Diffusion can begin with "+str(deciders[0])+" & "+str(deciders[1])+" (the two deciders) at time "+str(t))
