import sys
import csv
import boto3
import re
import json

dynamodb = boto3.resource('dynamodb')

tableName = 'petal-stack-myDynamoDBTable-4I5GQ39UPNHW'
filename = './biomim_pred_species.csv'
filename_labels = './labels.csv'
filename_creatures = './creaturesdb.csv'
filename_species_label = "./species-label.json"
filename_label_species = "./label-species.json"

def main():
    csvfile = open(filename)
    csvfile_labels = open(filename_labels)
    csvfile_species = open(filename_creatures)
    csvfile_species_mapping = json.load(open(filename_species_label))
    csvfile_label_mapping = json.load(open(filename_label_species))
    
    write_species_to_dynamo(csv.DictReader(csvfile_species))
    labelIDMapping = write_labels_to_dynamo(csv.DictReader(csvfile_labels))
    write_to_dynamo(csv.DictReader(csvfile), labelIDMapping)
    write_species_map_to_dynamo(csvfile_species_mapping, labelIDMapping)
    write_label_map_to_dynamo(csvfile_label_mapping, labelIDMapping)
    return print("Done")

def slicedict(d, s):
    return {k:v for k,v in d.items() if k.startswith(s)}

def write_labels_to_dynamo(rows):
    labelIDMapping = {}
    table = dynamodb.Table(tableName)
    with table.batch_writer() as batch:
        id = 1
        for row in rows:
            labelIDMapping[row['OldLabelID']] = id
            id += 1
            batch.put_item(
                Item={
                    'PartitionKey': 'LAB',
                    'SortKey': id,
                    'level2': row['Level2'],
                    'level3': row['Level3']
                }
            )
    return labelIDMapping
def write_species_map_to_dynamo(keyVal, labelIDMapping):
    table = dynamodb.Table(tableName)
    with table.batch_writer() as batch:
        for species in keyVal:
            for label in keyVal[species]:
                batch.put_item(
                    Item={
                        'PartitionKey': 'SPE' + species,
                        'SortKey': 'LAB' + labelIDMapping[label]
                    }
                )

# Write label to species function mapping to dynamo
def write_label_map_to_dynamo(keyVal, labelIDMapping):
    table = dynamodb.Table(tableName)
    with table.batch_writer() as batch:
        for label in keyVal:
            for species in keyVal[label]:
                batch.put_item(
                    Item={
                        'PartitionKey': 'LAB' + labelIDMapping[label],
                        'SortKey': 'SPE' + species
                    }
                )

def write_species_to_dynamo(rows):
    table = dynamodb.Table(tableName)
    with table.batch_writer() as batch:
        for row in rows:
            batch.put_item(
                Item={
                    'PartitionKey': 'SPE',
                    'SortKey': row['names'].lower().strip()
                }
            )
def write_to_dynamo(rows, labelIDMapping):
    table = dynamodb.Table(tableName)

    with table.batch_writer() as batch:
        for row in rows:
            batch.put_item(
                Item={
                    'PartitionKey': 'ART',
                    'SortKey': row['petalID'],
                    'title': row['title_full'],
                    'abstract': row['abstract_full'],
                    'doi': row['doi'],
                    'venue': row['venue'],
                    'url': row['url']
                }
            )
            labels = slicedict(row, 'LAB')
            for key, value in labels.items():
                if float(value) > .3:
                    batch.put_item(
                        Item={
                            'PartitionKey': 'LAB' + labelIDMapping[key],
                            'SortKey': 'ART' + row['petalID'],
                            'title': row['title_full'],
                            'abstract': row['abstract_full'],
                            'doi': row['doi'],
                            'venue': row['venue'],
                            'url': row['url'],
                            'score': value
                        }
                    )

            creature_idx = 0
            for creature_name in row['species']:
                batch.put_item(
                    Item={
                        'PartitionKey': 'SPE' + creature_name.lower().strip(),
                        'SortKey': 'ART' + row['petalID'],
                        'title': row['title_full'],
                        'abstract': row['abstract_full'],
                        'doi': row['doi'],
                        'venue': row['venue'],
                        'url': row['url'],
                        'speciesAbsoluteRelevancy': row['absolute_relevancy'][creature_idx],
                        'speciesRelativeRelevancy': row['relative_relevancy'][creature_idx]  
                    }
                )
                creature_idx += 1


main()
