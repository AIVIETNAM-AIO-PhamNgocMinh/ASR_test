import os
import time
from moviepy import VideoFileClip
from faster_whisper import WhisperModel

def extract_audio(video_path, audio_output_path):
    """Trích xuất file audio từ video"""
    print(f"\n[1/2] Đang trích xuất audio từ video: {video_path}...")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_output_path, fps=16000, nbytes=2, buffersize=2000, ffmpeg_params=["-ac", "1"])
    video.close()
    print("-> Trích xuất audio hoàn tất!")

def run_whisper_asr(audio_path, model_size="medium", device="cpu"):
    """Chạy nhận diện giọng nói bằng faster-whisper và lưu model tại ổ D"""
    print(f"\n[2/2] Đang tải model Whisper [{model_size}] trên {device.upper()}...")
    
    # ÉP LƯU Ổ D: Tạo thư mục tên 'whisper_models_storage' ngay tại ổ D chung với file code
    cache_dir = "./whisper_models_storage"
    
    # Truyền tham số download_root để chỉ định nơi lưu model
    model = WhisperModel(model_size, device=device, compute_type="int8", download_root=cache_dir)
    
    print("-> Đang xử lý nhận diện (Inference)...")
    start_time = time.time()
    
    segments, info = model.transcribe(audio_path, beam_size=5, language="vi")
    
    print(f"\n=== KẾT QUẢ NHẬN DIỆN (Model: {model_size}) ===")
    results = []
    for segment in segments:
        timestamp = f"[{time.strftime('%H:%M:%S', time.gmtime(segment.start))} -> {time.strftime('%H:%M:%S', time.gmtime(segment.end))}]"
        print(f"{timestamp} {segment.text}")
        results.append(f"{timestamp} {segment.text}")
        
    end_time = time.time()
    print(f"\n Tổng thời gian xử lý của [{model_size}]: {end_time - start_time:.2f} giây")
    return results

if __name__ == "__main__":
    VIDEO_INPUT = "source.mp4"  
    AUDIO_TEMP = "temp_audio.wav"
    
    # 2. CHỌN MODEL ĐỂ TEST (Bật/Tắt bằng dấu # ở đầu dòng)
    
    MODEL_TO_TEST = "large-v3-turbo"
    
    if os.path.exists(VIDEO_INPUT):
        extract_audio(VIDEO_INPUT, AUDIO_TEMP)
        
        # Chạy kiểm thử
        run_whisper_asr(AUDIO_TEMP, model_size=MODEL_TO_TEST, device="cpu")
        
        # Dọn dẹp file tạm
        if os.path.exists(AUDIO_TEMP):
            os.remove(AUDIO_TEMP)
    else:
        print(f"Lỗi: Không tìm thấy file video đầu vào tại: '{VIDEO_INPUT}'")