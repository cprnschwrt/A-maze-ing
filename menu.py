selected_button = 1

def load_settings(path: str="settings.txt") -> dict:
    """Data from config file"""

    settings = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=")
            if value.isdigit():
                value = int(value)
            elif value in ["True", "False"]:
                value = value == "True"
            settings[key] = value
    return settings

settings = load_settings()


def get_buttons(self) -> list[dict]:
    """Implements each button."""

    spacing = 20
    btn_width = 220
    btn_height = 40

    buttons = [
        {"label": "[S] Seeker", "id": 1},
        {"label": "[R] Rows", "id": 2},
        {"label": "[P] Path", "id": 3},
        {"label": "[C] Colors", "id": 4},
        {"label": "[M] Motif", "id": 5}]

    mlx_width = settings["WIDTH"] * self.mult + self.offsetx * 2
    mlx_height = 1750
    total_width = len(buttons) * btn_width + (len(buttons) - 1) * spacing
    start_x = (mlx_width - total_width) // 2
    base_y = mlx_height - btn_height - 20

    result = [{"label": "", "x": 0, "y": 0, "width": 0, "height": 0, "id": 0}]
    for i, btn in enumerate(buttons):
        x = start_x + i * (btn_width + spacing)
        result.append({"label": btn["label"], "x": x, "y": base_y,
                       "width": btn_width, "height": btn_height,
                       "id": btn["id"]})
    return result


def swap_rgb(col: int) -> int:
    """Change ABGR format colour to ARGB (B ⇆ R)."""

    a = (col >> 24) & 0xFF
    b = (col >> 16) & 0xFF
    g = (col >> 8) & 0xFF
    r = col & 0xFF
    return (a << 24) | (r << 16) | (g << 8) | b


def draw_button(self, label: str, x: int, y: int, width: int, height: int,
                selected: bool) -> None:
    """Creates the buttons."""

    text_col = swap_rgb(self.secondaryCol)
    btn_col = self.tertiaryCol if selected else self.primaryCol

    text_x = x + 10
    text_y = y + 12
    
    for ix in range(x, x + width):
        # # === highlight ===
        # for iy in range(y, y + height):
        #     self.mlx.mlx_pixel_put(
        #         self.initScreen, self.screen, ix, iy, btn_col)

        # === underline ===
            self.mlx.mlx_pixel_put(
                self.initScreen, self.screen, ix, y + height - 1, btn_col)
    
    self.mlx.mlx_string_put(
        self.initScreen, self.screen, text_x, text_y, text_col, label)


def draw_menu(self) -> None:
    """Displays the buttons."""

    global selected_button
    buttons = get_buttons(self)
    for i, btn in enumerate(buttons):
        draw_button(self, btn["label"], btn["x"], btn["y"],
                    btn["width"], btn["height"], i == selected_button)


def menu_manager(key: int, self) -> None:
    """Keyboard navigation"""

    global selected_button
    buttons = get_buttons(self)

    if key == 65307:  # ESC
        self.mlx.mlx_loop_exit(self.initScreen)
    elif key == 32:  # SPACE
        self.paused = not self.paused
    elif key == 65361:  # LEFT
        selected_button = (selected_button - 1) % len(buttons)
    elif key == 65363:  # RIGHT
        selected_button = (selected_button + 1) % len(buttons)
    elif key in (65293, 65421):  # ALPHA_ENTER, NUM_ENTER
        btn_id = buttons[selected_button]["id"]
        if btn_id == 1:
            self.start_generation_seeker()
        elif btn_id == 2:
            self.start_generation_rows()
        elif btn_id == 3:
            self.solve_maze()
        elif btn_id == 4:
            self.change_color()
            self.refresh(True)
        elif btn_id == 5:
            self.change_pattern()
    elif key in (115, 114, 112, 99, 109):  # S, R, P, C, M
        actions = {
            115: self.start_generation_seeker,
            114: self.start_generation_rows,
            112: self.solve_maze,
            99: lambda: (self.change_color(), self.refresh(True)),
            109: self.change_pattern}
        actions[key]()

    draw_menu(self)


def mouse_click(button: int, x: int, y: int, self) -> None:
    """Mouse click callback"""

    global selected_button
    if button != 1:  # left click only
        return

    buttons = get_buttons(self)
    for i, btn in enumerate(buttons):
        bx, by = btn["x"], btn["y"]
        bw, bh = btn["width"], btn["height"]
        if bx <= x <= bx + bw and by <= y <= by + bh:
            selected_button = i
            btn_id = btn["id"]
            if btn_id == 1:
                self.start_generation_seeker()
            elif btn_id == 2:
                self.start_generation_rows()
            elif btn_id == 3:
                self.solve_maze()
            elif btn_id == 4:
                self.change_color()
                self.refresh(True)
            elif btn_id == 5:
                self.change_pattern()
            break

    draw_menu(self)
