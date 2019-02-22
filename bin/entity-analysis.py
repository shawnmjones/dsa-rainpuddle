import sys

surrogate_entity_file = sys.argv[1]
collection_entity_file = sys.argv[2]
noise_entity_file = sys.argv[3]
decoy_entity = sys.argv[4]
number_of_collection_entities = int(sys.argv[5])
output_file = sys.argv[6]

surrogate_entities = []
collection_entities = []

with open(surrogate_entity_file) as f:
    for line in f:
        line = line.strip()

        surrogate_entities.append(line)

with open(collection_entity_file) as f:
    for line in f:
        line = line.strip()

        collection_entities.append(line)

surrogate_entity_set = set(surrogate_entities)
collection_entity_set = set(collection_entities)

surrogate_entity_counts = []
collection_entity_counts = []

for entity in surrogate_entity_set:

    surrogate_entity_counts.append(
        ( surrogate_entities.count(entity), entity )
    )

for entity in collection_entity_set:

    if entity not in surrogate_entity_set:

        collection_entity_counts.append( 
            ( collection_entities.count(entity), entity )
            )

for item in sorted(collection_entity_counts, reverse=True)[0:number_of_collection_entities]:

    print(":{}".format(item[1])) 
