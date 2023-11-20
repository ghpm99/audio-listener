import pyaudio
import wave

p = pyaudio.PyAudio()

device_target_name = 'Mixagem loopback'
device_target = None

device_target_name_output = 'Tempest  34\' (NVIDIA High Definition Audio)'
device_target_output = None

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))
    if p.get_device_info_by_index(i).get('name').startswith(device_target_name):
        device_target = p.get_device_info_by_index(i)
    elif p.get_device_info_by_index(i).get('name').startswith(device_target_name_output):
        device_target_output = p.get_device_info_by_index(i)

if device_target is None:
    print('Device not found')
else:
    print('Device found')
    print('Device info: ', device_target)
    print('Device output info: ', device_target_output)
    print('opening input stream')
    stream_input = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    stream_output = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True,
        output_device_index=5,
        frames_per_buffer=CHUNK,
    )
    print("* recording")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream_input.read(CHUNK)
        stream_output.write(data)
        frames.append(data)

    print("* done recording")
    stream_input.stop_stream()
    stream_output.stop_stream()
    stream_output.close()
    stream_input.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
