import serial
import time

class Connection:
    def __init__(self, port = "COM3"):
        self.port = port
        pass

    def __enter__(self):
        self._serial = serial.Serial(port=self.port, baudrate=9600)
        self._serial.flush()
        return self

    def __exit__(self, type, value, traceback):
        self._serial.flush()
        self._serial.close()
        pass

    def read(self):
        # baudrate 9600 * 2는 아님
        #   받는 수가 일정하지 않음
        #   9600일떄 받는 수가 일정함.
        time.sleep(1)
        return self._serial.read_all()
        #return self._serial.read_until(b'\x08\x08')
        #return self._serial.read_until(b'\x00\x18\x00\x80') 
        #return self._serial.read_until(b'\xaa\xaa ')

if __name__ == "__main__":
    with Connection(port="COM3") as con:
        while True:
            tmp = con.read()
            if len(tmp) > 0:
                print(tmp)
                print("size : %d" % (len(tmp), ))
        