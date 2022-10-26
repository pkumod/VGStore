# VGSTore Demo

## Usage

```bash
pip3 install -r requirements.txt
python3 app.py
```

## Installation Preconditions

Before starting-up this demo, please make sure the gStore has been installed and started.

The gStore can be installed by following the instructions in [gStore Installation](https://github.com/pkumod/gStore).

Besides, the RDF-VG dataset should be loaded into database before running this demo (refer to RDF-VG Builder).

## gStore Connection Config

Please modify the `gStore_config` variable to connect to your gStore database.

## About frontend

```bash
cd frontend
```

Requirement: node.js, yarn.

Install Dependencies:

```bash
yarn install
```

Build frontend:

```bash
yarn build
```

## About Backend

1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

2. Start gStore Endpoint
3. Start backend server
```bash
python3 app.py
```

### Query Example

Example SPARQL
```sparql
SELECT ?img ?x ?y ?h ?w ?dog_obj WHERE {
	?dog_obj <hasName> "dog"^^<http://www.w3.org/2001/XMLSchema#string>.
	?cat_obj <hasName> "cat"^^<http://www.w3.org/2001/XMLSchema#string>.
	?dog_obj ?mm.sim ?cat_obj.
	FILTER(?mm.sim > 0.7).
	# img,x,y,h,w is used to render the bounding box.
	?img <hasObject> ?dog_obj.
	?dog_obj <x> ?x.
	?dog_obj <y> ?y.
	?dog_obj <height> ?h.
	?dog_obj <width> ?w.
} ORDER BY DESC(?mm.sim) LIMIT 10
```

Converted SPARQL
```sparql
SELECT ?img ?x ?y ?h ?w ?dog_obj WHERE {
	?dog_obj <hasName> "dog"^^<http://www.w3.org/2001/XMLSchema#string>.
	?img <hasObject> ?dog_obj.
	?dog_obj <x> ?x.
	?dog_obj <y> ?y.
	?dog_obj <height> ?h.
	?dog_obj <width> ?w.
   <Image/2391890> <hasObject> ?dog_obj.
} LIMIT 10
```
