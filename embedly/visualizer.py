import argparse
import pandas as pd
import base64
from PIL import Image  # Pillow library for image handling
import io
from dash import Dash, dcc, html, Input, Output, no_update, callback
import plotly.graph_objects as go
import pandas as pd
import webbrowser


def viz_umap_plot(df_path = '../data/embeddings.csv', embeddings_col_0 = 'umap_embeddings_0', embeddings_col_1 = 'umap_embeddings_1', url_col = 'url', display_columns = ['name'], width_px = 128, height_px = 128, cluster_col = None, display_fraction=1, open_browser=True):
    '''
    Visualize UMAP embeddings with plotly. Hover over the points to see the thumbnails of the images.

    Parameters:

    df_path (str): path to the csv file with the embeddings and other columns
    embeddings_col_0 (str): name of the column with the first embedding
    embeddings_col_1 (str): name of the column with the second embedding
    url_col (str): name of the column with the url of the images
    display_columns (list): list of columns to display when hovering over the points
    width_px (int): width of the thumbnail
    height_px (int): height of the thumbnail
    cluster_col (str): name of the column with the cluster labels
    display_fraction (float): fraction of the data to display
    open_browser (bool): whether to open the browser automatically
    
    '''

    # Load the data
    data_df = pd.read_csv(df_path)
    if display_fraction < 1:
        data_df = data_df.sample(frac=display_fraction)

    # if there is a cluster column, use it for coloring
    if cluster_col is not None:
        data_colors = data_df[cluster_col]
    else:
        data_colors = None

    # Create the plot
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=data_df[embeddings_col_0],
            y=data_df[embeddings_col_1], 
            mode='markers',
            marker=dict(size=5, color=data_colors, opacity=1),
        )
    )

    fig.update_traces(
        hoverinfo="none",
        hovertemplate=None,
        marker=dict(size=5)
    )

    fig.update_layout(
        title="UMAP embeddings of the images",
        xaxis_title="UMAP embeddings 0",
        yaxis_title="UMAP embeddings 1", 
        #center the title
        title_x=0.5,
        showlegend=False,
        width=800, 
        height=800,
    )

    app = Dash()
    

    app.layout = html.Div(
        className="container",
        style={
            "display": "flex",
            "justify-content": "center",  # Horizontal centering
            "align-items": "center",  # Vertical centering
            "height": "100vh",  # Full viewport height
            "background-color": "#f8f9fa"  # Optional: Add a background color for clarity
        },
        children=[
            dcc.Graph(id="graph-2-dcc", figure=fig, clear_on_unhover=True),
            dcc.Tooltip(id="graph-tooltip-2", direction='bottom'),
        ],
    )

    @callback(
        Output("graph-tooltip-2", "show"),
        Output("graph-tooltip-2", "bbox"),
        Output("graph-tooltip-2", "children"),
        Output("graph-tooltip-2", "direction"),
        Input("graph-2-dcc", "hoverData"),
    )

    def display_hover(hoverData):
        if hoverData is None:
            return False, no_update, no_update, no_update

        hover_data = hoverData["points"][0]
        bbox = hover_data["bbox"]

        direction = "bottom"

        # control the position of the tooltip
        y = hover_data["y"]
        direction = "bottom" if y > 1.5 else "top"

        #name = data_df.iloc[hover_data["pointNumber"]][name_col]
        url = data_df.iloc[hover_data["pointNumber"]][url_col]

        display_data = []
        for col in display_columns:
            display_data.append(data_df.iloc[hover_data["pointNumber"]][col])

        children = [
            html.Img(
                src=url,
                style={"width": f"{width_px}px", "height": f"{height_px}px"},
            ),

        ] + [html.P(f'{col}: {display_data[i]}') for i, col in enumerate(display_columns)]

        return True, bbox, children, direction

    host = '127.0.0.1'
    port = 8070
    url = f"http://{host}:{port}/"
    if open_browser:
        webbrowser.open(url)

    app.run_server(debug=True, host=host, port=port)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='VizuMap')
    parser.add_argument('--input_file', type=str, default='../data/embeddings.csv', help='Path to the input file')
    parser.add_argument('--embeddings_col_0', default='umap_embedding_1', type=str, help='Name of the column with the first embedding')
    parser.add_argument('--embeddings_col_1', default='umap_embedding_2', type=str, help='Name of the column with the second embedding')
    parser.add_argument('--url_col', type=str, default='url', help='Name of the column with the url of the images')
    parser.add_argument('--display_columns', default=['image'], type=str, help='List of columns to display when hovering over the points')
    parser.add_argument('--width_px', default=128, type=int, help='Width of the thumbnail')
    parser.add_argument('--height_px', default=128, type=int, help='Height of the thumbnail')
    parser.add_argument('--cluster_col', default='k_means', type=str, help='Name of the column with the cluster labels')
    parser.add_argument('--display_fraction', default=1, type=float, help='Fraction of the data to display')
    parser.add_argument('--open_browser', default=True, type=bool, help='Whether to open the browser automatically')

    args = parser.parse_args()

    viz_umap_plot(df_path=args.input_file, embeddings_col_0=args.embeddings_col_0, embeddings_col_1=args.embeddings_col_1, url_col=args.url_col, display_columns=args.display_columns, width_px=args.width_px, height_px=args.height_px, cluster_col=args.cluster_col, display_fraction=args.display_fraction, open_browser=args.open_browser)
    
