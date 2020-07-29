# Challenge

## Development task

#### Context

Following the recent scandal with Wirecard, we would like to dedicate the development task to transparency in the financial world. We want also give the engineer a little bit of freedom for interpretation and creativity to allow to demonstrate his skills and thinking.

#### Goal 

- Create a RESTful application that will allow uploading an attached CSV file.
- After file upload application should process a file and calculate the sum of "amount EUR" column.
- After successful processing of file the application should send a notification on one of pre-configured service. This can be email, text message or SLACK channel. 

Notification content: 
"{date:dd/mm/yyyy hh24:mm} - {X} entries processed, sum: { sum of amount }"

# Solution

## The Algorithm

At first it seemed quite trivial to sum a column but I realized I have done something 
similar many times before in many different
ways and didn't know if there was an objective best way so I figured I'd investigate. Also it became apparent very 
quickly that using floats directly wouldn't provide the precision this task requires (unless using fsum).

I explored two different times, the time to read the file and the time to sum the file. 

The time to read the file is a constraint of the hard drive so it was used as a lower bound. I was also curious 
how the different line parsing methods compared to reading the file straight. You can see the results of the different 
methods in `algorithm_tests/reading_times.png` and `algorithm_tests/read_times_per_row.png`.

The second times are for the complete file read and summing. I tried a
lot of different ways just to compare. I had my hypotheses going into making each one and was interesting seeing how it 
actually did. I expected some overhead for some of the solutions but it was interesting to see how much it really can
be for files with a small number of rows. I have a lot more thoughts for things I could try but I had to say stop at 
some point. The results are in `algorithm_tests/sum_times.png`, `algorithm_tests/sum_times_per_row.png`, and
I did one more without the file with 1000 lines to see better detail of the bigger files here: 
`algorithm_tests/sum_times_per_row_no_1000.png`.

In the end I just ended up using dask because it does everything in a couple of lines and works well on a single cpu 
or in a distributed cluster. I think it would also be interesting to see how different methods do when the row size 
is larger or when some other variables are considered but like I said, I had to stop at some point.

#### Make running times graphs for your setup

```bash
cd test_files
python make_test_data.py
cd ../algorithm_tests
pip install -r requirements.txt
python sum_csv.py
```

## The Server

### Possible solutions

#### Scalable and Extendable Solution with Storage: Django Rest Framework + Dask

In this solution it is assumed we have verified that this process will be core to the business model and a scalable and
extendable solution is required. Also, it is assumes there is value in storing past processed files. Files will be 
uploaded to django where it is saved and then a dask task is kicked off 
to process the data. Its basically what I've been making for the last couple years for computer vision tasks. 
In the past, I have made a small demo here: 
https://github.com/MoonVision/django-dask-demo that I used as a starting point. 

The email just logs to stdout for the server. If you wanted to have an actual email you just need to set the env
variables `MAILGUN_API_KEY` and `MAILGUN_SENDER_DOMAIN` and then run the server with the setting 
(django/api/api/settings.py) `DEBUG = False`.

##### Setup

I am running on a mac so these are mac specific. You will need to have nging running locally and serving from the
folder /djangomedia/ on port 8001 to the /media/ location. The server file:

```
server {
    listen 8001 default_server;
    listen [::]:8001 default_server;

    index index.html;
    client_max_body_size 10240M;
    proxy_read_timeout 3600s;
    proxy_connect_timeout 3600s;

    root /djangomedia/;

    location /media/ {
        rewrite ^/media(.*)$ $1 permanent;
    }
}
```

```bash
sudo mkdir /djangomedia
sudo chown <YOUR USER> /djangomedia
cd django
pip install -r requirements.txt
cd api
python manage.py migrate
```

###### Email Setup: 

Mailgun is used (https://www.mailgun.com/) and requires `MAILGUN_API_KEY` and `MAILGUN_SENDER_DOMAIN` environment
variables to be set. Also, in `django/api/api/settings.py` DEBUG must be set to False. If these are not set, the
server will just log the email to stdout. You can set where the email is sent to with the environment variable 
`TASK_INFO_EMAIL`.

##### Run

From the folder oaze/django/api/:
```bash
python manage.py runserver
```

You can then go to `localhost:8000` in your browser and the path `http://localhost:8000/csv-documents/` is where you
can upload a csv file in browser and see results by following the `sum_task` link. The email is output in stdout of 
the server unless you setup the environment variables as mentioned above. In case you haven't used django rest framework
before, the browser urls are the same that are used in curl and the html is shown in browser because it
checks for cookies and shows the correct one. An example curl:

```bash
curl -X POST \
 -H "Content-Type: multipart/form-data" \
 -H "Accept: application/json" \
 -F  "file=@/path/to/file.csv" \
 http://localhost:8000/csv-documents/ 
```

#### No Storage Solution: Fastapi + Dask

If the only need of this solution is in processing the data and posting the results and there is no value in storing the 
data of past tasks then a simpler solution is possible. Also, if we know that the max number of lines in a file is 
small like the sample file, then it wouldn't make sense to have a distributed solution when it could just be computed 
in the request itself and on the server itself. I used fast api since you guys mentioned useing it.
I still used dask for this as it could work for a server only and distributed solution.

##### Setup

```bash
cd fast_api
pip install -r requirements.txt
```

###### Email Setup: 

I used fastapi-mail and it requires a gmail account. Also, if two factor authentication is enabled then you will need
to go through this https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor. You can set the receiver 
email with the env var `TASK_STATUS_EMAIL`. The seder email with `ADMIN_EMAIL`. The sender email password with 
`ADMIN_EMAIL_PASSWORD`. If no email is setup it will log to stdout on the server.

##### Run

```bash
uvicorn main:app
```

You can use the `http://localhost:8000/docs/` to post to `http://localhost:8000/sum_csv` or with a curl like above.

```bash
curl -X POST "http://localhost:8000/sum_csv" 
     -H "accept: application/json"
     -H "Content-Type: multipart/form-data"
     -F "file=@/path/to/file.csv;type=text/csv"
```

## Final thoughts

In the end, the correct solutions depends on the actual use case and its details. I have presented a bare bones
solution that just does what the prompt asks and a solution that also tracks the history and stores the data processed.
I wanted to see how it would compare and I don't have a strong preference for either, they both do the job. In the end
both could be correct or incorrect depending on the requirements of the system but both accomplish the goals in the 
task description.

###### Note: 
I tried to keep the requirements for each section separate but ended up just making everthing in a single
virtual env so sorry if one is missing for a section! If you install all 3 in algorithm_tests, django, and fast api
everything should work.
