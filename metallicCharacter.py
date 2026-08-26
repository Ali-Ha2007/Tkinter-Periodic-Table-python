import json
class elementChange:#Set which element is which type of metal/nonmetal/metalloid
    #-----------------------------

    def reactive_nonmetal(self, e):
        e[0]["Metallic Character"] = "reactive nonmetal"
        change = 0
        for i in range(4):
            for ii in range(4-i):
                e[5+change+ii]["Metallic Character"] = "reactive nonmetal"
            if i == 0:
                change += 9
            else:
                change +=19


    def vertical_line(self, e, value, metal_c):
        change = 0
        for i in range(6):
            e[value]["Metallic Character"] = metal_c
            if i%2 == 0:
                if change == 0:
                    change = 8
                elif change == 8:
                    change = 18
                else:
                    change = 32
            value += change


    def horizontal_line(self, e, start, lenght, exception, metal_c):
        for i in range(lenght):
            if (start+i) != exception:
                e[start+i]["Metallic Character"] = metal_c


    def transition_metal(self, e):
        metal_c = "transition metal"
        self.horizontal_line(e, 20, 9, None, metal_c)
        self.horizontal_line(e, 38, 9, None, metal_c)
        self.horizontal_line(e, 71, 8, None, metal_c)
        self.horizontal_line(e, 103, 5, None, metal_c)


    def metalloid(self, e):
        eList = [4, 13, 31, 32, 50, 51, 84]
        for i in eList:
            e[i]["Metallic Character"] = "metalloid"


    def post_transition_metal(self, e):
        a = 12
        for i in range(112-13+1):
            if len(e[a+i]["Metallic Character"]) <= 2:
                e[a+i]["Metallic Character"] = "post-transition metal"
    

    def give_Metallic_Character(self, e):
        self.reactive_nonmetal(e)
        self.vertical_line(e, 1, "noble gas")
        self.vertical_line(e, 2, "alkali metal")
        self.vertical_line(e, 3, "alkaline earth metal")
        self.transition_metal(e)
        self.metalloid(e)
        self.horizontal_line(e, 108, 10, 111, "unknown")
        self.horizontal_line(e, 56, 15, None, "lanthanide")
        self.horizontal_line(e, 88, 15, None, "actinide")
        self.post_transition_metal(e)


