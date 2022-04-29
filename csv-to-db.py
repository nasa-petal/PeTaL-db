import sys
import csv
import boto3

dynamodb = boto3.resource('dynamodb')

tableName = 'petal-stack-myDynamoDBTable-4I5GQ39UPNHW'
filename = './biomimicry_predictions.csv'
filename_labels = './labels.csv'

def main():
    csvfile = open(filename)
    csvfile_labels = open(filename_labels)

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
                if float(value) > .3:
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

main()