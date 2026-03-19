BUTTONS = [
    {"label": "[R] Re-Generate Maze", "x": 200, "y": 10, "width": 200,
     "height": 50, "id": 1},
    {"label": "[S] Soluce", "x": 460, "y": 10, "width": 200,
     "height": 50, "id": 2},
    {"label": "[C] Change colours", "x": 650, "y": 10, "width": 200,
     "height": 50, "id": 3},
    {"label": "[F] Change pattern", "x": 900, "y": 10, "width": 200,
     "height": 50, "id": 4}
]

selected_button = 0

def draw_button(self, label: str, x: int, y: int, width: int, height: int,
                is_selected: bool):
    background_color = 0xFFFFFF if is_selected else 0xFF0000
    
    for ix in range(x, x + width):
        for iy in range(y, y + height):
            self.mlx.mlx_pixel_put(self.initScreen, self.screen, ix, iy, background_color)

    text_color = 0xFF0000 if is_selected else 0xFFFFFF
    
    self.mlx.mlx_string_put(self.initScreen, self.screen, x + 10, y + 10, text_color, label)


def draw_buttons_only(self):
    for i, btn in enumerate(BUTTONS):
        draw_button(
            self, btn["label"], btn["x"], btn["y"], btn["width"],
            btn["height"], i == selected_button)

    for i in range(len(BUTTONS) - 1):
        right_edge = BUTTONS[i]["x"] + BUTTONS[i]["width"]
        sep_x = right_edge + 5
        sep_y = BUTTONS[i]["y"] + 10
        self.mlx.mlx_string_put(
            self.initScreen, self.screen, sep_x, sep_y, 0xFF0000, "")


def close_screen(key: int, self) -> any:
    global paused, selected_button

    if key == 65307:  # ESC
        self.mlx.mlx_loop_exit(self.initScreen)

    elif key in (32, 112):  # SPACE, P
        paused = not paused
        print("Paused" if paused else "Unpaused")

    elif key == 65361:  # LEFT
        selected_button = (selected_button - 1) % len(BUTTONS)
        draw_buttons_only(self)

    elif key == 65363:  # RIGHT
        selected_button = (selected_button + 1) % len(BUTTONS)
        draw_buttons_only(self)

    elif key in (65293, 65421):  # ALPHA_ENTER, NUM_ENTER
        btn_id = BUTTONS[selected_button]["id"]
        if btn_id == 1:
            self.start_generation()
        elif btn_id == 2:
            self.solve_maze()
        elif btn_id == 3:
            self.change_colours()
        elif btn_id == 4:
            self.change_pattern()

    elif key == 114:  # R
        self.start_generation()

    elif key == 99:  # C
        self.change_colours()
