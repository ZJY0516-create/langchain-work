import os
import traceback
from pathlib import Path

def get_ffmpeg_path():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

def extract_audio_from_video(video_path, output_audio_path=None):
    if output_audio_path is None:
        output_audio_path = str(Path(video_path).with_suffix('.wav'))
    
    try:
        ffmpeg_exe = get_ffmpeg_path()
        print(f"Using ffmpeg: {ffmpeg_exe}")
        
        import subprocess
        cmd = [
            ffmpeg_exe,
            '-i', video_path,
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            '-y',
            output_audio_path
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"ffmpeg stderr: {result.stderr}")
            raise Exception(f"ffmpeg failed: {result.stderr}")
        
        if not os.path.exists(output_audio_path):
            raise Exception("Audio file not created")
            
        return output_audio_path
        
    except Exception as e:
        print(f"Error extracting audio: {e}")
        traceback.print_exc()
        raise

def transcribe_audio(audio_path, model_name="tiny"):
    try:
        print(f"Starting transcription of: {audio_path}")
        
        if not os.path.exists(audio_path):
            raise Exception(f"Audio file not found: {audio_path}")
        
        print(f"Loading whisper model: {model_name}")
        import whisper
        model = whisper.load_model(model_name)
        
        print(f"Manually loading audio...")
        
        ffmpeg_exe = get_ffmpeg_path()
        import subprocess
        import numpy as np
        
        cmd = [
            ffmpeg_exe,
            '-i', audio_path,
            '-f', 's16le',
            '-ar', '16000',
            '-ac', '1',
            '-y',
            'pipe:1'
        ]
        
        result = subprocess.run(cmd, capture_output=True, check=True)
        audio = np.frombuffer(result.stdout, dtype=np.int16)
        audio = audio.astype(np.float32) / 32768.0
        
        print(f"Audio loaded, shape: {audio.shape}")
        
        print(f"Transcribing...")
        result = whisper.transcribe(model, audio)
        
        text = result["text"]
        print(f"Transcription successful, length: {len(text)}")
        return text
        
    except Exception as e:
        print(f"Error in transcription: {e}")
        traceback.print_exc()
        raise

def process_media_file(file_path):
    file_ext = Path(file_path).suffix.lower()
    
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg']
    
    if file_ext in video_extensions:
        print(f"Processing video: {file_path}")
        audio_path = extract_audio_from_video(file_path)
        try:
            text = transcribe_audio(audio_path)
            return text
        finally:
            try:
                os.remove(audio_path)
            except:
                pass
    elif file_ext in audio_extensions:
        print(f"Processing audio: {file_path}")
        return transcribe_audio(file_path)
    else:
        raise ValueError(f"Unsupported format: {file_ext}")

def check_ffmpeg_available():
    try:
        import subprocess
        ffmpeg_exe = get_ffmpeg_path()
        result = subprocess.run([ffmpeg_exe, '-version'], capture_output=True)
        return result.returncode == 0
    except:
        return False

def check_whisper_installed():
    try:
        import whisper
        return True
    except ImportError:
        return False
