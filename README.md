
# Embedly
This is a set of Python scripts to help one visualize low-dimensional embeddings of images. The script needs a .csv or other sort of table that can be loaded into pandas. This dataframe should have some x and y axis for each datapoint (it doesn't have to be embeddings), a base64 thumbnail and any other columns to be displayed. Illustration is done on a mock dataset which consists of a subset of 1000 MNIST images.

Embedly uses plotly and dash to plot the embeddings. Any stylistic changes to the plot have to be implemented by editing `visualizer.py`.

## Features

- Visualizes embeddings using UMAP
- Convert images to thumbnails if they are too large
- Convert thumbnails to base64 to add to a pandas 


## Usage

The behavior of the visualizer can be customized via command line arguments. 
If you already have the UMAP embeddings and base64 thumbnails loaded into your dataframe, run the script directly from the command line:

```bash 
python visualizer.py --input_file PATH_TO_EMBEDDINGS \
                  --embeddings_col_0 COLUMN_NAME_X \
                  --embeddings_col_1 COLUMN_NAME_Y \
                  --url_col IMAGE_URL_COLUMN \
                  --display_columns COL1 COL2 ... \
                  --width_px THUMBNAIL_WIDTH \
                  --height_px THUMBNAIL_HEIGHT \
                  --cluster_col CLUSTER_LABEL_COLUMN \
                  --display_fraction FRACTION \
                  --open_browser OPEN_BROWSER

```


| Parameter             | Type       | Default               | Description                                                                 |
|-----------------------|------------|-----------------------|-----------------------------------------------------------------------------|
| `--input_file`        | `str`      | `../data/embeddings.csv` | Path to the input CSV file containing embeddings and metadata.             |
| `--embeddings_col_0`  | `str`      | `umap_embedding_1`    | Name of the column with the first embedding coordinate (X-axis).           |
| `--embeddings_col_1`  | `str`      | `umap_embedding_2`    | Name of the column with the second embedding coordinate (Y-axis).          |
| `--url_col`           | `str`      | `url`                 | Name of the column with image URLs for thumbnails.                         |
| `--display_columns`   | `list[str]`| `['image']`           | Columns to display in the hover tooltip (e.g., `name`, `label`).           |
| `--width_px`          | `int`      | `128`                 | Width of the image thumbnails (in pixels).                                 |
| `--height_px`         | `int`      | `128`                 | Height of the image thumbnails (in pixels).                                |
| `--cluster_col`       | `str`      | `k_means`             | Column with cluster labels for coloring points (optional).                 |
| `--display_fraction`  | `float`    | `1.0`                 | Fraction of the dataset to display (e.g., `0.5` for 50%).                  |
| `--open_browser`      | `bool`     | `True`                | Whether to automatically open the visualization in a browser.              |


Otherwise, there is a `workflow.ipynb` script that extracts the umap embeddings and base64 thumbnails from a mock dataset of MNIST images. 



## Demo
![Example Visualization](assets/example1.gif)


## To do list:
- Extract embeddings using Resnet or other models.
- Populate `requirements.txt` and `setup.py`.




