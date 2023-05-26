from tkinter import *
from pygame import *
import pygame as py 
from copy import *
from time import * 

initial_state=[[1,2,3],[8,6,0],[7,5,4]]
final_state = [[1,2,3],[8,0,4],[7,6,5]]

def isGoalState(s): 
  return s==final_state
 
def emptySquarePosition(s): 
  for i in range(3): 
    if 0 in s[i]: 
      return s[i].index(0),i

def numberPosition(s,n):
     for i in range(3): 
        if n in s[i]: 
          return s[i].index(n),i

def number(s, x, y):
   return s[y][x]
 
def swap(s, c1, c2): 
  y=s[c1[1]][c1[0]] 
  s[c1[1]][c1[0]]=s[c2[1]][c2[0]]
  s[c2[1]][c2[0]]=y
 
def transitions(s):
  transitions=[]  
  i,j=emptySquarePosition(s)
  if i-1>=0: 
    t=deepcopy(s)
    swap(t,(i,j),(i-1,j))
    transitions.append(t) 
  if i+1<=2:  
    t=deepcopy(s)
    swap(t,(i,j),(i+1,j))
    transitions.append(t)
  if j-1>=0:  
    t=deepcopy(s)
    swap(t,(i,j),(i,j-1))
    transitions.append(t)
  if j+1<=2: 
    t=deepcopy(s)
    swap(t,(i,j),(i,j+1))
    transitions.append(t)
  return transitions 

def taquin_print(s): 
  print("+",end="") 
  for i in range(3): 
    for j in range(3): 
      print("-",end="")
    print("+",end="")  
  print()
  for i in range(3):
    print("|",end="") 
    for j in range(3): 
      print("",s[i][j],end=" |") 
    print("\n+",end="")
    for j in range(3): 
      for  k in range(3): 
        print("-",end="")
      print("+",end="")
    print()

def play_music_new_window():
    mixer.init()
    sound_file ="X2Download (mp3cut.net).mp3"
    mixer.music.load(sound_file)
    mixer.music.play(loops=-1)

cell_size = 120
canvas_width = cell_size * 3
canvas_height = cell_size * 3

def open_new_window():
    def new_window_on_close():
        mixer.music.stop()
        new_window.destroy()
    def play_music_window():
        mixer.init()
        sound_file ="song (mp3cut.net) (1).mp3"
        mixer.music.load(sound_file)
        mixer.music.play(loops=-1)
    def open_DFS_window():
        def DFS_window_on_close():
            mixer.music.stop()
            DFS_window.destroy()
        def back_to_sec_window():
            mixer.music.stop()
            DFS_window.destroy()
            new_window.deiconify()
            new_window.after(0, play_music_new_window)
            new_window.protocol("WM_DELETE_WINDOW", new_window_on_close)
      
        def animate_transition(state1, state2):
            py.init()
            clock = py.time.Clock() 
            t=0
            for i in range(3):
                for j in range(3): 
                    if state1[i][j] != state2[i][j]:
                        x0 = j * cell_size
                        y0 = i * cell_size
                        if not state1[i][j]:
                            canvas.delete(text[state2[i][j]-1])
                            text[state2[i][j]-1]=canvas.create_text(x0 + cell_size/2, y0 + cell_size/2, text=str(state2[i][j]), font=("Bungee Shade", 20, "bold"), fill="purple")
                            canvas.update()
                            clock.tick(1000)
                            sleep(2) 
                        else:
                            canvas.delete(text[state1[i][j]-1]) 
                            x,y=emptySquarePosition(state1)
                            x0 = x * cell_size
                            y0 = y * cell_size    
                            text[state1[i][j]-1] = canvas.create_text(x0 + cell_size/2, y0 + cell_size/2, text=str(state1[i][j]), font=("Bungee Shade", 20, "bold"),fill="purple", tags=str(state1[i][j]))
                            canvas.update()
                            clock.tick(1000)
                            sleep(2)
                        t=1
                        break
                if t:
                    break
        text=[]
        for i in range(9):
            text.append(0)
        def DFS():
            py.init()
            clock = py.time.Clock() 
            start_time = time()
            free_nodes = [initial_state]
            generated_nodes = []
            closed_nodes = []
            success = False 
            pr_state=initial_state
            t=0 
            while(len(free_nodes) != 0):
                s = free_nodes.pop()
                closed_nodes.append(s)
                if not t:
                         if s==initial_state:
                            label = Label(DFS_window, text="first state!", font=("Bungee Shade", 20, "bold"), fg="white", bg="purple")
                            label.pack()
                            label.place(x=120, y=400)
                            DFS_window.after(3000, label.destroy)  
                         else:
                            label = Label(DFS_window, text="Backward!", font=("Bungee Shade", 20, "bold"), fg="white", bg="purple")
                            label.pack() 
                            label.place(x=120, y=400)
                            DFS_window.after(3000, label.destroy)
                         canvas.delete("all")
                         for i in range(3):
                            for j in range(3):
                                x0 = j * cell_size
                                y0 = i * cell_size
                                x1 = x0 + cell_size
                                y1 = y0 + cell_size
                                canvas.create_rectangle(x0, y0, x1, y1, fill="pink", outline="white", width=4)
                                if s[i][j] != 0:
                                    text[s[i][j]-1] = canvas.create_text(x0 + cell_size/2, y0 + cell_size/2, text=str(s[i][j]), font=("Bungee Shade", 20, "bold"),fill="purple")  
                         canvas.update()
                         clock.tick(1000)
                         sleep(3) 
                else: 
                    animate_transition(pr_state, s)
                if (isGoalState(s)):
                    mixer.music.stop()
                    success = True
                    end_time = time()
                    total_time = end_time - start_time
                    total_time = "{:.3f}".format(total_time)
                    final_message = "Final State Reached!\n" + "Closed Nodes Number = " + str(len(closed_nodes)) + "\nGenerated Nodes Number = " + str(len(generated_nodes)) + "\nExecution time = " + str(total_time) + 's'      
                    final_label = Label(DFS_window, text=final_message, font=("Lucida Fax", 12, "bold"), fg="purple", bg="pink", relief="groove", borderwidth=3) 
                    final_label.pack()
                    final_label.place(x=120,y=400) 
                    break
                pr_state=s
                t=0 
                for i in transitions(s):
                    if i not in generated_nodes and i != initial_state: 
                        free_nodes.append(i)
                        generated_nodes.append(i) 
                        t=1
            if not success:
              end_time = time()
              total_time = end_time - start_time
              total_time = "{:.3f}".format(total_time)
              mixer.music.stop()
              final_message = "HARD LUCK!\n" + "Closed Nodes Number = " + str(len(closed_nodes)) + "\nGenerated Nodes Number = " + str(len(generated_nodes)) + "\nExecution time = " + str(total_time) + 's'     
              final_label = Label(DFS_window, text=final_message, font=("Lucida Fax", 12, "bold"), fg="purple", bg="pink", relief="groove", borderwidth = 3)
              final_label.pack()
              final_label.place(x=120,y=400) 
        mixer.music.stop()
        DFS_window=Toplevel(new_window)
        DFS_window.protocol("WM_DELETE_WINDOW", new_window.destroy)
        new_window.withdraw()
        DFS_window.geometry("500x500")
        DFS_window.iconbitmap("puzzle.ico")
        DFS_window.title('DFS')
        DFS_window.after(0, play_music_window)
        DFS_window.protocol("WM_DELETE_WINDOW", new_window_on_close)
        DFS_window.configure(background="purple")
        DFS_back_button = Button(DFS_window, text="Back", command=back_to_sec_window, font=("Bungee Shade",12, "bold"), fg="purple", bg="white", relief="groove", borderwidth=5, width=5, height=1)
        DFS_back_button.place(x=397, y=410)
        canvas = Canvas(DFS_window, width=canvas_width, height=canvas_height, bg="pink")
        canvas.pack(side=TOP, padx=10, pady=10) 
        DFS() 
        DFS_window.mainloop()
    def open_BFS_window():
        def BFS_window_on_close():
            mixer.music.stop()
            BFS_window.destroy()
        def back_to_sec_window():
            mixer.music.stop()
            BFS_window.destroy()
            new_window.deiconify()
            new_window.after(0, play_music_new_window)
            new_window.protocol("WM_DELETE_WINDOW", new_window_on_close)
        text=[]
        for i in range(9):
            text.append(0)
        def BFS():
            py.init()
            clock = py.time.Clock()
            start_time = time()
            free_nodes = [initial_state]
            generated_nodes = []
            closed_nodes = []
            success = False 
            while(len(free_nodes) != 0):
              s = free_nodes.pop(0)
              closed_nodes.append(s)
              if s==initial_state:
                label = Label(BFS_window, text="first state!", font=("Bungee Shade", 20, "bold"), fg="white", bg="purple")
                label.pack()
                label.place(x=120, y=400)
                BFS_window.after(3000, label.destroy)  
              for i in range(3):
                for j in range(3):
                  x0 = j * cell_size
                  y0 = i * cell_size
                  x1 = x0 + cell_size
                  y1 = y0 + cell_size
                  canvas.create_rectangle(x0, y0, x1, y1, fill="pink", outline="white", width=4)
                  if s[i][j] != 0:
                      text[s[i][j]-1] = canvas.create_text(x0 + cell_size/2, y0 + cell_size/2, text=str(s[i][j]), font=("Bungee Shade", 20, "bold"),fill="purple") 
              canvas.update()
              clock.tick(1000) 
              sleep(3) 
              if (isGoalState(s)):
                  mixer.music.stop()
                  success = True
                  end_time = time()
                  total_time = end_time - start_time
                  total_time = "{:.3f}".format(total_time)
                  final_message = "Final State Reached!\n" + "Closed Nodes Number = " + str(len(closed_nodes)) + "\nGenerated Nodes Number = " + str(len(generated_nodes)) + "\nExecution time = " + str(total_time) + 's'      
                  final_label = Label(BFS_window, text=final_message, font=("Lucida Fax", 12, "bold"), fg="purple", bg="pink", relief="groove", borderwidth=3) 
                  final_label.pack()
                  final_label.place(x=120,y=400) 
                  break
              for i in transitions(s):
                if i not in generated_nodes and i != initial_state: 
                  free_nodes.append(i)
                  generated_nodes.append(i)
            if not success:
              end_time = time()
              total_time = end_time - start_time
              total_time = "{:.3f}".format(total_time)
              mixer.music.stop()
              final_message = "HARD LUCK!\n" + "Closed Nodes Number = " + str(len(closed_nodes)) + "\nGenerated Nodes Number = " + str(len(generated_nodes)) + "\nExecution time = " + str(total_time) + 's'     
              final_label = Label(BFS_window, text=final_message, font=("Lucida Fax", 12, "bold"), fg="purple", bg="pink", relief="groove", borderwidth = 3)
              final_label.pack()
              final_label.place(x=120,y=400) 
        mixer.music.stop()
        BFS_window=Toplevel(new_window)
        BFS_window.protocol("WM_DELETE_WINDOW", new_window.destroy)
        new_window.withdraw()
        BFS_window.geometry("500x500")
        BFS_window.iconbitmap("puzzle.ico")
        BFS_window.title('BFS')
        BFS_window.after(0, play_music_window)
        BFS_window.protocol("WM_DELETE_WINDOW", new_window_on_close)
        BFS_window.configure(background="purple")
        BFS_back_button = Button(BFS_window, text="Back", command=back_to_sec_window, font=("Bungee Shade",12, "bold"), fg="purple", bg="white", relief="groove", borderwidth=5, width=5, height=1)
        BFS_back_button.place(x=397, y=410)
        canvas = Canvas(BFS_window, width=canvas_width, height=canvas_height, bg="pink")
        canvas.pack(side=TOP, padx=10, pady=10) 
        BFS() 
        BFS_window.mainloop()
    def open_LDFS_window():
        def LDFS_window_on_close():
            mixer.music.stop()
            LDFS_window.destroy()
        def back_to_sec_window():
            mixer.music.stop()
            LDFS_window.destroy()
            new_window.deiconify()
            new_window.after(0, play_music_new_window)
            new_window.protocol("WM_DELETE_WINDOW", new_window_on_close)
        
        def LDFS(L):
            def animate_transition(state1, state2):
              py.init()
              clock = py.time.Clock() 
              t=0
              for i in range(3):
                  for j in range(3): 
                      if state1[i][j] != state2[i][j]:
                          x0 = j * cell_size
                          y0 = i * cell_size
                          if not state1[i][j]:
                              canvas.delete(text[state2[i][j]-1])
                              text[state2[i][j]-1]=canvas.create_text(x0 + cell_size/2, y0 + cell_size/2, text=str(state2[i][j]), font=("Bungee Shade", 20, "bold"), fill="purple")
                              canvas.update()
                              clock.tick(1000)
                              sleep(2) 
                          else:
                              canvas.delete(text[state1[i][j]-1]) 
                              x,y=emptySquarePosition(state1)
                              x0 = x * cell_size
                              y0 = y * cell_size    
                              text[state1[i][j]-1] = canvas.create_text(x0 + cell_size/2, y0 + cell_size/2, text=str(state1[i][j]), font=("Bungee Shade", 20, "bold"),fill="purple", tags=str(state1[i][j]))
                              canvas.update()
                              clock.tick(1000)
                              sleep(2)
                          t=1
                          break
                  if t:
                     break
            text=[]
            for i in range(9):
              text.append(0)
            canvas = Canvas(LDFS_window, width=canvas_width, height=canvas_height, bg="pink")
            canvas.pack(side=TOP, padx=10, pady=72)
            LDFS_window.after(0, play_music_window)
            py.init()
            clock = py.time.Clock() 
            start_time = time()
            IN = [initial_state, 0] 
            free_nodes = [IN]
            generated_nodes = []
            closed_nodes = []
            success = False 
            pr_state=initial_state
            t=0 
            while(len(free_nodes) != 0):
                s = free_nodes.pop()
                closed_nodes.append(s[0])
                if not t:
                         if s[0]==initial_state:
                            label = Label(LDFS_window, text="first state!", font=("Bungee Shade", 15, "bold"), fg="white", bg="purple")
                            label.pack()
                            label.place(x=140, y=440)
                            LDFS_window.after(3000, label.destroy)  
                         else:
                            label = Label(LDFS_window, text="Backward!", font=("Bungee Shade", 15, "bold"), fg="white", bg="purple")
                            label.pack() 
                            label.place(x=140, y=440)
                            LDFS_window.after(3000, label.destroy)
                         canvas.delete("all")
                         for i in range(3):
                            for j in range(3):
                                x0 = j * cell_size
                                y0 = i * cell_size
                                x1 = x0 + cell_size
                                y1 = y0 + cell_size
                                canvas.create_rectangle(x0, y0, x1, y1, fill="pink", outline="white", width=4)
                                if s[0][i][j] != 0:
                                    text[s[0][i][j]-1] = canvas.create_text(x0 + cell_size/2, y0 + cell_size/2, text=str(s[0][i][j]), font=("Bungee Shade", 20, "bold"),fill="purple")  
                         canvas.update()
                         clock.tick(1000)
                         sleep(3) 
                else: 
                    animate_transition(pr_state, s[0])
                if (isGoalState(s[0])):
                    mixer.music.stop()
                    success = True
                    end_time = time()
                    total_time = end_time - start_time
                    total_time = "{:.3f}".format(total_time)
                    final_message = "Final State Reached!\n" + "Closed Nodes Number = " + str(len(closed_nodes)) + "\nGenerated Nodes Number = " + str(len(generated_nodes)) + "\nExecution time = " + str(total_time) + 's'      
                    final_label = Label(LDFS_window, text=final_message, font=("Lucida Fax", 10, "bold"), fg="purple", bg="pink", relief="groove", borderwidth=3) 
                    final_label.pack()
                    final_label.place(x=130,y=430)
                    LDFS_window.after(7000, final_label.destroy) 
                    LDFS_window.after(3000, canvas.destroy)   
                    break
                pr_state = s[0]
                t=0
                if s[1] < L: 
                  for i in transitions(s[0]):
                      if i not in generated_nodes and i != initial_state: 
                          free_nodes.append([i, s[1] + 1])
                          generated_nodes.append(i) 
                          t=1
            if not success:
              end_time = time()
              total_time = end_time - start_time
              total_time = "{:.3f}".format(total_time)
              mixer.music.stop()
              final_message = "HARD LUCK!\n" + "Closed Nodes Number = " + str(len(closed_nodes)) + "\nGenerated Nodes Number = " + str(len(generated_nodes)) + "\nExecution time = " + str(total_time) + 's'     
              final_label = Label(LDFS_window, text=final_message, font=("Lucida Fax", 10, "bold"), fg="purple", bg="pink", relief="groove", borderwidth = 3)
              final_label.pack()
              final_label.place(x=130,y=430)
              LDFS_window.after(7000, final_label.destroy)
              LDFS_window.after(3000, canvas.destroy)
        mixer.music.stop()
        LDFS_window=Toplevel(new_window)
        LDFS_window.protocol("WM_DELETE_WINDOW", new_window.destroy)
        new_window.withdraw()
        LDFS_window.geometry("500x500")
        LDFS_window.iconbitmap("puzzle.ico")
        LDFS_window.title('Limited DFS')
        LDFS_window.protocol("WM_DELETE_WINDOW", new_window_on_close)
        LDFS_window.configure(background="purple")
        LDFS_back_button = Button(LDFS_window, text="Back", command=back_to_sec_window, font=("Bungee Shade",12, "bold"), fg="purple", bg="white", relief="groove", borderwidth=5, width=5, height=1)
        LDFS_back_button.place(x=422, y=428)
        font_style = ('TkDefaultFont', 15)
        L = Entry(LDFS_window, font = font_style) 
        L.place(x = 50, y = 25)
        limit = -1
        def get_limit():
          limit = int(L.get())
          if limit >= 0:
            LDFS(limit)
        IPbutton = Button(LDFS_window, text="Limit", command=get_limit, font=("Bungee Shade",10, "bold"), fg="purple", bg="white", relief="groove", borderwidth=5, width=8)
        IPbutton.place(x = 350, y = 5)
        LDFS_window.mainloop()
    def open_HS_window():
          def Heuristic_window_on_close():
            mixer.music.stop()
            HS_window.destroy()
          def back_to_sec_window():
            mixer.music.stop()
            HS_window.destroy()
            new_window.deiconify()
            new_window.after(0, play_music_new_window)
            new_window.protocol("WM_DELETE_WINDOW", new_window_on_close)
          text=[]
          for i in range(9):
            text.append(0)
          def HS():
            def g(s):
              n = 0 
              for i in range(3):   
                for  j in range(3):
                  if  s[i][j] != final_state[i][j]: 
                    n += 1  
              return n 
            py.init()
            clock = py.time.Clock()
            start_time = time()
            IN = [initial_state, 0]
            free_nodes = [IN]
            generated_nodes = []
            closed_nodes = []
            success = False  
            while(len(free_nodes) != 0):
              s = free_nodes.pop()
              closed_nodes.append(s[0])
              if s[0]==initial_state:
                label = Label(HS_window, text="first state!", font=("Bungee Shade", 20, "bold"), fg="white", bg="purple")
                label.pack()
                label.place(x=120, y=400)
                HS_window.after(3000, label.destroy)  
              for i in range(3):
                for j in range(3):
                  x0 = j * cell_size
                  y0 = i * cell_size
                  x1 = x0 + cell_size
                  y1 = y0 + cell_size
                  canvas.create_rectangle(x0, y0, x1, y1, fill="pink", outline="white", width=4)
                  if s[0][i][j] != 0:
                      text[s[0][i][j]-1] = canvas.create_text(x0 + cell_size/2, y0 + cell_size/2, text=str(s[0][i][j]), font=("Bungee Shade", 20, "bold"),fill="purple") 
              canvas.update()
              clock.tick(1000) 
              sleep(3) 
              if (isGoalState(s[0])):
                mixer.music.stop()
                success = True
                end_time = time()
                total_time = end_time - start_time
                total_time = "{:.3f}".format(total_time)
                final_message = "Final State Reached!\n" + "Closed Nodes Number = " + str(len(closed_nodes)) + "\nGenerated Nodes Number = " + str(len(generated_nodes)) + "\nExecution time = " + str(total_time) + 's'      
                final_label = Label(HS_window, text=final_message, font=("Lucida Fax", 12, "bold"), fg="purple", bg="pink", relief="groove", borderwidth=3) 
                final_label.pack()
                final_label.place(x=120,y=400) 
                break
              h = []
              for i in transitions(s[0]): 
                if i not in generated_nodes and i != initial_state:
                  h.append([[i, s[1] + 1], g(i) + s[1] + 1])
                  generated_nodes.append(i) 
              h.sort(key=lambda s: s[1])
              for i in h: 
                if i[1] == h[0][1]: 
                  free_nodes.append(i[0]) 
              free_nodes.sort(key=lambda s: s[1])
            if not success:
              end_time = time()
              total_time = end_time - start_time
              total_time = "{:.3f}".format(total_time)
              mixer.music.stop()
              final_message = "HARD LUCK!\n" + "Closed Nodes Number = " + str(len(closed_nodes)) + "\nGenerated Nodes Number = " + str(len(generated_nodes)) + "\nExecution time = " + str(total_time) + 's'     
              final_label = Label(HS_window, text=final_message, font=("Lucida Fax", 12, "bold"), fg="purple", bg="pink", relief="groove", borderwidth = 3)
              final_label.pack()
              final_label.place(x=120,y=400) 
          mixer.music.stop()
          HS_window=Toplevel(new_window)
          HS_window.protocol("WM_DELETE_WINDOW", new_window.destroy)
          new_window.withdraw()
          HS_window.geometry("500x500")
          HS_window.iconbitmap("puzzle.ico")
          HS_window.title('A*')
          HS_window.after(0, play_music_window)
          HS_window.protocol("WM_DELETE_WINDOW", new_window_on_close)
          HS_window.configure(background="purple")
          HS_back_button = Button(HS_window, text="Back", command=back_to_sec_window, font=("Bungee Shade",12, "bold"), fg="purple", bg="white", relief="groove", borderwidth=5, width=5, height=1)
          HS_back_button.place(x=397, y=410)
          canvas = Canvas(HS_window, width=canvas_width, height=canvas_height, bg="pink")
          canvas.pack(side=TOP, padx=10, pady=10) 
          HS() 
          HS_window.mainloop()
    def open_it_DFS_window():
        def it_DFS_window_on_close():
            mixer.music.stop()
            it_DFS_window.destroy()
        def back_to_sec_window():
            mixer.music.stop()
            it_DFS_window.destroy()
            new_window.deiconify()
            new_window.after(0, play_music_new_window)
            new_window.protocol("WM_DELETE_WINDOW", new_window_on_close)
        
        def animate_transition(state1, state2):
            py.init()
            clock = py.time.Clock() 
            t=0
            for i in range(3):
                for j in range(3): 
                    if state1[i][j] != state2[i][j]:
                        x0 = j * cell_size
                        y0 = i * cell_size
                        if not state1[i][j]:
                            canvas.delete(text[state2[i][j]-1])
                            text[state2[i][j]-1]=canvas.create_text(x0 + cell_size/2, y0 + cell_size/2, text=str(state2[i][j]), font=("Bungee Shade", 20, "bold"), fill="purple") 
                            canvas.update()
                            clock.tick(1000)
                            sleep(2) 
                        else:
                            canvas.delete(text[state1[i][j]-1]) 
                            x,y=emptySquarePosition(state1)
                            x0 = x * cell_size
                            y0 = y * cell_size    
                            text[state1[i][j]-1] = canvas.create_text(x0 + cell_size/2, y0 + cell_size/2, text=str(state1[i][j]), font=("Bungee Shade", 20, "bold"),fill="purple", tags=str(state1[i][j]))          
                            canvas.update()
                            clock.tick(1000) 
                            sleep(2)
                        t=1
                        break
                if t:
                    break
            
        text=[]
        for i in range(9):
            text.append(0)
        def it_DFS():
            py.init()
            clock = py.time.Clock()
            success=False 
            l = -1 
            n = 0
            sn = 0
            start_time = time()
            o = 0 
            while (not success):
                l+=1
                IN=[initial_state,0] 
                free_nodes=[IN] 
                generated_nodes=[] 
                closed_nodes=[]
                pr_state=initial_state
                t=0 
                while(len(free_nodes)!=0): 
                    s=free_nodes.pop()
                    if not t:
                         if s[0]==initial_state:
                            label = Label(it_DFS_window, text="first state with L=" + str(l), font=("Bungee Shade", 14, "bold"), fg="white", bg="purple")
                            label.pack()
                            label.place(x=90, y=410)
                            it_DFS_window.after(3000, label.destroy)  
                         else:
                            label = Label(it_DFS_window, text="Backward!", font=("Bungee Shade", 20, "bold"), fg="white", bg="purple")
                            label.pack() 
                            label.place(x=120, y=400)
                            it_DFS_window.after(3000, label.destroy)
                         canvas.delete("all")
                         for i in range(3):
                            for j in range(3):
                                x0 = j * cell_size
                                y0 = i * cell_size
                                x1 = x0 + cell_size
                                y1 = y0 + cell_size
                                canvas.create_rectangle(x0, y0, x1, y1, fill="pink", outline="white", width=4)
                                if s[0][i][j] != 0:
                                    text[s[0][i][j]-1] = canvas.create_text(x0 + cell_size/2, y0 + cell_size/2, text=str(s[0][i][j]), font=("Bungee Shade", 20, "bold"),fill="purple")  
                         canvas.update()
                         clock.tick(1000)
                         sleep(3) 
                    else: 
                        animate_transition(pr_state, s[0])
                    closed_nodes.append(s[0]) 
                    if (isGoalState(s[0])):
                        end_time = time()
                        total_time = end_time - start_time
                        total_time = "{:.3f}".format(total_time)
                        success=True 
                        mixer.music.stop()
                        final_message = "Final State Reached On Limit = " + str(s[1]) + "\nClosed Nodes Number = " + str(n) + "\nGenerated Nodes Number = " + str(sn) + "\nExecution time = " + str(total_time) + "s"     
                        final_label = Label(it_DFS_window, text=final_message, font=("Lucida Fax", 12, "bold"), fg="purple", bg="pink", relief="groove", borderwidth=3)
                        final_label.pack()
                        final_label.place(x=100,y=400)
                        break
                    t=0 
                    pr_state=s[0]
                    if s[1]<l:  
                      for i in transitions(s[0]): 
                        if i not in generated_nodes and i != initial_state: 
                          free_nodes.append([i,s[1]+1])
                          generated_nodes.append(i) 
                          t=1
                    cu_time = time()
                    if cu_time - start_time >= 60:
                       end_time = cu_time 
                       total_time = end_time - start_time
                       total_time = "{:.3f}".format(total_time)
                       mixer.music.stop()
                       final_message = "HARD LUCK!\n" + "Closed Nodes Number = " + str(len(closed_nodes)) + "\nGenerated Nodes Number = " + str(len(generated_nodes)) + "\nExecution time = " + str(total_time) + 's'     
                       final_label = Label(it_DFS_window, text=final_message, font=("Lucida Fax", 12, "bold"), fg="purple", bg="pink", relief="groove", borderwidth = 3)
                       final_label.pack()
                       final_label.place(x=120,y=400)
                       o = 1 
                       break
                if o:
                  break 
                if (not success): 
                    n += len(closed_nodes)
                    sn += len(generated_nodes) 
        mixer.music.stop()
        it_DFS_window=Toplevel(new_window)
        it_DFS_window.protocol("WM_DELETE_WINDOW", new_window.destroy)
        new_window.withdraw()
        it_DFS_window.geometry("500x500")
        it_DFS_window.iconbitmap("puzzle.ico")
        it_DFS_window.title('Iterative DFS')
        it_DFS_window.after(0, play_music_window)
        it_DFS_window.protocol("WM_DELETE_WINDOW", it_DFS_window_on_close)
        it_DFS_window.configure(background="purple")
        it_DFS_back_button = Button(it_DFS_window, text="Back", command=back_to_sec_window, font=("Bungee Shade",12, "bold"), fg="purple", bg="white", relief="groove", borderwidth=5, width=5, height=1)
        it_DFS_back_button.place(x=397, y=410)
        canvas = Canvas(it_DFS_window, width=canvas_width, height=canvas_height, bg="pink")
        canvas.pack(side=TOP, padx=10, pady=10)
        it_DFS() 
        it_DFS_window.mainloop()
    def back_to_main_window():
        mixer.music.stop()
        new_window.destroy()
        window.deiconify()
        window.after(0, play_music)
        window.protocol("WM_DELETE_WINDOW", on_close)
    mixer.music.stop()
    new_window = Toplevel(window)
    new_window.protocol("WM_DELETE_WINDOW", window.destroy)
    window.withdraw()
    new_window.geometry("500x500")
    new_window.iconbitmap("puzzle.ico")
    new_window.title('Let The Game Begins!')
    new_window.after(0, play_music_new_window)
    new_window.protocol("WM_DELETE_WINDOW", new_window_on_close)
    new_bg = PhotoImage(file="4277821.png")
    new_label = Label(new_window,image=new_bg)
    new_label.pack()
    new_button = Button(new_window, text="DFS", command=open_DFS_window, font=("Bungee Shade",20, "bold"), fg="purple", bg="pink", relief="groove", borderwidth=4, width=5, height = 1)
    new_button.place(x=80,y=30)
    new_button3 = Button(new_window, text="BFS", command=open_BFS_window, font=("Bungee Shade",20, "bold"), fg="purple", bg="pink", relief="groove", borderwidth=4, width=5, height = 1)
    new_button3.place(x=290,y=30)
    new_button4 = Button(new_window, text="Limited\nDFS", command=open_LDFS_window, font=("Bungee Shade",15, "bold"), fg="purple", bg="pink", relief="groove", borderwidth=4, width=10, height = 1)
    new_button4.place(x=35,y=300)
    new_button2 = Button(new_window, text="Iterative\nDFS", command=open_it_DFS_window, font=("Bungee Shade",15, "bold"), fg="purple", bg="pink", relief="groove", borderwidth=4, width=10, height=1)
    new_button2.place(x=157,y=190)
    new_button5 = Button(new_window, text="Heuristic", command = open_HS_window, font=("Bungee Shade",15, "bold"), fg="purple", bg="pink", relief="groove", borderwidth=4, width=10, height = 1) 
    new_button5.place(x=280,y=300)
    back_button = Button(new_window, text="Back", command=back_to_main_window, font=("Bungee Shade",12, "bold"), fg="purple", bg="white", relief="groove", borderwidth=5, width=5, height=1)
    back_button.place(x=370, y=410)
    new_window.mainloop()
    
def play_music():
    mixer.init()
    sound_file ="sound.mp3"
    mixer.music.load(sound_file)
    mixer.music.play(loops=-1)

def on_close():
    mixer.music.stop()
    window.destroy()

x=y=0 
dx=dy=1 
def moving_button():
    global x,y,dx,dy
    x+=dx
    y+=dy
    if x > window.winfo_width() - button.winfo_width() or x < 0:
        dx *= -1
    if y > window.winfo_height() - button.winfo_height() or y < 0:
        dy *= -1        
    button.place(x=x, y=y)
    window.after(4,moving_button)

window=Tk()
window.iconbitmap("puzzle.ico")
window.geometry("500x500")
window.title("Puzzle Sliding 3x3")
window.after(0, play_music)
window.protocol("WM_DELETE_WINDOW", on_close)

bg_image = PhotoImage(file="5565958.png")
label = Label(window,image=bg_image)
label.pack()
button = Button(window, text="enter puzzle\nsliding 3x3", command=open_new_window,font=("Bungee Shade",25, "bold"), fg="purple", bg="pink", relief="groove", borderwidth=4, width=15)
moving_button()   

window.mainloop()
