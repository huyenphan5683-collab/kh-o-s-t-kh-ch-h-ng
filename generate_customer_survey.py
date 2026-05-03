import random
import numpy as np
import pandas as pd
from pathlib import Path

# =========================
# CONFIG
# =========================

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "smartlog_tms_customer_survey_2023_2025.xlsx"

RESPONSES_BY_YEAR = {
    2023: 48,
    2024: 56,
    2025: 65
}

COMPANIES = [
    "Nutifood", "Sabeco", "Sotrans", "SAFI", "SNPL",
    "Minh Phu Logistics", "An Phat Distribution", "Hoa Sen Logistics",
    "Nam Viet Transport", "Phuc Long Distribution", "Mekong Freight",
    "VietStar Logistics", "Delta Transport", "GreenLine Supply Chain",
    "Tan Cang Logistics", "Binh Minh Trading", "Dong A Warehouse",
    "Sai Gon Distribution", "VinaCold Logistics", "Blue Ocean Freight"
]

POSITIONS = [
    "Logistics Manager", "Transport Manager", "Operations Manager",
    "Warehouse Manager", "Supply Chain Executive", "Customer Service Manager",
    "Planning Executive", "Fleet Coordinator", "Distribution Supervisor",
    "IT/System Admin", "Import-Export Executive"
]

FUNCTIONS = [
    "Đơn hàng",
    "Giám sát",
    "Thanh toán",
    "Báo cáo",
    "Quản lí đội xe",
    "Thiết lập đội xe, khách hàng, nhà thầu",
    "Thiết lập excel"
]

YEAR_PROFILES = {
    2023: {
        "system_speed": 3.35,
        "interface": 3.40,
        "features": 3.45,
        "support_response": 3.50,
        "support_resolution": 3.38,
        "system_knowledge": 4.10,  # thang 1-6
        "business_process_knowledge": 3.30
    },
    2024: {
        "system_speed": 3.50,
        "interface": 3.55,
        "features": 3.60,
        "support_response": 3.65,
        "support_resolution": 3.52,
        "system_knowledge": 4.30,  # thang 1-6
        "business_process_knowledge": 3.45
    },
    2025: {
        "system_speed": 3.68,
        "interface": 3.72,
        "features": 3.78,
        "support_response": 3.82,
        "support_resolution": 3.70,
        "system_knowledge": 4.55,  # thang 1-6
        "business_process_knowledge": 3.62
    }
}

IMPROVEMENT_COMMENTS = {
    "system_speed": [
        "Cần cải thiện tốc độ phản hồi của hệ thống, đặc biệt khi xử lý nhiều đơn hàng.",
        "Hệ thống nên tải dữ liệu nhanh hơn vào giờ cao điểm.",
        "Cần tối ưu tốc độ đồng bộ dữ liệu và xuất báo cáo."
    ],
    "interface": [
        "Giao diện cần trực quan hơn và dễ sử dụng hơn.",
        "Một số màn hình thao tác còn phức tạp, cần đơn giản hóa.",
        "Nên cải thiện bố cục hiển thị để dễ theo dõi trạng thái đơn hàng."
    ],
    "features": [
        "Cần bổ sung thêm tính năng báo cáo linh hoạt hơn.",
        "Nên cải thiện chức năng cảnh báo trễ giao hàng.",
        "Một số tính năng nên tùy chỉnh tốt hơn theo quy trình vận hành thực tế."
    ],
    "support_response": [
        "Đội hỗ trợ nên phản hồi nhanh hơn khi có lỗi phát sinh.",
        "Cần cập nhật tiến độ xử lý thường xuyên hơn cho khách hàng.",
        "Nên có kênh hỗ trợ ưu tiên cho lỗi ảnh hưởng đến vận hành."
    ],
    "support_resolution": [
        "Câu trả lời của đội hỗ trợ cần cụ thể và dễ áp dụng hơn.",
        "Cần xử lý vấn đề dứt điểm hơn để tránh phát sinh lại.",
        "Nên giải thích rõ nguyên nhân lỗi và hướng phòng tránh."
    ],
    "business_process_knowledge": [
        "Nhân viên hỗ trợ nên hiểu rõ hơn quy trình vận hành của doanh nghiệp.",
        "Cần tư vấn giải pháp phù hợp hơn với thực tế vận tải.",
        "Đội hỗ trợ nên nắm rõ hơn các tình huống đặc thù trong logistics."
    ]
}


# =========================
# FUNCTIONS
# =========================

def likert_score(mean, scale_max=5):
    score = int(round(np.random.normal(loc=mean, scale=0.85)))
    return max(1, min(scale_max, score))


def choose_functions():
    k = np.random.choice([2, 3, 4, 5], p=[0.20, 0.35, 0.30, 0.15])
    return "; ".join(random.sample(FUNCTIONS, k))


def get_theme_and_comment(row):
    weak = []

    if row["Tốc độ phản hồi của hệ thống"] <= 3:
        weak.append("system_speed")
    if row["Giao diện hệ thống"] <= 3:
        weak.append("interface")
    if row["Tính năng hệ thống"] <= 3:
        weak.append("features")
    if row["Thời gian phản hồi của đội hỗ trợ"] <= 3:
        weak.append("support_response")
    if row["Câu trả lời của đội hỗ trợ giải quyết được vấn đề"] <= 3:
        weak.append("support_resolution")
    if row["Nhân viên hỗ trợ có hiểu biết về quy trình vận hành của doanh nghiệp"] <= 3:
        weak.append("business_process_knowledge")

    if not weak:
        weak = [random.choice(["features", "support_response", "support_resolution", "interface"])]

    theme = random.choice(weak)
    comment = random.choice(IMPROVEMENT_COMMENTS[theme])
    return theme, comment


def satisfaction_group(avg_score):
    if avg_score >= 4:
        return "Satisfied"
    elif avg_score >= 3:
        return "Neutral"
    else:
        return "Dissatisfied"


# =========================
# GENERATE RAW SURVEY DATA
# =========================

rows = []

for year, n in RESPONSES_BY_YEAR.items():
    profile = YEAR_PROFILES[year]

    for i in range(1, n + 1):
        row = {
            "Năm khảo sát": year,
            "Mã phản hồi": f"SV-{year}-{i:03d}",
            "Anh/chị hãy cho biết tên công ty của anh/chị": random.choice(COMPANIES),
            "Anh/chị hãy cho biết chức vụ hiện tại của anh/chị": random.choice(POSITIONS),
            "Những chức năng mà anh/chị đang sử dụng trên hệ thống": choose_functions(),

            "Tốc độ phản hồi của hệ thống": likert_score(profile["system_speed"], 5),
            "Giao diện hệ thống": likert_score(profile["interface"], 5),
            "Tính năng hệ thống": likert_score(profile["features"], 5),
            "Thời gian phản hồi của đội hỗ trợ": likert_score(profile["support_response"], 5),
            "Câu trả lời của đội hỗ trợ giải quyết được vấn đề": likert_score(profile["support_resolution"], 5),

            # Theo form gốc: câu này thang 1-6
            "Nhân viên hỗ trợ có hiểu biết về hệ thống": likert_score(profile["system_knowledge"], 6),

            "Nhân viên hỗ trợ có hiểu biết về quy trình vận hành của doanh nghiệp": likert_score(profile["business_process_knowledge"], 5),
        }

        # Quy đổi câu thang 6 về thang 5 để tính điểm trung bình chung
        normalized_system_knowledge = row["Nhân viên hỗ trợ có hiểu biết về hệ thống"] / 6 * 5

        csat_items = [
            row["Tốc độ phản hồi của hệ thống"],
            row["Giao diện hệ thống"],
            row["Tính năng hệ thống"],
            row["Thời gian phản hồi của đội hỗ trợ"],
            row["Câu trả lời của đội hỗ trợ giải quyết được vấn đề"],
            normalized_system_knowledge,
            row["Nhân viên hỗ trợ có hiểu biết về quy trình vận hành của doanh nghiệp"]
        ]

        avg_csat = round(float(np.mean(csat_items)), 2)

        row["Average CSAT"] = avg_csat
        row["Satisfaction Group"] = satisfaction_group(avg_csat)

        theme, comment = get_theme_and_comment(row)
        row["Feedback Theme"] = theme
        row["Để nâng cao chất lượng dịch vụ, Smartlog nên cải thiện những gì?"] = comment

        rows.append(row)

df = pd.DataFrame(rows)

# =========================
# SUMMARY
# =========================

summary_year = df.groupby("Năm khảo sát").agg(
    Survey_Responses=("Mã phản hồi", "count"),
    Average_CSAT=("Average CSAT", "mean"),
    Satisfied_Rate=("Satisfaction Group", lambda x: (x == "Satisfied").mean()),
    Neutral_Rate=("Satisfaction Group", lambda x: (x == "Neutral").mean()),
    Dissatisfied_Rate=("Satisfaction Group", lambda x: (x == "Dissatisfied").mean()),
    Avg_System_Speed=("Tốc độ phản hồi của hệ thống", "mean"),
    Avg_Interface=("Giao diện hệ thống", "mean"),
    Avg_Features=("Tính năng hệ thống", "mean"),
    Avg_Support_Response=("Thời gian phản hồi của đội hỗ trợ", "mean"),
    Avg_Support_Resolution=("Câu trả lời của đội hỗ trợ giải quyết được vấn đề", "mean"),
    Avg_System_Knowledge=("Nhân viên hỗ trợ có hiểu biết về hệ thống", "mean"),
    Avg_Business_Process_Knowledge=("Nhân viên hỗ trợ có hiểu biết về quy trình vận hành của doanh nghiệp", "mean")
).reset_index()

for col in summary_year.columns:
    if col not in ["Năm khảo sát", "Survey_Responses"]:
        summary_year[col] = summary_year[col].round(4)

theme_summary = (
    df.groupby(["Năm khảo sát", "Feedback Theme"])
    .size()
    .reset_index(name="Count")
)

theme_summary["Theme Share"] = theme_summary.groupby("Năm khảo sát")["Count"].transform(lambda x: x / x.sum())
theme_summary["Theme Share"] = theme_summary["Theme Share"].round(4)

function_rows = []
for _, r in df.iterrows():
    for fn in r["Những chức năng mà anh/chị đang sử dụng trên hệ thống"].split("; "):
        function_rows.append({
            "Năm khảo sát": r["Năm khảo sát"],
            "Mã phản hồi": r["Mã phản hồi"],
            "Function": fn
        })

function_df = pd.DataFrame(function_rows)

function_summary = (
    function_df.groupby(["Năm khảo sát", "Function"])
    .size()
    .reset_index(name="Count")
)

function_summary["Function Share"] = function_summary.groupby("Năm khảo sát")["Count"].transform(lambda x: x / x.sum())
function_summary["Function Share"] = function_summary["Function Share"].round(4)

# =========================
# EXPORT
# =========================

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="1. Survey Raw Data", index=False)
    summary_year.to_excel(writer, sheet_name="2. Yearly Summary", index=False)
    theme_summary.to_excel(writer, sheet_name="3. Feedback Theme", index=False)
    function_summary.to_excel(writer, sheet_name="4. Function Usage", index=False)

print(f"Generated file: {OUTPUT_FILE}")
print(summary_year)
