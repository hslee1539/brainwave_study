# 뇌파 측정기 결과

## 결과

가장 디폴트 설정일때 36개의 바이트를 주기적으로 반환합니다.

앞부분 3바이트는 시작 문자를 나타내는 것 같습니다.

baudrate는 9600으로 통신하는 것 같습니다.

그외 baudrate에서는 받는 수가 일정하지 않거나 이상하게 받아 집니다.

## 테스트 코드

```python
import serial

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
        #return self._serial.read_all()
        #return self._serial.read_until(b'\x00\x18\x00\x80') 
        return self._serial.read_until(b'\xaa\xaa ')

if __name__ == "__main__":
    with Connection(port="COM3") as con:
        while True:
            tmp = con.read()
            if len(tmp) > 0:
                print(tmp)
                print("size : %d" % (len(tmp), ))
```
