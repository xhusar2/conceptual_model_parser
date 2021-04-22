from models.Model import Model
from neomodel import StructuredNode, StringProperty, Relationship, StructuredRel, UniqueIdProperty


class ActivityDiagramModel(Model):

    def __init__(self, model_id, nodes, relations):
        self.id = model_id
        self.nodes = nodes
        self.relations = relations

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
            return Action(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, type="Action")
        elif node.node_type == "Initial":
            return InitialNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, type="InitialNode")
        elif node.node_type == "ActivityFinal":
            return ActivityFinalNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, type="ActivityFinalNode")
        elif node.node_type == "ForkJoin":
            return ForkJoinNode(_id=node.id, model_id=self.id, visibility=node.visibility, type="ForkJoinNode")
        elif node.node_type == "FlowFinal":
            return FlowFinalNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, type="FlowFinalNode")
        elif node.node_type == "DecisionMerge":
            return DecisionMergeNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, type="DecisionMergeNode")
        elif node.node_type == "Partition":
            return ActivityPartition(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, type="ActivityPartition")
        elif node.node_type == "CentralBuffer":
            return CentralBufferNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, type="CentralBufferNode")
        elif node.node_type == "OutputPin":
            return OutputPin(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, ordering=node.ordering, type="OutputPin")
        elif node.node_type == "InputPin":
            return InputPin(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, ordering=node.ordering, type="InputPin")
        elif node.node_type == "DataStore":
            return DataStoreNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, type="DataStoreNode")
        else:
            return None


class RelationModel(StructuredRel):
    relation_id = StringProperty()
    rel_type = StringProperty()
    guard = StringProperty()
    model_id = StringProperty()


class ActivityDiagramNode(StructuredNode):
    model_id = StringProperty()
    _id = UniqueIdProperty()
    type = StringProperty()
    visibility = StringProperty()


class ActivityNode(ActivityDiagramNode):
    PartitionMember = Relationship("ActivityPartition", "partitionMember", model=RelationModel)


class ControlFlowNode(ActivityNode):
    ControlFlow = Relationship("ControlFlowNode", "controlFlow", model=RelationModel)


class ActivityPartition(ActivityDiagramNode):
    name = StringProperty()
    PartitionMember = Relationship("ActivityPartition", "partitionMember", model=RelationModel)


class ObjectNode(ActivityNode):
    ObjectFlow = Relationship("ActivityNode", "objectFlow", model=RelationModel)
    name = StringProperty()
    ordering = StringProperty()


class Pin(ObjectNode):
    pass


class OutputPin(Pin):
    pass


class InputPin(Pin):
    pass


class CentralBufferNode(ObjectNode):
    pass


class DataStoreNode(CentralBufferNode):
    pass


class ExecutableNode(ControlFlowNode):
    pass


class Action(ExecutableNode):
    HasPin = Relationship("Pin", "has", model=RelationModel)
    name = StringProperty()


class ControlNode(ControlFlowNode):
    name = StringProperty()
    ObjectFlow = Relationship("ActivityNode", "objectFlow", model=RelationModel)


class FinalNode(ControlNode):
    pass


class ActivityFinalNode(FinalNode):
    pass


class FlowFinalNode(FinalNode):
    pass


class InitialNode(ControlNode):
    pass


class ForkJoinNode(ControlNode):
    pass


class DecisionMergeNode(ControlNode):
    pass
