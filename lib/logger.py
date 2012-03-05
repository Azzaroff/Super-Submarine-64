from vr_lib.simple_navigation import *

def log_scene_graph(node, level):
    children = node.Children.value
    num_children = children.__len__()
    i = 0
    j = 0
        
    indent = ""
    while j < level:
        indent += "  "
        j = j + 1

    print indent, node.Name.value, " children: ", num_children
        
    while i < num_children:
        child = children[i]
        i = i + 1
        
        if isinstance(child, avango.osg._osg.Group):
            log_scene_graph(child, level + 1) 
