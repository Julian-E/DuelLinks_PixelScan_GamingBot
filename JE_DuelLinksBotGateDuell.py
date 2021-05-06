from PIL import ImageGrab
import datetime
import pyautogui as pag
import time
import sys
import keyboard
import random
import os

desktop = os.path.expanduser("~/Desktop") #desktop location
duelcount = 1 #für log file benötigt
disconnect = False #needed, to see in the outer while loop, where the program shall start. If False, the program will start in game without loggin in.
localtime = time.asctime( time.localtime(time.time()) ) #timestamp when script beginns
start_timecounter_calc = time.time()#timestamp for Duels/min - calculation at the end of outer While loop
handle_duelcount = open(f"{desktop}/duellog.txt", "w", encoding="utf-8")#creates new duellog-file
print(handle_duelcount)
#handle_duelcount.write(f"Disconnected!!!!: {localtime}\n")#FOR TESTING-> NEEDS TO BE DELETED AT THE END
handle_duelcount.close()#closes new duellog-file. File should be empty

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
        handle_duelcount = open(f"{desktop}/duellog.txt", "a", encoding="utf-8")#opens logfile for appending text
        handle_duelcount.write(f"Duels won: {duelcount}\t{duels_per_minute} Duels / min\nDisconnected!!!!: {timestamp}\n")
        handle_duelcount.close()
        duelcount = 0  
        disconnect = True        
        return

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

def _getpixel(x,y):
    screen = ImageGrab.grab()
    #screen.show()
    px = screen.load()
    color = px[x,y]
    #print(color)
    return _RGBtoHex((color))

def _waitpixel(x,y,color, color2 = ""):
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        pixelcolor = _getpixel(x,y)
        #print(color)
        #print(color2)
        if pixelcolor == color or pixelcolor == color2:
            time.sleep(1)
            break

def _waitpixel_getting_started():
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        pag.click(1087, 531)
        time.sleep(0.3)
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für gelb in Duell
        color_1 = _RGBtoHex(px[927, 997])      

        if color_1 == "0xF9CE22" or color_1 == "0xF9D426":
            time.sleep(0.5)
            return

def _waitpixel_second_duell_button():
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        pag.click(700, 999)
        time.sleep(0.3)
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für gelb in Duell
        color_1 = _RGBtoHex(px[927, 997])      

        if color_1 == "0xF9CE22" or color_1 == "0xF9D426" or color_1 =="0xFACD21":
            time.sleep(0.5)
            return

def _use_EXP_booster():
    global disconnect
    pag.click(1287, 885)
    while True:
        _check_disconnect()
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
            break
    pag.click(799, 456) #EXP-Booster
    time.sleep(1)
    pag.click(956, 1039) #OK
    while True:
        _check_disconnect()
        if disconnect == True:
            return
        screen = ImageGrab.grab()
        px = screen.load()
        color_1 = _RGBtoHex(px[927, 1001])#D in Duell, gelb 
        color_2 = _RGBtoHex(px[968, 1002])#e in Duell, gelb
        color_3 = _RGBtoHex(px[1328, 895])#Gegenständefenster, hellblau leuchtend (wird so, wenn ein booster aktiviert ist)     

        if color_1 == "0xFAC51C" or color_2 == "0xF9CF23" or color_3 =="0x04BBFF":
            time.sleep(1)
            return      

def _waitpixel_beginner1():
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        pag.click(927, 906)#random click um den start schneller zu machen
        time.sleep(0.3)
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für Erster: w,w
        color_1 = _RGBtoHex(px[2855-1920,701]) #T in ERSTER
        color_2 = _RGBtoHex(px[2980-1920,701]) #n in dran
        #coordinaten für Zweiter: w,w
        color_3 = _RGBtoHex(px[2862-1920,701])
        color_4 = _RGBtoHex(px[2988-1920,701])
        #Hilfskoordinaten: w,s
        color_5 = _RGBtoHex(px[3170-1920,918]) #4 in 4000 eigene lebensanzeige
        color_6 = _RGBtoHex(px[3128-1920,955]) #schwarz in P von (LP:) 

        #if keyboard.read_key() == "q":
        #    print(color_1)
        #    print(color_2)
        #    print(color_3)
        #    print(color_4)
        #    print(color_5)
        if color_1 == "0xFFFFFF" and color_2 == "0xFFFFFF" and color_5 == "0xFFFFFF" and color_6 == "0x000000":
            beginner = True
            return beginner
        elif color_3 == "0xFFFFFF" and color_4 == "0xFFFFFF" and color_5 == "0xFFFFFF" and color_6 == "0x000000":
            beginner = False
            return beginner
        
def _waitpixel_draw():
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für gelb in "Deine Phase" und schwarz in mitten des Kartenstapels
        color_1 = _RGBtoHex(px[3066-1920,124])
        color_2 = _RGBtoHex(px[2877-1920,528])
        #coordinaten für sprachbox Gegner zum wegklicken: w,w
        color_3 = _RGBtoHex(px[664,284])
        color_4 = _RGBtoHex(px[666,284])
        #coordinaten für sprachbox ich zum wegklicken: w,w
        color_5 = _RGBtoHex(px[1271,856])
        color_6 = _RGBtoHex(px[1273,856])

        if color_1 == "0xFFCC00" and color_2 == "0x000000":
            time.sleep(0.5)
            return
        elif color_3 == "0xFFFFFF" and color_4 == "0xFFFFFF":
            _randomclick()#random click um sprachdialog abzukürzen
            time.sleep(0.5)
        elif color_5 == "0xFFFFFF" and color_6 == "0xFFFFFF":
            _randomclick()#random click um sprachdialog abzukürzen
            time.sleep(0.5)

def _waitpixel_battlephase():
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für battlephase message; s,w,s
        color_1 = _RGBtoHex(px[1023,553])
        color_2 = _RGBtoHex(px[1083,664])
        color_3 = _RGBtoHex(px[994, 559])
        if color_1 == "0x000000" and color_2 == "0xFFFFFF" and color_3 == "0x000000":
            time.sleep(0.5)
            return

def _waitpixel_phasebutton():
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        _randomclick()#random click um sprachdialog abzukürzen
        time.sleep(0.3)
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für phasebutton: w, w
        color_1 = _RGBtoHex(px[3230-1920,721])
        color_2 = _RGBtoHex(px[3238-1920,721])
        #coordinaten für sprachbox Gegner zum wegklicken: w,w

        if color_1 == "0xFFFFFF" and color_2 == "0xFFFFFF":
            time.sleep(0.5)
            return

def _waitpixel_phasebutton_end():
    while True:
        _check_disconnect()
        global disconnect
        if disconnect == True:
            return
        a = False
        screen = ImageGrab.grab()
        px = screen.load()
        #coordinaten für phasebutton + schwarz in eigener LP Anzeige (in P), da der ganze bildschirm weiß wird. Würde falschen Button simulieren.: w, w, s
        color_1 = _RGBtoHex(px[3230-1920,721])
        color_2 = _RGBtoHex(px[3238-1920,721])
        color_3 = _RGBtoHex(px[3129-1920,955])
        #coordinaten für sprachbox Gegner zum wegklicken: w,w
        color_4 = _RGBtoHex(px[664,284])
        color_5 = _RGBtoHex(px[666,284])
        #coordinaten für sprachbox ich zum wegklicken: w,w
        color_6 = _RGBtoHex(px[1271,856])
        color_7 = _RGBtoHex(px[1273,856])
        #coordinaten für Ende(oben im E; oben im N, im O von OK): w,w,w
        color_8 = _RGBtoHex(px[904,571])
        color_9 = _RGBtoHex(px[1035,571])
        color_10 = _RGBtoHex(px[959,1084])

        if color_1 == "0xFFFFFF" and color_2 == "0xFFFFFF" and color_3 == "0x000000":
            time.sleep(0.5)
            return a
        elif color_4 == "0xFFFFFF" and color_5 == "0xFFFFFF":
            _randomclick()#random click um sprachdialog abzukürzen
            time.sleep(0.5)
        elif color_6 == "0xFFFFFF" and color_7 == "0xFFFFFF":
            _randomclick()#random click um sprachdialog abzukürzen
            time.sleep(0.5)
        elif color_8 == "0xFFFFFF" and color_9 == "0xFFFFFF" and color_10 == "0xFFFFFF":
            pag.click(959, 1084)#Click auf OK um Duell zu beenden
            time.sleep(0.5)
            a = True
            return a 

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

def _read_and_log_old_logfile_text():
    duelcount_text = ""
    handle_duelcount = open(f"{desktop}/duellog.txt", "r", encoding="utf-8")#reads logfile
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
    handle_duelcount = open(f"{desktop}/duellog.txt", "w", encoding="utf-8")#opens logfile for (over)writing
    handle_duelcount.write(duelcount_text)
    handle_duelcount.close()
    
def _duel_count_and_log():
    global start_timecounter_calc
    global duelcount
    end_timecounter_calc = time.time()
    minutes = (end_timecounter_calc-start_timecounter_calc)/60 #time passed since script was started in minutes
    duels_per_minute = "{:.2f}".format((duelcount/minutes)) #formates the duels/min in a string and ROUNDS the Value to 2 decimal points
    _read_and_log_old_logfile_text()
    handle_duelcount = open(f"{desktop}/duellog.txt", "a", encoding="utf-8")#opens logfile for appending text
    handle_duelcount.write(f"Duels won: {duelcount}\t{duels_per_minute} Duels / min\n")
    handle_duelcount.close()
    duelcount = duelcount + 1

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
        time.sleep(30)
        disconnect = False

    if disconnect == False:
        time.sleep(5)#5 sekunden bis programm startet
        while True:
            _waitpixel_getting_started()
            if disconnect == True:
                break
            #pag.click(927, 997)#Duell
            #_waitpixel(927, 997, "0xF9CE22", color2="0xF9D426")#gelb bei Duell Button
            pag.click(927, 997)#Duell
            _waitpixel_second_duell_button()
            if disconnect == True:
                break
            #_use_EXP_booster() #wird exp booster verwenden. Kann auskommentiert werden, um keinen zu benutzen.
            pag.click(927, 999)#Duell
            beginner = _waitpixel_beginner1()
            if disconnect == True:
                break
            if beginner == True:
                _waitpixel_phasebutton()
                if disconnect == True:
                    break
                pag.moveTo(946, 1028)#zieht mittlere Karte
                pag.dragTo(966, 870, 0.3, button='left')#zieht mittlere Karte
                _waitpixel(856, 878, '0xFFFFFF')#warter auf weiß in Normalbeschwörung
                if disconnect == True:
                    break
                pag.click(856, 878)#Normalbeschwörung
                _waitpixel_phasebutton()
                if disconnect == True:
                    break
                pag.click(1300, 741)#phase wechseln
                time.sleep(1)#warten bis dialogfenster sich ändert
                pag.click(1242, 773)#Zug beenden
                _waitpixel_draw()
                if disconnect == True:
                    break
                pag.click(2889-1920, 781)#ziehen
                time.sleep(1)
                pag.click(2889-1920, 781)#ziehen
                time.sleep(1)
                pag.moveTo(946, 1028)#zieht mittlere Karte
                pag.dragTo(966, 870, 0.3, button='left')#zieht mittlere Karte
                _waitpixel(856, 878, '0xFFFFFF')#warter auf weiß in Normalbeschwörung
                if disconnect == True:
                    break
                pag.click(856, 878)#Normalbeschwörung
                _waitpixel_phasebutton()
                if disconnect == True:
                    break
                pag.moveTo(2881-1920, 668)#AngriffKarte1->Phasenwechsel
                pag.dragTo(2881-1920, 545, 0.3, button='left')#AngriffKarte1->Phasenwechsel
                _waitpixel_battlephase()
                if disconnect == True:
                    break
                pag.click(1086, 674)
                time.sleep(1)
                pag.moveTo(2881-1920, 668)#AngriffKarte1
                pag.dragTo(2881-1920, 545, 0.3, button='left')#AngriffKarte1
                _waitpixel_phasebutton()
                if disconnect == True:
                    break
                pag.moveTo(3006-1920, 668)#AngriffKarte2
                pag.dragTo(3006-1920, 545, 0.3, button='left')#AngriffKarte2
                _waitpixel_phasebutton()
                if disconnect == True:
                    break
                pag.click(1300, 741)#phase wechseln
                time.sleep(1)#warten bis dialogfenster sich ändert
                pag.click(1242, 773)#Zug beenden
                _waitpixel_draw()
                if disconnect == True:
                    break
                pag.click(2889-1920, 781)#ziehen
                time.sleep(1)
                pag.click(2889-1920, 781)#ziehen
                time.sleep(1)    
                while True: #letzte Angriffswelle
                    pag.moveTo(2881-1920, 668)#AngriffKarte1->Phasenwechsel
                    pag.dragTo(2881-1920, 545, 0.3, button='left')#AngriffKarte1->Phasenwechsel
                    _waitpixel_battlephase()
                    if disconnect == True:
                        break
                    pag.click(1086, 674)
                    time.sleep(1)
                    pag.moveTo(2881-1920, 668)#AngriffKarte1
                    pag.dragTo(2881-1920, 545, 0.3, button='left')#AngriffKarte1
                    end = _waitpixel_phasebutton_end()
                    if disconnect == True:
                        break
                    if end == True:
                        #print("Duell finished; Attacke1")
                        break
                    pag.moveTo(3006-1920, 668)#AngriffKarte2
                    pag.dragTo(3006-1920, 545, 0.3, button='left')#AngriffKarte2
                    end = _waitpixel_phasebutton_end()
                    if disconnect == True:
                        break
                    if end == True:
                        #print("Duell finished; Attacke2")
                        break
                    pag.click(1300, 741)#phase wechseln
                    time.sleep(1)#warten bis dialogfenster sich ändert
                    pag.click(1242, 773)#Zug beenden
                    _waitpixel_draw()
                    if disconnect == True:
                        break
                    pag.click(2889-1920, 781)#ziehen
                    time.sleep(1)
                    pag.click(2889-1920, 781)#ziehen
                    time.sleep(1)

            if beginner == False:
                _waitpixel_draw()
                if disconnect == True:
                        break
                pag.click(2889-1920, 781)#ziehen
                time.sleep(1)
                pag.click(2889-1920, 781)#ziehen
                time.sleep(1)
                pag.moveTo(946, 1028)#zieht mittlere Karte
                pag.dragTo(966, 870, 0.3, button='left')#zieht mittlere Karte
                _waitpixel(856, 878, '0xFFFFFF')#warter auf weiß in Normalbeschwörung
                if disconnect == True:
                        break
                pag.click(856, 878)#Normalbeschwörung
                _waitpixel_phasebutton()
                if disconnect == True:
                        break
                pag.moveTo(2881-1920, 668)#AngriffKarte1->Phasenwechsel
                pag.dragTo(2881-1920, 545, 0.3, button='left')#AngriffKarte1->Phasenwechsel
                _waitpixel_battlephase()
                if disconnect == True:
                        break
                pag.click(1086, 674)
                time.sleep(1)
                pag.moveTo(2881-1920, 668)#AngriffKarte1
                pag.dragTo(2881-1920, 545, 0.3, button='left')#AngriffKarte1
                _waitpixel_phasebutton()
                if disconnect == True:
                        break
                pag.click(1300, 741)#phase wechseln
                time.sleep(1)#warten bis dialogfenster sich ändert
                pag.click(1242, 773)#Zug beenden
                _waitpixel_draw()
                if disconnect == True:
                        break
                pag.click(2889-1920, 781)#ziehen
                time.sleep(1)
                pag.click(2889-1920, 781)#ziehen
                time.sleep(1)
                pag.moveTo(946, 1028)#zieht mittlere Karte
                pag.dragTo(966, 870, 0.3, button='left')#zieht mittlere Karte
                _waitpixel(856, 878, '0xFFFFFF')#warter auf weiß in Normalbeschwörung
                if disconnect == True:
                        break
                pag.click(856, 878)#Normalbeschwörung
                _waitpixel_phasebutton()
                if disconnect == True:
                        break
                while True: #letzte Angriffswelle
                    pag.moveTo(2881-1920, 668)#AngriffKarte1->Phasenwechsel
                    pag.dragTo(2881-1920, 545, 0.3, button='left')#AngriffKarte1->Phasenwechsel
                    _waitpixel_battlephase()
                    if disconnect == True:
                        break
                    pag.click(1086, 674)
                    time.sleep(1)
                    pag.moveTo(2881-1920, 668)#AngriffKarte1
                    pag.dragTo(2881-1920, 545, 0.3, button='left')#AngriffKarte1
                    end = _waitpixel_phasebutton_end()
                    if disconnect == True:
                        break
                    if end == True:
                        #print("Duell finished; Attacke1")
                        break
                    pag.moveTo(3006-1920, 668)#AngriffKarte2
                    pag.dragTo(3006-1920, 545, 0.3, button='left')#AngriffKarte2
                    end = _waitpixel_phasebutton_end()
                    if disconnect == True:
                        break
                    if end == True:
                        #print("Duell finished; Attacke2")
                        break
                    pag.click(1300, 741)#phase wechseln
                    time.sleep(1)#warten bis dialogfenster sich ändert
                    pag.click(1242, 773)#Zug beenden
                    _waitpixel_draw()
                    if disconnect == True:
                        break
                    pag.click(2889-1920, 781)#ziehen
                    time.sleep(1)
                    pag.click(2889-1920, 781)#ziehen
                    time.sleep(1)
            
            if disconnect == True:
                break
            _waitpixel_chartalk()
            if disconnect == True:
                break
            pag.click(1041, 1098)#click auf weißes feld um ins Startmenü zu kommen
            _duel_count_and_log()


