from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Iterable

import pandas as pd
import plotly.express as px
import streamlit as st

APP_TITLE = "Climate data explorer"
DEFAULT_DATASET = Path(__file__).with_name("KlimaLoggPro.csv")
MISSING_MARKERS = ["---", "", " "]


def _friendly_name(column: str) -> str:
    names = {
        "TI": "Indoor temperature",
        "RHI": "Indoor humidity",
        "DEWI": "Indoor dew point",
    }
    if column in names:
        return names[column]
    if column.startswith("T") and column[1:].isdigit():
        return f"Sensor {column[1:]} temperature"
    if column.startswith("RH") and column[2:].isdigit():
        return f"Sensor {column[2:]} humidity"
    if column.startswith("DEW") and column[3:].isdigit():
        return f"Sensor {column[3:]} dew point"
    return column


@st.cache_data(show_spinner=False)
def load_data(source: str | bytes) -> pd.DataFrame:
    csv_source = BytesIO(source) if isinstance(source, bytes) else source
    frame = pd.read_csv(
        csv_source,
        sep=";",
        decimal=",",
        na_values=MISSING_MARKERS,
        encoding="utf-8-sig",
    )
    frame.columns = [column.replace('"', "").strip() for column in frame.columns]
    frame["Timestamp"] = pd.to_datetime(frame["Timestamp"], errors="coerce")
    frame = frame.dropna(subset=["Timestamp"]).sort_values("Timestamp")

    for column in frame.columns:
        if column == "Timestamp":
            continue
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    return frame.reset_index(drop=True)



def metric_columns(frame: pd.DataFrame) -> list[str]:
    return [column for column in frame.columns if column != "Timestamp"]



def default_selection(columns: Iterable[str]) -> list[str]:
    columns = list(columns)
    preferred = ["TI", "RHI", "T1", "RH1"]
    selected = [column for column in preferred if column in columns]
    return selected or columns[: min(4, len(columns))]



def format_stats(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    summary = frame[columns].agg(["count", "mean", "min", "max"]).T
    summary = summary.rename(
        columns={
            "count": "Samples",
            "mean": "Average",
            "min": "Minimum",
            "max": "Maximum",
        }
    )
    summary.index = [_friendly_name(index) for index in summary.index]
    return summary.round(2)



def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)
    st.caption("Load your climate CSV data, focus on a date range, and interactively choose which signals to plot.")

    st.sidebar.header("Data source")
    uploaded_file = st.sidebar.file_uploader("Upload a CSV export", type=["csv"])
    data_source = uploaded_file.getvalue() if uploaded_file is not None else str(DEFAULT_DATASET)

    if uploaded_file is None:
        st.sidebar.info(f"Using bundled sample file: {DEFAULT_DATASET.name}")

    frame = load_data(data_source)
    columns = metric_columns(frame)

    if not columns:
        st.error("No numeric columns were detected in the selected file.")
        st.stop()

    min_timestamp = frame["Timestamp"].min()
    max_timestamp = frame["Timestamp"].max()

    st.sidebar.header("Filters")
    selected_dates = st.sidebar.date_input(
        "Time frame",
        value=(min_timestamp.date(), max_timestamp.date()),
        min_value=min_timestamp.date(),
        max_value=max_timestamp.date(),
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date = end_date = selected_dates

    filtered = frame.loc[
        frame["Timestamp"].between(
            pd.Timestamp(start_date),
            pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1),
        )
    ].copy()

    st.sidebar.header("Signals")
    chosen_columns = st.sidebar.multiselect(
        "Select or unselect series",
        options=columns,
        default=default_selection(columns),
        format_func=_friendly_name,
    )

    if not chosen_columns:
        st.warning("Choose at least one signal to show the chart and summary table.")
        st.stop()

    if filtered.empty:
        st.warning("No rows match the selected time frame. Expand the date range to continue.")
        st.stop()

    chart_data = filtered.melt(
        id_vars="Timestamp",
        value_vars=chosen_columns,
        var_name="Signal",
        value_name="Value",
    ).dropna(subset=["Value"])
    chart_data["Signal label"] = chart_data["Signal"].map(_friendly_name)

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows in range", f"{len(filtered):,}")
    col2.metric("Signals selected", len(chosen_columns))
    col3.metric("Date span", f"{start_date} → {end_date}")

    line_chart = px.line(
        chart_data,
        x="Timestamp",
        y="Value",
        color="Signal label",
        markers=False,
        title="Selected signals over time",
    )
    line_chart.update_layout(legend_title_text="Signal", hovermode="x unified")
    st.plotly_chart(line_chart, use_container_width=True)

    with st.expander("Summary statistics", expanded=True):
        st.dataframe(format_stats(filtered, chosen_columns), use_container_width=True)

    with st.expander("Filtered raw data"):
        preview = filtered[["Timestamp", *chosen_columns]].copy()
        preview.columns = ["Timestamp", *[_friendly_name(column) for column in chosen_columns]]
        st.dataframe(preview, use_container_width=True)

    st.markdown(
        """
        ### Next ideas
        - Add saved dashboards for common sensor groups.
        - Export filtered data to CSV.
        - Add automatic resampling for hourly, daily, and weekly views.
        """
    )


if __name__ == "__main__":
    main()
