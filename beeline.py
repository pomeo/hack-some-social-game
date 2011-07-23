#!/usr/bin/python
import os
import sys
import gtk.gdk
from random import Random
from time import sleep
from pymouse import PyMouse
import Image
import ImageChops
from datetime import datetime
from multiprocessing import Pool

def start_game():
  m = PyMouse()
  m.click(240, 300, 1)

def move_mouse(x,y):
  m = PyMouse()
  m.move(x, y)

def make_screen_left():
  os.system("xwd -id 0x1000859 -screen -display :0.0 -out scr_left.xwd")
  os.system("gm convert scr_left.xwd -colorspace GRAY -crop 260x150+0+90 -page +0+0 -resize 180x75 screenshot_left.png")

def make_screen_right():
  os.system("xwd -id 0x1000859 -screen -display :0.0 -out scr_right.xwd")
  os.system("gm convert scr_right.xwd -colorspace GRAY -crop 260x150+240+90 -page +0+0 -resize 180x75 screenshot_right.png")
  
def matchTemplate(searchImage, templateImage):
    minScore = -1000
    matching_xs = 0
    matching_ys = 0
    # convert images to "L" to reduce computation by factor 3 "RGB"->"L"
    searchImage = searchImage.convert(mode="L")
    templateImage = templateImage.convert(mode="L")
    searchWidth, searchHeight = searchImage.size
    templateWidth, templateHeight = templateImage.size
    # make a copy of templateImage and fill with color=1
    templateMask = Image.new(mode="L", size=templateImage.size, color=1)
    #loop over each pixel in the search image
    for xs in range(searchWidth-templateWidth+1):
        for ys in range(searchHeight-templateHeight+1):
        #for ys in range(10):
            #set some kind of score variable to "All equal"
            score = templateWidth*templateHeight
            # crop the part from searchImage
            searchCrop = searchImage.crop((xs,ys,xs+templateWidth,ys+templateHeight))
            diff = ImageChops.difference(templateImage, searchCrop)
            notequal = ImageChops.darker(diff,templateMask)
            countnotequal = sum(notequal.getdata())
            score -= countnotequal

            if minScore < score:
                minScore = score
                matching_xs = xs
                matching_ys = ys

    if (minScore > 100):
        print "Location=",(matching_xs, matching_ys), "Score=",minScore
        quit()
    #im1 = Image.new('RGB', (searchWidth, searchHeight), (80, 147, 0))
    #im1.paste(templateImage, ((matching_xs), (matching_ys)))
    #searchImage.show()
    #im1.show()
    #im1.save('template_matched_in_search.png')


def match_img_left():
    searchImage = Image.open("screenshot_left.png")
    templateImage = Image.open("livejournal.png")
    matchTemplate(searchImage, templateImage)

def match_img_right():
    t1 = datetime.now()
    searchImage = Image.open("screenshot_right.png")
    templateImage = Image.open("livejournal.png")
    matchTemplate(searchImage, templateImage)
    delta = datetime.now()-t1
    print "Time=%d.%d"%(delta.seconds,delta.microseconds)

def numcheck(x):
    s = 0
    for number in x:
      #t1 = datetime.now()
      s += 1
      result_scrleft = pool.apply_async(make_screen_left, [])
      result_scrright = pool.apply_async(make_screen_right, [])
      result_left = pool.apply_async(match_img_left, [])
      result_right = pool.apply_async(match_img_right, [])
      #delta = datetime.now()-t1
      #print "Time=%d.%d"%(delta.seconds,delta.microseconds)
      
if __name__ == '__main__':
    pool = Pool(processes=8)
    start_game()
    numcheck(range(10000))
    #make_screen()
    #match_img()
    #print result
    #print pool.map(f, range(10))

