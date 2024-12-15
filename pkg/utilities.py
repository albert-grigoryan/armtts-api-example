from io import BytesIO

import time
import soundfile as sf

def measure_time(func):
    """
    Decorator to measure and display the execution time of a function in milliseconds.
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start timing
        result = func(*args, **kwargs)   # Call the original function
        end_time = time.perf_counter()   # End timing
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"{func.__name__} executed in {execution_time:.2f} ms")
        return result
    return wrapper

def mel_to_wav(waveform, sr):
    wav_buffer = BytesIO()
    sf.write(wav_buffer, waveform, samplerate=sr, format="WAV")
    wav_buffer.seek(0)
    return wav_buffer
