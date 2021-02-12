# PeTaL (Periodic Table of Life) Database

The Periodic Table of Life (PeTaL, pronounced petal) is a design tool aimed at allowing users to seemlesly move from ideas (from nature or other sources) to design.

PeTaL is comprised of multiple interconnected services. This repository houses the AWS CloudFormation template that creates the DynamoDB table and AWS API Gateway REST API, and a json file with data to load into the DynamoDB table. There are other repositories for the [ReactJS web front end client](https://github.com/nasa/PeTaL) and [Labeller](https://github.com/nasa/petal-labeller).

## Getting started

1. Run cloud formation template (dynamodb-cf-template.yaml) to create PetalLabels dynamodb table and api
1. Open Aws cloudshell
1. Upload data.json file
1. Run this command to add items to the PetalLabels table:    
`aws dynamodb batch-write-item --request-items file://data.json`