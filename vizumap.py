import argparse
import utils
import pandas as pd
import toml

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
