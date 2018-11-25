from ..util.indices_1d import flip_1d_index_vertically
from ..disk_loader import DiskLoader
from os.path import dirname, join, normpath


def load_tmx_tileset(tmx_path, tileset_node):
    """Yields a tuple of (tileset_index, graphic) for each tile in a tileset.

    Args:
        tmx_path (str): Path to the TMX file, relative to the :obj:`DiskLoader`
            resource path.
        tileset_node (:obj:`xml.etree.Element`): Tileset element to load.

    Raises:
        ValueError if the render order is invalid.

    Yields:
        A tuple of (tileset_index, graphic) for each tile, where the index is
        an int and the graphic can be used to construct a
        :obj:`GraphicsObject`.
    """
    # Get the image node for this tileset
    image_node = tileset_node.find('image')

    # Get the image source relative to resources instead of rooms directory
    tmx_dir = dirname(tmx_path)
    image_path = normpath(join(tmx_dir, image_node.attrib['source']))

    # Get the starting index for the tiles in the set
    first_index = int(tileset_node.attrib['firstgid'])

    # Get the rows, columns, and total number of tiles
    tile_count = int(tileset_node.attrib['tilecount'])
    columns = int(tileset_node.attrib['columns'])
    rows = tile_count // columns

    # Load the image source into an image grid
    image_grid = DiskLoader.load_image_grid(image_path, rows, columns)

    # Add each tile from this image source to the tile map
    for i in range(0, tile_count):
        # Flip tileset indexing to bottom-up image_grid indexing
        grid_index = flip_1d_index_vertically(i, rows, columns)

        # Map the tileset index to the corresponding tile image
        yield (first_index + i, image_grid[grid_index])
