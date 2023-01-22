
import plotly.graph_objects as go

layout = go.Layout(
    template="plotly_dark",
    # plot_bgcolor="#FFFFFF",
    hovermode="x",
    hoverdistance=100,  
    spikedistance=1000,  
    xaxis=dict(
        title="time",
        linecolor="#BCCCDC",
        showspikes=True,
        spikesnap="cursor",
        spikethickness=1,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
    yaxis=dict(
        title="price",
        linecolor="#BCCCDC",
        tickformat=".2%",
        showspikes=True,
        spikesnap="cursor",
        spikethickness=1,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
)

layout_simple = go.Layout(
    template="plotly_dark",
    hovermode="x",
    hoverdistance=100,  
    spikedistance=1000,  
    xaxis=dict(
        showgrid=True,
        title="time",
        linecolor="#BCCCDC",
        showspikes=True,
        spikesnap="cursor",
        spikethickness=1,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
    yaxis=dict(
        showgrid=True,
        title="price",
        linecolor="#BCCCDC",
        showspikes=True,
        spikesnap="cursor",
        spikethickness=1,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
)

layout_bars = go.Layout(
    template="plotly_dark",
    xaxis=dict(title=""),
    yaxis=dict(
        title="",
    ),
)

layout_vertical = go.Layout(
    template="plotly_dark",
    hovermode="y",
    hoverdistance=100,  
    xaxis=dict(
        title="time",
        linecolor="#BCCCDC",
        showspikes=True,
        spikesnap="cursor",
        spikethickness=1,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
    yaxis=dict(
        title="price",
        linecolor="#BCCCDC",
        showspikes=True,
        spikesnap="cursor",
        spikethickness=1,
        spikedash="dot",
        spikecolor="#999999",
        spikemode="across",
    ),
)

tool_config = {
    "modeBarButtonsToAdd": [
        "drawline",
        "drawopenpath",
        "drawclosedpath",
        "drawcircle",
        "drawrect",
        "eraseshape",
        "hoverclosest",
        "hovercompare",
    ],
    "modeBarButtonsToRemove": [
        "zoom2d",
        "pan2d",
        "select2d",
        "lasso2d",
        "zoomIn2d",
        "zoomOut2d",
        "autoScale2d",
    ],
    "showTips": False,
    "displaylogo": False,
}
