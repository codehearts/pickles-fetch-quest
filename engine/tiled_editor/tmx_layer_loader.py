from .tmx_object_layer import load_tmx_object_layer
from .tmx_tile_layer import load_tmx_tile_layer
from engine.geometry import Point2d
from engine.graphics import GraphicsBatch, GraphicsObject
from engine.room import RoomLayer


class TmxLayerLoader(object):
    """Creates a :obj:`engine.room.RoomLayer` from a TMX layer node.

    Attributes:
        layer (:obj:`engine.room.RoomLayer`): Layer created from the TMX node.
        name (str): Name of the layer from the TMX node.
    """

    def __init__(self, layer_node, map_node, tileset, tile_objects,
                 object_factory):
        """Loads a :obj:`engine.room.RoomLayer` from a TMX layer node.

        Supported TMX layer nodes are "layer" and "objectgroup".

        Args:
            layer_node (:obj:`xml.etree.Element`): TMX layer node.
            map_node (:obj:`xml.etree.Element`): TMX map node.
            tileset (dict of int to :obj:`pyglet.image.AbstractImage`):
                Tileset for the map.
            tile_objects (dict of int to str):
                Mapping of tileset indices to tile object types.
            object_factory (:obj:`engine.factory.GenericFactory`):
                Factory to create objects from names in the TMX layer.
        """
        super(TmxLayerLoader, self).__init__()

        self.layer = RoomLayer(batch=GraphicsBatch())
        self.name = layer_node.attrib['name']

        self._layer_node = layer_node
        self._tileset = tileset
        self._tile_objects = tile_objects
        self._object_factory = object_factory

        # Get render order and dimensions of map
        map_attr = map_node.attrib
        self._tile_size = int(map_attr['tilewidth'])
        self._map_width_px = (int(map_attr['width']) - 1) * self._tile_size
        self._map_height_px = (int(map_attr['height']) - 1) * self._tile_size

        self._load()

    def _load(self):
        """Loads the TMX map."""
        if self._layer_node.tag == 'layer':
            self._load_tile_layer()
        elif self._layer_node.tag == 'objectgroup':
            self._load_object_layer()

    def _load_tile_layer(self):
        """Creates tile graphics and adds them to the layer."""
        # Load the tiles from this layer
        tiles = load_tmx_tile_layer(self._layer_node)

        # Filter out tiles not in the tileset
        filtered_tiles = filter(
            lambda tile_spec: tile_spec[-1] in self._tileset,
            tiles)

        for tile_spec in filtered_tiles:
            x, y, tileset_index = tile_spec
            self._create_graphic_on_layer(
                self._tileset[tileset_index], Point2d(x, y) * self._tile_size)

    def _load_object_layer(self):
        """Creates objects using the factory and adds them to the layer."""
        # Load the objects from this layer
        objects = load_tmx_object_layer(
            self._map_width_px, self._map_height_px,
            self._layer_node, self._tile_objects)

        # Filter out tiles not in the factory
        filtered_objects = filter(
            lambda obj: self._object_factory.can_create(obj['type']),
            objects)

        # Create and add all supported objects to the layer
        for obj in filtered_objects:
            obj['name'] = obj['type']  # The factory expects a "name"

            created_object = self._object_factory.create(
                **obj, batch=self.layer.batch)

            self.layer.add_object(created_object)

            # Draw the tile for tile objects
            if 'tile' in obj:  # Only tile objects have a "tile" property
                graphic = self._create_graphic_on_layer(
                    self._tileset[obj['tile']], Point2d(obj['x'], obj['y']))

                created_object.attach(graphic, (0, 0))

    def _create_graphic_on_layer(self, texture, coordinates):
        """Creates a graphic and adds it to the layer before returning it."""
        graphic = GraphicsObject(texture, coordinates, batch=self.layer.batch)

        self.layer.add_object(graphic)
        return graphic
