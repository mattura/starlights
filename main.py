import plasma
from plasma import plasma2040
from pimoroni import RGBLED, Button
from random import randrange, uniform

NUM_LEDS = 66

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT,rgbw=False, color_order=plasma.COLOR_ORDER_RGB)

led_strip.start()

current_leds = [[0] * 3 for i in range(NUM_LEDS)]
target_leds = [[0] * 3 for i in range(NUM_LEDS)]
FADE_UP_SPEED = 255
FADE_DOWN_SPEED = 10
S_INTENSITY = 0.03
B_COLOUR = [3, 5, 5]
S_COLOUR = [240, 255, 255]
SPEED_FACTOR = 1

#These 'presets' contain a base colour, sparkle colour, fade-up-speed, fade-down-speed and intensity
#They are consistent with presets in the LightJar code (https://github.com/mattura/lightjar)
#Use the html file to create your own (unless you speak hex!)
presets = {
          'Off': '#000000#000000#010101',
          'Carrot & Parsnip': '#D2691E#FFFFFF#030305',
          'Warm Rainbows': '#D2691E#004444#01010A',
          'Jewel of the Nile': '#D2691E#4B0082#01013C',
          'Soft Snow': '#222222#CCCCEE#0C013C',
          'NightJar': '#440000#000000#010101',
          'Caustic Water': '#004444#87CEEB#010CC8',
          'Aquamarine': '#004444#2E8B57#010164',
          'Skeleton': '#2E8B57#8B4513#02023C',
          'Poison Potion': '#004400#00FF00#02023C',
          'Christmas Tree': '#00FF00#FF0000#03023C',
          'Key Lime Pie': '#444400#FFC096#02020A',
          'Ice Cream': '#FF60CF#FFFF00#0C020A',
          #New colours for the summer!!!
          'Wheat Field': '#D2691E#441100#01010A',
          'Summer Blush': '#D26932#440000#010220',
          'Warm Snow': '#222222#CCAAAA#0C013C',
          'Night Red':'#390000#270000#010110',
}

preset_order = [
    'Off',
    'Summer Blush',
    'Wheat Field',
    'Carrot & Parsnip',
    'Warm Snow',
    'Jewel of the Nile',
    'Ice Cream',
    'Caustic Water',
    'Night Red'
]
preset = 1	#Starting preset

def hex_to_rgb(hex_colour):
    """Convert a hex colour string to an RGB tuple."""
    hex_colour = hex_colour.lstrip('#')
    bigint = int(hex_colour, 16)
    r = (bigint >> 16) & 255
    g = (bigint >> 8) & 255
    b = bigint & 255
    return [r, g, b]

def sparkle():
    for i in range(NUM_LEDS):
        # randomly add sparkles
        if S_INTENSITY > uniform(0, 1):
            # set a target to start a sparkle
            target_leds[i] = S_COLOUR
        # for any sparkles that have achieved max sparkliness, reset them to background
        if current_leds[i] == target_leds[i]:
            target_leds[i] = B_COLOUR
    move_to_target()   # nudge our current colours closer to the target colours
    display_current()  # display current colours to strip

def display_current():
    # paint our current LED colours to the strip
    for i in range(NUM_LEDS):
        led_strip.set_rgb(i, int(current_leds[i][0]), int(current_leds[i][1]), int(current_leds[i][2]))

def move_to_target():
    # nudge our current colours closer to the target colours
    for i in range(NUM_LEDS):
        for c in range(3):  # 3 times, for R, G & B channels
            if current_leds[i][c] < target_leds[i][c]:
                current_leds[i][c] = min(current_leds[i][c] + FADE_UP_SPEED, target_leds[i][c])  # increase current, up to a maximum of target
            elif current_leds[i][c] > target_leds[i][c]:
                current_leds[i][c] = max(current_leds[i][c] - FADE_DOWN_SPEED, target_leds[i][c])  # reduce current, down to a minimum of target

def set_from_presets():
    global B_COLOUR, S_COLOUR, FADE_UP_SPEED, FADE_DOWN_SPEED, S_INTENSITY
    n = preset_order[preset]
    hash = presets[n]
    #print(n)
    hex_list = [hash[i:i+7] for i in range(0, len(hash), 7)]
    B_COLOUR = hex_to_rgb(hex_list[0])
    S_COLOUR = hex_to_rgb(hex_list[1])
    fufdi = hex_to_rgb(hex_list[2])
    FADE_UP_SPEED = fufdi[0] / 1
    FADE_DOWN_SPEED = fufdi[1] / 1
    S_INTENSITY = fufdi[2] / 10000 / SPEED_FACTOR

led = RGBLED(plasma2040.LED_R, plasma2040.LED_G, plasma2040.LED_B)
led.set_rgb(0, 0, 255)
button_a = Button(plasma2040.BUTTON_A)
button_b = Button(plasma2040.BUTTON_B)
button_boot = Button(plasma2040.USER_SW)
led.set_rgb(0, 0, 0)

set_from_presets()

while True:
    sparkle()
    if button_b.read():	#TODO: Debounce
        preset += 1
        if preset >= len(preset_order):
            preset = 0
        set_from_presets()
    if button_a.read():
        preset -= 1
        if preset < 0:
            preset = len(preset_order) - 1
        set_from_presets()
