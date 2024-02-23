from collections import defaultdict
from copy import deepcopy
from typing import Dict, Tuple
import pandas as pd

def deduction(num:list):

    sudo=deepcopy(num)
    isfindnew=True
    while isfindnew:
        isfindnew=False

        sudo_pos = pd.DataFrame([[[z for z in range(1,10)]for y in range(1,10)]for x in range(1,10)])
        for (x,v) in enumerate(sudo):
            for (y,v) in enumerate(v):
                if v != 0:
                    sudo_pos.loc[x,y]=v
                    sudo_pos.loc[x,:].apply(lambda x:x.remove(v) if isinstance(x,list) and v in x else (x))
                    sudo_pos.loc[:,y].apply(lambda x:x.remove(v) if isinstance(x,list) and v in x else (x))
                    for x1 in range(3):
                        for y1 in range(3):
                            # print((int(x/3)*3+x1,int(y/3)*3+y1))
                            if isinstance(sudo_pos.loc[int(x/3)*3+x1,int(y/3)*3+y1],list) and v in sudo_pos.loc[int(x/3)*3+x1,int(y/3)*3+y1]:
                                sudo_pos.loc[int(x/3)*3+x1,int(y/3)*3+y1].remove(v)

        line_possibility=defaultdict(lambda:defaultdict(list))
        row_possibility=defaultdict(lambda:defaultdict(list))
        square_possibility=defaultdict(lambda:defaultdict(list))
        for x in range(9):
            for y in range(9):
                if isinstance(sudo_pos.loc[x,y],list) and len(sudo_pos.loc[x,y]) == 1:
                    sudo[x][y]=sudo_pos.loc[x,y][0]
                    # print((x,y),sudo_pos.loc[x,y])
                    line_possibility[x][sudo[x][y]]=y
                    row_possibility[y][sudo[x][y]]=x
                    square_possibility[int(x/3)*3+int(y/3)][sudo[x][y]]=y%3+int(x%3)*3
                    isfindnew=True
                elif isinstance(sudo_pos.loc[x,y],int):
                    line_possibility[x][sudo[x][y]]=y
                    row_possibility[y][sudo[x][y]]=x
                    square_possibility[int(x/3)*3+int(y/3)][sudo[x][y]]=y%3+int(x%3)*3
                else:
                    for i in sudo_pos.loc[x,y]:
                        if isinstance(line_possibility[x][i],list):
                            line_possibility[x][i].append(y)
                        if isinstance(row_possibility[y][i],list):
                            row_possibility[y][i].append(x)
                        if isinstance(square_possibility[int(x/3)*3+int(y/3)][i],list):
                            square_possibility[int(x/3)*3+int(y/3)][i].append(y%3+int(x%3)*3)
        for x in range(9):
            for y in range(1,10):
                if isinstance(line_possibility[x][y],list) and len(line_possibility[x][y]) == 1:
                    line_possibility[x][y] = line_possibility[x][y][0]
                    sudo[x][line_possibility[x][y]]=y
                    isfindnew=True
                if isinstance(row_possibility[x][y],list) and len(row_possibility[x][y]) == 1:
                    row_possibility[x][y] = row_possibility[x][y][0]
                    sudo[row_possibility[x][y]][x]=y
                    isfindnew=True
                if isinstance(square_possibility[x][y],list) and len(square_possibility[x][y]) == 1:
                    square_possibility[x][y] = square_possibility[x][y][0]
                    sudo[int(x/3)*3+int(square_possibility[x][y]/3)][x%3*3+square_possibility[x][y]%3]=y
                    isfindnew=True
    return sudo,sudo_pos

class gusstree:
    sudo_pos:pd.DataFrame
    children_nodes:Dict[Tuple[int, int, int], "gusstree"]
    parent_node:"gusstree"

    def __init__(self,sudo_pos:pd.DataFrame) -> None:
        self.sudo_pos = sudo_pos
        self.sudo = [v for k,v in sudo_pos.T.map(lambda x: 0 if isinstance(x, list) else x).to_dict("list").items()]

    def exec(self):
        if self.sudo_pos.map(lambda x:isinstance(x,int)).all().all():
            return self.sudo_pos,True
        if self.sudo_pos.map(lambda x:x==[]).any().any():
            return self.sudo_pos,False
        for record in [(row, col) for row in range(len(self.sudo_pos)) for col in range(len(self.sudo_pos.columns)) if isinstance(self.sudo_pos.iloc[row, col], list)]:
            sudo = deepcopy(self.sudo)
            for value in self.sudo_pos.loc[*record]:
                sudo[record[0]][record[1]]=value
                print((record[0],record[1]),value)
                sudo,sudo_pos=deduction(sudo)
                sudo_pos,result=gusstree(sudo_pos).exec()
                if result:
                    return sudo_pos,result

def sudoku(num:list[list:[list|int]]):
    return gusstree(deduction(num)[1]).exec()[0]