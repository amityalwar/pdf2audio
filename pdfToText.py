import os, io
import re
from google.cloud import vision_v1
from google.cloud import storage
from google.protobuf import json_format

""" 
# pip install --upgrade google-cloud-storage
"""
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'storageServiceKey.json'
client = vision_v1.ImageAnnotatorClient()

batch_size = 2
mime_type = 'application/pdf'
feature = vision_v1.types.Feature(
    type=vision_v1.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

gcs_source_uri = 'gs://firstpdf2text/Martha McCaskey.pdf'
gcs_source = vision_v1.types.GcsSource(uri=gcs_source_uri)
input_config = vision_v1.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

gcs_destination_uri = 'gs://firstpdf2text/pdf_result'
gcs_destination = vision_v1.types.GcsDestination(uri=gcs_destination_uri)
output_config = vision_v1.types.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)

async_request = vision_v1.types.AsyncAnnotateFileRequest(
    features=[feature], input_config=input_config, output_config=output_config)

operation = client.async_batch_annotate_files(requests=[async_request])
operation.result(timeout=180)

storage_client = storage.Client()
match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
bucket_name = match.group(1)
prefix = match.group(2)
bucket = storage_client.get_bucket(bucket_name)

# List object with the given prefix
blob_list = list(bucket.list_blobs(prefix=prefix))
print('Output files:')
for blob in blob_list:
    print(blob.name)

output = blob_list[0]
json_string = output.download_as_string()
response = json_format.Parse(
            json_string, vision_v1.types.AnnotateFileResponse())

first_page_response = response.responses[0]
annotation = first_page_response.full_text_annotation

print(u'Full text:')
print(annotation.text)