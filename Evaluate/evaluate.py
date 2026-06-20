import os
import re
from jiwer import wer, cer

def parse_time_to_seconds(ts_str):
    try:
        parts = ts_str.strip().split(':')
        if len(parts) == 3:
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2].replace(',', '.'))
        elif len(parts) == 2:
            return float(parts[0]) * 60 + float(parts[1].replace(',', '.'))
    except:
        return 0.0
    return 0.0

def parse_timestamps_and_text(file_path):
    segments = []
    text_list = []
    pattern = r'\[([\d:\.,\s]+)(?:->|-)([\d:\.,\s]+)\](.*)'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line_str = line.strip()
            if "=== KẾT QUẢ" in line_str or "Tổng thời gian xử lý" in line_str or not line_str:
                continue
                
            match = re.match(pattern, line_str)
            if match:
                start_s = parse_time_to_seconds(match.group(1))
                end_s = parse_time_to_seconds(match.group(2))
                txt = match.group(3).strip()
                
                segments.append({'start': start_s, 'end': end_s, 'text': txt})
                text_list.append(txt)
            else:
                # Nếu dòng không có timestamp (PhoWhisper hoặc dòng thường), vẫn giữ lại chữ để tính WER
                if line_str:
                    text_list.append(line_str)
                
    full_text = " ".join(text_list)
    return full_text, segments

def clean_and_normalize(text):
    text_lower = text.lower()
    text_no_punctuation = re.sub(r'[.,\/#!$%\^&\*;:{}=\-_`~()?\"]', ' ', text_lower)
    return re.sub(r'\s+', ' ', text_no_punctuation).strip()

def calculate_overlap_time_error(gt_segments, hyp_segments):
    total_error = 0.0
    matched_count = 0
    
    for gt in gt_segments:
        best_match = None
        max_overlap = 0.0
        
        for hyp in hyp_segments:
            overlap_start = max(gt['start'], hyp['start'])
            overlap_end = min(gt['end'], hyp['end'])
            overlap_duration = overlap_end - overlap_start
            
            if overlap_duration > max_overlap:
                max_overlap = overlap_duration
                best_match = hyp
        
        if best_match is not None and max_overlap > 0:
            start_diff = abs(gt['start'] - best_match['start'])
            end_diff = abs(gt['end'] - best_match['end'])
            total_error += (start_diff + end_diff) / 2.0
            matched_count += 1
            
    if matched_count == 0:
        return 0.0, "Không khớp đoạn nào"
        
    mae_seconds = total_error / matched_count
    return mae_seconds, f"{mae_seconds:.2f}s (Khớp {matched_count}/{len(gt_segments)} đoạn)"

def run_alignment_evaluation(ground_truth_path, target_dir="."):
    if not os.path.exists(ground_truth_path):
        print(f"❌ Không tìm thấy file key chuẩn: {ground_truth_path}")
        return
        
    gt_text, gt_segments = parse_timestamps_and_text(ground_truth_path)
    clean_gt = clean_and_normalize(gt_text)
    
    if not gt_segments:
        print("⚠️ Cảnh báo: File key chuẩn không chứa timestamp hợp lệ để so sánh thời gian!")
        return

    print("\n⏱️ BẢNG ĐÁNH GIÁ TỔNG HỢP CHỮ & TIMESTAMP (ALL MODELS)")
    print("=" * 105)
    print(f"{'Tên File Mô Hình':<32} | {'WER (%)':<10} | {'CER (%)':<10} | {'Độ lệch Time chuẩn (MAE)':<35}")
    print("=" * 105)
    
    for file_name in os.listdir(target_dir):
        if file_name.lower().startswith("result_") and file_name.endswith(".txt"):
            file_path = os.path.join(target_dir, file_name)
            try:
                hyp_text, hyp_segments = parse_timestamps_and_text(file_path)
                clean_hyp = clean_and_normalize(hyp_text)
                
                if not clean_hyp:
                    continue
                
                # 1. Luôn tính toán số liệu chữ cho mọi mô hình (Kể cả PhoWhisper)
                error_word = wer(clean_gt, clean_hyp) * 100
                error_char = cer(clean_gt, clean_hyp) * 100
                
                # 2. Phân loại để tính Timestamp
                if not hyp_segments:
                    # Nếu mô hình không có timestamp (PhoWhisper)
                    time_status = "N/A (Không có timestamp)"
                else:
                    # Nếu mô hình có timestamp (Whisper, WhisperX)
                    _, time_status = calculate_overlap_time_error(gt_segments, hyp_segments)
                    
                print(f"{file_name:<32} | {error_word:>7.2f}% | {error_char:>7.2f}% | {time_status:<35}")
            except Exception as e:
                print(f"❌ Lỗi xử lý file {file_name}: {str(e)}")
    print("=" * 105)

if __name__ == "__main__":
    GROUND_TRUTH_FILE = "ground_truth.txt"
    run_alignment_evaluation(GROUND_TRUTH_FILE)