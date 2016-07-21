
class RunningMean:
    def __init__(self, n): 
        self.n = n 
        self.last = []
    
    def push(self, n): 
        self.last.append(float(n))
        if len(self.last) > self.n:
            self.last.pop(0)

    def mean(self):
        return sum(self.last) / len(self.last)

    def set(self, n):
        self.last = [n]

    def all_over(self, n): 
        for l in self.last:
            if l < n:
                return False
        return True

