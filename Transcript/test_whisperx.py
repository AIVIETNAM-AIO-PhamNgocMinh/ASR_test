import os
import time
from moviepy import VideoFileClip
import whisperx

def extract_audio(video_path, audio_output_path):
    """Trích xuất file audio từ video sử dụng MoviePy (chạy ngầm FFmpeg)"""
    print(f"\n[1/2] Đang trích xuất audio từ video: {video_path}...")
    video = VideoFileClip(video_path)
    # Convert về 16kHz, Mono để mô hình ASR đọc chuẩn nhất
    video.audio.write_audiofile(audio_output_path, fps=16000, nbytes=2, buffersize=2000, ffmpeg_params=["-ac", "1"])
    video.close()
    print("-> Trích xuất audio hoàn tất!")

def run_whisperx(audio_path, model_size="small", device="cpu"):
    """Chạy nhận diện giọng nói bằng WhisperX"""
    print(f"\n[2/2] Đang tải model WhisperX [{model_size}] trên {device.upper()}...")
    
    # Chỉ định thư mục lưu trữ tại ổ D (không động vào ổ C)
    cache_dir = "./whisperx_models_storage"
    
    # Load mô hình kèm cấu hình int8 tối ưu cho CPU
    model = whisperx.load_model(model_size, device, compute_type="int8", download_root=cache_dir)
    
    print("-> Đang xử lý nhận diện (Inference) + VAD cắt khoảng lặng...")
    start_time = time.time()
    
    audio = whisperx.load_audio(audio_path)
    result = model.transcribe(audio, batch_size=1, language="vi")
    
    print(f"\n=== KẾT QUẢ WHISPERX (Model: {model_size}) ===")
    for segment in result["segments"]:
        print(f"[{segment['start']:.2f}s -> {segment['end']:.2f}s] {segment['text']}")
        
    end_time = time.time()
    print(f"\n Tổng thời gian xử lý: {end_time - start_time:.2f} giây")

if __name__ == "__main__":
    VIDEO_INPUT = "source.mp4"  
    AUDIO_TEMP = "temp_audio_whisperx.wav"
    
    if os.path.exists(VIDEO_INPUT):
        extract_audio(VIDEO_INPUT, AUDIO_TEMP)
        run_whisperx(AUDIO_TEMP, model_size="large-v3-turbo", device="cpu")
        
        # Dọn dẹp file tạm
        if os.path.exists(AUDIO_TEMP):
            os.remove(AUDIO_TEMP)
    else:
        print(f"Lỗi: Không tìm thấy file video đầu vào tại: '{VIDEO_INPUT}'")