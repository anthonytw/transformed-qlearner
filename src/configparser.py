import xml.parsers.expat

class ConfigParser:
    # Initialize object.
    def __init__(self, filename):
        self.elements = {}
        self.xml_filename = ""
        
        # Internal parameters.
        self.__on_map = -1
        
        # Load file.
        self.load(filename)
        
    # Load XML file.
    def load(self, filename):
        assert(filename != "")
        self.elements = {
            'config': {
                'tileset': {'filename': ""},
                'agent': {'x': 0, 'y': 0, 'filename': ""},
                'map': {
                    'width': 0, 'height': 0, 'states': [] }
            }
        }
        self.xml_filename = filename
        
        # Create parser.
        parser = xml.parsers.expat.ParserCreate()
        parser.StartElementHandler = self.__handle_start_element__
        parser.EndElementHandler = self.__handle_end_element__
        parser.CharacterDataHandler = self.__handle_character_data__
        
        # Load file.
        self.__on_map = -1
        parser.ParseFile(open(self.xml_filename, "r"))
    
    # Define start element handler.
    def __handle_start_element__(self, name, attributes):
        if name == 'config':
            self.elements['config']['draw_grid'] = attributes['draw_grid'].lower() == "true"
        elif name == 'tileset':
            self.elements['config']['tileset']['filename'] = attributes['filename']
        elif name == 'agent':
            self.elements['config']['agent']['x'] = int(attributes['x'])
            self.elements['config']['agent']['y'] = int(attributes['y'])
            self.elements['config']['agent']['filename'] = attributes['filename']
        elif name == 'map':
            self.__on_map = 0
            self.elements['config']['map']['width'] = int(attributes['width'])
            self.elements['config']['map']['height'] = int(attributes['height'])
            self.elements['config']['map']['states'] = \
                [[0 for x in xrange(self.elements['config']['map']['width'])] \
                    for y in xrange(self.elements['config']['map']['height'])]
    
    # Define end element handler.
    def __handle_end_element__(self, name):
        if name == 'map':
            if self.__on_map != self.elements['config']['map']['height']:
                print "Not enough valid rows read for map"
                raise
            self.__on_map = -1
    
    # Define character data handler.
    def __handle_character_data__(self, data):
        if self.__on_map > -1:
            elems = data.split()
            if (elems != []) and (len(elems) == self.elements['config']['map']['width']):
                if self.__on_map >= self.elements['config']['map']['height']:
                    print "Too many map rows!"
                    raise
                for elem_id in xrange(len(elems)):
                    self.elements['config']['map']['states'][self.__on_map][elem_id] = int(elems[elem_id])
                self.__on_map += 1