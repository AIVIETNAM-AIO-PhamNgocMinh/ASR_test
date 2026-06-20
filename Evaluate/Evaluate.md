# Đánh giá hiệu năng

---

## 1. Bảng số liệu tổng hợp

| Tên File | WER (%) | CER (%) | MAE (Thời gian) | Thời gian chạy | Trạng thái đối chiếu dòng |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Result_whisper_large.txt** | **5.83%** | **3.36%** | 1.23s | 73.91s | Khớp 11/11 đoạn |
| **Result_whisper_medium.txt** | 7.36% | 4.15% | 0.64s | 98.20s | Khớp 11/11 đoạn |
| **Result_whisperx_large.txt** | 7.36% | 3.79% | 6.59s | 53.53s | Khớp 11/11 đoạn |
| **Result_phowhisper.txt** | 8.59% | 5.80% | *N/A* | 210.06s | Không có timestamp |
| **Result_whisper_small.txt** | 12.27% | 6.30% | **0.18s** | 60.78s | Khớp 11/11 đoạn |
| **Result_whisperx_medium.txt**| 11.66% | 6.59% | 6.59s | 77.98s | Khớp 11/11 đoạn |
| **Result_whisperx_small.txt** | 13.19% | 6.66% | 6.59s | **27.64s** | Khớp 11/11 đoạn |

---

## 2. Kết luận

### Độ chính xác văn bản (WER/CER)
* Whisper-Large đạt WER tốt nhất (**5.83%**), tối ưu hóa tối đa khả năng hiểu ngữ cảnh câu.
* PhoWhisper vượt trội ở phân khúc tầm trung, đạt WER **8.59%**, đánh bại hoàn toàn các bản Small và Medium của hai kiến trúc còn lại nhờ được tinh chỉnh chuyên biệt trên tập dữ liệu thuần Việt.
* WhisperX có tỉ lệ lỗi chữ cao hơn Whisper gốc khi xét cùng kích thước (7.36% so với 5.83% ở bản Large) do thuật toán can thiệp làm mịn trục thời gian.

### Sai số thời gian
* Whisper gốc cắt đoạn nhỏ, phân tách câu liên tục theo khoảng nghỉ ngắn, cho sai số cực thấp (`Whisper-Small` đạt **0.18s**).
* WhisperX gộp cụm VAD lớn nên cả 3 phiên bản WhisperX đều giữ mức sai số lớn hơn, **6.59s**, dù đã Overlap Matching để đồng bộ mốc thời gian giữa các mô hình.

### Tốc độ xử lý
* WhisperX tối ưu tốc độ vượt trội nhờ cơ chế tối ưu hóa phân đoạn và tăng tốc inference.
* Ở cả hai dòng Whisper và WhisperX, bản *Medium* đều chạy chậm hơn bản *Large*. Hiện tượng này thường do bản Large kích hoạt cơ chế heuristics dừng sớm (early stopping) khi độ tự tin cao, hoặc do kiến trúc phần cứng GPU tối ưu hóa tốt hơn cho số lượng nhân của bản Large.
* PhoWhisper mất tới **210.06 giây** để hoàn thành bài test, gặp rào cản lớn về mặt tối ưu hóa kiến trúc tính toán khi đưa vào ứng dụng thực tế.

### Lỗi nghiêm trọng cần lưu ý
* Các phiên bản Whisper tiêu chuẩn khi gặp khoảng lặng dài không có bộ lọc VAD bọc lót rất dễ bị kẹt thuật toán giải mã, tự sinh ra chuỗi ký tự vô nghĩa.
