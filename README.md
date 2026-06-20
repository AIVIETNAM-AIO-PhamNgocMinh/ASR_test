# So sánh các mô hình ASR Tiếng Việt

Hệ thống tiến hành so sánh toàn diện giữa:

- **OpenAI Whisper**
- **WhisperX** (phiên bản tối ưu hóa căn chỉnh thời gian)
- **PhoWhisper** (mô hình tinh chỉnh chuyên biệt cho tiếng Việt)

Các mô hình được đánh giá trên các phương diện:

- Chất lượng văn bản (`WER`, `CER`)
- Độ chính xác mốc thời gian (`MAE`)

---

# Cấu trúc thư mục

```text
.
├── source/
│   ├── source.mp4
│   └── ground_truth.txt
│
├── result/
│   ├── result_whisper_small.txt
│   ├── result_whisper_medium.txt
│   ├── result_whisper_large.txt
│   ├── result_whisperx_small.txt
│   ├── result_whisperx_medium.txt
│   ├── result_whisperx_large.txt
│   └── result_phowhisper.txt
│
├── transcript/
│   ├── test_whisper.py
│   ├── test_whisperx.py
│   └── test_phowhisper.py
│
└── evaluate/
    └── evaluate.py
```

### Mô tả

| Thư mục/Tệp | Chức năng |
|------------|-----------|
| `source/source.mp4` | Video đầu vào dùng để thử nghiệm |
| `source/ground_truth.txt` | Phụ đề chuẩn được xây dựng thủ công |
| `result/*.txt` | Kết quả nhận dạng từ các mô hình |
| `transcript/*.py` | Script thực hiện transcript |
| `evaluate/evaluate.py` | Script đánh giá và tổng hợp kết quả |

---

# Chỉ số đánh giá

Hệ thống sử dụng các chỉ số phổ biến trong lĩnh vực Automatic Speech Recognition (ASR).

## 1. WER (Word Error Rate)

**Word Error Rate** đo tỷ lệ lỗi ở cấp độ từ, phản ánh số lượng từ bị nhận dạng sai, bị thiếu hoặc bị thừa.

Công thức:

```text
WER = (S + D + I) / N
```

Trong đó:

- `S`: Substitution (thay thế sai)
- `D`: Deletion (thiếu từ)
- `I`: Insertion (thừa từ)
- `N`: Tổng số từ chuẩn

---

## 2. CER (Character Error Rate)

**Character Error Rate** đo tỷ lệ lỗi ở cấp độ ký tự, giúp đánh giá chi tiết hơn các lỗi chính tả hoặc lỗi nhận dạng từng chữ cái.

Công thức:

```text
CER = (S + D + I) / N
```

Trong đó:

- `N` là tổng số ký tự của văn bản chuẩn.

---

## 3. MAE (Mean Absolute Error)

**Mean Absolute Error** được sử dụng để đánh giá độ chính xác của mốc thời gian.

Hệ thống áp dụng thuật toán **Overlap Matching** để ghép các đoạn phụ đề dự đoán với các đoạn chuẩn dựa trên phần giao nhau của thời gian.

Phương pháp này giúp xử lý hiệu quả hiện tượng:

- Lệch dòng phụ đề
- Gộp nhiều câu thành một segment
- Khác biệt do cơ chế Voice Activity Detection của WhisperX

---

# Cách cài đặt và chạy

## 1. Cài đặt môi trường

Đảm bảo hệ thống đã cài đặt Python 3.10+ và FFmpeg

Cài đặt các thư viện cần thiết:

```bash
pip install python-Levenshtein jiwer
```

Ngoài ra cần cài đặt backend tương ứng cho các mô hình:

- `openai-whisper`
- `whisperx`
- `PhoWhisper`

---

## 2. Thực hiện nhận dạng giọng nói (Inference)

Di chuyển vào thư mục `transcript`:

```bash
cd transcript
```

Chạy các mô hình:

### OpenAI Whisper

```bash
python test_whisper.py
```

### WhisperX

```bash
python test_whisperx.py
```

### PhoWhisper

```bash
python test_phowhisper.py
```

Kết quả sẽ được tự động lưu vào thư mục:

```text
result/
```

---

## 3. Đánh giá kết quả

Di chuyển đến thư mục đánh giá:

```bash
cd ../evaluate
```

Chạy script đánh giá:

```bash
python evaluate.py
```

Script sẽ:

1. Đọc file Ground Truth từ:

```text
source/ground_truth.txt
```

2. Tự động quét toàn bộ các tệp:

```text
result/result_*.txt
```

3. Tính toán WER, CER, MAE

4. Xuất bảng tổng hợp kết quả cuối cùng.

---

# Chuẩn hóa dữ liệu văn bản

Trước khi tính toán WER và CER, dữ liệu từ Ground Truth và kết quả mô hình đều được chuẩn hóa thông qua pipeline làm sạch trong `evaluate.py`.

Các bước bao gồm:

1. Loại bỏ timestamp

2. Chuyển về chữ thường

3. Loại bỏ dấu câu và ký tự đặc biệt
4. Chuẩn hóa khoảng trắng
