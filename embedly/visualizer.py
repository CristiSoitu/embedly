import argparse
import pandas as pd
import toml
import base64
from PIL import Image  # Pillow library for image handling
import io
from dash import Dash, dcc, html, Input, Output, no_update, callback
import plotly.graph_objects as go
import pandas as pd



def viz_umap_plot(data_df, embeddings_col_0 = 'umap_embeddings_0', embeddings_col_1 = 'umap_embeddings_1', name_col = 'name', x_px_col = 'x_px', y_px_col = 'y_px', url_col = 'url', cluster_col = 'k_means'):
    '''
    Visualize UMAP embeddings with plotly. Hover over the points to see the thumbnails of the images.

    :param images_df: DataFrame with the images data.
    :param embeddings_col_0: Column name for the first UMAP embedding.
    :param embeddings_col_1: Column name for the second UMAP embedding.
    :param name: Column name for the image name.
    :param x_px: Column name for the image height.
    :param y_px: Column name for the image width.
    :param url: Column name for the image URL.
    '''

    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=data_df[embeddings_col_0],
            y=data_df[embeddings_col_1], 
            mode='markers',
            marker=dict(size=5, color=data_df[cluster_col], opacity=1),
        )
    )

    fig.update_traces(
        hoverinfo="none",
        hovertemplate=None,
        marker=dict(size=5)
    )

    fig.update_layout(
        title="UMAP embeddings of MNIST dataset",
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
        x_px = data_df[x_px_col][hover_data["pointNumber"]]
        y_px = data_df[y_px_col][hover_data["pointNumber"]]
        name = data_df[name_col][hover_data["pointNumber"]]
        url = data_df[url_col][hover_data["pointNumber"]]
        cluster = data_df[cluster_col][hover_data["pointNumber"]]

        children = [
            html.Img(
                src=url,
                style={"width": f"{y_px}px", "height": f"{x_px}px"},
            ),
            html.P(f'{name}'),
            html.P(f'Cluster: {cluster}')
        ]

        return True, bbox, children, direction
    #app.run_server(debug=True)
    app.run(jupyter_mode='external')




if __name__ == '__main__':

    config = toml.load('config.toml')

    parser = argparse.ArgumentParser(description='VizuMap')
    parser.add_argument('--input_file', type=str, default=config['PARAMS']['INPUT_FILE'],  help='Input file with embeddings')
    parser.add_argument('--name_col', type=str, default=config['PARAMS']['NAME_COL'], help='Name column')
    parser.add_argument('--embeddings_col_0', type=str, default=config['PARAMS']['EMBEDDINGS_COL_0'], help='Embeddings column 0')
    parser.add_argument('--embeddings_col_1', type=str, default=config['PARAMS']['EMBEDDINGS_COL_1'], help='Embeddings column 1')
    parser.add_argument('--x_px_col', type=str, default=config['PARAMS']['X_PX_COL'], help='X pixel column name')
    parser.add_argument('--y_px_col', type=str, default=config['PARAMS']['Y_PX_COL'], help='Y pixel column name')
    parser.add_argument('--url_col', type=str, default=config['PARAMS']['URL_COL'], help='URL column name')
    parser.add_argument('--cluster_col', type=str, default=config['PARAMS']['CLUSTER_COL'], help='Cluster column name')

    args = parser.parse_args()

    data_df = pd.read_csv(args.input_file)

    utils.viz_umap_plot(data_df=data_df, embeddings_col_0=args.embeddings_col_0, embeddings_col_1=args.embeddings_col_1, name_col=args.name_col, x_px_col=args.x_px_col, y_px_col=args.y_px_col, url_col=args.url_col, cluster_col=args.cluster_col)
