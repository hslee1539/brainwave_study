import matplotlib.pyplot as plt
import matplotlib.axes as axes
from collections import deque

def zeros(maxlen : int):
    for _ in range(maxlen):
        yield 0

class Plot:
    def __init__(self, maxlen = 100):
        self.x = deque(maxlen=maxlen)
        self.ys = [None] * 36
        self.ys[:] = map(lambda _: deque(maxlen=maxlen), self.ys)
        self.x.extend(range(maxlen))
        for ys_item in self.ys:
            ys_item : deque
            ys_item.extend(zeros(maxlen=maxlen))

        
        pass

    def __enter__(self):
        self.fig = plt.figure(figsize=[6,6])
        self.fig : plt.Figure
        self.subplots = []
        for i in range(6 * 6):
            self.subplots.append(self.fig.add_subplot(6,6, i + 1))

        return self

    def __exit__(self, type, value, traceback):
        pass

    def push(self, y : bytes):
        if(len(y) == 36):
            for y_item, ys_item in zip(y, self.ys):
                ys_item : deque
                ys_item.append(int(y_item))
                pass
    
    def draw(self):
        self.subplot1 : axes.Axes
        #self.subplot1.clear()
        for subplot, y in zip(self.subplots, self.ys):
            subplot : axes.Axes
            subplot.clear()
            subplot.plot(self.x, y)
            
        plt.draw()
        plt.pause(0.0001)

        pass
    

if __name__ == "__main__":
    import connection
    with Plot(10) as plot:
        with connection.Connection(port="COM3") as con:
            while True:
                tmp = con.read()
                if(len(tmp) == 36):
                    plot.push(tmp)
                    plot.draw()
                else:
                    print("wow")
        