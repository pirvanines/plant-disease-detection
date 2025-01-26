
class Check():
    def __init__(self):
        self.specii = ["capsuna", "vie", "piersica"]
        self.batchInterval = (0, 32)
        self.epochInterval = (0, 300)

    def CheckSpecies(self, specie):
        for sp in self.specii:
            if sp == specie:
                return 0
        return 2
    
    def CheckBatch(self, batch):
        if batch > self.batchInterval[0] and batch <=self.batchInterval[1]:
            return 0
        return 2
    
    def CheckEpochs(self, epochs):
        if epochs > self.epochInterval[0] and epochs <= self.epochInterval[1]:
            return 0
        elif epochs > self.epochInterval[1]:
            return 1
        return 2