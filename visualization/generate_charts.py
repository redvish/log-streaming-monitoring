from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHARTS_DIR = BASE_DIR / "charts"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "font.size": 11
})

def save_bar_chart(df, x, y, title, xlabel, ylabel, filename, rotation=0):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
    ax.bar(df[x], df[y])

    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.setp(
        ax.get_xticklabels(),
        rotation=rotation,
        ha="right" if rotation else "center"
    )

    fig.tight_layout()
    fig.savefig(CHARTS_DIR / filename, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)

def save_grouped_bar_chart(df, x_labels, y_columns, title, xlabel, ylabel, filename, legend_labels):
    x = np.arange(len(x_labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6), facecolor="white")

    for i, col in enumerate(y_columns):
        offset = (i - 0.5) * width
        ax.bar(x + offset, df[col], width, label=legend_labels[i])

    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend()

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    fig.tight_layout()
    fig.savefig(CHARTS_DIR / filename, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)

# 1. HTTP status codes
status_df = pd.read_csv(
    DATA_DIR / "status_counts.tsv",
    sep="\t",
    names=["status_code", "requests_count"]
)
status_df["status_code"] = status_df["status_code"].astype(str)

save_bar_chart(
    status_df,
    "status_code",
    "requests_count",
    "Распределение HTTP-кодов",
    "HTTP-код",
    "Количество запросов",
    "status_counts.png"
)

# 2. Top URLs
url_df = pd.read_csv(
    DATA_DIR / "url_counts.tsv",
    sep="\t",
    names=["url", "requests_count"]
)

save_bar_chart(
    url_df,
    "url",
    "requests_count",
    "Топ URL",
    "URL",
    "Количество запросов",
    "url_counts.png",
    rotation=25
)

# 3. Top IPs
ip_df = pd.read_csv(
    DATA_DIR / "ip_counts.tsv",
    sep="\t",
    names=["ip", "requests_count"]
)

save_bar_chart(
    ip_df,
    "ip",
    "requests_count",
    "Топ IP-адресов",
    "IP-адрес",
    "Количество запросов",
    "ip_counts.png",
    rotation=15
)

# 4. HTTP methods
method_df = pd.read_csv(
    DATA_DIR / "method_counts.tsv",
    sep="\t",
    names=["method", "requests_count"]
)

save_bar_chart(
    method_df,
    "method",
    "requests_count",
    "Распределение HTTP-методов",
    "HTTP-метод",
    "Количество запросов",
    "method_counts.png"
)

# 5. Requests per minute
minute_requests_df = pd.read_csv(
    DATA_DIR / "minute_requests.tsv",
    sep="\t",
    names=["minute_window", "requests_count"]
)
minute_requests_df["minute_window"] = pd.to_datetime(minute_requests_df["minute_window"])
minute_requests_df = minute_requests_df.sort_values("minute_window")
minute_requests_df["minute_label"] = minute_requests_df["minute_window"].dt.strftime("%m-%d %H:%M")

save_bar_chart(
    minute_requests_df,
    "minute_label",
    "requests_count",
    "Количество запросов по минутам",
    "Временное окно",
    "Количество запросов",
    "minute_requests.png",
    rotation=45
)

# 6. 4xx / 5xx errors per minute
minute_errors_df = pd.read_csv(
    DATA_DIR / "minute_errors.tsv",
    sep="\t",
    names=["minute_window", "client_errors_4xx", "server_errors_5xx"]
)
minute_errors_df["minute_window"] = pd.to_datetime(minute_errors_df["minute_window"])
minute_errors_df = minute_errors_df.sort_values("minute_window")
minute_errors_df["minute_label"] = minute_errors_df["minute_window"].dt.strftime("%m-%d %H:%M")

save_grouped_bar_chart(
    minute_errors_df,
    minute_errors_df["minute_label"],
    ["client_errors_4xx", "server_errors_5xx"],
    "Ошибки 4xx/5xx по минутам",
    "Временное окно",
    "Количество ошибок",
    "minute_errors.png",
    ["Ошибки 4xx", "Ошибки 5xx"]
)

print("Charts regenerated successfully.")
