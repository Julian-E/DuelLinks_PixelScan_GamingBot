from PIL import ImageGrab
import datetime
import pyautogui as pag
import time
import sys
import keyboard
import random

duelcount = 1 #für log file benötigt
disconnect = False #needed, to see in the outer while loop, where the program shall start. If False, the program will start in game without loggin in.
localtime = time.asctime( time.localtime(time.time()) ) #timestamp when script beginns
start_timecounter_calc = time.time()#timestamp for Duels/min - calculation at the end of outer While loop
handle_duelcount = open("duellog.txt", "w", encoding="utf-8")#creates new duellog-file
handle_duelcount.close()#closes new duellog-file. File should be empty

dict_window_x = {1: 850, #refering to current_window
2: 709,
3: 709,
4: 709
}
dict_window_y = {1: 611, #refering to current_series
2: 665,
3: 611,
4: 611,
5: 698
}

use_exp_booster = True #True oder False
wanted_rounds = 10 #how many rounds standard duelists until he switchs series to search for legendaries
start_series = 1 #=1:YuGiOH, =2:DSOD, =3:GX, =4:5D, =5:XYZ
start_window = 1 #=1:Gate, =2:Duel, =3:Shop, =4:Cards
positiv_color_standard = 4
positiv_color_legendary = 3
round_counter = 2 #set 2 to skip the legendary start at beginn. Else, set =1.

current_series = start_series #=1:YuGiOH, =2:DSOD, =3:GX, =4:5D, =5:XYZ
current_window = start_window #=1:YuGiOH, =2:DSOD, =3:GX, =4:5D, =5:XYZ
exception_series3_window1 = "0xEFFFFF"
window_change_counter = 0
series_change_counter = 0


def _RGBtoHex(vals, rgbtype=256):
    """Converts RGB values in a variety of formats to Hex values.

     @param  vals     An RGB/RGBA tuple
     @param  rgbtype  Valid valus are:
                          1 - Inputs are in the range 0 to 1
                        256 - Inputs are in the range 0 to 255

     @return A hex string in the form '#RRGGBB' or '#RRGGBBAA'
    """
    if len(vals)!=3 and len(vals)!=4:
        raise Exception("RGB or RGBA inputs to RGBtoHex must have three or four elements!")
    if rgbtype!=1 and rgbtype!=256:
        raise Exception("rgbtype must be 1 or 256!")

    #Convert from 0-1 RGB/RGBA to 0-255 RGB/RGBA
    if rgbtype==1:
        vals = [255*x for x in vals]

    #Ensure values are rounded integers, convert to hex, and concatenate
    return '0x' + ''.join(['{:02X}'.format(int(round(x))) for x in vals])

    #Examples:

    #print(RGBtoHex((0.1,0.3,  1)))
    #print(RGBtoHex((0.8,0.5,  0)))
    #print(RGBtoHex((  3, 20,147), rgbtype=256))
    #print(RGBtoHex((  3, 20,147,43), rgbtype=256))

def _check_disconnect():
    screen = ImageGrab.grab()
    px = screen.load()
    #coordinaten für schwarze Buchstaben und weißes "Neustart"
    color_1 = _RGBtoHex(px[2370-1920, 526])
    color_2 = _RGBtoHex(px[2777-1920, 526])
    color_3 = _RGBtoHex(px[2860-1920, 526])
    color_4 = _RGBtoHex(px[2961-1920, 526])        
    color_5 = _RGBtoHex(px[2859-1920, 562])
    color_6 = _RGBtoHex(px[2809-1920, 708])
    color_7 = _RGBtoHex(px[2890-1920, 708])
    color_8 = _RGBtoHex(px[2921-1920, 708])
    color_9 = _RGBtoHex(px[2871-1920, 764])
    if color_1 == "0x000000" and color_2 == "0x000000" and color_3 == "0x000000" and color_4 == "0x000000" and color_5 == "0x000000" and color_6 == "0xFFFFFF" and color_7 == "0xFFFFFF" and color_8 == "0xFFFFFF" and color_9 == "0xFFFFFF":
        global start_timecounter_calc
        global duelcount
        global disconnect
        timestamp = time.asctime( time.localtime(time.time()) )
        end_timecounter_calc = time.time()
        minutes = (end_timecounter_calc-start_timecounter_calc)/60 #time passed since script was started in minutes
        duels_per_minute = "{:.2f}".format((duelcount/minutes)) #formates the duels/min in a string and ROUNDS the Value to 2 decimal points
        _read_and_log_old_logfile_text()
        handle_duelcount = open("duellog.txt", "a", encoding="utf-8")#opens logfile for appending text
        handle_duelcount.write(f"Duels won: {duelcount}\t{duels_per_minute} Duels / min\nDisconnected!!!!: {timestamp}\n")
        handle_duelcount.close()
        duelcount = 0  
        disconnect = True        
        return

def check_bluecolor_standard(scan_color):
    if (
        scan_color == "0xFAFFFF"
        #or scan_color == "0xFFFFFF"
        or scan_color == "0xFBFFFF"
        or scan_color == "0xF2FFFF"
        or scan_color == "0xF4FFFF"
        or scan_color == "0xF6FFFF"
        or scan_color == "0xF7FFFF"
        or scan_color == "0xEFFFFF"
        or scan_color == "0xEEFFFF"
        or scan_color == "0xEBFFFF"
        or scan_color == "0xE5FFFF"
        or scan_color == "0xE9FFFF"
        or scan_color == "0xDDFFFF"
        or scan_color == "0xDBFFFF"
        or scan_color == "0xDEFFFF"
        or scan_color == "0xDFFFFF"
        or scan_color == "0xDCFFFF"
        or scan_color == "0xD2FFFF"
    ):
        #print("found")
        return 1
    else:
        return 0

def check_bluesurrounding_standard(scan_color):
    global exception_series3_window1
    if (
        scan_color == "0xFAFFFF"
        or scan_color == "0xFFFFFF"
        or scan_color == "0xFBFFFF"
        or scan_color == "0xF2FFFF"
        or scan_color == "0xF4FFFF"
        or scan_color == "0xF6FFFF"
        or scan_color == "0xF7FFFF"
        or scan_color == exception_series3_window1
        or scan_color == "0xEEFFFF"
        or scan_color == "0xEBFFFF"
        or scan_color == "0xE5FFFF"
        or scan_color == "0xE9FFFF"
        or scan_color == "0xDDFFFF"
        or scan_color == "0xDBFFFF"
        or scan_color == "0xDEFFFF"
        or scan_color == "0xDFFFFF"
        or scan_color == "0xDCFFFF"
        or scan_color == "0xD2FFFF"
    ):
        #print("found")
        return 1
    else:
        return 0

def check_bluecolor_legendary(scan_color):
    if (
        scan_color == "0xEFEFEF"
        or scan_color == "0xE1E6EF"
        or scan_color == "0xE0E3EF"
        or scan_color == "0xE4E6EF"
        or scan_color == "0xE1E5EF"
        or scan_color == "0xE4E5EF"
        or scan_color == "0xE0E2EF"
        or scan_color == "0xE4EAAF"
        or scan_color == "0xEBEBEF"
        or scan_color == "0xEAEAEF"
        or scan_color == "0xEEEEEF"
        or scan_color == "0xEDEEEF"
        or scan_color == "0xECECEF"
        or scan_color == "0xE2E2EF"
        or scan_color == "0xD9DAEF"
        or scan_color == "0xD6DBEF"
        or scan_color == "0xD2D8EF"
        or scan_color == "0xD5D8EF"
        or scan_color == "0xD3D3EF"
        or scan_color == "0xD2D2EF"
        or scan_color == "0xCFD0EF"
        or scan_color == "0xC1CAEF"
        or scan_color == "0xCFD5EF"
        or scan_color == "0xCCD6EF"
        or scan_color == "0xC7C7EF"
    ):
        #print("found")
        return 1
    else:
        return 0

def check_bluesurrounding_legendary(scan_color):
    global exception_series3_window1
    if (
        scan_color == "0xEFEFEF"
        or scan_color == "0xE1E6EF"
        or scan_color == "0xE0E3EF"
        or scan_color == "0xE4E6EF"
        or scan_color == "0xE1E5EF"
        or scan_color == "0xE4E5EF"
        or scan_color == "0xE0E2EF"
        or scan_color == "0xE4EAAF"
        or scan_color == "0xEBEBEF"
        or scan_color == "0xEAEAEF"
        or scan_color == "0xEEEEEF"
        or scan_color == "0xEDEEEF"
        or scan_color == "0xECECEF"
        or scan_color == "0xE2E2EF"
        or scan_color == "0xD9DAEF"
        or scan_color == "0xD6DBEF"
        or scan_color == "0xD2D8EF"
        or scan_color == "0xD5D8EF"
        or scan_color == "0xD3D3EF"
        or scan_color == "0xD2D2EF"
        or scan_color == "0xCFD0EF"
        or scan_color == "0xC1CAEF"
        or scan_color == "0xCFD5EF"
        or scan_color == "0xCCD6EF"
        or scan_color == "0xC7C7EF"
    ):
        #print("found")
        return 1
    else:
        return 0

def check_standard_duelist_left():
    screen = ImageGrab.grab()
    px = screen.load()
    color_1 = _RGBtoHex(px[651, 115])            

    if color_1 == "0x6666AA": #Farbe, wenn KEIN Duellant mehr übrig ist!
        print(color_1)
        return False
    else:
        print(color_1)
        return True

def scan_duelists_standard():
    global current_window
    global current_series
    global dict_window_x
    global dict_window_y
    global positiv_color_standard
    global exception_series3_window1

    screen = ImageGrab.grab()
    px = screen.load()
    for x in range(dict_window_x[current_window], 1154, 2):
        for y in range(dict_window_y[current_series], 991, 2):
            scan_color = _RGBtoHex(px[x, y])
            if check_bluecolor_standard(scan_color) == 1:
                #Exceptions General-------------------------------------------------------
                if current_window == 4 and 899 <= x <=  923 and 691 <= y <= 724: #dueltelevision in allen Serien
                    continue
                if current_window == 2 and 903 <= x <=  1020 and 779 <= y <= 993: #PVP-Duel-Button in allen Serien
                    continue
                if current_window == 1 and 730 <= x <=  865 and 810 <= y <= 1071: #eventcardtrader
                    continue
                if current_window == 1 and 667 <= x <=  875 and 588 <= y <= 884: #Tourguide
                    continue
                #Exceptions YuGiOh-------------------------------------------------------
                if current_series == 1 and current_window == 4 and 1006 <= x <=  1109 and 638 <= y <= 678: #Duellstudio eingang
                    continue
                if current_series == 1 and current_window == 1 and 1099 <= x <=  1142 and 840 <= y <= 882: #Straße rechts unten
                    continue
                if current_series == 1 and current_window == 2 and 699 <= x <=  742 and 676 <= y <= 725: #Lampe links unten
                    continue
                if current_series == 1 and current_window == 2 and 750 <= x <=  836 and 570 <= y <= 660: #Lampe links oben
                    continue
                if current_series == 1 and current_window == 2 and 1038 <= x <=  1127 and 562 <= y <= 658: #Lampe rechts oben
                    continue
                if current_series == 1 and current_window == 2 and 1160 <= x <=  1204 and 680 <= y <= 730: #Lampe rechts unten
                    continue
                if current_series == 1 and current_window == 2 and 554 <= x <=  806 and 830 <= y <= 1015: #Straße links unten
                    continue
                if current_series == 1 and current_window == 2 and 1111 <= x <=  1168 and 892 <= y <= 941: #Mülleimer unten rechts
                    continue
                if current_series == 1 and current_window == 3 and 854 <= x <=  882 and 944 <= y <= 960: #straße links unten
                    continue
                if current_series == 1 and current_window == 3 and 1090 <= x <=  1115 and 930 <= y <= 949: #Straße rechts unten
                    continue
                #Exceptions YuGiOh DSOD-------------------------------------------------------
                if current_series == 2 and current_window == 1 and 1115 <= x <=  1158 and 863 <= y <= 887: #rechte untere Straßenbeleuchtung
                    continue
                if current_series == 2 and current_window == 4 and 741 <= x <=  773 and 792 <= y <= 831: #laterne unten links
                    continue
                if current_series == 2 and current_window == 4 and 1124 <= x <=  1138 and 642 <= y <= 658: #laterne oben rechts
                    continue
                if current_series == 2 and current_window == 2 and 709 <= x <=  1154 and 611 <= y <= 655: #ganz oberer scan bereich
                    continue
                if current_series == 2 and current_window == 2 and 848 <= x <=  880 and 948 <= y <= 977: #Straßenbereich unten links
                    continue
                if current_series == 2 and current_window == 2 and 552 <= x <= 766 and 903 <= y <= 1010: #Geländer links unten
                    continue
                #if current_series == 2 and current_window == 2 and 1033 <= x <=  1053 and 925 <= y <= 951: #Straßenbereich unten rechts
                #    continue
                if current_series == 2 and current_window == 2 and 1040 <= x <=  1070 and 850 <= y <= 870: #Straße rechts mitte
                    continue
                if current_series == 2 and current_window == 3 and 762 <= x <=  851 and 841 <= y <= 892: #Tisch  mitte links
                    continue

                #Exceptions YuGiOh GX-------------------------------------------------------
                if current_series == 3 and current_window == 1 and 1103 <= x <=  1163 and 725 <= y <= 743: #rechte Steinbeleuchtung
                    continue
                if current_series == 3 and current_window == 1 and 1110 <= x <=  1134 and 947 <= y <= 963: #rechte Straßenbeleuchtung
                    continue
                if current_series == 3 and current_window == 1 and 791 <= x <=  1186 and 737 <= y <= 950: #Die ganze Straße ist voll mit blau-Tönen... Wert auf 8 setzen und "0xEFFFFF" razusnehmen. dann erkennt er straße nicht. Hoffentlich aber Duelentan. Wird unten rückgängig gemacht.
                    positiv_color_standard = 8
                    exception_series3_window1 = ""
                    #continue
                if current_series == 3 and current_window == 2 and 807 <= x <=  836 and 849 <= y <= 880: #Straße mitte links
                    continue
                if current_series == 3 and current_window == 2 and 865 <= x <=  896 and 911 <= y <= 933: #linke untere Statuebeleuchtung
                    continue
                if current_series == 3 and current_window == 2 and 813 <= x <=  846 and 671 <= y <= 715: #linke obere Statuebeleuchtung
                    continue
                if current_series == 3 and current_window == 2 and 1060 <= x <=  1089 and 669 <= y <= 718: #rechte obere Statuebeleuchtung
                    continue
                if current_series == 3 and current_window == 2 and 1014 <= x <=  1048 and 912 <= y <= 937: #linke untere Statuebeleuchtung
                    continue
                if current_series == 3 and current_window == 3 and 889 <= x <=  1018 and 838 <= y <= 885: #Straße Mitte
                    continue   
                if current_series == 3 and current_window == 3 and 721 <= x <=  765 and 901 <= y <= 945: #linke untere Statuebeleuchtung
                    continue
                if current_series == 3 and current_window == 3 and 1119 <= x <=  1169 and 908 <= y <= 947: #rechte untere Statuebeleuchtung
                    continue
                
                #Exceptions YuGiOh GX-------------------------------------------------------
                if current_series == 4 and current_window == 2 and 755 <= x <=  786 and 800 <= y <= 838: #rechte untere Leitplanke
                    continue
                if current_series == 4 and current_window == 2 and 1062 <= x <=  1159 and 860 <= y <= 1026: #rechte untere straßenbeleuchtung
                    continue
                if current_series == 4 and current_window == 3 and 921 <= x <=  994 and 677 <= y <= 727: #Brunnen
                    continue
                #Exceptions YuGiOh XYZ-------------------------------------------------------
                if current_series == 5 and current_window == 1 and 675 <= x <=  895 and 580 <= y <= 872: #Guidetusse
                    continue
                if current_series == 5 and current_window == 2:
                    positiv_color_standard = 6
                if current_series == 5 and current_window == 2 and 683 <= x <=  774 and 838 <= y <= 924: #Trompetentyp
                    continue
                if current_series == 5 and current_window == 2 and 867 <= x <=  950 and 936 <= y <= 997: #Trompetentyp
                    continue
                #if current_series == 5 and current_window == 2 and 826 <= x <=  860 and 727 <= y <= 845: #Straße mitte links
                #    continue
                #if current_series == 5 and current_window == 2 and 861 <= x <=  913 and 954 <= y <= 985: #Straße mitte links
                #    continue
                if current_series == 5 and current_window == 3 and 945 <= x <=  970 and 862 <= y <= 877: #Straßenbeleuchtung mitte 2. von unten
                    continue
                if current_series == 5 and current_window == 3 and 945 <= x <=  970 and 933 <= y <= 951: #Straßenbeleuchtung mitte 1. von unten
                    continue
                if current_series == 5 and current_window == 3 and 945 <= x <=  970 and 813 <= y <= 823: #Straßenbeleuchtung mitte 3. von unten
                    continue
                if current_series == 5 and current_window == 4 and 709 <= x <=  877 and 828 <= y <= 945: #Gelaender links unten
                    continue

                color1 = _RGBtoHex(px[x-1, y+1])
                color1_blue = check_bluesurrounding_standard(color1)
                color2 = _RGBtoHex(px[x, y+1])
                color2_blue = check_bluesurrounding_standard(color2)
                color3 = _RGBtoHex(px[x+1, y+1])
                color3_blue = check_bluesurrounding_standard(color3)
                color4 = _RGBtoHex(px[x-1, y])
                color4_blue = check_bluesurrounding_standard(color4)
                color5 = _RGBtoHex(px[x+1, y])
                color5_blue = check_bluesurrounding_standard(color5)
                color6 = _RGBtoHex(px[x-1, y-1])
                color6_blue = check_bluesurrounding_standard(color6)
                color7 = _RGBtoHex(px[x, y-1])
                color7_blue = check_bluesurrounding_standard(color7)
                color8 = _RGBtoHex(px[x+1, y-1])
                color8_blue = check_bluesurrounding_standard(color8)
                sum_color = color1_blue + color2_blue + color3_blue + color4_blue + color5_blue + color6_blue + color7_blue + color8_blue
                
                if sum_color >= positiv_color_standard:
                    if current_series == 3 and current_window == 1 and 791 <= x <=  1186 and 737 <= y <= 950: #Mache Ausnahme von Straße links unten rückgängig
                        positiv_color_standard = 4
                        exception_series3_window1 = "0xEFFFFF"
                    if current_series == 5 and current_window == 2:
                        positiv_color_standard = 4

                    print(f"Found at: {x},{y}")
                    print(current_series, current_window)
                    print(color1)
                    print(color2)
                    print(color3)
                    print(color4)
                    print(color5)
                    print(color6)
                    print(color7)
                    print(color8)
                    coords = (x,y)
                    return coords      
                
                if current_series == 3 and current_window == 1 and 791 <= x <=  1186 and 737 <= y <= 950: #Mache Ausnahme von Straße links unten rückgängig
                    positiv_color_standard = 4
                    exception_series3_window1 = "0xEFFFFF"
                if current_series == 5 and current_window == 2:
                    positiv_color_standard = 4

    return -1

def scan_duelists_legendary():
    global current_window
    global current_series
    global dict_window_x
    global dict_window_y
    global positiv_color_legendary

    screen = ImageGrab.grab()
    px = screen.load()
    for x in range(dict_window_x[current_window], 1154, 2):
        for y in range(dict_window_y[current_series], 991, 2):
            scan_color = _RGBtoHex(px[x, y])
            if check_bluecolor_legendary(scan_color) == 1:
                 #Exceptions General-------------------------------------------------------
                if current_window == 4 and 899 <= x <=  923 and 691 <= y <= 724: #dueltelevision in allen Serien
                    continue
                if current_window == 2 and 903 <= x <=  1020 and 779 <= y <= 993: #PVP-Duel-Button in allen Serien
                    continue
                if current_window == 1 and 730 <= x <=  865 and 810 <= y <= 1071: #eventcardtrader
                    continue
                if current_window == 1 and 667 <= x <=  875 and 588 <= y <= 884: #Tourguide
                    continue

                #Exceptions YuGiOh-------------------------------------------------------

                #Exceptions YuGiOh DSOD-------------------------------------------------------

                #Exceptions YuGiOh GX-------------------------------------------------------
               
                #Exceptions YuGiOh GX-------------------------------------------------------

                #Exceptions YuGiOh XYZ-------------------------------------------------------

                color1 = _RGBtoHex(px[x-1, y+1])
                color1_blue = check_bluesurrounding_legendary(color1)
                color2 = _RGBtoHex(px[x, y+1])
                color2_blue = check_bluesurrounding_legendary(color2)
                color3 = _RGBtoHex(px[x+1, y+1])
                color3_blue = check_bluesurrounding_legendary(color3)
                color4 = _RGBtoHex(px[x-1, y])
                color4_blue = check_bluesurrounding_legendary(color4)
                color5 = _RGBtoHex(px[x+1, y])
                color5_blue = check_bluesurrounding_legendary(color5)
                color6 = _RGBtoHex(px[x-1, y-1])
                color6_blue = check_bluesurrounding_legendary(color6)
                color7 = _RGBtoHex(px[x, y-1])
                color7_blue = check_bluesurrounding_legendary(color7)
                color8 = _RGBtoHex(px[x+1, y-1])
                color8_blue = check_bluesurrounding_legendary(color8)
                sum_color = color1_blue + color2_blue + color3_blue + color4_blue + color5_blue + color6_blue + color7_blue + color8_blue
                
                if sum_color >= positiv_color_legendary:

                    print(f"Found at: {x},{y}")
                    print(color1)
                    print(color2)
                    print(color3)
                    print(color4)
                    print(color5)
                    print(color6)
                    print(color7)
                    print(color8)
                    coords = (x,y)
                    return coords      
                
    return -1

def _waitpixel_getting_started(tuple):
    x = tuple[0]
    y = tuple[1]
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        pag.click(x, y)
        pag.click(x+10, y)
        pag.click(x-10, y)
        pag.click(x, y+10)
        pag.click(x, y-10)
        time.sleep(0.3)
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für weißten Pfeil im blauen Kasten unten links
        color_1 = _RGBtoHex(px[577, 1081])
        color_2 = _RGBtoHex(px[627, 1076])
        color_3 = _RGBtoHex(px[601, 1102])            

        if color_1 == "0x00225D" and color_2 == "0x002255" and color_3 == "0xFFFFFF":
            time.sleep(0.5)
            return

def _waitpixel_duel_finished():
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        #_randomclick()
        time.sleep(0.3)
        screen = ImageGrab.grab()
        px = screen.load()
        
        color_1 = _RGBtoHex(px[602, 928])
        color_2 = _RGBtoHex(px[737, 947])
        color_3 = _RGBtoHex(px[950, 1075]) 
        color_4 = _RGBtoHex(px[970, 1084])
         
        if color_1 == "0x062766" and color_2 == "0x093992" and color_3 == "0xFFFFFF" and color_4 == "0xFFFFFF":
            time.sleep(0.5)
            print("finished")
            return

def _waitpixel_chartalk():
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für schwarzes Namesfeld, 3x weißes Textfeld
        color_1 = _RGBtoHex(px[566, 858])
        color_2 = _RGBtoHex(px[615, 1094])
        color_3 = _RGBtoHex(px[816, 1099])
        color_4 = _RGBtoHex(px[1041, 1098])        
        if color_1 == "0x000000" and color_2 == "0xFFFFFF" and color_3 == "0xFFFFFF" and color_4 == "0xFFFFFF":
            time.sleep(0.5)
            return
        pag.click(950,800)
        time.sleep(0.1)
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für schwarzes Namesfeld, 3x weißes Textfeld
        color_1 = _RGBtoHex(px[566, 858])
        color_2 = _RGBtoHex(px[615, 1094])
        color_3 = _RGBtoHex(px[816, 1099])
        color_4 = _RGBtoHex(px[1041, 1098])        
        if color_1 == "0x000000" and color_2 == "0xFFFFFF" and color_3 == "0xFFFFFF" and color_4 == "0xFFFFFF":
            time.sleep(0.5)
            return
        pag.click(950,900)
        time.sleep(0.1)
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für schwarzes Namesfeld, 3x weißes Textfeld
        color_1 = _RGBtoHex(px[566, 858])
        color_2 = _RGBtoHex(px[615, 1094])
        color_3 = _RGBtoHex(px[816, 1099])
        color_4 = _RGBtoHex(px[1041, 1098])        
        if color_1 == "0x000000" and color_2 == "0xFFFFFF" and color_3 == "0xFFFFFF" and color_4 == "0xFFFFFF":
            time.sleep(0.5)
            return
        pag.click(950,1000)
        time.sleep(0.1)
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für schwarzes Namesfeld, 3x weißes Textfeld
        color_1 = _RGBtoHex(px[566, 858])
        color_2 = _RGBtoHex(px[615, 1094])
        color_3 = _RGBtoHex(px[816, 1099])
        color_4 = _RGBtoHex(px[1041, 1098])        
        if color_1 == "0x000000" and color_2 == "0xFFFFFF" and color_3 == "0xFFFFFF" and color_4 == "0xFFFFFF":
            time.sleep(0.5)
            return
        pag.click(950,1050)
        time.sleep(0.1)
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für schwarzes Namesfeld, 3x weißes Textfeld
        color_1 = _RGBtoHex(px[566, 858])
        color_2 = _RGBtoHex(px[615, 1094])
        color_3 = _RGBtoHex(px[816, 1099])
        color_4 = _RGBtoHex(px[1041, 1098])        
        if color_1 == "0x000000" and color_2 == "0xFFFFFF" and color_3 == "0xFFFFFF" and color_4 == "0xFFFFFF":
            time.sleep(0.5)
            return
        pag.click(950,1100)
        time.sleep(0.1)      

def _waitpixel_second_chartalk():
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        #_randomclick()
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für gelb in Duell
        color_1 = _RGBtoHex(px[641, 1047])
        color_2 = _RGBtoHex(px[700, 1047])
        color_3 = _RGBtoHex(px[750, 1047]) 
    

        if color_1 == "0xFFFFFF" and color_2 == "0xFFFFFF" and color_3 == "0xFFFFFF":
            #time.sleep(0.5)
            pag.click(641, 1047)
            return
        else:
            return

def _waitpixel_use_orbs():
    start_timecounter = time.time()#benutzen um 30 sekunden abzuwarten, ob Event-Fenster für Reginald erscheuint. DAS HIER IST FLEXIBEL!
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        #_randomclick()
        time.sleep(0.3)
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für gelb in Duell
        color_1 = _RGBtoHex(px[2700-1920, 214])
        color_2 = _RGBtoHex(px[2771-1920, 228])
        color_3 = _RGBtoHex(px[2815-1920, 219]) 
        color_4 = _RGBtoHex(px[2782-1920, 1025])
        color_5 = _RGBtoHex(px[2853-1920, 1041])           

        if color_1 == "0x072E76" and color_2 == "0x093992" and color_3 == "0xFFFFFF" and color_4 == "0x062865" and color_5 == "0xFFFFFF":
            time.sleep(0.5)
            pag.click(2883-1920, 1038)
            time.sleep(2)
            print("finished")
            return

        end_timecounter = time.time()
        if end_timecounter - start_timecounter >= 3:#warte drei sekunden ob Fenster auftaucht oder nicht
            return

def _use_EXP_booster():
    pag.click(1287, 885)
    time.sleep(0.3)
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für schwarze Kreise der Booster-Möglichkeiten
        color_1 = _RGBtoHex(px[799, 290])
        color_2 = _RGBtoHex(px[799, 456])  
        color_3 = _RGBtoHex(px[799, 625])
        color_4 = _RGBtoHex(px[799, 797])
        
        if color_1 == "0x000000" or color_2 == "0x000000" or color_3 =="0x000000" or color_4 =="0x000000":
            time.sleep(0.5)
            pag.click(799, 456) #EXP-Booster
            time.sleep(2)
            pag.click(956, 1039) #OK
            time.sleep(2)
            return

def _use_orbs():
    global disconnect
    pag.click(591,130)
    while True:
        _check_disconnect()        
        if disconnect == True:
            return
        screen = ImageGrab.grab()
        px = screen.load()
        color_1 = _RGBtoHex(px[929, 217])#P in PvP-Arena, weiß
        color_2 = _RGBtoHex(px[840, 275])#D in Duellkugel, gelb
        color_3 = _RGBtoHex(px[840, 455])#D in Der Landstreicher, gelb      
        if color_1 == "0xFFFFFF" and color_2 == "0xFFCC00" and color_3 == "0xFFCC00":
            break
    time.sleep(0.5)
    pag.click(1018,400)
    while True:
        _check_disconnect()
        if disconnect == True:
            return
        screen = ImageGrab.grab()
        px = screen.load()
        color_1 = _RGBtoHex(px[885, 517])#B in BESTÄTIGEN, weiß
        color_2 = _RGBtoHex(px[833, 571])#D in Duellkugeln, schwarz
        color_3 = _RGBtoHex(px[963, 574])#v in verwenden, schwarz      
        color_4 = _RGBtoHex(px[1087, 654])#J in JA, weiß    
        if color_1 == "0xFFFFFF" and color_2 == "0x000000" and color_3 == "0x000000" and color_4 == "0xFFFFFF":
            break
    time.sleep(0.5)
    pag.click(1092, 666)
    while True:
        _check_disconnect()
        if disconnect == True:
            return
        screen = ImageGrab.grab()
        px = screen.load()
        color_1 = _RGBtoHex(px[908, 487])#D in Duellkugeln, weiß
        color_2 = _RGBtoHex(px[849, 538])#D in Duellkugeln, schwarz
        color_3 = _RGBtoHex(px[852, 570])#A in Anzahl, schwarz      
        color_4 = _RGBtoHex(px[950, 675])#O in OK, weiß    
        if color_1 == "0xFFFFFF" and color_2 == "0x000000" and color_3 == "0x000000" and color_4 == "0xFFFFFF":
            break
    time.sleep(0.5)
    pag.click(965, 682)

            


def seach_n_fight_standard():
    global window_change_counter
    global current_window
    global current_series

    while True:
        while True:
            if window_change_counter == 4:
                window_change_counter = 0
                return
            coords = scan_duelists_standard()
            if coords == -1:
                if current_window == 1:
                    current_window = 2
                    window_change_counter = window_change_counter + 1
                    pag.click(884, 1102)#go to duel window
                    print(window_change_counter)
                    time.sleep(2)
                elif current_window == 2:
                    current_window = 3
                    window_change_counter = window_change_counter + 1
                    pag.click(1055, 1101)#go to shop window
                    print(window_change_counter)
                    time.sleep(2)
                elif current_window == 3:
                    current_window = 4
                    window_change_counter = window_change_counter + 1
                    pag.click(1247, 1106)#go to cards window
                    print(window_change_counter)
                    time.sleep(2)
                elif current_window == 4:
                    current_window = 1
                    window_change_counter = window_change_counter + 1
                    pag.click(693, 1095)#go to gate window
                    print(window_change_counter)
                    time.sleep(2)
            else:
                break
        _waitpixel_getting_started(coords)
        if disconnect == True:
            break
        if use_exp_booster == True:
            _use_EXP_booster()
        time.sleep(1)
        pag.click(1145, 993)#Autoduel
        time.sleep(5)
        _waitpixel_duel_finished()
        if disconnect == True:
            break
        pag.click(942, 1082)#OK            
        if disconnect == True:
            break
        _waitpixel_chartalk()
        if disconnect == True:
            break
        time.sleep(4)
        pag.click(1041, 1098)#click auf weißes feld um ins Startmenü zu kommen
        time.sleep(1)
        _waitpixel_second_chartalk()#checkt, ob es einen zweiten weißen dialog gibt, wenn ja klickt er ihn weg.
        time.sleep(1)
        _waitpixel_use_orbs()
        _duel_count_and_log()

def seach_n_fight_legendary():
    global window_change_counter
    global current_window
    global current_series

    while True:
        while True:
            if window_change_counter == 4:
                window_change_counter = 0
                return
            coords = scan_duelists_legendary()
            if coords == -1:
                if current_window == 1:
                    current_window = 2
                    window_change_counter = window_change_counter + 1
                    pag.click(884, 1102)#go to duel window
                    time.sleep(2)
                elif current_window == 2:
                    current_window = 3
                    window_change_counter = window_change_counter + 1
                    pag.click(1055, 1101)#go to shop window
                    time.sleep(2)
                elif current_window == 3:
                    current_window = 4
                    window_change_counter = window_change_counter + 1
                    pag.click(1247, 1106)#go to cards window
                    time.sleep(2)
                elif current_window == 4:
                    current_window = 1
                    window_change_counter = window_change_counter + 1
                    pag.click(693, 1095)#go to gate window
                    time.sleep(2)
            else:
                break
        _waitpixel_getting_started(coords)
        if disconnect == True:
            break
        pag.click(1145, 993)#Autoduel
        time.sleep(5)
        _waitpixel_duel_finished()
        if disconnect == True:
            break
        pag.click(942, 1082)#OK            
        if disconnect == True:
            break
        _waitpixel_chartalk()
        if disconnect == True:
            break
        time.sleep(5)
        pag.click(1041, 1098)#click auf weißes feld um ins Startmenü zu kommen
        _waitpixel_use_orbs()
        _duel_count_and_log()    

def _read_and_log_old_logfile_text():
    duelcount_text = ""
    handle_duelcount = open("duellog.txt", "r", encoding="utf-8")#reads logfile
    list_lines = handle_duelcount.readlines()
    handle_duelcount.close()
    try: #Falls der log-file leer ist wird es kein list_lines[-1] geben -> Index Error
        list_split = list_lines[-1].split(":")
    except IndexError:#catch index error -> manually creates empty list -> list_split[0] = ""!
        list_split = [""]
    if list_split[0] == "":
        duelcount_text = str(localtime) + "\n"
    elif list_split[0] == "Duels won":
        for i in range(0,(len(list_lines)-1),1): #nimmt den ganzen Text mit außer der letzten Zeile, also KEIN "Duels won: x". Range(i,j,k)-> j ist exklusive in python!
            duelcount_text = duelcount_text + str(list_lines[i])
    elif list_split[0] == "Disconnected!!!!":
        for i in range(0,len(list_lines),1): #nimmt den ganzen Text mit! Range(i,j,k)-> j ist exklusive in python!
            duelcount_text = duelcount_text + str(list_lines[i])
    handle_duelcount = open("duellog.txt", "w", encoding="utf-8")#opens logfile for (over)writing
    handle_duelcount.write(duelcount_text)
    handle_duelcount.close()

def _duel_count_and_log():
    global start_timecounter_calc
    global duelcount
    end_timecounter_calc = time.time()
    minutes = (end_timecounter_calc-start_timecounter_calc)/60 #time passed since script was started in minutes
    duels_per_minute = "{:.2f}".format((duelcount/minutes)) #formates the duels/min in a string and ROUNDS the Value to 2 decimal points
    _read_and_log_old_logfile_text()
    handle_duelcount = open("duellog.txt", "a", encoding="utf-8")#opens logfile for appending text
    handle_duelcount.write(f"Duels won: {duelcount}\t{duels_per_minute} Duels / min\n")
    handle_duelcount.close()
    duelcount = duelcount + 1

def _randomclick():
    dict_click_x = {1: (2657-1920),
        2: (2730-1920),
        3: (2804-1920),
        4: (2860-1920),
        5: (2923-1920),
        6: (2979-1920)
        }
    dict_click_y = {1: (887),
        2: (910),
        3: (960)
        }
    x = dict_click_x[random.randint(1,6)]
    y = dict_click_y[random.randint(1,3)]
    pag.click(x, y)

while True:
    start_timecounter_calc = time.time()#timestamp for Duels/min - calculation at the end of outer While loop
    if disconnect == True:        
        time.sleep(5)#5 sekunden bis programm startet
        pag.click(954,722)#neustart
        time.sleep(20)
        pag.click(954,722)#verbindung herstellen
        time.sleep(30)
        pag.click(615,1103)#mitteilungen wegclicken
        time.sleep(5)
        start_timecounter = time.time()#benutzen um 30 sekunden abzuwarten, ob Event-Fenster für Reginald erscheuint. DAS HIER IST FLEXIBEL!
        while True:            
            screen = ImageGrab.grab()
            px = screen.load()
            #coordinaten für schwarzes Namesfeld, 3x weißes Textfeld
            color_1 = _RGBtoHex(px[723, 450])
            color_2 = _RGBtoHex(px[856, 447])
            color_3 = _RGBtoHex(px[955, 446])
            color_4 = _RGBtoHex(px[1084, 446])     
            color_5 = _RGBtoHex(px[785, 476])     
            if color_1 == "0xFFFFFF" and color_2 == "0xFFFFFF" and color_3 == "0xFFFFFF" and color_4 == "0xFFFFFF" and color_5 == "0x112233":
                time.sleep(2)
                pag.click(844,784)#schließ charakterfeld
                time.sleep(30)
                break
            end_timecounter = time.time()
            if end_timecounter - start_timecounter >= 30:
                break   
        pag.click(1262,1098)#klick auf Karten, um doppelklick auf Tor zu vermeiden
        time.sleep(30)
        pag.click(664,1104)#klicke auf Tor
        current_window = 1
        time.sleep(30)
        disconnect = False

    if disconnect == False:
        if round_counter == 1:
            time.sleep(2)#2 sekunden bis programm startet
            if check_standard_duelist_left() == True:
                seach_n_fight_standard()
            print("legendary inc")
            seach_n_fight_legendary()
            time.sleep(0.5)
            pag.click(599,400)
            time.sleep(0.5)
            if current_series == 1:
                pag.click(712, 515)
                current_series = 2
                series_change_counter = series_change_counter + 1
            elif current_series == 2:
                pag.click(712, 615)
                current_series = 3
                series_change_counter = series_change_counter + 1
            elif current_series == 3:
                pag.click(712, 728)
                current_series = 4
                series_change_counter = series_change_counter + 1
            elif current_series == 4:
                pag.click(712, 845)
                current_series = 5
                series_change_counter = series_change_counter + 1        
            elif current_series == 5:
                pag.click(712, 399)
                current_series = 1
                series_change_counter = series_change_counter + 1
            if series_change_counter == 5:
                round_counter = round_counter +1    
            time.sleep(10)
        else:
            time.sleep(2)#2 sekunden bis programm startet
            if check_standard_duelist_left() == False:
                _use_orbs()
                time.sleep(1.0)            
            seach_n_fight_standard()
            round_counter = round_counter + 1
            if round_counter == wanted_rounds:
                round_counter = 1

