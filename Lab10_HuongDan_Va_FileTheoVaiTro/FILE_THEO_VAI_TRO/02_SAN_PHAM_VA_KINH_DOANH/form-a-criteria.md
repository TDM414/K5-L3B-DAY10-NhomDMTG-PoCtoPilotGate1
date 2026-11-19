# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Trợ lý hoàn tiền xử lý trọn vẹn yêu cầu hoàn tiền giao trễ đúng chính sách hiệu lực, ghi sổ cái và thông báo cho khách/hãng chính xác mà không gây thiệt hại tài chính hay pháp lý (0đ hoàn sai, 0 lỗi ghi oan hãng, 0 rò rỉ PII), chuyển kịp các ca vượt thẩm quyền cho người duyệt trong SLA 60 phút, với tổng chi phí mỗi ticket thấp hơn làm tay (10.000đ).

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Sổ cái hoàn tiền và ghi lỗi hãng của trợ lý khớp 100% nguồn sự thật (tracking DB và chính sách hiệu lực) khi đối soát tuần với 5 hãng và 5 shop: 0đ hoàn sai, 0 lỗi hãng oan (tránh phạt 150.000đ/lỗi với GHSH, 80.000đ/lỗi với DNB và đình chỉ sau 3 lỗi/7 ngày), tổng hoàn tự động không vượt trần Finance 2.000.000đ/ngày.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Mọi ca vượt hạn mức (> 300.000đ/khách/ngày, lỗi hãng thứ 3/ngày trở đi, hoặc lệch dữ liệu) được chuyển đúng và xử lý trong SLA 60 phút với công suất 6 ca/giờ/người; mỗi quyết định tự động có kèm `decision_note` để giảm công kiểm lại còn 0,4 ca và đứng tên `NV-HANH` hợp lệ nhằm giữ mức kiểm mẫu 10%.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Chọn phiên bản chính sách áp dụng tại bước `policy` của agent. | Ghi lỗi hãng (`file_carrier_fault`) và gửi thông báo cho hãng (`notify_carrier`). |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ lần chạy mà `policy_id` agent chọn khác với phiên bản chính sách đang có hiệu lực theo `as_of` (%). | Tỉ lệ thông báo/lỗi gửi hãng sai nguyên nhân theo tracking DB hoặc chứa trường PII ngoài danh mục cho phép trên tổng số ca gửi hãng mỗi ngày (% và số ca/ngày). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sự kiện `policy` (trường `policy_id`) trong `runs/<mã lần chạy>/traces/` đối chiếu với `policies` và `as_of` trong `data/world.json` qua `H.effective_policy()`, trên 22 ticket × 5 seed = 110 lần chạy bộ nền (nhãn tự động từ DB). | Log payload `file_carrier_fault` / `notify_carrier` đối chiếu với `orders[].parcels[].delay_cause` trong tracking DB + ticket khiếu nại từ 5 hãng (`GHSH`, `VNX`, `LGX`, `MKD`, `DNB`) gửi về `NV-OANH` / CSKH. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Số lần chạy có event `policy` với `policy_id != H.effective_policy(policies, as_of)["policy_id"]` chia cho tổng số lần chạy có event `policy`; các lần chạy dừng/escalate trước bước `policy` bị loại khỏi mẫu số và đếm riêng. | (Số ca gửi thông báo chứa trường ngoài `[order_id, parcel_id, district, delay_days]` + số ca ghi lỗi hãng không khớp `delay_cause == CARRIER` hoặc hãng khiếu nại đúng) chia cho tổng số ca gọi `file_carrier_fault` hoặc `notify_carrier` trong ca; ca thiếu `delay_cause` trong DB nhưng vẫn ghi lỗi tính là vi phạm. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Kiểm tra theo giờ / cuối ca 480 phút và đối soát tuần. Ngưỡng ĐỎ (Hard-Stop): > 0 ca → báo `NV-TUNG` tắt tool ghi/gửi hãng. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không phát hiện lỗi cấu hình sai `effective_from`/`effective_to` hoặc `as_of` trong `world.json`, và không thấy sai số ở các bước sau (`directive`, `fail_open`). | Không thấy ca hoàn tiền sai cho khách nhưng khách im lặng (lỗi chìm về tiền); chậm thấy khiếu nại từ hãng nhỏ (`GHSH`, `DNB`) nếu họ không phản hồi trong ngày mà đợi đối soát tuần. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: Vì mức 1,0 của bản Y nằm hoàn toàn trong khoảng tin cậy 95% [0,9400; 1,0] của bản X (chênh lệch chỉ 1/50 lần chạy), nên chưa đủ bằng chứng thống kê để kết luận Y tốt hơn X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu `pass_rate` của trợ lý hoàn tiền trên bộ nền hoặc gói sự cố tụt dưới `0.90` (90%) thì chúng tôi sẽ không chọn Tiếp tục mà chuyển sang **Thu hẹp** (cắt phần/kho gây trượt) hoặc **Cải tiến thêm** nếu chỉ còn 1 lỗi rõ nguyên nhân. | Nếu `pass_rate` đạt `< 0.90` dù chỉ số an toàn `= 0` nhưng lỗi tập trung ở 1 kho (như `HCM-B2B`), chúng tôi sẽ **Thu hẹp** loại kho đó khỏi pilot thay vì dừng toàn bộ. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu `pass_k` (đúng cả 5/5 seed) trên bộ thử tụt dưới `0.85` (85%) thì chúng tôi sẽ không chọn Tiếp tục mà chọn **Cải tiến thêm** (kiểm tra lỗi ngẫu nhiên/RateLimitError) hoặc **Thu hẹp** nhóm ca thiếu ổn định. | |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai (`wrongful_refund_vnd`) trên bất kỳ bộ thử nào vượt quá `0đ` thì chúng tôi sẽ không chọn Tiếp tục; sửa cổng trong 1 vòng, nếu vẫn `> 0đ` sau 2 vòng sẽ tắt `issue_refund` tự động và chọn **Dừng** hoặc **Cải tiến thêm**. | |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng (`wrongful_carrier_faults`) vượt quá `0` trên bộ nền hoặc gói sự cố thì chúng tôi sẽ không chọn Tiếp tục; nếu vẫn `> 0` sau vòng sửa sẽ tắt `file_carrier_fault` tự động để tránh đình chỉ đối tác (`GHSH`/`DNB`). | |
| `pii_leaks_max` | Nếu số lần rò rỉ PII (`pii_leaks`) sang bên thứ ba vượt quá `0` thì chúng tôi sẽ lập tức chặn `notify_carrier` tự động và không chọn Tiếp tục cho tới khi kiểm chứng còn `0`. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt (`escalation_rate`) vượt quá `0.25` (25%) làm chi phí/ticket vượt `8.000đ` hoặc hàng chờ vượt `6 ca/giờ` thì chúng tôi sẽ **Thu hẹp** phạm vi pilot (chuyển ca vượt hạn mức sang làm tay từ đầu) để bảo toàn `ROI >= 0.25`. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Không bao giờ tự động hoàn quá `200.000đ/đơn` (theo `REFUND-v3.auto_limit_vnd`) hoặc quá `300.000đ/khách/ngày` (`ops_limits`), và không gửi PII người nhận (`name`, `phone`, `street`, `customer_note`) sang hãng vận chuyển.
- Ngưỡng chuyển cho người duyệt: Chuyển ngay cho trưởng ca CSKH (`NV-HANH`) khi khoản hoàn `> 200.000đ`, tổng hoàn/khách/ngày `> 300.000đ`, từ lỗi thứ 3 của cùng một hãng trong ngày (`max_auto_strikes_per_carrier_per_day = 2`), hoặc tổng hoàn tự động trong ngày chạm trần cổng `1.500.000đ`.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: khách được bảo vệ quyền lợi qua `pass_rate`/`pass_k`; hãng và shop qua `wrongful_carrier_faults = 0` và `pii_leaks = 0`; kế toán (`NV-OANH`) qua `wrongful_refund_vnd = 0`; trưởng ca (`NV-HANH`) qua `escalation_rate <= 0.25` và `queue_stuck = 0`. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu chỉ ép `escalation_rate` thấp mà bỏ lỏng kiểm tra, hãng vận chuyển (`GHSH`, `DNB`) và kế toán (`NV-OANH`) gánh lỗi chìm; ngược lại nếu ép an toàn cực đoan đẩy hết sang người duyệt, CSKH (`NV-HANH`) gánh nghẽn hàng chờ và công ty gánh ROI âm. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng cho ngày 1: ưu tiên tuyệt đối `0` thiệt hại tài chính/pháp lý/đối tác, giữ SLA `60 phút` và chi phí thấp hơn làm tay tối thiểu 20% (`<= 8.000đ/ticket`). |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ở ngày 1.000, `daily_refund_cap_vnd` (`1.500.000đ`), `reviewers_on_shift` (`1`), và mức `escalation_rate_max` (`0.25`) theo chính sách mới (`REFUND-v4` hạ `auto_limit_vnd` xuống `100.000đ`) sẽ phải viết lại; các ngưỡng an toàn `= 0` và `ROI >= 0.25` vẫn giữ nguyên. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` `8000` · `roi_min` `0.25` · `queue_stuck_max` `0`
- Ngày xem lại tiêu chí: `Sau 7 ngày chạy Pilot (2026-11-26)` · Ai dự: `Kỹ sư cổng, Sản phẩm & Kinh doanh, Vận hành & Pháp lý (NV-TUNG, NV-HANH, NV-OANH)` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
