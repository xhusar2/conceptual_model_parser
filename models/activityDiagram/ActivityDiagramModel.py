from models.Model import Model
from neomodel import StructuredNode, StringProperty, Relationship, StructuredRel, UniqueIdProperty


class ActivityDiagramModel(Model):

    def __init__(self, model_id, nodes, relations, url=None):
        self.id = model_id
        self.nodes = nodes
        self.relations = relations
        self.url = url

    def get_neo4j_model(self):
        m_nodes = self.get_nodes()
        relations = self.get_relations()
        return m_nodes, relations

    def get_nodes(self):
        nodes = {}
        for n in self.nodes:
            node = self.get_node_type(n)
            if node is not None:
                nodes[n.id] = node
        return nodes

    def get_relations(self):
        relations = []
        for relation in self.relations:
            if relation.target is not None and relation.source is not None:
                relation_source = relation.source
                relation_target = relation.target
                relation_properties = {
                    'rel_type': relation.relation_type,
                    'relation_id': relation.id,
                    'guard': relation.guard,
                    'model_id': self.id
                }
                relation_type = relation.relation_type
                relations.append((relation_source, relation_target, relation_properties, relation_type))
        return relations

    def get_node_type(self, node):
        if node.node_type == "Action":
            return Action(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, type="Action",
                          url=self.url)
        elif node.node_type == "Initial":
            return InitialNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                               type="InitialNode", url=self.url)
        elif node.node_type == "ActivityFinal":
            return ActivityFinalNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                     type="ActivityFinalNode", url=self.url)
        elif node.node_type == "ForkJoin":
            return ForkJoinNode(_id=node.id, model_id=self.id, visibility=node.visibility, type="ForkJoinNode",
                                url=self.url)
        elif node.node_type == "FlowFinal":
            return FlowFinalNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                 type="FlowFinalNode", url=self.url)
        elif node.node_type == "DecisionMerge":
            return DecisionMergeNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                     type="DecisionMergeNode", url=self.url)
        elif node.node_type == "Partition":
            return Partition(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                             type="Partition", url=self.url)
        elif node.node_type == "CentralBuffer":
            return CentralBufferNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                     type="CentralBufferNode", url=self.url)
        elif node.node_type == "OutputPin":
            return OutputPin(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                             ordering=node.ordering, type="OutputPin", url=self.url)
        elif node.node_type == "InputPin":
            return InputPin(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                            ordering=node.ordering, type="InputPin", url=self.url)
        elif node.node_type == "Object":
            return InstanceSpecification(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                         type="InstanceSpecification", url=self.url)
        elif node.node_type == "DataStore":
            return DataStoreNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                 type="DataStoreNode", url=self.url)
        else:
            return None


class RelationModel(StructuredRel):
    relation_id = StringProperty()
    rel_type = StringProperty()
    guard = StringProperty()
    model_id = StringProperty()


class ActivityDiagramNode(StructuredNode):
    url = StringProperty()


class ActivityNode(ActivityDiagramNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    type = StringProperty()
    visibility = StringProperty()
    name = StringProperty()
    PartitionMember = Relationship("Partition", "partitionMember", model=RelationModel)


class ControlFlowNode(ActivityNode):
    ControlFlow = Relationship("ControlFlowNode", "controlFlow", model=RelationModel)


class Partition(ActivityDiagramNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    type = StringProperty()
    visibility = StringProperty()
    name = StringProperty()


class ObjectNode(ActivityNode):
    ObjectFlow = Relationship("ObjectNode", "objectFlow", model=RelationModel)
    name = StringProperty()


class Pin(ObjectNode):
    ordering = StringProperty()


class OutputPin(Pin):
    pass


class InputPin(Pin):
    pass


class CentralBufferNode(ObjectNode):
    pass


class InstanceSpecification(ObjectNode):
    pass


class DataStoreNode(CentralBufferNode):
    pass


class ExecutableNode(ControlFlowNode):
    pass


class Action(ExecutableNode):
    HasPin = Relationship("Pin", "has", model=RelationModel)
    name = StringProperty()


class ControlNode(ControlFlowNode):
    pass


class FinalNode(ControlNode):
    name = StringProperty()


class ActivityFinalNode(FinalNode):
    pass


class FlowFinalNode(FinalNode):
    pass


class InitialNode(ControlNode):
    name = StringProperty()


class ForkJoinNode(ControlNode):
    pass


class DecisionMergeNode(ControlNode):
    name = StringProperty()
