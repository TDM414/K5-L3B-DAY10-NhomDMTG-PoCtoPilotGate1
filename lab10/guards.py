"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    """Cổng 1: Ghim phiên bản chính sách đang có hiệu lực theo ctx.as_of."""
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if pol:
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


def _guard_issue_refund(ctx, action, pol, order, parcel, delay):
    """Cổng 2: Chặn hoàn đúp, khóa quyền lợi theo tracking DB, và kiểm trần/hạn mức."""
    order_id = action.get("order_id")
    entitlement = H.entitlement_vnd(pol, order, delay, parcel.get("delay_cause"))
    if entitlement <= 0:
        return Verdict.deny("không đủ điều kiện hoàn tiền theo tracking DB và chính sách hiệu lực")

    refunded = sum(r.get("amount_vnd", 0) for r in ctx.tools.ledger_rows(order_id=order_id))
    if refunded >= entitlement:
        return Verdict.deny("đơn hàng đã được hoàn đủ quyền lợi theo chính sách")
    refund_due = entitlement - refunded

    limits = ctx.tools.ops_limits()
    cust_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
    cust_id = order.get("customer_id")
    cust_spent = sum(
        r.get("amount_vnd", 0)
        for r in ctx.tools.ledger_rows(customer_id=cust_id)
        if not r.get("approval_id")
    )

    approval_id = action.get("approval_id")
    has_valid_approval = bool(
        approval_id and ctx.tools.lookup_approvals(approval_id=approval_id, order_id=order_id)
    )
    if not has_valid_approval:
        if refund_due > pol.get("auto_limit_vnd", 0):
            return Verdict.escalate("khoản hoàn vượt auto_limit_vnd và chưa có phê duyệt hợp lệ")
        if cust_cap is not None and cust_spent + refund_due > cust_cap:
            return Verdict.escalate("tổng hoàn tự động trong ngày vượt trần khách hàng")

    if action.get("amount_vnd") != refund_due or action.get("payer") != "LOGIX":
        return Verdict.modify(
            "điều chỉnh số tiền hoàn còn thiếu và người trả đúng quyền lợi từ tracking DB",
            amount_vnd=refund_due,
            payer="LOGIX",
        )
    return Verdict.allow()


def _guard_file_carrier_fault(ctx, action, pol, order, parcel, delay):
    """Cổng 3a: Chỉ ghi lỗi hãng khi đủ điều kiện theo DB, đúng kiện trễ và không vượt trần strike."""
    if not H.carrier_at_fault(pol, parcel, delay):
        return Verdict.deny("không đủ căn cứ lỗi hãng theo tracking DB và chính sách hiệu lực")

    parcel_id = parcel.get("parcel_id")
    if ctx.tools.fault_rows(order_id=order.get("order_id"), parcel_id=parcel_id):
        return Verdict.deny("kiện hàng này đã được ghi lỗi hãng trước đó")

    carrier_id = parcel.get("carrier_id")
    max_strikes = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    if max_strikes is not None and len(ctx.tools.fault_rows(carrier_id=carrier_id)) >= max_strikes:
        return Verdict.escalate("vượt số lỗi hãng tự động tối đa trong ngày")

    if (
        action.get("parcel_id") != parcel_id
        or action.get("carrier_id") != carrier_id
        or action.get("delay_days") != delay
    ):
        return Verdict.modify(
            "khóa đúng kiện hàng trễ, hãng vận chuyển và số ngày trễ từ tracking DB",
            parcel_id=parcel_id,
            carrier_id=carrier_id,
            delay_days=delay,
        )
    return Verdict.allow()


def _guard_notify_carrier(pol, action):
    """Cổng 3b: Whitelist payload gửi hãng theo carrier_notice_fields để chặn rò rỉ PII."""
    allowed_fields = set(pol.get("carrier_notice_fields", []))
    payload = action.get("payload") or {}
    if not allowed_fields or set(payload.keys()).issubset(allowed_fields):
        return Verdict.allow()
    clean_payload = {k: v for k, v in payload.items() if k in allowed_fields}
    return Verdict.modify("loại bỏ trường ngoài carrier_notice_fields để chống rò rỉ PII", payload=clean_payload)


def write_gate(ctx, action):
    """Cổng phòng ngừa trước mỗi lệnh ghi."""
    tool = action.get("tool")
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if not pol:
        return Verdict.escalate("không tìm thấy chính sách hiệu lực theo as_of")

    if tool == "notify_carrier":
        return _guard_notify_carrier(pol, action)

    if tool in ("issue_refund", "file_carrier_fault"):
        order = ctx.tools.lookup_order(action.get("order_id"))
        if not order or not order.get("parcels"):
            return Verdict.escalate("không tìm thấy đơn hàng hoặc kiện hàng trong DB")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        delay = H.db_delay_days(parcel, ctx.as_of)
        if tool == "issue_refund":
            return _guard_issue_refund(ctx, action, pol, order, parcel, delay)
        return _guard_file_carrier_fault(ctx, action, pol, order, parcel, delay)

    return Verdict.allow()
