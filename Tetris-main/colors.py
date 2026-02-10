class Colors:
    # --- Basic Cell Colors ---
    dark_grey = (26, 31, 40)      # empty grid cell
    green     = (47, 230, 23)     # S-block
    red       = (232, 18, 18)     # Z-block
    orange    = (226, 116, 17)    # L-block
    yellow    = (237, 234, 4)     # O-block
    purple    = (166, 0, 247)     # T-block
    cyan      = (21, 204, 209)    # I-block
    blue      = (13, 64, 216)     # J-block

    # --- UI / Panel Colors ---
    white     = (255, 255, 255)
    dark_blue = (44, 44, 127)
    lightblue = (59, 85, 162)

    @classmethod
    def get_cell_colors(cls):
        """
        Returns a list where index matches block ID used in Grid.
        0 = empty (dark grey), 1–7 = blocks
        """
        return [
            cls.dark_grey,  # 0 - empty cell
            cls.green,      # 1 - S
            cls.red,        # 2 - Z
            cls.orange,     # 3 - L
            cls.yellow,     # 4 - O
            cls.purple,     # 5 - T
            cls.cyan,       # 6 - I
            cls.blue        # 7 - J
        ]
