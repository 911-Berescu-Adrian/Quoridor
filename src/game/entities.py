class Cell:
    def __init__(self,value):
        self.value=value

    def __str__(self):
        return str(self.value)

class Wall:
    def __init__(self,dir,a,b,c,d):
        self.direction=dir
        self.coords=[a,b,c,d]

    def __str__(self):
        return self.direction+" "+str(self.coords[0])+" "+str(self.coords[1])+" "+str(self.coords[2])+" "+str(self.coords[3])