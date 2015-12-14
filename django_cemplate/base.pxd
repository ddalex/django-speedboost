cdef class Node(object):
    # Set this to True for nodes that must be first in the template (although
    # they can be preceded by text nodes.
    cdef public source
    cpdef render(self, context)
    cpdef list get_nodes_by_type(self, nodetype)


cdef class NodeList(list):
    # Set to True the first time a non-TextNode is inserted by
    # extend_nodelist().
    cdef public bint contains_nontext
    cpdef list get_nodes_by_type(self, nodetype)


