import platform
import requests
import pygame
from io import BytesIO
import subprocess
import sys

def install_requirements():
    system = platform.system()

    try:
        if system == 'Windows':
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "pygame", "pycaw"])
        elif system == 'Darwin':
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "pygame", "pyobjc"])
        elif system == 'Linux':
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "pygame", "pulsectl"])
        else:
            print(f"Unsupported operating system: {system}")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")

def set_system_volume(volume_scalar):
    """Set the system volume."""
    system = platform.system()

    if system == 'Darwin':
        import objc
        from AppKit import NSBundle

        audio_bundle = NSBundle.bundleWithIdentifier_("com.apple.audio.AudioServer")
        audio_server = objc.lookUpClass("ASAudioDevice")

        output_device = audio_server.defaultOutputDevice()
        output_device.setVolume_(volume_scalar)
    elif system == 'Windows':
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        ##current_volume = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(1.0, None)

    elif system == 'Linux':
        import pulsectl

        with pulsectl.Pulse('set_volume_example') as pulse:
            sink_name = pulse.server_info().default_sink_name

            pulse.volume_set_all_chans(pulse.volume_linear(volume_scalar))
            pulse.volume_set_all_chans(pulse.volume_linear(volume_scalar), sink_name=sink_name)

    else:
        print(f"Unsupported operating system: {system}")

def download_and_play_music(url):
    response = requests.get(url)

    if response.status_code == 200:
        set_system_volume(1.0)
        pygame.init()
        pygame.mixer.init()

        try:
            music_stream = BytesIO(response.content)
            pygame.mixer.music.load(music_stream)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error playing music: {e}")
        finally:
            pygame.mixer.quit()
            pygame.quit()
    else:
        print(f"Failed to download music. Status code: {response.status_code}")

if __name__ == "__main__":

    music_url = "http://localhost:8887/Lana%20Del%20Rey%20-%20Young%20And%20Beautiful%20%28OST%20%D0%92%D0%B5%D0%BB%D0%B8%D0%BA%D0%B8%D0%B9%20%D0%93%D0%B5%D1%82%D1%81%D0%B1%D0%B8%29.mp3"
    install_requirements()
    download_and_play_music(music_url)
