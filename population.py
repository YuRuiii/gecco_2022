

class Population:
    def __init__(self, size):
        self.max_size = size
        self.population = []
        
    def update(self):
        if(len(self.population) > self.max_size):
            self.population.sort(key=lambda tup: tup[1], reverse=True)
        
        self.population = self.population[:self.max_size]
        # print(self.population)
        
    