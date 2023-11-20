import asyncio
import websockets
import pyaudio

p = pyaudio.PyAudio()

device_target_name_output = 'Tempest  34\' (NVIDIA High Definition Audio)'
device_target_output = None

CHUNK = 1
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"


async def listener_audio(websocket):
    stream_output = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True,
        frames_per_buffer=CHUNK,
    )
    while True:
        data = await websocket.recv()
        stream_output.write(data)

    stream_output.stop_stream()
    stream_output.close()


async def main():
    async with websockets.serve(listener_audio, port=8765):
        await asyncio.Future()  # run forever
        p.terminate()

if __name__ == "__main__":
    asyncio.run(main())
