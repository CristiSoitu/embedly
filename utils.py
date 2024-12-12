import base64
from PIL import Image  # Pillow library for image handling
import io
from dash import Dash, dcc, html, Input, Output, no_update, callback
import plotly.graph_objects as go
import pandas as pd
import cv2

## requirements.txt file should include the following:
'''
dash
plotly
pandas
opencv-python-headless

'''

def create_thumbnail(input_image_path, output_image_path, max_size=256, chan_to_save=None, enhance_contrast=False):
    """
    Create a thumbnail of the image at `input_image_path` and save it to `output_image_path`.

    :param input_image_path: Path to the original image.
    :param output_image_path: Path to save the thumbnail.
    :param max_size: Maximum size of the thumbnail (width or height). If the image is smaller than this, it will not be resized. Keep the aspect ratio.
    """
    # Read the image
    image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)  # Load with all channels, including alpha
    
    if image is None:
        raise FileNotFoundError(f"Image not found: {input_image_path}")
    

    # check to see if it's single channel or not
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        # Convert the image to RGB (OpenCV uses BGR as default) but check if dims are (h, w, c) or (c, h, w)
        if image.shape[0] < 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.cvtColor(image.transpose(1, 2, 0), cv2.COLOR_BGR2RGB)
    
    # If a specific channel is requested, keep only that channel
    h, w = image.shape[:2]

    if chan_to_save is not None:
        image = image[:, :, chan_to_save]
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    # keep the aspect ratio, resize the bigger dimension to size if bigger than max_size
    if h > max_size or w > max_size:
        if h > w:
            new_h = max_size
            new_w = int(w * (max_size / h))
        else:
            new_w = max_size
            new_h = int(h * (max_size / w))
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    if enhance_contrast:
        image = cv2.convertScaleAbs(image, alpha=1.5, beta=0)
    # Resize the image
    #image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)

    # Save the thumbnail
    cv2.imwrite(output_image_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    
     
def encode_image_to_base64(image_path):


    """
    Encode a local image file (including TIFF) as a base64 string.

    :param image_path: Path to the image file.
    :return: Base64-encoded image string.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    buffer = io.BytesIO()
    img = Image.open(image_path)
    img.save(buffer, format="jpeg")
    return base64.b64encode(buffer.getvalue()).decode()


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
        title="UMAP embeddings", 
        #center the title
        title_x=0.5,
        showlegend=True,
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
    app.run_server(debug=True)
