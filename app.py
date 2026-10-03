import streamlit as st
st.image("logo.jpg")
import pandas as pd

# =========================
# CẤU HÌNH GIAO DIỆN
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 ỨNG DỤNG TÍNH LÃI GỬI TIẾT KIỆM")
st.write(
    "Nhập thông tin khoản tiền gửi để tính tiền lãi "
    "và tổng số tiền nhận được khi đáo hạn."
)

st.divider()


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_vnd(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin khoản tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_goc = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=100_000,
        value=10_000_000,
        step=1_000_000,
        format="%d"
    )

    ky_han = st.number_input(
        "Kỳ hạn gửi (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

with col2:
    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    )

    hinh_thuc = st.selectbox(
        "Hình thức nhận lãi",
        ["Cuối kỳ", "Hàng tháng", "Hàng quý"]
    )

phuong_phap = st.radio(
    "Phương pháp tính lãi",
    ["Lãi đơn", "Lãi kép"],
    horizontal=True
)

st.caption(
    "Lãi suất được tính theo năm. Với lãi kép, tiền lãi được "
    "nhập vào gốc theo chu kỳ đã chọn. Vì vậy, hàng tháng và "
    "hàng quý là chu kỳ tính lãi/tái đầu tư trong mô hình này."
)

st.divider()


# =========================
# TÍNH TOÁN LÃI
# =========================
if st.button("🧮 TÍNH TIỀN LÃI", type="primary", use_container_width=True):

    lai_suat_nam = lai_suat / 100

    # Xác định chu kỳ tính lãi theo tháng
    if hinh_thuc == "Hàng tháng":
        chu_ky = 1
    elif hinh_thuc == "Hàng quý":
        chu_ky = 3
    else:
        chu_ky = int(ky_han)

    so_tien_hien_tai = float(tien_goc)
    tong_lai = 0.0
    bang_chi_tiet = []

    thang_da_tinh = 0
    ky = 0

    while thang_da_tinh < ky_han:
        ky += 1

        # Hỗ trợ cả kỳ hạn không chia hết cho 3
        so_thang_ky_nay = min(
            chu_ky,
            int(ky_han) - thang_da_tinh
        )

        # Lãi suất quy đổi theo số tháng của kỳ
        lai_ky = (
            so_tien_hien_tai
            * lai_suat_nam
            * so_thang_ky_nay / 12
        )

        if phuong_phap == "Lãi đơn":
            # Lãi luôn tính trên số tiền gốc ban đầu
            lai_ky = (
                tien_goc
                * lai_suat_nam
                * so_thang_ky_nay / 12
            )
        else:
    # Lãi kép: lãi được cộng vào số dư sau mỗi kỳ
            so_tien_hien_tai += lai_ky

        tong_lai += lai_ky
        thang_da_tinh += so_thang_ky_nay

        bang_chi_tiet.append({
            "Kỳ": ky,
            "Thời gian": (
                f"Tháng {thang_da_tinh - so_thang_ky_nay + 1}"
                if so_thang_ky_nay == 1
                else
                f"Tháng {thang_da_tinh - so_thang_ky_nay + 1}"
                f" - {thang_da_tinh}"
            ),
            "Số dư đầu kỳ (VNĐ)": (
                tien_goc
                if phuong_phap == "Lãi đơn"
                else so_tien_hien_tai - lai_ky
            ),
            "Tiền lãi kỳ này (VNĐ)": lai_ky,
            "Lũy kế tiền lãi (VNĐ)": tong_lai,
            "Số dư cuối kỳ (VNĐ)": (
                tien_goc + tong_lai
                if phuong_phap == "Lãi đơn"
                else so_tien_hien_tai
            )
        })

    tong_tien = tien_goc + tong_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("Đã tính toán thành công!")

    st.subheader("💰 Kết quả tính lãi")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiền lãi kỳ đầu tiên",
            format_vnd(bang_chi_tiet[0]["Tiền lãi kỳ này (VNĐ)"])
        )

        st.metric(
            "Tổng tiền gốc",
            format_vnd(tien_goc)
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            format_vnd(tong_lai)
        )

        st.metric(
            "Tổng gốc + lãi",
            format_vnd(tong_tien)
        )

    st.caption(
        f"Phương pháp: {phuong_phap} | "
        f"Kỳ hạn: {ky_han} tháng | "
        f"Lãi suất: {lai_suat:.2f}%/năm | "
        f"Hình thức: {hinh_thuc}"
    )

    st.divider()

    # =========================
    # BẢNG CHI TIẾT
    # =========================
    st.subheader("📊 Chi tiết tiền lãi theo từng kỳ")

    df = pd.DataFrame(bang_chi_tiet)

    # Định dạng số tiền để dễ đọc
    cot_tien = [
        "Số dư đầu kỳ (VNĐ)",
        "Tiền lãi kỳ này (VNĐ)",
        "Lũy kế tiền lãi (VNĐ)",
        "Số dư cuối kỳ (VNĐ)"
    ]

    df_hien_thi = df.copy()

    for cot in cot_tien:
        df_hien_thi[cot] = df_hien_thi[cot].apply(
            lambda x: f"{x:,.0f}".replace(",", ".")
        )

    st.dataframe(
        df_hien_thi,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # TẢI KẾT QUẢ
    # =========================
    csv = df.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        label="📥 Tải bảng chi tiết (CSV)",
        data=csv,
        file_name="chi_tiet_tien_lai.csv",
        mime="text/csv",
    use_container_width=True
    )

    st.info(
        "Lưu ý: Đây là kết quả mô phỏng theo công thức lãi đơn "
        "hoặc lãi kép, giả định lãi suất không đổi trong suốt "
        "kỳ hạn. Kết quả thực tế tại ngân hàng có thể khác do "
        "quy ước số ngày tính lãi, ngày đáo hạn, thuế hoặc phí."
    )
