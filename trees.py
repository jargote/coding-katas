__author__ = 'jargote'

class BinaryTree(object):
    def __init__(self, value):
        self._root = Node(value)

    def add_node(self, value):
        node = Node(value)
        self._root.add_child_node(node)

    def count_nodes(self):
        return self._root.count_children() + 1

    def get_depth(self):
        return self._root.depth()

    def get_nodes(self, level):
        pass

    def render(self):
        depth = self.get_depth()
        for level in range(depth+1):
            nodes = self.get_nodes(level)
            for node in nodes:
                out = '\n' * (pow(2, depth)/2) * depth
                out += '%s\t' % node.valu e

class Node(object):
    def __init__(self, value):
        self._value = value
        self._left_child = None
        self._right_child = None

    @property
    def value(self):
        return self._value

    def add_child_node(self, node):
        if not self._left_child:
            self._left_child = node
            return
        elif not self._right_child:
            self._right_child = node
            return
        else:
            return self._left_child.add_child_node(node)

    def count_children(self):
        children = 0

        if self._left_child:
            children += self._left_child.count_children() + 1
        if self._right_child:
            children += self._right_child.count_children() + 1

        return children

    def render(self):
        print '-------'
        print '|  %s  |' % self._value
        print '-------'

        ch = ''
        if self._left_child:
            ch += '  / '
        if self._right_child:
            ch += '  \ '

        if self._left_child:
            print self._left_child.render()
        if self._right_child:
            print self._right_child.render()

        print ch

    def depth(self):
        left_depth = 0
        right_depth = 0

        if self._left_child:
            left_depth += self._left_child.depth() + 1
        if self._right_child:
            right_depth += self._right_child.depth() + 1

        return left_depth if left_depth >= right_depth else right_depth