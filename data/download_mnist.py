import os
from tensorflow.keras.datasets import mnist
import tifffile as tif


def save_mnist_as_tiff(output_dir='images', subset_size=100):
    '''
    Save MNIST dataset as tiff images.

    Args:
        output_dir (str): Directory to save images.
        subset_size (int): Number of images to save.
    '''

    # Load MNIST dataset
    (x_train, y_train), _ = mnist.load_data()

    # Limit the subset size
    x_train = x_train[:subset_size]
    y_train = y_train[:subset_size]

    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save images as tiff
    for i, image in enumerate(x_train):
        tif.imwrite(f'{output_dir}/{i}.tiff', image)
    
    print(f'Saved {subset_size} images to {output_dir}')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Download MNIST dataset')
    parser.add_argument('--output_dir', type=str, default='images', help='Directory to save images')
    parser.add_argument('--subset_size', type=int, default=1000, help='Number of images to save')
    args = parser.parse_args()

    save_mnist_as_tiff(output_dir=args.output_dir, subset_size=args.subset_size)