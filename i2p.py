import img2pdf
import os
from PIL import Image
from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
from PyPDF2 import PdfFileMerger, PdfFileReader



def pdfMerger(files, folderName):
    mergedObject = PdfFileMerger()
    for pdf in os.listdir(folderName):
        mergedObject.append(PdfFileReader(open(folderName+"/"+pdf, 'rb')))
    mergedObject.write("download.pdf")

    try:
        filelist = [ f for f in os.listdir(folderName) ]
        for f in filelist:
            os.remove(os.path.join(folderName, f))
    except Exception as e:
        pass
    try:
        os.rmdir(folderName)
    except Exception as e:
        print(e)

def i2pconverter(files, folderName):

    for image in os.listdir(folderName):
        remove_transparency(folderName+"/"+image)

    try:
        print("i2pcon ",folderName)
        os.remove(folderName)
    except Exception as e:
        pass
    # pdfname = folderName + ".pdf"
    pdfname = "download.pdf"
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    with open(pdfname,'wb') as f:
        f.write(img2pdf.convert([folderName+"/"+i for i in os.listdir(folderName)], layout_fun=layout_fun))

    try:
        filelist = [ f for f in os.listdir(folderName) ]
        for f in filelist:
            os.remove(os.path.join(folderName, f))
    except Exception as e:
        pass
    try:
        os.rmdir(folderName)
    except Exception as e:
        print(e)
    


def i2pconverterAutoCrop(files, folderName):

    for image in os.listdir(folderName):
        remove_transparency(folderName+"/"+image)
    
    for image in os.listdir(folderName):
        autoCropHelper(folderName+"/"+image)

    try:
        print("i2pcon ",folderName)
        os.remove(folderName)
    except Exception as e:
        pass
    # pdfname = folderName + ".pdf"
    pdfname = "download.pdf"
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    with open(pdfname,'wb') as f:
        f.write(img2pdf.convert([folderName+"/"+i for i in os.listdir(folderName)], layout_fun=layout_fun))

    try:
        filelist = [ f for f in os.listdir(folderName) ]
        for f in filelist:
            os.remove(os.path.join(folderName, f))
    except Exception as e:
        pass
    try:
        os.rmdir(folderName)
    except Exception as e:
        print(e)
    


def remove_transparency(image, bg_colour=(255, 255, 255)):
    im = Image.open(image)
    
    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        newimg = im.convert('RGB')
        newimg.save(image, 'PNG', quality=80)

    else:
        pass


def autoCropHelper(img):
    image = cv2.imread(img)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break
        
    try:
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        T = threshold_local(warped, 11, offset = 10, method = "gaussian")
        warped = (warped > T).astype("uint8") * 255

        cv2.imwrite(img, imutils.resize(warped, height = 650))
    except Exception as e:
        print("Error: ", e)
        cv2.imwrite(img, orig)
