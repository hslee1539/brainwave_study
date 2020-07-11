import matplotlib.pyplot as plt
import matplotlib.axes as axes
from collections import deque

def zeros(maxlen : int):
    for _ in range(maxlen):
        yield 0

class Plot:
    def __init__(self, maxlen = 100):
        self.x = deque(maxlen=maxlen)
        self.ys = [None] * 8
        self.ys[:] = map(lambda _: deque(maxlen=maxlen), self.ys)
        self.x.extend(range(maxlen))
        for ys_item in self.ys:
            ys_item : deque
            ys_item.extend(zeros(maxlen=maxlen))

        
        pass

    def __enter__(self):
        self.fig = plt.figure(figsize=[2,4])
        self.fig : plt.Figure
        self.subplots = []
        self.life = True
        plt.connect("close_event", self.__onClose)
        for i in range(2 * 4):
            self.subplots.append(self.fig.add_subplot(2,4, i + 1))
            self.subplots[-1].set_ylim((0, 3000000))

        return self

    def __exit__(self, type, value, traceback):
        pass

    def __onClose(self, event):
        self.life = False

    def push(self, y : list):
        if(len(y) == 8):
            for y_item, ys_item in zip(y, self.ys):
                ys_item : deque
                ys_item.append(int(y_item))
                pass
    
    def draw(self):
        if self.life:
            self.subplot1 : axes.Axes
            #self.subplot1.clear()
            tmp = True
            for subplot, y in zip(self.subplots, self.ys):
                subplot : axes.Axes
                subplot.clear()
                if tmp:
                    subplot.set_ylim((0, 3000000))
                    tmp = False
                else:
                    subplot.set_ylim((0, 500000))
                subplot.plot(self.x, y)

            plt.draw()
            plt.pause(0.0001)

        pass
    

if __name__ == "__main__":
    import connection
    import mindwave
    parser = mindwave.Parser()
    with Plot(50) as plot:
        with connection.Connection(port="COM5") as con:
            while plot.life:
                retval = parser.feed(con.read())
                if type(retval) == tuple:
                    if retval[0] == 'vector':
                        plot.push(retval[1])
                        plot.draw()
                    