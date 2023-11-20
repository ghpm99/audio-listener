import pyaudio
import websockets
import asyncio

p = pyaudio.PyAudio()

device_target_name = 'Mixagem loopback'
device_target = None

CHUNK = 24
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
uri = "ws://192.168.100.12:8765"


async def send_audio():
    stream_input = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    print("* recording")
    async with websockets.connect(uri) as websocket:
        while True:
            data = stream_input.read(CHUNK)
            await websocket.send(data)

    stream_input.stop_stream()
    stream_input.close()
    print("* done recording")
    p.terminate()

for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))
    if p.get_device_info_by_index(i).get('name').startswith(device_target_name):
        device_target = p.get_device_info_by_index(i)

if device_target is None:
    print('Device not found')
else:
    print('Device info: ', device_target)
    asyncio.run(send_audio())
