from models.Model import Model
from neomodel import StructuredNode, StringProperty, Relationship, StructuredRel, UniqueIdProperty


class ActivityDiagramModel(Model):

    def __init__(self, model_id, nodes, relations):
        self.id = model_id
        self.nodes = nodes
        self.relations = relations

    # return dict id, node
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
        for r in self.relations:
            if r.target is not None and r.source is not None:
                rel_source = r.source
                rel_destination = r.target
                rel_props = {
                    'rel_type': r.relation_type,
                    'relation_id': r.id,
                    'guard': r.guard,
                    'model_id': self.id
                }
                rel_attrib = r.relation_type
                relations.append((rel_source, rel_destination, rel_props, rel_attrib))
        return relations

    def get_node_type(self, node):
        if node.node_type == "Action":
            return Action(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility, type="Action")
        elif node.node_type == "Initial":
            return InitialNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                               type="InitialNode")
        elif node.node_type == "ActivityFinal":
            return ActivityFinalNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                     type="ActivityFinalNode")
        elif node.node_type == "ForkJoin":
            return ForkJoinNode(_id=node.id, model_id=self.id, visibility=node.visibility, type="ForkJoinNode")
        elif node.node_type == "FlowFinal":
            return FlowFinalNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                 type="FlowFinalNode")
        elif node.node_type == "DecisionMerge":
            return DecisionMergeNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                     type="DecisionMergeNode")
        elif node.node_type == "Partition":
            return Partition(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                             type="Partition")
        elif node.node_type == "CentralBuffer":
            return CentralBufferNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                     type="CentralBufferNode")
        elif node.node_type == "OutputPin":
            return OutputPin(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                             ordering=node.ordering, type="OutputPin")
        elif node.node_type == "InputPin":
            return InputPin(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                            ordering=node.ordering, type="InputPin")
        elif node.node_type == "Object":
            return InstanceSpecification(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                         type="InstanceSpecification")
        elif node.node_type == "DataStore":
            return DataStoreNode(_id=node.id, name=node.name, model_id=self.id, visibility=node.visibility,
                                 type="DataStoreNode")
        else:
            return None


class RelationModel(StructuredRel):
    relation_id = StringProperty()
    rel_type = StringProperty()
    guard = StringProperty()
    model_id = StringProperty()


class ActivityDiagramNode(StructuredNode):
    pass


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
    pass


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
