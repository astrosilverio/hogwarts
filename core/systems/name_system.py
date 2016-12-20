from collections import defaultdict

from braga import Aspect, System
from chainmap import ChainMap

from core.components import Name


class NameSystem(System):
    """Associates strings with Entities."""
    def __init__(self, world):
        super(NameSystem, self).__init__(world=world, aspect=Aspect(all_of=set([Name])))
        self.names = defaultdict(list)
        self.contexts = defaultdict(dict)
        self.update()

    @property
    def tokens(self):
        return self.names.keys()

    def get_entity(self, name, entities_for_context=None):
        if entities_for_context:
            dictionaries = [self.contexts[entity] for entity in entities_for_context]
            dictionaries.append(self.names)
            names_in_priority_order = ChainMap(*dictionaries)
            entity = names_in_priority_order.get(name, None)
        else:
            entity = self.names.get(name, None)
        if isinstance(entity, list):
            if len(entity) > 1:
                raise ValueError("Which {} do you mean?".format(name))
            entity = entity[0]

        return entity

    def add_name(self, name, entity):
        if entity in self.names[name]:
            raise ValueError('Duplicate entity names')
        self.names[name].append(entity)
        entity.names.append(name)

    def add_name_to_context(self, name, entity, entity_for_context):
        self.contexts[entity_for_context][name] = entity

    def update(self):
        for entity in self.entities:
            for name in entity.names:
                self.names[name].append(entity)
