import logging
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARN)

class Field(object):
    def __init__(self, name="", type="int"):  # @ReservedAssignment
        self.name = name
        self.type = type

    def read(self, stream_object, type_method_mapping, peek=False, game_state={}):
        "Returns a tuple ('field name', field_data)"
        logger.debug("\tReading field: {}".format(self.name))
        try:
            value = type_method_mapping[self.type](stream_object, peek)
            logger.debug("\t\tRead value: {}".format(self.name))
            return (self.name, value)
        except:
            print "Exception occurred while reading field '%s'" % self.name
            raise
            
class GameStateField(Field): pass
    
class RawField(object):
    def __init__(self, name="", size=1):
        self.name = name
        self.size = size
        
    def read(self, stream_object, type_method_mapping, game_state={}):
        return (self.name, type_method_mapping['stream_data'](stream_object, self.size))
        
class FieldCollection(object):
    def __init__(self, *fields):
        self.fields = fields

    def read(self, stream_object, type_method_mapping, game_state={}):
        "Returns a dictionary {'field_name': field_data}"
        message_datum = {}
    
        for field in self.fields:
            if isinstance(field, ConditionalFieldCollection) or isinstance(field, SwitchField):
                field_data = field.read(stream_object, type_method_mapping, game_state=game_state)
                message_datum.update(field_data)
            else:
                field_name, field_datum = field.read(stream_object, type_method_mapping, game_state=game_state)
                if isinstance(field, GameStateField):
                    game_state[field_name] = field_datum
                message_datum[field_name] = field_datum
            
        return message_datum
        
class IteratedFieldCollection(object):
    def __init__(self, name, count, field_collection):
        self.name = name
        self.count = count
        self.field_collection = field_collection

    def read(self, stream_object, type_method_mapping, game_state={}):
        "Returns a tuple ('field name', [{from field collection},])"
        if isinstance(self.count, Field):
            _, field_count = self.count.read(stream_object, type_method_mapping, game_state=game_state)
        else:
            field_count = int(self.count)
            
        field_data = []
        
        for fc in range(field_count): #@UnusedVariable
            field_data.append(self.field_collection.read(stream_object, type_method_mapping, game_state=game_state))
            
        return (self.name, field_data)

class TerminatedFieldCollection(object):
    def __init__(self, name, terminator_field, terminator_comparison, field_collection):
        self.name = name
        self.terminator_field = terminator_field
        self.terminator_comparison = terminator_comparison
        self.field_collection = field_collection

    def read(self, stream_object, type_method_mapping, game_state={}):
        "Returns a tuple ('field name', field_data)"
        
        field_data = []
        
        _, term_value = self.terminator_field.read(stream_object, type_method_mapping, peek=True, game_state=game_state)
        while(self.terminator_comparison(term_value)):
            field_data.append(self.field_collection.read(stream_object, type_method_mapping, game_state=game_state))
            _, term_value = self.terminator_field.read(stream_object, type_method_mapping, peek=True, game_state=game_state)
            
        # throw away the terminator once it is found
        _, term_value = self.terminator_field.read(stream_object, type_method_mapping, peek=False, game_state=game_state)
            
        return (self.name, field_data)
        
class StateDependent(object):
    def __init__(self, func):
        self.func = func
        
    def __call__(self, value, game_state):
        return self.func(value, game_state)
    
class ConditionalFieldCollection(object):
    def __init__(self, predicate, predicate_comparison, consequent, alternative=None, peek_predicate=False):
        self.predicate = predicate
        self.predicate_comparison = predicate_comparison
        self.consequent = consequent
        self.alternative = alternative
        self.peek_predicate = peek_predicate
        
    def read(self, stream_object, type_method_mapping, game_state={}):
        "Returns a dictionary {'field_name': field_data}"
        
        if self.predicate is not None:
            _, value = self.predicate.read(stream_object, type_method_mapping, peek=self.peek_predicate, game_state=game_state)
        else:
            value = None
            
        if isinstance(self.predicate_comparison, StateDependent):
            logger.debug("StateDependent predicate_comparison occurring: game_state={}".format(game_state))
            predicate_result = self.predicate_comparison(value, game_state)
        else:
            predicate_result = self.predicate_comparison(value)
        
        if predicate_result:
            return self.consequent.read(stream_object, type_method_mapping, game_state=game_state)
        elif self.alternative is not None:
            return self.alternative.read(stream_object, type_method_mapping, game_state=game_state)
        else:
            return {}
            
class SwitchField(object):
    def __init__(self, predicate, cases, default=None, peek_predicate=False):
        self.predicate = predicate
        self.cases = cases
        self.default = default
        self.peek_predicate = peek_predicate
        
    def read(self, stream_object, type_method_mapping, game_state={}):
        "Returns a dictionary {'field_name': field_data}"
        
        if self.predicate is not None:
            _, value = self.predicate.read(stream_object, type_method_mapping, peek=self.peek_predicate, game_state=game_state)
        else:
            value = None
        
        for case in self.cases:
            if isinstance(case.predicate_comparison, StateDependent):
                logger.debug("StateDependent predicate_comparison occurring: game_state={}".format(game_state))
                predicate_result = case.predicate_comparison(value, game_state)
            else:
                predicate_result = case.predicate_comparison(value)
            
            if predicate_result:
                return case.consequent.read(stream_object, type_method_mapping, game_state=game_state)
        if self.default is not None:
            return self.default.read(stream_object, type_method_mapping, game_state=game_state)
        else:
            return {}
    
class CaseField(object):
    def __init__(self, predicate_comparison, consequent):
        self.predicate_comparison = predicate_comparison
        self.consequent = consequent
        
class MessageType(FieldCollection):
    def __init__(self, message_name, *fields):
        self.message_name = message_name
        FieldCollection.__init__(self, *fields)
        
    def read(self, stream_object, type_method_mapping, game_state={}):
        "Returns a tuple ('message_name', {from field collection})"
        try:
            return (self.message_name, FieldCollection.read(self, stream_object, type_method_mapping, game_state=game_state))
        except:
            logger.error("Exception occurred in MessageType '{}'".format(self.message_name))
            raise
            
class CustomMessageType(object):
    def __init__(self, message_name, func):
        self.message_name = message_name
        self.func = func
        
    def read(self, stream_object, type_method_mapping, game_state={}):
        "Returns a tuple ('message_name', {from field collection})"
        try:
            return (self.message_name, self.func(stream_object, type_method_mapping, game_state=game_state))
        except:
            logger.error("Exception occurred in MessageType '{}'".format(self.message_name))
            raise
    
class StreamStateModifierType(FieldCollection):
    def __init__(self, *fields):
        FieldCollection.__init__(self, *fields)
    
    def read(self, stream_object, type_method_mapping, stream_state, game_state={}):
        stream_state.update(FieldCollection.read(self, stream_object, type_method_mapping, game_state=game_state))
    

class UnknownMessageType(Exception): pass

class StreamSpecification(object):
    message_types = {}
    container_types = {}
    state_modifier_types = {}
    
    StreamClass = object
    type_method_mapping = {}
    default_state = {}
    message_type_id_type = ""

    def __init__(self, StreamClass, type_method_mapping, default_state, message_type_id_type, message_type_enum):
        self.StreamClass = StreamClass
        self.type_method_mapping = type_method_mapping
        self.default_state = default_state
        self.message_type_id_type = message_type_id_type
        self.message_type_enum = message_type_enum
        
        # indexed by message type identifier
        self.message_types = {}
        self.container_types = {}
        self.state_modifier_types = {}
        
    def add_message_type(self, message_type_id, message_type):
        self.message_types[message_type_id] = message_type
        
    def add_container_type(self, message_type_id, container_type):
        self.container_types[message_type_id] = container_type
        
    def add_state_modifier_type(self, message_type_id, state_modifier_type):
        self.state_modifier_types[message_type_id] = state_modifier_type
        
    def read(self, raw_stream, initial_state, game_state={}):
        state = {}
        state.update(self.default_state)
        state.update(initial_state)
    
        read_data = []
        
        try:
            stream_object = self.StreamClass(raw_stream)
            
            while(not stream_object.empty()):
                message_type_id = self.type_method_mapping[self.message_type_id_type](stream_object)
                
                debug_message_type_name = self.message_type_enum.by_value(message_type_id) if self.message_type_enum is not None else message_type_id
                logger.debug("Reading message: {}".format(debug_message_type_name))
                
                if message_type_id in self.message_types.keys():
                    message_name, datum = self.message_types[message_type_id].read(stream_object, self.type_method_mapping, game_state)
                    datum.update(state)
                    logger.debug(repr((message_name, datum)))
                    read_data.append((message_name, datum))
                elif message_type_id in self.container_types.keys():
                    try:
                        data = self.container_types[message_type_id].read(stream_object, self.type_method_mapping, state, game_state=game_state)
                        read_data.extend(data)
                    except TypeError:
                        logger.error("{}: {}".format(self.container_types[message_type_id], debug_message_type_name))
                        raise
                elif message_type_id in self.state_modifier_types.keys():
                    self.state_modifier_types[message_type_id].read(stream_object, self.type_method_mapping, state, game_state=game_state)
                else:
                    logger.error("Unknown message: {}".format(debug_message_type_name))
                    raise UnknownMessageType(message_type_id)
            return read_data
        except TypeError:
            print repr(raw_stream)
            raise

class StreamContainerType(StreamSpecification):
    def __init__(self, StreamClass, type_method_mapping, default_state, message_type_id_type, field_collection, length_field, message_type_enum):
        StreamSpecification.__init__(self, StreamClass, type_method_mapping, default_state, message_type_id_type, message_type_enum)
        self.field_collection = field_collection
        self.length_field = length_field
        
    def read(self, stream_object, type_method_mapping, initial_state, game_state={}):
        state = {}
        state.update(initial_state)
        state.update(self.field_collection.read(stream_object, type_method_mapping, game_state=game_state))
        
        _, stream_length = self.length_field.read(stream_object, type_method_mapping, game_state=game_state)
        
        stream_data = type_method_mapping['stream_data'](stream_object, stream_length)
        
        return StreamSpecification.read(self, stream_data, state, game_state=game_state)
