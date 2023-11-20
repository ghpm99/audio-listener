import asyncio
import websockets
import pyaudio

p = pyaudio.PyAudio()

device_target_name_output = 'Tempest  34\' (NVIDIA High Definition Audio)'
device_target_output = None

CHUNK = 1024
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
        output_device_index=5,
        frames_per_buffer=CHUNK,
    )
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = await websocket.recv()
        stream_output.write(data)

    stream_output.stop_stream()
    stream_output.close()
    p.terminate()


async def main():
    async with websockets.serve(listener_audio, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
