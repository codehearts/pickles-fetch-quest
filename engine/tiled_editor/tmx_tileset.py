from engine.util.indices_1d import flip_1d_index_vertically
from os.path import dirname, join, normpath
from engine import disk


def load_tmx_tileset(tmx_path, tileset_node):
    """Yields a tuple of (tileset_index, graphic) for each tile in a tileset.

    Args:
        tmx_path (str): Path to the TMX file, relative to the
            :obj:`engine.disk.DiskLoader` resource path.
        tileset_node (:obj:`xml.etree.Element`): Tileset element to load.

    Raises:
        ValueError if the render order is invalid.

    Yields:
        A tuple of (tileset_index, graphic) for each tile, where the index is
        an int and the graphic can be used to construct a
        :obj:`engine.graphics.GraphicsObject`.
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
    image_grid = disk.DiskLoader.load_image_grid(image_path, rows, columns)

    # Add each tile from this image source to the tile map
    for i in range(0, tile_count):
        # Flip tileset indexing to bottom-up image_grid indexing
        grid_index = flip_1d_index_vertically(i, rows, columns)

        # Map the tileset index to the corresponding tile image
        yield (first_index + i, image_grid[grid_index])


def load_tmx_tile_objects(tileset_node):
    """Yields a tuple of (type, tileset_index) for tile objects in a tileset.

    Args:
        tileset_node (:obj:`xml.etree.Element`): Tileset element to use.

    Raises:
        ValueError if the render order is invalid.

    Yields:
        A tuple of (type, tileset_index) for each tile object, where the type
        is a string and the index is an int.
    """
    # Get the tile object nodes for this tileset
    tile_objects = tileset_node.findall('tile')

    if tile_objects:
        # Get the starting index for the tiles in the set
        first_index = int(tileset_node.attrib['firstgid'])

        # Add each tile from this image source to the tile map
        for tile_object in tile_objects:
            # Obtain the index into the tileset's image
            tile_object_index = int(tile_object.attrib['id'])

            # Map the type to the corresponding tile index
            yield (first_index + tile_object_index, tile_object.attrib['type'])
