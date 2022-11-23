

class Locations:
    def __init__(self, setup):

        if setup == 'fullscreen_hermes':
            self.safe = (835, 219)
            self.server_error = (757, 566)
            self.base_level_number = (1222, 167, 30, 25)
        if setup == 'windowed_hermes':
            self.safe = (835, 219)
            self.server_error = (871, 495)
            self.base_level_number = (1188, 159, 38, 26)
        
        self.res_factor = 2
        self.base_level_number = tuple(i * self.res_factor for i in self.base_level_number)
