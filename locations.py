

class Locations:
    def __init__(self, setup):

        if setup == 'fullscreen_hermes':
            # Fullscreen, force 16:9, 1920x1080, 75% UI.
            self.safe = (1151, 183)
            self.server_error = (757, 566)
            self.back = (1198, 179)
            self.level1 = (1237, 181)
            self.level2 = (1285, 181)
            self.level3 = (1330, 181)
            self.level4 = (1377, 181)
            self.level5 = (1424, 181)
            self.load_ok = (759, 661)
            self.steam_start_button = (393, 471)
            self.welcome_back_button = (753, 609)
            self.welcome_back_button_2 = (753, 662)
            # self.base_level_number = (1222, 167, 30, 25)
            # self.enrage_box = (629, 710, 254, 37)
            self.base_level_number = {"top": 171, "left": 1222, "width": 26, "height": 16}
            self.enrage_box = {"top": 710, "left": 629, "width": 254, "height": 37}
            self.steam_start_button_box = {"top": 442, "left": 289, "width": 231, "height": 55}
            self.welcome_back = {"top": 362, "left": 520, "width": 474, "height": 296}
            # self.background_snippet = (23, 665, 15, 15)  # Unused
            # self.modron_reset_icon = (575, 493, 45, 45)  # Unused
        if setup == 'windowed_hermes':
            # Windowed, force 16:9, 1280x720, 125% UI (although it shouldn't matter).
            # I move this up to the top right, so you can't restart this easily programatically.
            self.safe = (1130, 190)
            self.server_error = (828, 508)  # THIS IS A GUESS!
            self.back = (1157, 176)
            self.level1 = (1207, 176)
            self.level2 = (1254, 176)
            self.level3 = (1303, 176)
            self.level4 = (1350, 176)
            self.level5 = (1398, 176)
            # self.load_ok = (759, 661)
            self.steam_start_button = (393, 471)
            self.base_level_number = {"top": 161, "left": 1183, "width": 36, "height": 25}
            self.enrage_box = {"top": 528, "left": 711, "width": 334, "height": 42}
        
        # self.res_factor = 2
        # self.base_level_number = tuple(i * self.res_factor for i in self.base_level_number)
        # self.enrage_box = tuple(i * self.res_factor for i in self.enrage_box)
        # # self.background_box = tuple(i * self.res_factor for i in self.background_box)
