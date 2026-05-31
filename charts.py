import plotly.express as px
import plotly.graph_objects as go

_FONT = dict(family="Inter, sans-serif", color="#222222", size=12)
_PASTEL = px.colors.qualitative.Pastel

_BASE = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=_FONT,
    margin=dict(l=0, r=8, t=4, b=0),
    height=320,
)


def hbar_chart(df, y_col: str, x_col: str, color: str = "#FF385C") -> go.Figure:
    """Horizontal bar chart: Inter font, no x-axis, largest on top, inline value labels."""
    fig = go.Figure(go.Bar(
        y=df[y_col],
        x=df[x_col],
        orientation="h",
        marker_color=color,
        marker_line_width=0,
        text=df[x_col],
        textposition="inside",
        insidetextanchor="middle",
        textangle=0,
        textfont=dict(family="Inter, sans-serif", color="#fff", size=11),
    ))
    fig.update_layout(
        **_BASE,
        showlegend=False,
        yaxis=dict(
            autorange="reversed",
            title=None,
            tickfont=dict(family="Inter, sans-serif", size=12, color="#484848"),
            automargin=True,
        ),
        xaxis=dict(visible=False),
    )
    return fig


def area_chart(df, x_col: str = "date", y_col: str = "cumulative") -> go.Figure:
    """Cumulative area chart for network growth over time."""
    fig = go.Figure(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode="lines",
        line=dict(color="#FF385C", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(255,56,92,0.10)",
        hovertemplate="%{x|%b %Y}: %{y} total<extra></extra>",
    ))
    fig.update_layout(
        **_BASE,
        showlegend=False,
        xaxis=dict(
            gridcolor="#F0F0F0",
            title=None,
            tickfont=dict(family="Inter, sans-serif", size=11, color="#717171"),
        ),
        yaxis=dict(
            gridcolor="#F0F0F0",
            title=None,
            tickfont=dict(family="Inter, sans-serif", size=11, color="#717171"),
        ),
    )
    return fig


def donut_chart(labels: list, values: list, total: int) -> go.Figure:
    """Donut chart: soft pastel colors, no slice labels, total in center, hover only."""
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        textinfo="none",
        marker=dict(colors=_PASTEL),
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        **_BASE,
        showlegend=True,
        legend=dict(
            orientation="v",
            x=1.02,
            y=0.5,
            font=dict(family="Inter, sans-serif", size=11, color="#484848"),
        ),
        annotations=[
            dict(
                text=f"<b>{total:,}</b>",
                x=0.5, y=0.56,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(family="Inter, sans-serif", size=22, color="#222222"),
            ),
            dict(
                text="connections",
                x=0.5, y=0.44,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(family="Inter, sans-serif", size=12, color="#717171"),
            ),
        ],
    )
    return fig