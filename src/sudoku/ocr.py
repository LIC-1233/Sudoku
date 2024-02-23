import cv2
import numpy as np
from PIL import Image


def ocr(imgs: list[Image.Image]) -> list:
    img = cv2.imread(r"D:\work\dev\project\Sudoku\asset\number.png")

    ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ref = cv2.threshold(ref, 150, 255, cv2.THRESH_BINARY_INV)[1]

    digits={}

    refCnts, hierarchy = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #找到外轮廓
    refCnts=sorted(refCnts,key=lambda x:x[0][0][0])

    x, y, w, h = cv2.boundingRect(refCnts[0])

    for (i, c) in enumerate(refCnts):
        (x, y, w, h) = cv2.boundingRect(c) #外接矩形
        roi = ref[y:y + h, x:x + w]
        digits[i+1] = roi

    results=[]
    for img in imgs:
        scores={0:0}
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ref = cv2.threshold(ref, 150, 255, cv2.THRESH_BINARY_INV)[1]
        # refCnts, hierarchy = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #找到外轮廓
        # display(Image.fromarray(cv2.drawContours(blank_img,refCnts[0],-1,(0,0,255),3)))
        for num in digits:
            if len(refCnts)==0:
                scores[num] = 0
            else:
                (_, score, _, _) = cv2.minMaxLoc(cv2.matchTemplate(digits[num], ref,cv2.TM_CCOEFF_NORMED))
                scores[num]=score

        results.append(max(scores,key=scores.get))
    return results
