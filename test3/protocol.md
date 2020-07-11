# mindwave 프로토콜

## 패킷

|   인덱스          |   내용    |
|   -----           |   ----    |
|   0               |   시작문자( 0xAA )    |
|   1               |   시작문자( 0xAA )    |
|   2               |   길이                |
|   3 ~ 3 + 길이    |   페이로드(체크썸 대상)  |
|   4 + 길이        |   체크 썸             |

> 체크 썸의 경우 좀더 확인이 필요

### 데이터

#### 포멧

1. 코드
2. 값 길이(값이 없는 경우 생략)
3. 값

#### 페이로드

|   코드    |   내용    |
|   ----    |   ----    |
|   0x80      |   raw 값   |
|   0x02    |   poor 값 (0~200)   |
|   0x04    |   attention 값 (0~100)(벗은 경우 100을 초과함)    |
|   
d4

```c++
PSD4::SerialPortBridge serialPortBridge ("COM3");
serialPortBridge.open();
PSD4::Controller controller (serialPortBridge, '1');
try{
    auto state = controller.getState();
}
catch( PSD4::SerialPortBridge::TimeoutException){
    // 연결 문제 (응답 없음)
}
catch()
```