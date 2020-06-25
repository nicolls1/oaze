# Oaze challenge

## Development task

#### Context

Following the recent scandal with Wirecard, we would like to dedicate the development task to transparency in the financial world. We want also give the engineer a little bit of freedom for interpretation and creativity to allow to demonstrate his skills and thinking.

#### Goal 

- Create a RESTful application that will allow uploading an attached CSV file.
- After file upload application should process a file and calculate the sum of "amount EUR" column.
- After successful processing of file the application should send a notification on one of pre-configured service. This can be email, text message or SLACK channel. 

Notification content: 
"{date:dd/mm/yyyy hh24:mm} - {X} entries processed, sum: { sum of amount }"

#### Preffered programming language: Python

# Solution

### Requirements

* User should be able to quickly upload the file without having to wait for it to be processed. A large file might not
be able to processed in a reasonable amount of time. 
* File should be processed at least once

### Possible solutions

#### Comfort and Scalable Solution: Django Rest Framework + Dask

In this solution it is assumed we have verified that this process will be core to the business model and a scalable and
extendable solution is required. Also, it is assumes there is value in storing past processed files. Files will be 
uploaded to django where it is saved and then a dask task is kicked off 
to process the data. Its basically what I've been making for the last couple years for computer vision tasks. 
In the past, I have made a small demo here: 
https://github.com/MoonVision/django-dask-demo that I will use as a template. 

#### MVP Solution:

If the only value of this solution is in processing the data and posting the results and there is no value to store the 
data of past tasks then a simpler solution is possible. 

## Benchmarks

for 1,10,100,1000 documents
with rows 1000,100000,10000000,1000000000 

* Just read file
* Plain python solution
* c++?
* Simple server
* Dask
* Dask sub-task spawning

### Considerations when deployed in production

* file reading?
* 