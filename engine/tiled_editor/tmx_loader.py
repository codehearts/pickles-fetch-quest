from distutils.version import StrictVersion
from .tmx_layer_loader import TmxLayerLoader
from .tmx_tileset import load_tmx_tileset
from ..room import RoomLayerCollection
from engine import disk


class TmxLoader(object):
    """Loads a TMX file from disk into graphical objects and room layers.

    Attributes:
        layers (:obj:`RoomLayerCollection`): Collection of layers from the map.
    """

    def __init__(self, tmx_path, object_factory):
        """Loads a TMX map file from disk into layers for a :obj:`Room`.

        Args:
            tmx_path (str): Path to the TMX file, relative to the
                :obj:`engine.disk.DiskLoader` resource path.
            object_factory (:obj:`GenericFactory`): An object factory to
                convert TMX object names into Python objects.
        """
        super(TmxLoader, self).__init__()

        # Get the root map node from the TMX file
        self._map_node = disk.DiskLoader.load_xml(tmx_path)
        map_attr = self._map_node.attrib

        if StrictVersion(map_attr['version']) < StrictVersion('1.2'):
            raise AttributeError(
                'TMX format 1.2 or higher is supported, found {}'.format(
                    map_attr['version']))

        if map_attr['orientation'] != 'orthogonal':
            raise NotImplementedError('Non-orthogonal maps are not supported')

        if map_attr['infinite'] != '0':
            raise NotImplementedError('Infinite maps are not supported')

        self.layers = RoomLayerCollection()

        self._object_factory = object_factory
        self._path = tmx_path

        # Dict of tileset indices to tile image
        self._tileset = {}

        # Parse each node in the TMX map
        for node in self._map_node.iter():
            self._parse_node(node)

    def _parse_node(self, node):
        """Parses a node from a TMX file into the relevant object.

        Tileset elements are parsed into a map of tileset indices to graphics.
        Layer indices are parsed into :obj:`RoomLayer` objects.

        Args:
            node (:obj:`xml.etree.Element`): The TMX file node to parse.
        """
        if node.tag == 'tileset':
            self._parse_tileset(node)
        elif node.tag in ('layer', 'objectgroup'):
            # Load the layer
            layer_loader = TmxLayerLoader(
                node, self._map_node, self._tileset, self._object_factory)

            # Add the layer to the collection
            self.layers.add_layer(layer_loader.name, layer_loader.layer)

    def _parse_tileset(self, node):
        """Parses a tileset into an index to image mapping in `self._tileset`.

        Args:
            node (:obj:`xml.etree.Element`): The tileset node to parse.
        """
        for i, image in load_tmx_tileset(self._path, node):
            self._tileset[i] = image
