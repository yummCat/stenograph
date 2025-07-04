import board
import digitalio
import time

los_switches = {
    "SW1":  {"row": 1, "col": 0, "key": "S"},
    "SW2":  {"row": 0, "col": 1, "key": "T"},
    "SW3":  {"row": 1, "col": 1, "key": "K"},
    "SW4":  {"row": 0, "col": 2, "key": "P"},
    "SW5":  {"row": 1, "col": 2, "key": "W"},
    "SW6":  {"row": 2, "col": 2, "key": "A"},
    "SW7":  {"row": 0, "col": 3, "key": "H"},
    "SW8":  {"row": 1, "col": 3, "key": "R"},
    "SW9":  {"row": 2, "col": 3, "key": "O"},
    "SW10": {"row": 0, "col": 4, "key": "*"},
    "SW11": {"row": 2, "col": 4, "key": "#"},
    "SW12": {"row": 0, "col": 5, "key": "F"},
    "SW13": {"row": 1, "col": 5, "key": "R"},
    "SW14": {"row": 2, "col": 5, "key": "E"},
    "SW15": {"row": 0, "col": 6, "key": "P"},
    "SW16": {"row": 1, "col": 6, "key": "B"},
    "SW17": {"row": 2, "col": 6, "key": "U"},
    "SW18": {"row": 0, "col": 7, "key": "L"},
    "SW19": {"row": 1, "col": 7, "key": "G"},
    "SW20": {"row": 0, "col": 8, "key": "T"},
    "SW21": {"row": 1, "col": 8, "key": "S"},
    "SW22": {"row": 0, "col": 9, "key": "D"},
    "SW23": {"row": 1, "col": 9, "key": "Z"}
}

switch_matrix = {(data["row"], data["col"]): data["key"] for data in los_switches.values()}

los_row_pins_yay = [board.GP12, board.GP11, board.GP10]
los_col_pins_yay = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9]

PLOVER_ORDER = "#STKPWHRAO*FRPBLGTSDZ"
DEBOUNCE_DELAY = 0.01

def set_pins_yay():
    rows, cols = [], []
    for pin in los_row_pins_yay:
        r = digitalio.DigitalInOut(pin)
        r.direction = digitalio.Direction.OUTPUT
        r.value = True
        rows.append(r)
    for pin in los_col_pins_yay:
        c = digitalio.DigitalInOut(pin)
        c.direction = digitalio.Direction.INPUT
        c.pull = digitalio.Pull.UP
        cols.append(c)
    return rows, cols

los_rows, los_cols = set_pins_yay()

def scan_keys():
    pressed = set()
    for row_index, row in enumerate(los_rows):
        row.value = False
        time.sleep(0.020)
        for col_index, col in enumerate(los_cols):
            if not col.value:
                key = switch_matrix.get((row_index, col_index))
                if key:
                    pressed.add(key)
        row.value = True
    return pressed

def scan_keys_debounced():
    first = scan_keys()
    time.sleep(DEBOUNCE_DELAY)
    second = scan_keys()
    return first if first == second else set()

def process_steno_chord(pressed_keys):
    sorted_keys = sorted(pressed_keys, key=lambda k: PLOVER_ORDER.index(k))
    return "".join(sorted_keys)

def output_stroke(stroke):
    print("Detected steno stroke:", stroke)

def main():
    time.sleep(0.5)
    pressed = scan_keys_debounced()
    if pressed:
        stroke = process_steno_chord(pressed)
        output_stroke(stroke)

if __name__ == "__main__":
    try:
        while True:
            main()
            time.sleep(0.1)
    except KeyboardInterrupt:
        for pin in los_rows + los_cols:
            pin.deinit()
        print("Exiting")
