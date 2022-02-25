
## Assign variable 

export PROJECT_ID="Projecid"

export TOPIC_ID="Topic Name"

export SUBSCRIPTION_ID="Topic Name -sub"

export service_acct="server account name "

## Step 1 
Create Service account and assing roles 

gcloud config set project $PROJECT_ID

gcloud iam service-accounts create $service_acct

srv_acc=$(gcloud iam service-accounts list | grep $service_acct | awk {'print $2'})

gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:$srv_acc --role=roles/pubsub.publisher

gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:$srv_acc --role=roles/bigquery.admin

gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:$srv_acc --role=roles/storage.admin

gcloud projects add-iam-policy-binding $PROJECT_ID --member=serviceAccount:$srv_acc --role=roles/storage.legacyBucketWriter

## setp 2

create pub/sub topic 

gcloud pubsub topics create $TOPIC_ID

## setp 3

Create Big Query table,schma and storage bucket 

bq mk $PROJECT_ID_bq

bq mk $PROJECT_ID_bk.dfdata hostname:STRING,time:TIMESTAMP,size:FLOAT,used:FLOAT,avail:FLOAT,Mounted:STRING

gsutil mb gs://$PROJECT_ID

mkdir temp && touch temp/test && gsutil cp -r temp gs://$PROJECT_ID

## setp 4

Create Data flow jobs 

gcloud dataflow jobs run ps-to-bq-aimlproject \
--gcs-location gs://dataflow-templates-us-central1/latest/PubSub_to_BigQuery \
--region us-central1 --staging-location gs://$PROJECT_ID/temp \
--parameters inputTopic=projects/$PROJECT_ID/topics/$TOPIC_ID,outputTableSpec=$PROJECT_ID:$PROJECT_ID_bq.dfdata
