import keyboard
from time import sleep
from PIL import Image, ImageDraw, ImageFont
import pyautogui as pg
import pandas as pd
from .ocr import ocr

# https://sudoku.com/zh/evil/

def get_num(imageFile:str|Image.Image):
    firstblocktopleft=364
    firstblockbottomright=262
    width=heigh=54
    a=[[364 + 54*i + i + int(i/3)*2,364 + 54*(i+1) + i + int(i/3)*2] for i in range(9)]
    b=[[262 + 54*i + i + int(i/3)*2, 262 + 54*(i+1) + i + int(i/3)*2] for i in range(9)]
    d=[[((x1,y1),(x2,y2)) for x1,x2 in a] for y1,y2 in b]

    image=Image.new(mode="RGB",size=[1920,1080],color="white")
    if isinstance(imageFile,Image.Image):
        image=imageFile
    else:
        image=Image.open(imageFile)
    draw=ImageDraw.Draw(image)
    imgs=[]
    for i in d:
        lines=[]
        for j in i:
            lines.append(image.crop([j[0][0]+3,j[0][1]+3,j[1][0]-3,j[1][1]-3]))
        imgs.append(lines)
    image_width, image_height = imgs[0][0].size
    board_image = Image.new('RGB', (image_width * len(imgs[0]), image_height * len(imgs)))
    for i in range(len(imgs)):
        for j in range(len(imgs[i])):
            board_image.paste(imgs[i][j], (j * image_width, i * image_height))
    num=[]
    for i in imgs:
        num.append(ocr(i))
    return num


def finish(num:list,sudo:pd.DataFrame):
    a=[[364 + 54*i + i + int(i/3)*2,364 + 54*(i+1) + i + int(i/3)*2] for i in range(9)]
    b=[[262 + 54*i + i + int(i/3)*2, 262 + 54*(i+1) + i + int(i/3)*2] for i in range(9)]
    d=[[((x1,y1),(x2,y2)) for x1,x2 in a] for y1,y2 in b]
    pos=[[940,1053,1167],[410,522,635]]
    numb_pos={n:(pos[0][(n-1)%3],pos[1][int((n-1)/3)]) for n in range(1,10)}
    sudo_pos=pd.DataFrame([[(int((y[0][0]+y[1][0])/2),int((y[0][1]+y[1][1])/2)) for y in x]for x in d])
    sudo_ori=pd.DataFrame(num)
    sudo_new=sudo[sudo_ori==0]
    for row, col in [(row, col) for row in range(9) for col in range(9) if pd.notna(sudo_new.iloc[row, col])]:
        if keyboard.is_pressed('down') or keyboard.is_pressed('0'):
            exit()
        pg.click(*sudo_pos.iloc[row, col])
        sleep(0.02)
        keyboard.press_and_release(sudo_new.iloc[row, col]+1)
        # pg.click(*numb_pos[sudo_new.iloc[row, col]])
        # sleep(0.05)


def drawguess(sudo:pd.DataFrame):
    def getpic(v):
        result = Image.new("RGB",(60,60),(255,255,255))
        font = ImageFont.truetype(r"D:\work\dev\project\Sudoku\asset\微软雅黑.ttf",size=20)
        font1 = ImageFont.truetype(r"D:\work\dev\project\Sudoku\asset\微软雅黑.ttf",size=60)
        draw = ImageDraw.Draw(result)
        if isinstance(v,list):
            for i in v:
                draw.text((((i-1)%3)*20+4,int((i-1)/3)*20-5),f"{i}",(0,0,0),font)
        else:
            draw.text((12,-12),f"{v}",(0,0,0),font1)
        draw.rectangle((0,0,60,60),outline="red")
        return result
    d=[]
    for k,v in sudo.apply(lambda x:x.apply(getpic)).to_dict("list").items():
        d.append(v)
    image_width=image_height = 60
    board_image = Image.new('RGB', (image_width * len(d[0]), image_height * len(d)))
    for i in range(len(d)):
        for j in range(len(d[i])):
            board_image.paste(d[j][i], (j * image_width, i * image_height))
    board_image.show()