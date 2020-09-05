def load_tmx_object_layer(map_pixel_width, map_pixel_height, layer_node,
                          tile_objects):
    """Yields a dict for each object in the layer.

    Each dict contains the following fields:
        type (str): Type of the object
        x (int): X coordinate, in pixels. Origin at lower left corner.
        y (int): Y coordinate, in pixels. Origin at lower left corner.
        width (int): Width of object, in pixels.
        height (int): Height of object, in pixels.
        tile (int, optional): Tileset index, for tile objects only.

    Args:
        map_pixel_width (int): Total width of the map, in pixels.
        map_pixel_height (int): Total height of the map, in pixels.
        layer_node (:obj:`xml.etree.Element`): Layer node to load.
        tile_objects (dict of int to str):
            Map of tile objects which can exist on an object layer.

    Raises:
        ValueError if the render order is invalid.

    Yields:
        A dict for each object in the layer.
    """
    for object_node in layer_node.findall('object'):
        # Get the object's type, position, and size
        object_type = _get_type(object_node.attrib, tile_objects)
        x = int(object_node.attrib['x'])
        y = int(object_node.attrib['y'])
        width = int(object_node.attrib['width'])
        height = int(object_node.attrib['height'])

        object_properties = {
            'type': object_type,
            'x': x,
            'y': map_pixel_height - y,  # Flip origin from top to bottom
            'width': width,
            'height': height
        }

        # Add the tile attribute and adjust the positioning of tile objects
        if 'gid' in object_node.attrib:
            object_properties['tile'] = int(object_node.attrib['gid'])
            object_properties['y'] += height  # Adjust bottom left alignment

        yield object_properties


def _get_type(object_attributes, tile_objects):
    """Gets an object node's type name, accounting for tile objects."""
    if 'gid' in object_attributes:
        return tile_objects[int(object_attributes['gid'])]

    return object_attributes['type']
