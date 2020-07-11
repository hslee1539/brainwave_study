
class Parser:
    """
    protocol 문서
    http://developer.neurosky.com/docs/doku.php?id=thinkgear_communications_protocol
    
    python 예제
    https://github.com/akloster/python-mindwave/blob/master/mindwave/parser.py
    """
    def __init__(self):
        self._parser = self._parse()
        next(self._parser)
        pass

    def _parse(self):
        """코루틴임. 입력은 바이트만 받음."""
        output = "please input start bytes (1/2)"
        while True:
            if b'\xaa' == (yield output):
                if b'\xaa' == (yield "please input start bytes (2/2)"):
                    packet_len = (yield "please input packet length")[0]
                    packet_code = yield "please input packet code"
                    packet_left = packet_len - 2

                    if packet_code == b'\xd4':
                        self.state = "standby"
                        output = ("state", self.state)
                    elif packet_code == b'\xd0':
                        self.state = "connected"
                        output = ("state", self.state)
                    elif packet_code == b'\xd2':
                        yield "please input data length"
                        yield "please input headset id (1/2)"
                        yield "please input headset id (2/2)" # headset id (1/2)결과와 더해서 사용
                        self.dongle_state = "disconnect"
                        output = ("dongle state", self.dongle_state)
                    else:
                        self.sending_data = True
                        while packet_left > 0:
                            if packet_code == b'\x80':
                                yield "please input row length"
                                # 빅엔디안임.
                                a = (yield "please input row data...")[0]
                                b = (yield "please input row data...")[0]
                                value = a * 256 + b
                                packet_left -= 2 # 왜 2인지 모르겠음...
                                output = ("row data", value)
                            elif packet_code == b'\x02':
                                value = (yield "please input poor data")[0]
                                packet_left -= 1
                                output = ("poor data", value)
                            elif packet_code == b'\x04':
                                a = (yield "please input attention")[0]
                                if 0 < a <= 100:
                                    value = a
                                    output = ("attention", value)
                                else:
                                    output = ("attention-fail", value)
                                packet_left -= 1

                            elif packet_code == b'\x05':
                                a = (yield "please input meditation")[0]
                                if 0 < a <= 100:
                                    value = a
                                    output = ("meditation", value)
                                else:
                                    output = ("meditation-fail", value)
                                packet_left -= 1
                            elif packet_code == b'\x16':
                                self.current_blink_strength = (yield "please input blink strength")[0]
                                packet_left -= 1
                                output = ("current blink strength", self.current_blink_strength)
                            elif packet_code == b'\x83':
                                vec_len = (yield "please input vector lenghth")[0]
                                self.current_vector = []
                                """
                                delta, theta, low-alpha, high-alpha, low-beta, high-beta, low-gamma, mid-gamma
                                빅 엔디안으로 unsiged 3바이트 값임.
                                """

                                for _ in range(vec_len // 3):
                                    a = (yield "vector...")[0]
                                    b = (yield "vector...")[0]
                                    c = (yield "vector...")[0]
                                    value = a * 256 * 256 + b  * 256 + c # 왜 255인지는 모르겠음. 256이 맞을 거 같음.
                                    self.current_vector.append(value)
                                packet_left -= vec_len
                                output = ("vector", self.current_vector)
                            elif packet_code == b'\x81':
                                pass
                            packet_code = yield output
            else:
                output = "please input start bytes (1/2)"

    def feed(self, data : bytes):
        """1 바이트를 처리"""
        return self._parser.send(data)


if __name__ == "__main__":
    import serial
    ser = serial.Serial(port="COM3")
    ser.flush()
    parser = Parser()
    while True:
        retval = parser.feed(ser.read())
        if type(retval) == tuple:
            print(retval)

                                
                            





