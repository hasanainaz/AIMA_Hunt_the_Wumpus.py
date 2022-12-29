
## Author: AhmadZuhair.com
# Umm Al Qura University
# Dec 23, 2022

# "Hunt the Wumpus" is a classic video game that was designed by Gregory Yob in 1973 and was one of the TI-99 famous games in 1979. We placed this Python variation on the standard AI problem described by Stuart Russell & Peter Norvig in "Artificial Intelligence: A Modern Approach", 2020, Global, 4th Ed. The player has to move to block [-1,0] from block [0,0] for the Climb action.

# Use the following code for a human player:
"""
import MP2Game
_ = MP2Game.HuntTheWumpusGame()
"""
# Use the following code for a computer player:
"""
import MP2Game
import time
from sympy import ask, Symbol, Equivalent
from sympy import satisfiable, And
cnts = MP2Game.HuntTheWumpusGame(human = False)
# <-------------------------------- Add your initialization code here.
Wumpus_alive = True
while True: 
    sensors = cnts.percept()
    if not sensors:
        Wumpus_alive = True
        # <-------------------------------- Add your reset code here.
        cnts.start()
        continue
    # here is the location of the agent at this time step for simplification
    x = cnts.x
    y = cnts.y
    
    # update your agent's knowledge base 
    # <-------------------------------- here
    
    if (sensors[0] == "Stench") & Wumpus_alive:
        # <-------------------------------- here
    else:
        # <-------------------------------- here
    if sensors[1] == "Breeze":
        # <-------------------------------- here
    else:
        # <-------------------------------- and here
        
    if sensors[2] == "Glitter":
        cnts.action( "Grab" )
    if sensors[4] == "Scream":
        print( "Wumpus Killed" )
    
    # find and shoot the wumpus <-------------------------------- SOLVE this at the end
                    # cnts.go_to( LineSight_x , LineSight_y )
                # cnts.shoot_at( WumpusLocation_x , WumpusLocation_y )
                # continue
    
    # Find the next best move 
    frontier = cnts.frontier()
    frontier.sort(key=lambda k: abs(k[0]-x) + abs(k[1]-y)  )
    destination = [-1,0]
    for d in frontier:
        # <-------------------------------- SOLVE this line first by checking whether the null hypothesis is unsatisfiable using the SymPy library.
            destination = d
            break
    # You can use cnts.action( "TurnRight" ), cnts.action( "TurnLeft" ), and response = cnts.action( "MoveForward" ), OR:
    response = cnts.action( destination ) # just keep this line for simplification.
    if not response:
        break
    time.sleep(0.2)
"""

import random
import tkinter as tk



class HuntTheWumpusGame:
    
    def __init__(self, human = True, gm = 100 , gn = 100 , m = 4 , n = 4):

        self.Action_Time = 100
        self.Reset_Time = 2000
        
        self.gm = gm
        self.gn = gn
        self.m = m
        self.n = n
        self.gmm = gm*m
        self.gnn = gn*n
        
        self.x = 0
        self.y = 0
        self.z = 0
        self.picked = False
        self.shot = 1
        self.gameover = 1

        self.hidden = None
        self.states = None
        
        self.Scream = None
        self.Bump = None
        
        self.window = tk.Tk()
        self.window.title('Hunt the Wumpus')
        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id()))
        self.window_closed = False
        self.window.protocol("WM_DELETE_WINDOW", self.window_close )

        

        


        
        
        self.canvas = tk.Canvas(self.window, width=gm*m*2, height=gn*n)


        self.pause = self.canvas.create_rectangle(0, 0, gm*m*2, gn*n, fill="#efcbb8", outline="#efcbb8",)
        # self.pause2 = self.PlaceWumpusAt(gm*(m-1),gn*(0.2),sx=0.8,sy=0.8,color="white")
        self.pause2 = self.PlaceWumpusAt(gm*m*1.5,gn*n/2,sx=2,sy=2,color="white")

        
        self.canvas.pack()
        
        self.PlayerName = "Agent"
        self.PlayerMessage = "(Waiting for Your Agent's Input)"
        if human == True:
            self.PlayerName = "You"
            self.PlayerMessage = "(Click Anywhere to Continue)"

        
        self.canvas.create_text(gm*m, gn*0.5, text="Hunt the Wumpus", fill="black", font=('"Times New Roman" 20 bold'))
        self.canvas.create_text(gm*m, gn*0.5+gn*(n-1)/2, text="Goal: Find the piece, hunt the wumpus, and return. You have only one shot per map.\n\nControls:\nUp -> MoveForward\nLeft/Right -> TurnLeft/Right\nDown -> Grab\nSpace.\n\n\n\n"+self.PlayerMessage, fill="black", font=('"Times New Roman" 15'))
        
        

        if human == True:
            self.Action_Time = 0
            self.Reset_Time = 0
            self.window.bind("<Button-1>", self.reset )
            self.window.bind("<Button-2>", self.goto )
            self.window.bind("<Key>", self.key_input )
            self.window.mainloop()
        
        
        
    def reset(self, e):

        self.Visited = []
        self.hidden = []
        self.states = []
        for i in range(self.m):
            self.Visited.append([])
            self.hidden.append([])
            self.states.append([])
            for j in range(self.n):
                self.Visited[i].append([0,])
                self.hidden[i].append(set([]))
                self.states[i].append(set([]))

        w = random.randint(1,self.m*self.n-1)
        g = random.randint(1,self.m*self.n-1)
        # print(w,g)
        for i in range(self.m):
            for j in range(self.n):
                if (i == 0 and j == 0):
                    pass
                else:
                    if g == (i+j*self.m):
                        self.Visited[i][j].append(5)
                        self.hidden[i][j].add(5)
                    if random.randint(0,5) < 1:
                        self.Visited[i][j].append(3)
                        self.hidden[i][j].add(3)
                        self.adjacent(i,j,4)
                    if w == (i+j*self.m):
                        self.Visited[i][j].append(1)
                        self.hidden[i][j].add(1)
                        self.adjacent(i,j,2)


        self.x = 0
        self.y = 0
        self.z = 0
        self.picked = False
        self.shot = 1
        self.gameover = 0

        self.canvas.delete("all")

        self.pause = self.canvas.create_oval(0, 0, self.gm*self.m, self.gn*self.n, fill="#efe9d9", outline="#efe9d9",)


        self.wumpus = []
        self.pit = []
        self.gold = []
        

        # right panel
        self.canvas.create_rectangle(self.gm*self.m, 0, self.gm*self.m*2, self.gn*self.n, fill="#c9bfc9", outline="#c9bfc9",)




        for i in range(self.m):
            for j in range(self.n):
                self.canvas.create_rectangle(self.gm*(i), self.gn*(self.n-j-1), self.gm*(i+1), self.gn*(self.n-j), fill="#FFFFFF", outline="#000000",)

                if 4 in self.Visited[i][j]:
                    self.canvas.create_oval(self.gm*(i+0.1), self.gn*(self.n-j-1*0.1), self.gm*(i+1*0.9), self.gn*(self.n*0.9-j), fill="#3f9eb5", outline="#3f9eb5",)
                if 2 in self.Visited[i][j]:
                    self.canvas.create_oval(self.gm*(i+0.2), self.gn*(self.n-j-1*0.15), self.gm*(i+1*0.8), self.gn*(self.n-0.4-j), fill="#d3223e", outline="#d3223e",)

                if 3 in self.Visited[i][j]:
                    self.pit.append( [i,j] )
                    self.canvas.create_rectangle(self.gm*(i), self.gn*(self.n-j-1), self.gm*(i+1), self.gn*(self.n-j), fill="#3f9eb5", outline="#3f9eb5",)
                if 1 in self.Visited[i][j]:
                    k = self.PlaceWumpusAt(self.gm*(i), self.gn*(self.n-j-1.1))
                    self.wumpus.append( [i,j,k] )

                if 5 in self.Visited[i][j]:
                    k = self.canvas.create_oval(self.gm*(i+0.4), self.gn*(self.n-j-1*0.05), self.gm*(i+1*0.6), self.gn*(self.n-0.2-j), fill="#f6ff00", outline="#000000",)
                    self.gold.append( [i,j,k] )

                # the tiles 
                self.Visited[i][j] = self.canvas.create_rectangle(self.gm*(i), self.gn*(self.n-j-1), self.gm*(i+1), self.gn*(self.n-j), fill="#d6cfc3", outline="#d6cfc3",)


        self.agent = self.canvas.create_oval(self.gm*0.2, self.gn*(self.n-self.y-1*0.2), self.gm*.8, self.gn*(self.n*0.8-self.y), fill="#de752f", outline="#de752f",)
        self.arrow = self.canvas.create_oval(self.gm*0.5, self.gn*(self.n-self.y-1+0.3), self.gm*.9, self.gn*(self.n-self.y-0.3) , fill="#de752f", outline="#de752f",)

        # enterance
        self.canvas.create_rectangle(self.gm*0.1, self.gn*(self.n-self.y-1*0.2), self.gm*.3, self.gn*(self.n-0.8-self.y), fill="#51b831", outline="#51b831",)
        self.canvas.create_rectangle(0, self.gn*(self.n-self.y-1*0.22), self.gm*.2, self.gn*(self.n-self.y-0.78), fill="#51b831", outline="#51b831",)        
        
        self.canvas.move(self.Visited[self.x][self.y],self.gm*self.m,0)
        self.canvas.itemconfigure( self.Visited[self.x][self.y] , fill = "#c6c9bf" )
        self.Visited[self.x][self.y] = self.canvas.create_text(self.gm*(self.m+self.x+0.5), self.gn*(self.n-self.y-0.5))

        e.keysym = "Start"
        self.key_input(e)
        self.window.after( self.Reset_Time )

    def PlaceWumpusAt( self, lx , ly , sx=1. , sy=1. , color = "#d3223e" ):
        WumpusImage = [40,25,5,70,15,90,10,100,15,100,20,95,25,100,30,100,15,70,30,50,30,70,30,70,30,80,40,90,60,90,70,80,70,70,60,85,60,75,57,75,57,85,54,85,54,75,52,75,52,85,48,85,48,75,46,75,46,85,43,85,43,75,40,75,40,85,30,70,30,70,33,70,40,60,40,70,43,70,43,60,46,60,46,40,43,40,35,50,40,50,40,45,49,40,46,40,46,70,48,70,48,60,52,60,52,70,54,70,54,40,51,40,60,45,60,50,65,50,57,40,54,40,54,60,57,60,57,70,60,70,60,60,67,70,70,70,70,80,70,70,70,50,85,70,70,100,75,100,80,95,85,100,90,100,85,90,95,70,60,25,45,25,]
        WumpusImage2 = []
        for i in range(0, len(WumpusImage), 2):
            WumpusImage2.append( WumpusImage[i]*sx+lx )
            WumpusImage2.append( WumpusImage[i+1]*sy+ly )
        return self.canvas.create_polygon( WumpusImage2,  fill=color, outline=color,)

    def adjacent(self,i,j,a):
        if i > 0:
            self.Visited[i-1][j].append(a)
            self.hidden[i-1][j].add(a)
        if i < (self.m-1):
            self.Visited[i+1][j].append(a)
            self.hidden[i+1][j].add(a)
        if j > 0:
            self.Visited[i][j-1].append(a)
            self.hidden[i][j-1].add(a)
        if j < (self.n-1):
            self.Visited[i][j+1].append(a)
            self.hidden[i][j+1].add(a)

    def window_close(self):
        self.window.destroy()
        self.window_closed = True
        
        


    def update_screen(self):

        if self.canvas.coords(self.Visited[self.x][self.y])[0] < self.gm*self.m :
            self.canvas.move(self.Visited[self.x][self.y],self.gm*self.m,0)
            self.canvas.itemconfigure( self.Visited[self.x][self.y] , fill = "#c6c9bf" )
            self.Visited[self.x][self.y] = self.canvas.create_text(self.gm*(self.m+self.x+0.5), self.gn*(self.n-self.y-0.5))
            

        for p in self.pit:
            if (self.x == p[0] and self.y == p[1] ):
                self.gameover = 1
        for p in self.wumpus:
            if (self.x == p[0] and self.y == p[1] ):
                self.gameover = 2

        if self.gameover>0:
            self.canvas.delete(self.agent)
            self.canvas.delete(self.arrow)
            # self.x = -1
            # self.y = -1

            for i in range(self.m):
                for j in range(self.n):
                    self.canvas.delete(self.Visited[i][j])
            # canvas.delete("all")
            if self.gameover == 2:
                # canvas.configure(bg='#ff4000')
                self.pause = self.canvas.create_rectangle(self.gm*self.m, 0, self.gm*self.m*2, self.gn*self.n, fill="#d3223e", outline="#d3223e",)
                # self.pause2 = self.PlaceWumpusAt(-self.gm*self.m/2, -self.gn*self.n,sx=9,sy=9,color="white")
                self.canvas.create_text(self.gm*self.m*1.5, self.gn*self.n/4, text=self.PlayerName+" Lost!", fill="black", font=('"Times New Roman" 20 bold'))
                self.canvas.create_text(self.gm*self.m*1.5, self.gn*self.n/2, text="Eaten by the Wumpus\n\n\n"+self.PlayerMessage, fill="black", font=('"Times New Roman" 15'))

            elif self.gameover == 1:
                # canvas.configure(bg='#0033ff')
                self.pause = self.canvas.create_rectangle(self.gm*self.m, 0, self.gm*self.m*2, self.gn*self.n, fill="#3f9eb5", outline="#3f9eb5",)
                self.canvas.create_text(self.gm*self.m*1.5, self.gn*self.n/4, text=self.PlayerName+" Lost!", fill="black", font=('"Times New Roman" 20 bold'))
                self.canvas.create_text(self.gm*self.m*1.5, self.gn*self.n/2, text="Fell in a Pit\n\n\n"+self.PlayerMessage, fill="black", font=('"Times New Roman" 15'))
            


    def key_input(self,e):

        
        self.Scream = None
        self.Bump = None
        
        if self.gameover > 0 and e.keysym == "Down":
            self.canvas.delete(self.pause)
            self.canvas.delete(self.pause2)

        if self.gameover > 0 :
            return

        if e.keysym == "Left":
            self.z = self.z + 1
            if self.z == 4:
                self.z = 0
            if self.z == 3:
                self.canvas.move(self.arrow, self.gm*0.2, self.gn*0.2)
            if self.z == 0:
                self.canvas.move(self.arrow, self.gm*0.2, -self.gn*0.2)
            if self.z == 1:
                self.canvas.move(self.arrow, -self.gm*0.2, -self.gn*0.2)
            if self.z == 2:
                self.canvas.move(self.arrow, -self.gm*0.2, self.gn*0.2)
        if e.keysym == "Right":
            self.z = self.z - 1
            if self.z == -1:
                self.z = 3
            if self.z == 0:
                self.canvas.move(self.arrow, self.gm*0.2, self.gn*0.2)
            if self.z == 1:
                self.canvas.move(self.arrow, self.gm*0.2, -self.gn*0.2)
            if self.z == 2:
                self.canvas.move(self.arrow, -self.gm*0.2, -self.gn*0.2)
            if self.z == 3:
                self.canvas.move(self.arrow, -self.gm*0.2, self.gn*0.2)
        if e.keysym == "Up":
            
            self.states[self.x][self.y].discard( self.PlayerName )
            self.canvas.itemconfigure( self.Visited[self.x][self.y] , text= f"[{self.x},{self.y}]\n" + "\n".join( str(a) for a in self.states[self.x][self.y] ) )

            if self.z == 2 and self.x == 0 and self.y == 0:
                for i in range(self.m):
                    for j in range(self.n):
                        self.canvas.delete(self.Visited[i][j])

                if self.picked == True:
                    self.pause = self.canvas.create_rectangle(self.gm*self.m, 0, self.gm*self.m*2, self.gn*self.n, fill="#c1d999", outline="#c1d999",)
                    self.canvas.create_text(self.gm*self.m*1.5, self.gn*self.n/4, text=self.PlayerName+" Won!", fill="black", font=('"Times New Roman" 20 bold'))
                    self.canvas.create_text(self.gm*self.m*1.5, self.gn*self.n/2, text="Safely Returned\n\n\n"+self.PlayerMessage, fill="black", font=('"Times New Roman" 15'))

                if self.picked == False:
                    self.pause = self.canvas.create_rectangle(self.gm*self.m, 0, self.gm*self.m*2, self.gn*self.n, fill="#f6d2b9", outline="#f6d2b9",)
                    self.canvas.create_text(self.gm*self.m*1.5, self.gn*self.n/4, text=self.PlayerName+" Fled!", fill="black", font=('"Times New Roman" 20 bold'))
                    self.canvas.create_text(self.gm*self.m*1.5, self.gn*self.n/2, text="No Harm Occoured\n\n\n"+self.PlayerMessage, fill="black", font=('"Times New Roman" 15'))

                self.canvas.delete(self.agent)
                self.canvas.delete(self.arrow)
                # self.x = -1
                # self.y = -1
                self.gameover = 3

            if self.z==1 and self.y + 1 < self.n: # up
                self.y += 1
                self.canvas.move(self.agent, 0, -self.gn)
                self.canvas.move(self.arrow, 0, -self.gn)
                self.Bump = None
                self.update_screen()
            elif self.z==0 and self.x + 1 < self.m: # right
                self.x += 1
                self.canvas.move(self.agent, self.gm, 0)
                self.canvas.move(self.arrow, self.gm, 0)
                self.Bump = None
                self.update_screen()
            elif self.z==2 and self.x - 1 >= 0: # left
                self.x -= 1
                self.canvas.move(self.agent, -self.gm, 0)
                self.canvas.move(self.arrow, -self.gm, 0)
                self.Bump = None
                self.update_screen()
            elif self.z == 3 and self.y - 1 >= 0: # down
                self.y -= 1
                self.canvas.move(self.agent, 0, self.gn)
                self.canvas.move(self.arrow, 0, self.gn)
                self.Bump = None
                self.update_screen()
            else:
                self.Bump = "Bump"
                
        if e.keysym == "Up" or e.keysym == "Start":
            
            self.states[self.x][self.y].update([self.PlayerName,"Safe"])
            
            # print( self.Visited[self.x][self.y] )
            
            if 2 in self.hidden[self.x][self.y]:
                self.states[self.x][self.y].add("Stench")
                self.states[self.x][self.y].discard("Safe")
            if 4 in self.hidden[self.x][self.y]:
                self.states[self.x][self.y].add("Breeze")
                self.states[self.x][self.y].discard("Safe")
            if 5 in self.hidden[self.x][self.y]:
                self.states[self.x][self.y].add("Glitter")
                
            if 1 in self.hidden[self.x][self.y]:
                self.states[self.x][self.y].add("Wumpus")
                self.states[self.x][self.y].discard("Safe")
            if 3 in self.hidden[self.x][self.y]:
                self.states[self.x][self.y].add("Pit")
                self.states[self.x][self.y].discard("Safe")
            
            self.canvas.itemconfigure( self.Visited[self.x][self.y] , text= f"[{self.x},{self.y}]\n" + "\n".join( str(a) for a in self.states[self.x][self.y] ) )
                
        if e.char == ' ':
            if self.shot > 0:
                self.shot -= 1
                for p in range(len(self.wumpus)):
                    if self.z == 0:
                        if self.wumpus[p][0] > self.x and self.wumpus[p][1] == self.y:
                            # self.canvas.delete(self.Visited[self.wumpus[p][0]][self.wumpus[p][1]])
                            self.canvas.delete(self.wumpus[p][2])
                            self.wumpus[p] = [-1,-1,-1]
                            self.Scream = "Scream"
                    elif self.z == 2:
                        if self.wumpus[p][0] < self.x and self.wumpus[p][1] == self.y:
                            # self.canvas.delete(self.Visited[self.wumpus[p][0]][self.wumpus[p][1]])
                            self.canvas.delete(self.wumpus[p][2])
                            self.wumpus[p] = [-1,-1,-1]
                            self.Scream = "Scream"
                    elif self.z == 1:
                        if self.wumpus[p][1] > self.y and self.wumpus[p][0] == self.x:
                            # self.canvas.delete(self.Visited[self.wumpus[p][0]][self.wumpus[p][1]])
                            self.canvas.delete(self.wumpus[p][2])
                            self.wumpus[p] = [-1,-1,-1]
                            self.Scream = "Scream"
                    elif self.z == 3:
                        if self.wumpus[p][1] < self.y and self.wumpus[p][0] == self.x:
                            # self.canvas.delete(self.Visited[self.wumpus[p][0]][self.wumpus[p][1]])
                            self.canvas.delete(self.wumpus[p][2])
                            self.wumpus[p] = [-1,-1,-1]
                            self.Scream = "Scream"
                            
                s = self.canvas.create_rectangle(0, 0, self.gm*self.m, self.gn*self.n, fill="#000000", outline="#000000",)
                self.window.update()
                self.window.after(5, self.canvas.move(s,-self.gm*self.m,0) )
                self.window.update()
                self.window.after(10, self.canvas.move(s,self.gm*self.m,0) )
                self.window.update()
                self.window.after(20, self.canvas.delete(s) )
                self.window.update()
                            
        if e.keysym == "Down":
            for p in self.gold:
                if p[0] == self.x and p[1] == self.y:
                    self.picked = True
                    self.canvas.delete(p[2])


    
    
    def goto( self, e ):
        
        # get goal cords from the right click mouse
        gx = int( e.x / self.gm )
        gy = int( self.n - e.y / self.gn )
        
        self.go_to(gx,gy)
        
    def go_to(self, gx, gy ):
        
        if (gx,gy) == (self.x,self.y):
            print( "No path needed" )
            return False
        
        parents = { } # dictionary of visited nodes
        frontier = [ (self.x,self.y) ]
        
        # find the state space
        allowed = set( [ (gx,gy) ] )
        for i in range(self.m):
            for j in range(self.n):
                if len( self.states[i][j] ) > 0:
                    allowed.add( (i,j) )
                
        path = [] 
        for iter in range( 100 ):
            
            if len( frontier ) == 0 :
                print( "No valid path found" )
                return False
            s = frontier.pop(0)
            
            if s == (gx,gy):
                # print( "Valid path found" )
                for iter2 in range( 100 ):
                    p = parents[s]
                    path.append( [p,s] )
                    s = p
                    if s == (self.x,self.y):
                        break
                path.reverse()
                break
            
            # find candidates
            ss = set( [ ( s[0] + 1 , s[1] ), ( s[0] - 1 , s[1] ), ( s[0] , s[1] + 1 ), ( s[0] , s[1] - 1 ) ] )
            # filter to find allowed moves
            ss = ss.intersection( allowed )
            # add allowed nodes to visited
            for i in ss:
                if i not in parents.keys():
                    parents[i] = s
                    frontier.append( i )
        
        
        # find the directions
        sz = self.z # current direction 
        
        moves = []
        actions = []
        for i in path:
            
            RotateLeft = 0
            
            if i[1][0] - i[0][0] > 0 :
                moves.append( "right" )
                while sz != 0:
                    RotateLeft += 1
                    sz = (sz + 1) % 4
            elif i[1][0] - i[0][0] < 0 :
                moves.append( "left" )
                while sz != 2:
                    RotateLeft += 1
                    sz = (sz + 1) % 4
            elif i[1][1] - i[0][1] > 0 :
                moves.append( "up" )
                while sz != 1:
                    RotateLeft += 1
                    sz = (sz + 1) % 4
            elif i[1][1] - i[0][1] < 0 :
                moves.append( "down" )
                while sz != 3:
                    RotateLeft += 1
                    sz = (sz + 1) % 4
            
            # find the sequence of actions
            if RotateLeft == 3:
                actions.append("TurnRight")
            elif RotateLeft == 2:
                actions.extend(["TurnRight","TurnRight"])
            elif RotateLeft == 1:
                actions.append("TurnLeft")
            actions.append("MoveForward")
            
        for i in actions:
            # print(i)
            self.action(i)
            # time.sleep(1)
        
    def shoot_at(self,a,b):
        
        x = self.x
        y = self.y
        sz = self.z # current direction 
        moves = []
        actions = []

        RotateLeft = 0

        if a - x > 0 :
            moves.append( "right" )
            while sz != 0:
                RotateLeft += 1
                sz = (sz + 1) % 4
        elif a - x < 0 :
            moves.append( "left" )
            while sz != 2:
                RotateLeft += 1
                sz = (sz + 1) % 4
        elif b - y > 0 :
            moves.append( "up" )
            while sz != 1:
                RotateLeft += 1
                sz = (sz + 1) % 4
        elif b - y < 0 :
            moves.append( "down" )
            while sz != 3:
                RotateLeft += 1
                sz = (sz + 1) % 4

        # find the sequence of actions
        if RotateLeft == 3:
            actions.append("TurnRight")
        elif RotateLeft == 2:
            actions.extend(["TurnRight","TurnRight"])
        elif RotateLeft == 1:
            actions.append("TurnLeft")
        actions.append("Shoot")

        for i in actions:
            # print(i)
            self.action(i)
            # print( "shot" )
            # time.sleep(1)
            
        

    def percept(self):
        
        if (self.gameover > 0) or (self.states == None):
            self.window.update()
            return False
        
        current = self.states[self.x][self.y]
        
        p = []
        if "Stench" in current:
            p.append("Stench")
        else:
            p.append(None)
        if "Breeze" in current:
            p.append("Breeze")
        else:
            p.append(None)
        if "Glitter" in current:
            p.append("Glitter")
        else:
            p.append(None)

        p.append( self.Bump )
        p.append( self.Scream )
        return p
    
    def frontier(self):

        # find reachable but unreached states
        frontier = []
        if self.states != None:
            for i in range(self.m):
                for j in range(self.n):
                    if self.states[i][j] == set():
                        if ( i>0 and self.states[i-1][j] != set() ) or ( i<self.m-1 and self.states[i+1][j] != set() ) or (j>0 and self.states[i][j-1] != set() ) or (j<self.n-1 and self.states[i][j+1] != set() ):
                            frontier.append( [i,j] )
        
        return frontier
    

    def action(self,a):
        self.window.after( self.Action_Time )
        
        if self.window_closed == True:
            return False
        
        if self.states == None:
            self.window.update()
            return True
        
        if isinstance(a,list) or a == None :
            self.go_to(a[0],a[1])
        
        if a == "MoveForward":
            e = type('', (), {})()
            e.keysym = "Up"
            e.char = None
            self.key_input(e)

        if a == "TurnRight":
            e = type('', (), {})()
            e.keysym = "Right"
            e.char = None
            self.key_input(e)

        if a == "TurnLeft":
            e = type('', (), {})()
            e.keysym = "Left"
            e.char = None
            self.key_input(e)

        if a == "Grab":
            e = type('', (), {})()
            e.keysym = "Down"
            e.char = None
            self.key_input(e)

        if a == "Shoot":
            e = type('', (), {})()
            e.keysym = None
            e.char = ' '
            self.key_input(e)


        if a == "restart":
            e = type('', (), {})()
            e.keysym = "Start"
            e.char = None
            # e.keysym = "Down"
            self.reset(e)
            
        self.window.update()
        return True
    
    
    def start(self):
        e = type('', (), {})()
        e.keysym = "Start"
        e.char = None
        # e.keysym = "Down"
        self.reset(e)
        self.window.update()
        return True