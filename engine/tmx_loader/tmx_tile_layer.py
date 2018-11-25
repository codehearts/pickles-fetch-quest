from io import StringIO
import csv


def load_tmx_tile_layer(layer_node):
    """Yields a tuple of (x, y, tileset_index) for each tile in the layer.

    Args:
        layer_node (:obj:`xml.etree.Element`): Layer node to load.

    Raises:
        ValueError if the render order is invalid.

    Yields:
        A tuple of (x, y, tileset_index), where x and y are in tile units
        rather than pixels.
    """
    # Get layer size
    layer_width = int(layer_node.attrib['width'])
    layer_height = int(layer_node.attrib['height'])

    # Get the tile map as a matrix of tileset indices with whitespace
    raw_tile_map = layer_node.find('data').text

    # Strip all whitespace from the tile map
    raw_tile_map = ''.join(raw_tile_map.split())

    # Read the tile map as a CSV
    tile_map_reader = csv.reader(StringIO(raw_tile_map))

    # Call `next` to get the first line of the CSV, convert all entries to int
    tile_map = map(int, next(tile_map_reader))

    for tile_map_index, tileset_index in enumerate(tile_map):
        # Calculate the position of this tile in the map
        x = (tile_map_index % layer_width)
        y = (tile_map_index // layer_width)

        # Flip origin from top left to bottom left
        y = layer_height - 1 - y

        yield (x, y, tileset_index)
