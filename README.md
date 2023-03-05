# VnGPT - AI cho mọi nhà
Phần mềm nguồn mở giúp mỗi cá nhân trực tiếp sử dụng ChatGPT và hơn thế nữa ngay trên máy tính của mình

## Cài đặt và sử dụng
Để sử dụng VnGPT bạn cần các thông tin sau:
- [OpenAI API Key lấy ở đây](https://platform.openai.com/account/api-keys)

### VnGPT Cài đặt trên Windows
1. Cài đặt [Python 3.10.6](https://www.python.org/downloads/windows/), tích chọn vào "Add Python to PATH" trong quá trình cài đặt
2. Cài đặt git [git](https://git-scm.com/download/win).
3. Tải về mã nguồn của VnGPT bằng cách sử dụng command promt và chạy lệnh sau:  `git clone https://github.com/AIV-Group/VnGPT-CE`.
4. Tiếp theo bạn mở thư mục mã nguồn VnGPT đã tải về và copy file `.env.example` thành file `.env` sau đó thay đoạn `your_open_api_key` thành Open API Key của bạn.
5. Tiếp theo bạn kích đúp chuột vào file `run.bat` ở thư mục mã nguồn VnGPT và chờ đợi chương trình khởi chạy.
6. Sau khi chương trình đã chạy bạn có thể mở đường dẫn `http://127.0.0.1:7860` trên trình duyệt để sử dụng VnGPT.

### VnGPT cài đặt trên Linux
Để chạy các lệnh dưới đây bạn cần sử dụng Terminal trên máy của bạn
1. Cài đặt python (phiên bản 3.10.6 trở lên):
```bash
# Debian-based:
sudo apt install wget git python3 python3-venv
# Red Hat-based:
sudo dnf install wget git python3
# Arch-based:
sudo pacman -S wget git python3
```
2. Tiếp theo tải về mã nguồn của VnGPT bằng lệnh sau:
```bash
git clone https://github.com/AIV-Group/VnGPT-CE
```
3. Tiếp theo bạn mở thư mục mã nguồn VnGPT đã tải về và copy file `.env.example` thành file `.env` sau đó thay đoạn `your_open_api_key` thành Open API Key của bạn.
4. Tiếp theo chạy file `bash run.sh` để chương trình khởi chạy. (Có thể bạn cần chạy thêm lệnh `chmod +x run.sh` để cấp quyền chạy chương trình cho VnGPT)
5. Sau khi chương trình đã chạy bạn có thể mở đường dẫn `http://127.0.0.1:7860` trên trình duyệt để sử dụng VnGPT.