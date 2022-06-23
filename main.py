import time
import pyautogui
from pynput.keyboard import Listener
from pynput import mouse
from pynput.mouse import Button
import threading
import datetime

is_stop = False
is_record_finish = False
start_record = False
pos = []
each_delay = [] #与pos number保持一致
cur_time = 0

def mouse_recorder():
    while not is_record_finish:
        global pos
        _pos = pyautogui.position()
        pos.append(_pos)

def on_press(key):
    global is_stop
    global is_record_finish
    global start_record
    if(key.name == 'space'):
        if is_record_finish:
            if not is_stop:
                is_stop = True
                print("===程序结束===")
                quit()
        # 开始录制
        elif not start_record:
            print("===开始录制===")
            start_record = True

    if(key.name == 'enter' and not is_record_finish):
        is_record_finish = True
        start_record = False
        print("===录制结束,开始执行,按空格键结束===")
        MouseListener.stop()

        # 录制完成之后，添加一轮时间间隔
        d = datetime.datetime.now() - cur_time
        seconds = d.days * 24 * 60 * 60 + d.seconds + d.microseconds / 1000000
        each_delay.append(seconds)
        try:
            click_thread = threading.Thread(target=sim_click, args=[])
            click_thread.start()
        except:
            print("无法启动线程")

def on_click(x, y, button, pressed):
    global pos
    global each_delay
    global cur_time
    if pressed and start_record:
        if len(pos) == 0 :
            cur_time = datetime.datetime.now()
        else:
            temp_time = datetime.datetime.now()
            d = temp_time - cur_time
            cur_time = temp_time
            seconds = d.days * 24 * 60 * 60 + d.seconds + d.microseconds / 1000000
            each_delay.append(seconds)
        print("记录点击位置:",(x,y))
        pos.append((x, y))
    else:
       pass

def sim_click():
    count = 0
    while not is_stop:
        for i,ivalue in enumerate(pos):
            pyautogui.moveTo(ivalue)
            pyautogui.click()
            if i == len(pos) -1:
                count += 1
                print("执行次数:",count)
            time.sleep(each_delay[i])

if __name__ == '__main__':
    print("===按空格键开始录制,录制完成按Enter开始执行===")

    MouseListener =  mouse.Listener(on_click=on_click)
    MouseListener.start()

    with Listener(on_press=on_press) as Keylistener:
        Keylistener.join()









