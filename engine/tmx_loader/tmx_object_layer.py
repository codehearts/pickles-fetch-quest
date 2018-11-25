def load_tmx_object_layer(map_pixel_width, map_pixel_height, layer_node):
    """Yields a dict for each object in the layer.

    Each dict contains the following fields:
        name (str): Name of the object
        x (int): X coordinate, in pixels. Origin at lower left corner.
        y (int): Y coordinate, in pixels. Origin at lower left corner.
        width (int): Width of object, in pixels.
        height (int): Height of object, in pixels.

    Args:
        map_pixel_width (int): Total width of the map, in pixels.
        map_pixel_height (int): Total height of the map, in pixels.
        layer_node (:obj:`xml.etree.Element`): Layer node to load.

    Raises:
        ValueError if the render order is invalid.

    Yields:
        A dict for each object in the layer.
    """
    for object_node in layer_node.findall('object'):
        # Get the object's name, position, and size
        name = object_node.attrib['name']
        x = int(object_node.attrib['x'])
        y = int(object_node.attrib['y'])
        width = int(object_node.attrib['width'])
        height = int(object_node.attrib['height'])

        # Flip origin from top left to bottom left
        y = map_pixel_height - y

        yield {'name': name, 'x': x, 'y': y, 'width': width, 'height': height}
