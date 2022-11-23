

class Locations:
    def __init__(self, setup):

        if setup == 'fullscreen_hermes':
            self.safe = (835, 219)
            self.server_error = (757, 566)
            self.back = (1198, 179)
            self.level1 = (1237, 181)
            self.level2 = (1285, 181)
            self.level3 = (1330, 181)
            self.level4 = (1377, 181)
            self.level5 = (1424, 181)
            self.base_level_number = (1222, 167, 30, 25)
            self.enrage_box = (629, 710, 254, 37)
        if setup == 'windowed_hermes':
            self.safe = (835, 219)
            self.server_error = (871, 495)
            self.back = (1158, 176)
            self.level1 = (1209, 176)
            self.level2 = (1255, 176)
            self.level3 = (1301, 176)
            self.level4 = (1352, 176)
            self.level5 = (1399, 176)
            self.base_level_number = (1188, 159, 38, 26)
            self.enrage_box = (708, 527, 330, 49)
        
        self.res_factor = 2
        self.base_level_number = tuple(i * self.res_factor for i in self.base_level_number)
        self.enrage_box = tuple(i * self.res_factor for i in self.enrage_box)
