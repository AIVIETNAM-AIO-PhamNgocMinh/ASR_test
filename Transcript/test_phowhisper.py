import os
import time
from moviepy import VideoFileClip
import torch
from transformers import pipeline

def extract_audio(video_path, audio_output_path):
    """Trích xuất file audio từ video sử dụng MoviePy (chạy ngầm FFmpeg)"""
    print(f"\n[1/2] Đang trích xuất audio từ video: {video_path}...")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_output_path, fps=16000, nbytes=2, buffersize=2000, ffmpeg_params=["-ac", "1"])
    video.close()
    print("-> Trích xuất audio hoàn tất!")

def run_phowhisper(audio_path, model_name="vinai/phowhisper-small"):
    """Chạy nhận diện giọng nói bằng PhoWhisper của VinAI"""
    print(f"\n[2/2] Đang tải mô hình PhoWhisper từ VinAI: {model_name}...")
    
    # ÉP LƯU Ổ D: Thiết lập biến môi trường cache của HuggingFace ngay trong code
    os.environ["HF_HOME"] = "./phowhisper_models_storage"
    
    # Khởi tạo pipeline ASR từ transformers
    asr_pipeline = pipeline(
        "automatic-speech-recognition",
        model=model_name,
        chunk_length_s=30,
        device="cpu"
    )
    
    print("-> Đang xử lý nhận diện giọng nói tiếng Việt...")
    start_time = time.time()
    
    generate_kwargs = {"language": "vi", "task": "transcribe"}
    result = asr_pipeline(audio_path, generate_kwargs=generate_kwargs)
    
    print(f"\n=== KẾT QUẢ PHOWHISPER ===")
    print(result["text"])
    
    end_time = time.time()
    print(f"\n Tổng thời gian xử lý: {end_time - start_time:.2f} giây")

if __name__ == "__main__":
    VIDEO_INPUT = "source.mp4"  
    AUDIO_TEMP = "temp_audio_phowhisper.wav"
    
    if os.path.exists(VIDEO_INPUT):
        extract_audio(VIDEO_INPUT, AUDIO_TEMP)
        run_phowhisper(AUDIO_TEMP, model_name="vinai/phowhisper-small")
        
        # Dọn dẹp file tạm
        if os.path.exists(AUDIO_TEMP):
            os.remove(AUDIO_TEMP)
    else:
        print(f"Lỗi: Không tìm thấy file video đầu vào tại: '{VIDEO_INPUT}'")