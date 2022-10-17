import gc

x = open('scene_graph.nt').readlines()
x = list(set(x))
open('scene_graph.nt', 'w').writelines(x)

gc.collect()

x = open('region.nt').readlines()
x = list(set(x))
open('region.nt', 'w').writelines(x)
