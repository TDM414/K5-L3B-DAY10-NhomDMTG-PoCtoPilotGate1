# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `NhomDMTG`
- Lớp: `L3B`
- Repo của bàn: `https://github.com/TDM414/K5-L3B-DAY10-NhomDMTG-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S5`

## Thành viên

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
| 1 | Nguyễn Xuân Dương | 2A202603955 | Trưởng nhóm, điều phối chung | Có |
| 2 | Trần Duy Mạnh | 2A202603998 | Sản phẩm và kinh doanh | Không |
| 3 | Đinh Lê Thịnh | 2A202603953 | Kỹ sư cổng | Không |
| 4 | Trần Thị Hồng Gấm | 2A202603967 | Vận hành và pháp lý | Không |

`submission/submission.json` dùng định dạng `HoVaTen-MSSV`, không dấu.

## Cá nhân

## NguyenXuanDuong-2A202603955

### Phần việc phụ trách

Trưởng nhóm; điều phối các mốc CP2–CP5, thống nhất phạm vi pilot và tổng hợp quyết định Gate 1.

### Đóng góp cụ thể

Điều phối nhóm hoàn tất Phiếu A/B/C, đối chiếu quyết định với tiêu chí đã ký và tổng hợp bằng chứng cho bài nộp.

### Bằng chứng

Tiêu chí ký tại commit `7c42f21`; mốc cổng vòng 1 `4bbf36bc`; báo cáo S5 cuối `R-S5-grade-20261119-170854-0400f3`.

### Exit ticket

Học được rằng quyết định Gate 1 phải dựa trên số liệu từng phân khúc, không chỉ điểm trung bình toàn pilot. Còn chưa chắc mức chi phí thực tế và tải của hàng chờ thủ công khi loại một kho khỏi pilot.

## TranDuyManh-2A202603998

### Phần việc phụ trách

Vai Sản phẩm và kinh doanh; mục tiêu sản phẩm, ngưỡng chấp nhận, chi phí, ROI và phạm vi pilot.

### Đóng góp cụ thể

Hoàn thiện Phiếu A và Bản tiêu chí đã ký; đề xuất trần chi phí, ROI và thu hẹp phạm vi khỏi kho `HCM-B2B` khi chi phí mỗi ticket vượt làm tay.

### Bằng chứng

Phiếu A và `config/acceptance_criteria.json`; commit ký tiêu chí `7c42f21`; quyết định và số đo S5 trong Phiếu C mục C12.

### Exit ticket

Học được rằng lợi nhuận toàn pilot có thể che một phân khúc lỗ. Còn cần đo thêm chi phí và tỷ lệ ticket theo kho khi chạy pilot thật.

## DinhLeThinh-2A202603953

### Phần việc phụ trách

Kỹ sư cổng; triển khai `pre_guard`, `write_gate`, kiểm thử hồi quy và chỉ số giám sát.

### Đóng góp cụ thể

Hoàn thiện cổng kiểm tra khoản hoàn theo tracking và sổ cái, xử lý hoàn phần quyền lợi còn thiếu mà không hoàn đúp; bổ sung monitor chi phí cao nhất theo kho.

### Bằng chứng

`lab10/guards.py`, `lab10/monitors.py`; commit CP3 `0bea693`; trace `S5-21@11` và báo cáo cuối `R-S5-after-20261119-170855-0400f3`.

### Exit ticket

Học được rằng kiểm tra có dòng sổ cái thôi chưa đủ: cần so số đã hoàn với quyền lợi tổng để vừa ngăn hoàn đúp vừa cho phép hoàn phần còn thiếu. Còn chưa chắc cách xử lý đồng thời khi sổ cái production cập nhật trễ.

## TranThiHongGam-2A202603967

### Phần việc phụ trách

Vận hành và pháp lý; risk register, checklist go-live, runbook, cổng vận hành và nội dung nộp bài.

### Đóng góp cụ thể

Phân tích tác động S5 theo kho và chi phí, cập nhật runbook/checklist; cùng nhóm đặt phạm vi pilot không gồm `HCM-B2B` và yêu cầu theo dõi chi phí theo kho.

### Bằng chứng

Commit `f674752`; `config/operating_gates.json`; Phiếu C mục C1, C8, C10–C12; báo cáo cuối `R-S5-grade-20261119-170854-0400f3`.

### Exit ticket

Học được rằng thêm người duyệt không giải quyết được phân khúc mà mọi ticket đều chuyển người và trở nên đắt hơn làm tay. Còn cần xác minh khả năng xử lý của CSKH đối với ticket bị đưa ra ngoài phạm vi pilot.
