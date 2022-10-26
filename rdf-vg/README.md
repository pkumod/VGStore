# RDF-VG Builder

## Introduction

This is a tool for building a RDF-stored Visual Genome dataset.

The data structure of Visual Genome is refer to [Visual Genome Python Driver](https://github.com/ranjaykrishna/visual_genome_python_driver).

The ontology of RDF-VG is described in our paper and this repo.


## Usage

1. Download the [Visual Genome](https://visualgenome.org/) dataset and unzip it.
2. Install requirements: `pip install -r requirements.txt`
3. Run rdf-vg builder by `python3 process.py`
4. Deduplicate the triples by `python3 clean_dup.py`

Now you are supposed to get a series of `.nt` files which contain the RDF triples of Visual Genome.

## Import RDF-VG into gStore

1. Install gStore (refer to [gStore](https://github.com/pkumod/gStore)).
2. run `./bin/gbuild -db vg -f xxxxx.nt` to import RDF-VG nt triples into gStore.
3. Serve RDF-VG by `./bin/grpc -db vg -p 5001`.

Now you can use the RDF-VG dataset by gStore query interface (SPARQL).
