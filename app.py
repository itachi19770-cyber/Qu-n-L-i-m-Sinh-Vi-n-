import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Tiêu đề ứng dụng theo đúng yêu cầu đề bài
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# 1. Tạo dữ liệu mẫu của 10 sinh viên
data = {
    "Ho_va_ten": [
        "An",
        "Bình",
        "Chi",
        "Đông",
        "Hà",
        "Lan",
        "Minh",
        "Nam",
        "Phúc",
        "Thông",
    ],
    "Chuyen_can": [9.0, 8.0, 7.5, 10.0, 8.5, 6.0, 9.0, 7.5, 8.0, 9.5],
    "Giua_ky": [8.0, 7.5, 7.0, 9.0, 7.5, 6.5, 8.5, 7.0, 7.5, 9.0],
    "Cuoi_ky": [8.5, 8.0, 7.5, 9.5, 8.0, 6.0, 9.0, 7.5, 8.0, 9.5],
}

df = pd.DataFrame(data)

# Tính điểm tổng kết theo công thức: 20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"] + 0.3 * df["Giua_ky"] + 0.5 * df["Cuoi_ky"]
).round(2)


# Xếp loại sinh viên theo bảng quy định
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"


df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# 2. Hiển thị bảng điểm của 10 sinh viên
st.subheader("Bảng điểm chi tiết của sinh viên")
st.dataframe(df)

# 3. Thống kê cơ bản
st.subheader("Thông tin thống kê chung")
diem_tb_lop = df["Tong_ket"].mean()
sv_max = df.loc[df["Tong_ket"].idxmax()]["Ho_va_ten"]
sv_min = df.loc[df["Tong_ket"].idxmin()]["Ho_va_ten"]
so_sv_dat = (df["Tong_ket"] >= 5.0).sum()

col1, col2 = st.columns(2)
col1.metric("Điểm trung bình lớp", f"{diem_tb_lop:.2f}")
col1.metric("Số sinh viên đạt (>= 5 điểm)", so_sv_dat)

col2.metric("Sinh viên điểm cao nhất", sv_max)
col2.metric("Sinh viên điểm thấp nhất", sv_min)

# 4. Tạo Selectbox để chọn sinh viên và xem chi tiết
st.subheader("Tra cứu thông tin cá nhân sinh viên")
selected_student = st.selectbox("Chọn tên sinh viên:", df["Ho_va_ten"])

student_info = df[df["Ho_va_ten"] == selected_student].iloc[0]

st.write(f"- **Họ tên:** {student_info['Ho_va_ten']}")
st.write(f"- **Điểm Chuyên cần:** {student_info['Chuyen_can']}")
st.write(f"- **Điểm Giữa kỳ:** {student_info['Giua_ky']}")
st.write(f"- **Điểm Cuối kỳ:** {student_info['Cuoi_ky']}")
st.write(f"- **Điểm Tổng kết:** {student_info['Tong_ket']}")
st.write(f"- **Xếp loại:** {student_info['Xep_loai']}")

# 5. Hiển thị biểu đồ cột điểm tổng kết
st.subheader("Biểu đồ cột điểm tổng kết của 10 sinh viên")
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(df["Ho_va_ten"], df["Tong_ket"], color="skyblue")
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Tên sinh viên")
ax.set_title("Biểu đồ điểm tổng kết")
ax.set_xlim(0, 10)
ax.grid(axis="x", linestyle="--", alpha=0.5)
st.pyplot(fig)

# 6. Hiển thị họ tên và MSSV ở cuối trang với kích thước chữ nhỏ
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: small; color: gray;'>Họ và tên: [Tên của bạn] - MSSV: [Mã số sinh viên của bạn]</p>",
    unsafe_allow_html=True,
)