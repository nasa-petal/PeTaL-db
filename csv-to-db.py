import sys
import csv
import boto3
import re

dynamodb = boto3.resource('dynamodb')

tableName = 'petal-stack-myDynamoDBTable-4I5GQ39UPNHW'
filename = './biomim_pred_species.csv'
filename_labels = './labels.csv'
# need to update this to include rows for common to scientific mappings and rows for just the common names
filename_creatures = './creaturesdb.csv'

def main():
    csvfile = open(filename)
    csvfile_labels = open(filename_labels)
    csvfile_species = open(filename_creatures)
    
    write_species_to_dynamo(csv.DictReader(csvfile_species))
    write_labels_to_dynamo(csv.DictReader(csvfile_labels))
    write_to_dynamo(csv.DictReader(csvfile))

    return print("Done")

def slicedict(d, s):
    return {k:v for k,v in d.items() if k.startswith(s)}

def write_labels_to_dynamo(rows):
    table = dynamodb.Table(tableName)
    with table.batch_writer() as batch:
        for row in rows:
            batch.put_item(
                Item={
                    'PartitionKey': row['PartitionKey'],
                    'SortKey': row['SortKey'],
                    'level2': row['Level2'],
                    'level3': row['Level3']
                }
            )
def write_species_to_dynamo(rows):
    table = dynamodb.Table(tableName)
    with table.batch_writer() as batch:
        for row in rows:
            batch.put_item(
                Item={
                    'PartitionKey': row['PartitionKey'],
                    'SortKey': row['SortKey'],
                    'names': row['names']
                }
            )
def write_to_dynamo(rows):
    table = dynamodb.Table(tableName)
    with table.batch_writer() as batch:
        for row in rows:
            batch.put_item(
                Item={
                    'PartitionKey': 'ARTICLE',
                    'SortKey': 'ARTICLE-' + row['petalID'],
                    'title': row['title_full'],
                    'abstract': row['abstract_full'],
                    'doi': row['doi'],
                    'venue': row['venue'],
                    'url': row['url']
                }
            )
            labels = slicedict(row, 'LABEL-')
            for key, value in labels.items():
                batch.put_item(
                    Item={
                        'PartitionKey': key,
                        'SortKey': 'ARTICLE-' + row['petalID'],
                        'title': row['title_full'],
                        'abstract': row['abstract_full'],
                        'doi': row['doi'],
                        'venue': row['venue'],
                        'url': row['url'],
                        'score': value
                    }
                )

            creature_idx = 0
            for creature_name in row["species"]:
                only_letters = re.sub("[^A-z ]","",creature_name).lower().strip()
                no_space_name = re.sub("\s","_",only_letters)
                batch.put_item(
                    Item={
                        'PartitionKey': 'SPECIES-' + no_space_name,
                        'SortKey': 'ARTICLE-' + row['petalID'],
                        'title': row['title_full'],
                        'abstract': row['abstract_full'],
                        'doi': row['doi'],
                        'venue': row['venue'],
                        'url': row['url'],
                        'speciesName': creature_name,
                        'speciesAbsoluteRelevancy': row["absolute_relevancy"][creature_idx],
                        'speciesRelativeRelevancy': row["relative_relevancy"][creature_idx]  
                    }
                )
                creature_idx += 1


main()
