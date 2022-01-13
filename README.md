# PeTaL (Periodic Table of Life) Database

The Periodic Table of Life (PeTaL, pronounced petal) is a design tool aimed at allowing users to seemlesly move from ideas (from nature or other sources) to design.

PeTaL is comprised of multiple interconnected services. This repository houses the AWS CloudFormation template that creates the DynamoDB table, AWS API Gateway REST API, Lambdas, Step Functions, and S3 definitions for the labeller, and a json file with dummy data to load into the DynamoDB table. There are other repositories for the [ReactJS web front end client](https://github.com/nasa/PeTaL) and [Labeller](https://github.com/nasa/petal-labeller).

## Getting started

1. In AWS console, go to CloudFormation and run this template (dynamodb-cf-template.yaml) to create PetalLabels dynamodb table and api
1. Open AWS cloudshell
1. Upload biomimicry_predictions.csv, labels.csv, and csv-to-db.py.
1. Run this command to initialize the PetalLabels table with data:    
`python3 csv-to-db.py &`
1. The script takes about 45 minutes to complete. Make sure you interact with the shell every 15 minutes or so; the shell will close if there's no activity for 20-30 minutes.

## Contributing

We're using the [Git Feature Branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow), to contribute code to the code base. To summarize, `main` should always contain only stable, tested code. To work on a change, first create a feature branch off of `main`, perform your changes, and when your code is ready, submit a pull request to merge your branch with `main` and select an appropriate reviewer. 
