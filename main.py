# dggochi

from ssd1327 import SSD1327_I2C
import time
from machine import SoftI2C, Pin, I2C
import _thread
import paints
import music

SDA_PIN_NUM=12
SCL_PIN_NUM=13
BTN_1_PIN_NUM=26
BTN_2_PIN_NUM=27
BTN_3_PIN_NUM=28
SPK_PIN_NUM=15

btns = [
    Pin(BTN_1_PIN_NUM, Pin.IN),
    Pin(BTN_2_PIN_NUM, Pin.IN),
    Pin(BTN_3_PIN_NUM, Pin.IN)
]
spk=Pin(SPK_PIN_NUM, Pin.OUT)

btn_state=[0, 0, 0]
btn_duration=[0, 0, 0]



def listen_btn(action, stop_cond):
    while not stop_cond():
        for btn in btns:
            if stop_cond():
                print('stop button listening')
                break
            btn_idx = btns.index(btn)
            btn_num = btn_idx + 1
            if btn_state[btn_idx]:
                if not btn.value():
                    action()
                    btn_state[btn_idx] = 0
                else:
                    if time.ticks_ms() - btn_duration[btn_idx] > 500:
                        action()
            else:
                if btn.value():
                    action()
                    btn_state[btn_idx] = 1
                    btn_duration[btn_idx]=time.ticks_ms()
            time.sleep(0.01)

#_thread.start_new_thread(button_runner, ())
# change into annonymous function

music.volumn=300
_thread.start_new_thread(music.playsong_loop, (music.sample_song))

# i2c = SoftI2C(sda=Pin(SDA_PIN_NUM), scl=Pin(SCL_PIN_NUM))
i2c = I2C(0, sda=Pin(SDA_PIN_NUM), scl=Pin(SCL_PIN_NUM), freq=200000)
oled = SSD1327_I2C(128, 128, i2c)

def detect_btn():
    pressed_btn=[]
    for btn in btns:
        if btn.value():
            pressed_btn.append(btns.index(btn) + 1)
    return pressed_btn
            
        
def print_line(string, a=0, b=0, c=255):
    oled.fill(0)
    oled.text(string , 0, 0, 255)
    oled.show()
    
    
def print_btn():
    btn_num = detect_btn()
    if btn_num :
        print_line(f'button {btn_num} is pressed')
    else :
        print_line('')
    
def tmp_func():
    return btn_state[0] * btn_state[1] * btn_state[2]
    
listen_btn(print_btn, tmp_func)

music.volumn=0
music.music_running=False
print_line('end program')


