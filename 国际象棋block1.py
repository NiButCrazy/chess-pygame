print("该版本需要玩家有一定国际象棋素养，且无王车互换，复活棋子,胜负判定等功能。后需完善马上到来")
qp=[["___" for i in range(8)] for j in range(8)]
qp[0]=["w车","w马","w相","w王","w后","w相","w马","w车"]
qp[1]=["w兵","w兵","w兵","w兵","w兵","w兵","w兵","w兵"] 
qp[7]=["b车","b马","b相","b王","b后","b相","b马","b车"]
qp[6]=["b兵","b兵","b兵","b兵","b兵","b兵","b兵","b兵"]

for i in range(8):
    print(qp[i])
def panding1(x,y):
    if 0<=x<=7 and 0<=y<=7:
        return True
    else:
        return False
    
def shunxu(sx):# :black,:white    
    if sx=="w":
        sx="b"   
    else:
        sx="w"
    return sx
def che():
    flag=False
    if (x_me==x and y_me!=y) or (x_me!=x and y_me==y):
        flag=True
    return flag
def xiang():
    flag=False
    if x_me-y_me==x-y:
        flag=True
    return flag

def ma():
    flag=False
    if (x_me==x+2 and y_me==y+1) or (
        x_me==x-2 and y_me==y+1) or (
            x_me==x-2 and y_me==y-1) or (
                x_me==x+2 and y_me==y-1) or (
                    x_me==x+1 and y_me==y+2) or (
                        x_me==x-1 and y_me==y+2) or (
                            x_me==x-1 and y_me==y-2) or (
                                x_me==x+1 and y_me==y-2):
        flag=True
    return flag

def hou():
    flag=False
    if (x_me==x and y_me!=y) or (x_me!=x and y_me==y) or (x_me-y_me==x-y):
        flag=True
    return flag
    
def wang():
    flag=False
    if (x_me==x+1 and y_me==y+1) or (
        x_me==x-1 and y_me==y+1) or (
            x_me==x-1 and y_me==y-1) or (
                x_me==x+1 and y_me==y-1) or (
                    x_me==x+1 and y_me==y+1) or (
                        x_me==x-1 and y_me==y+1) or (
                            x_me==x-1 and y_me==y-1) or (
                                x_me==x+1 and y_me==y-1):
        flag=True
    return flag
    
    
def zudang():
    flag=True
    if qp[x_me][y_me][1]=="车" or\
       qp[x_me][y_me][1]=="兵" or\
       qp[x_me][y_me][1]=="王" or\
       qp[x_me][y_me][1]=="后" :
        if x==x_me:
            if y>y_me:
                for i in range(y+1,y_me-1):
                    if qp[x][i][0]==sx:
                        flag=False
            elif y<y_me:
                for i in range(y_me+1,y-1):
                    if qp[x][i][0]==sx:
                        flag=False            
        elif y==y_me:   
            if x>x_me:
                for i in range(x,x_me-1):
                    if qp[i][y][0]==sx:
                        flag=False
            elif x<x_me:
                for i in range(x_me,x-1):
                    if qp[i][y][0]==sx:
                        flag=False            
    elif qp[x_me][y_me][1]=="相" or\
         qp[x_me][y_me][1]=="王" or\
         qp[x_me][y_me][1]=="后":
        if x_me>x:
            for i in range(x+1,x_me):
                if y<y_me:               
                    for j in range(y+1,y_me):
                        if qp[i][j][0]==sx:
                            flag=False
                if y>y_me:
                    for j in range(y_me+1,y):
                        if qp[i][j][0]==sx:
                            flag=False 
        if x_me< x:
            for i in range(x_me+1,x):
                if y>y_me:
                    for j in range(y_me+1,y):
                        if qp[i][j][0]==sx:
                            flag=False
                if y<y_me:
                    for j in range(y+1,y_me):
                        if qp[i][j][0]==sx:
                            flag=False 
    
    return flag
def bing():
    flag=False
    if sx=="b":
        if y==y_me:
            if ((x_me==6 and x==5) or (x_me==6 and x==4)) or (
                x_me-x==1) and qp[x][y][0]=="_":
                flag=True
            else:
                flag=False
        elif y==y_me+1 or y==y_me-1:
            if x==x_me-1 and qp[x][y][0]=="w":
                flag=True
            else:
                flag=False
    if sx=="w":
        if y==y_me:
            if ((x_me==1 and x==2) or (x_me==1 and x==3)) or (x-x_me==1) and qp[x][y][0]=="_":
                flag=True
            else:
                flag=False
        elif y==y_me+1 or y==y_me-1:
            if x==x_me+1 and qp[x][y][0]=="b":
                flag=True
            else:
                flag=False
    return flag
        

sx="b"                        
while True:
    sx=shunxu(sx)
    print("nice")
    if sx=="b":
        print("黑方落子")
        a=input("行 列 行 列").split()
        x_me=int(a[0])
        y_me=int(a[1])
        x=int(a[2])
        y=int(a[3])
        k=True
        if qp[x_me][y_me][0]=="w":
            print("这是白棋")
            k=False
        if qp[x_me][y_me][0]=="_":
            print("这里没棋")
            k=False
        while k==False:
            a=input("行 列 行 列").split()
            x_me=int(a[0])
            y_me=int(a[1])
            x=int(a[2])
            y=int(a[3])  
            if qp[x_me][y_me][0]=="b":
                k=True
            if qp[x_me][y_me][0]=="_":
                print("这里没棋")         
            else:
                print("这是白棋")
    elif sx=="w":
        print("白方落子")        
        a=input("行 列 行 列").split()
        x_me=int(a[0])
        y_me=int(a[1])
        x=int(a[2])
        y=int(a[3])
        k=True
        if qp[x_me][y_me][0]=="b":
            print("这是黑棋")
            k=False
        if qp[x_me][y_me][0]=="_":
            print("这里没棋")
            k=False     
        while k==False:
            a=input("行 列 行 列").split()
            x_me=int(a[0]);y_me=int(a[1]);x=int(a[2]);y=int(a[3]) 
            if qp[x_me][y_me][0]=="w":
                k=True
            if qp[x_me][y_me][0]=="_":
                print("这里没棋")    
            else:
                print("这是黑棋")
                    
    while k==True:  #顺序正确       
        if panding1(x,y) and panding1(x_me,y_me):
            t=False
            if  qp[x_me][y_me][1]=="车" and (che() and """zudang()"""):
                t=True
            if qp[x_me][y_me][1]=="马":
                t=True 
            if qp[x_me][y_me][1]=="相" and (xiang() and """zudang()"""):
                t=True 
            if qp[x_me][y_me][1]=="王" and (wang() and """zudang()"""):
                t=True 
            if qp[x_me][y_me][1]=="后" and (hou() and """zudang()"""):
                t=True
            if qp[x_me][y_me][1]=="兵" and (bing() and """zudang()"""):
                t=True
            print(t)
        if t==False:
            print("下的啥棋")
                
        elif t==True:
            qp[x][y]=qp[x_me][y_me]
            qp[x_me][y_me]="___"
            for i in range(8):
                print(qp[i])
            break
        
            
        while t==False:
            a=input("行 列 行 列").split()
            x_me=int(a[0]);y_me=int(a[1]);x=int(a[2]);y=int(a[3])
            if panding1(x,y) and panding1(x_me,y_me):
                t=False
                if qp[x_me][y_me][1]=="车" and (che() and """zudang()"""):
                    t=True
                if qp[x_me][y_me][1]=="马":
                    t=True 
                if qp[x_me][y_me][1]=="相" and (xiang() and """zudang()"""):
                    t=True 
                if qp[x_me][y_me][1]=="王" and (wang() and """zudang()"""):
                    t=True
                if qp[x_me][y_me][1]=="后" and (hou() and """zudang()"""):
                    t=True
                if qp[x_me][y_me][1]=="兵" and (bing() and """zudang()"""):
                    t=True
            if t==False:
                print("下的啥棋")
                        
            elif t==True:
                qp[x][y]=qp[x_me][y_me]
                qp[x_me][y_me]="___"
                for i in range(8):
                    print(qp[i])
                break
                

               
                    
                    
                    
    
        
        
        

            
            
            
