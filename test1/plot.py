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
        self.fig = plt.figure(figsize=[1,1])
        self.subplot1 = self.fig.add_subplot(111)
        self.life = True
        plt.connect("close_event", self.__onClose)

        return self

    def __exit__(self, type, value, traceback):
        pass

    def __onClose(self, event):
        self.life = False

    def push(self, y : bytes):
        if(len(y) == 36):
            for y_item, ys_item in zip(y, self.ys):
                ys_item : deque
                ys_item.append(int(y_item))
                pass
    
    def draw(self):
        if self.life:
            self.subplot1 : axes.Axes
            self.subplot1.clear()
            for ys_item in self.ys:
                ys_item : deque
                self.subplot1.plot(self.x, ys_item)
            plt.draw()
            plt.pause(0.0001)

        pass
    

if __name__ == "__main__":
    import connection
    with Plot() as plot:
        with connection.Connection(port="COM3") as con:
            while plot.life:
                tmp = con.read()
                if(len(tmp) == 36):
                    plot.push(tmp)
                    plot.draw()
        