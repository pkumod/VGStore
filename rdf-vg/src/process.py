import json
import gc
from tqdm import tqdm
from rdflib import Literal

VG_PATH = '~/Download/VG/'

def process_image():
    print('Processing image')
    data = json.load(open('VG_PATHimage_data.json', 'r', encoding='utf-8'))

    with open('VG_PATHimage_no_url.nt', 'w', encoding='utf-8') as f:
        for img in tqdm(data):
            n = f"""
<Image/{img['image_id']}> <width> "{img['width']}"^^<http://www.w3.org/2001/XMLSchema#int> .
<Image/{img['image_id']}> <height> "{img['height']}"^^<http://www.w3.org/2001/XMLSchema#int> .
"""
            if img['coco_id'] is not None:
                n += f"""<Image/{img['image_id']}> <coco_id> "{img['coco_id']}"^^<http://www.w3.org/2001/XMLSchema#string> .
"""
            if img['flickr_id'] is not None:
                n += f"""<Image/{img['image_id']}> <flickr_id> "{img['flickr_id']}"^^<http://www.w3.org/2001/XMLSchema#string> .
"""
            f.write(n)
    x = open('VG_PATHimage_no_url.nt', 'r', encoding='utf-8').readlines()
    x = list(set(x))
    open('VG_PATHimage_no_url.nt', 'w', encoding='utf-8').writelines(x)
    gc.collect()


def process_region():
    print('Processing region')
    data = json.load(open('VG_PATHregion_descriptions.json', 'r', encoding='utf-8'))

    with open('VG_PATHregion.nt', 'w', encoding='utf-8') as f:
        for regions in tqdm(data):
            for region in regions['regions']:
                phrase = region['phrase'].replace('\n', ' ')
                n = f"""
<Region/{region['region_id']}> <x> "{region['x']}"^^<http://www.w3.org/2001/XMLSchema#int> .
<Region/{region['region_id']}> <y> "{region['y']}"^^<http://www.w3.org/2001/XMLSchema#int> .
<Region/{region['region_id']}> <height> "{region['height']}"^^<http://www.w3.org/2001/XMLSchema#int> .
<Region/{region['region_id']}> <width> "{region['width']}"^^<http://www.w3.org/2001/XMLSchema#int> .
<Region/{region['region_id']}> <description> {Literal(phrase).n3()}^^<http://www.w3.org/2001/XMLSchema#string> .
<Image/{region['image_id']}> <hasRegion> <Region/{region['region_id']}> .   
"""
                f.write(n)

    x = open('VG_PATHregion.nt', 'r', encoding='utf-8').readlines()
    x = list(set(x))
    open('VG_PATHregion_no_dup.nt', 'w', encoding='utf-8').writelines(x)
    gc.collect()

def process_object():
    print('Processing object')
    data = json.load(open('VG_PATHobjects.json', 'r', encoding='utf-8'))

    with open('VG_PATHobject.nt', 'w', encoding='utf-8') as f:
        for objs in tqdm(data):
            for obj in objs['objects']:
                n = f"""
<Image/{objs['image_id']}> <hasObject> <Object/{obj['object_id']}> .
<Object/{obj['object_id']}> <x> "{obj['x']}"^^<http://www.w3.org/2001/XMLSchema#int> .
<Object/{obj['object_id']}> <y> "{obj['y']}"^^<http://www.w3.org/2001/XMLSchema#int> .
<Object/{obj['object_id']}> <height> "{obj['h']}"^^<http://www.w3.org/2001/XMLSchema#int> .
<Object/{obj['object_id']}> <width> "{obj['w']}"^^<http://www.w3.org/2001/XMLSchema#int> .
"""
                for name in obj['names']:
                    n += f"""
<Object/{obj['object_id']}> <hasName> {Literal(name).n3()}^^<http://www.w3.org/2001/XMLSchema#string> .
"""

                for synet in obj['synsets']:
                    n += f"""
<Object/{obj['object_id']}> <inSynset> <Synset/{synet}> .
"""
                f.write(n)
    x = open('VG_PATHobject.nt', 'r', encoding='utf-8').readlines()
    x = list(set(x))
    open('VG_PATHobject.nt', 'w', encoding='utf-8').writelines(x)
    gc.collect()

def process_relation():
    print('Processing relation')
    data = json.load(open('VG_PATHrelationships.json', 'r', encoding='utf-8'))

    with open('VG_PATHrelation_v2.nt', 'w', encoding='utf-8') as f:
        for rels in tqdm(data):
            n = ""
            for rel in rels['relationships']:
                pred_name = rel['predicate'].split()
                try: 
                    pred_name = ''.join([pred_name[0]] + [x.title() for x in pred_name[1:]])
                except:
                    continue
                '''
                n = f"""
<Relation/{rel['relationship_id']}> <hasName> "{rel['predicate']}"^^<http://www.w3.org/2001/XMLSchema#string> .
<Object/{rel['subject']['object_id']}> <Relation/{rel['relationship_id']}> <Object/{rel['object']['object_id']}> ."""
                '''
                n += f"""
<Object/{rel['subject']['object_id']}> <{pred_name}> <Object/{rel['object']['object_id']}> ."""
                for synet in rel['synsets']:
                    # n += f"""<Relation/{rel['relationship_id']}> <inSynset> <Synset/{Literal(synet).n3()}> ."""
                    pass
            f.write(n)
    x = open('VG_PATHrelation_v2.nt', 'r', encoding='utf-8').readlines()
    x = list(set(x))
    open('VG_PATHrelation_v2.nt', 'w', encoding='utf-8').writelines(x)
    gc.collect()

def process_scene_graph():
    print('Processing scene graph')
    data = json.load(open('VG_PATHscene_graphs.json', 'r', encoding='utf-8'))
 
    with open('VG_PATHscene_graph_v2.nt', 'w', encoding='utf-8') as f:
        for sg in tqdm(data):
            n = ""
            for rel in sg['relationships']:
                pred_name = rel['predicate'].split()
                try: 
                    pred_name = ''.join([pred_name[0]] + [x.title() for x in pred_name[1:]])
                except:
                    continue
                '''
                n = f"""
<Image/{sg['image_id']}> <hasRelation> <Relation/{rel['relationship_id']}> .
<Object/{rel['subject_id']}> <Relation/{rel['relationship_id']}> <Object/{rel['object_id']}> .
<Relation/{rel['relationship_id']}> <predicate> "{rel['predicate']}"^^<http://www.w3.org/2001/XMLSchema#string> .
"""
                '''
                n += f"""
<Object/{rel['subject_id']}> <{pred_name}> <Object/{rel['object_id']}> .
"""
                for synet in rel['synsets']:
                    # n += f"""<Relation/{rel['relationship_id']}> <inSynset> <Synset/{Literal(synet).n3()}> ."""
                    pass

            for obj in sg['objects']:
                n += f"""
<Image/{sg['image_id']}> <hasObject> <Object/{obj['object_id']}> .
<Object/{obj['object_id']}> <x> "{obj['x']}"^^<http://www.w3.org/2001/XMLSchema#int> .
<Object/{obj['object_id']}> <y> "{obj['y']}"^^<http://www.w3.org/2001/XMLSchema#int> .
<Object/{obj['object_id']}> <height> "{obj['h']}"^^<http://www.w3.org/2001/XMLSchema#int> .
<Object/{obj['object_id']}> <width> "{obj['w']}"^^<http://www.w3.org/2001/XMLSchema#int> ."""
                for name in obj['names']:
                    n += f"""
<Object/{obj['object_id']}> <hasName> {Literal(name).n3()}^^<http://www.w3.org/2001/XMLSchema#string> .
"""

                for synet in obj['synsets']:
                    n += f"""
<Object/{obj['object_id']}> <inSynset> <Synset/{synet}> .
"""
            f.write(n)

    x = open('VG_PATHscene_graph_v2.nt', 'r', encoding='utf-8').readlines()
    x = list(set(x))
    open('VG_PATHscene_graph_v2.nt', 'w', encoding='utf-8').writelines(x)
    gc.collect()


if __name__ == '__main__':
    process_image()
    process_scene_graph()
    process_object()
    process_region()
    process_relation()
    print('Done')
