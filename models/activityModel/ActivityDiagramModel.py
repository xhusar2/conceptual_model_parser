from models.Model import Model
from neomodel import StructuredNode, StringProperty, Relationship, StructuredRel, UniqueIdProperty


class ActivityDiagramModel(Model):

    def __init__(self, model_id, nodes, relations):
        self.id = model_id
        self.nodes = nodes
        self.relations = relations

    # return dict id, node
    def get_neo4j_model(self):
        m_nodes = {}
        relations = []
        for n in self.nodes:
            if n.node_type == "Action":
                node = Action(_id=n.id, name=n.name, model_id=self.id, visibility=n.visibility, type="Action")
            elif n.node_type == "Initial":
                node = InitialNode(_id=n.id, name=n.name, model_id=self.id, visibility=n.visibility, type="InitialNode")
            elif n.node_type == "ActivityFinal":
                node = ActivityFinalNode(_id=n.id, name=n.name, model_id=self.id, visibility=n.visibility, type="ActivityFinalNode")
            elif n.node_type == "ForkJoin":
                node = ForkJoinNode(_id=n.id, model_id=self.id, visibility=n.visibility, type="ForkJoinNode")
            elif n.node_type == "FlowFinal":
                node = FlowFinalNode(_id=n.id, name=n.name, model_id=self.id, visibility=n.visibility, type="FlowFinalNode")
            elif n.node_type == "DecisionMerge":
                node = DecisionMergeNode(_id=n.id, name=n.name, model_id=self.id, visibility=n.visibility, type="DecisionMergeNode")
            elif n.node_type == "Partition":
                node = Partition(_id=n.id, name=n.name, model_id=self.id, visibility=n.visibility, type="Partition")
            elif n.node_type == "CentralBuffer":
                node = CentralBufferNode(_id=n.id, name=n.name, model_id=self.id, visibility=n.visibility, type="CentralBufferNode")
            elif n.node_type == "OutputPin":
                node = OutputPin(_id=n.id, name=n.name, model_id=self.id, visibility=n.visibility, ordering=n.ordering, type="OutputPin")
            elif n.node_type == "InputPin":
                node = InputPin(_id=n.id, name=n.name, model_id=self.id, visibility=n.visibility, ordering=n.ordering, type="InputPin")
            else:
                node = None
            m_nodes[node._id] = node

        for r in self.relations:
            if r.dest is not None and r.src is not None:
                rel_source = r.dest
                rel_dest = r.src
                rel_props = {
                    'rel_type': r.relation_type,
                    'relation_id': r.id,
                    'guard': r.guard
                }
                rel_attrib = r.relation_type
                relations.append((rel_source, rel_dest, rel_props, rel_attrib))

        return m_nodes, relations


class RelationModel(StructuredRel):
    relation_id = StringProperty()
    rel_type = StringProperty()


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
    ObjectFlow = Relationship("ObjectNode", "controlFlow", model=RelationModel)
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


class ExecutableNode(ControlFlowNode):
    pass


class Action(ExecutableNode):
    Pin = Relationship("Pin", "has", model=RelationModel)
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
