"""Wrapper around storage apis.
"""
import httplib2
import json

from apiclient import discovery
from oauth2client.client import GoogleCredentials


class StorageApi(object):
  """Apis for sotrage bucket operations."""
  BUCKET_NAME = 'aromanenko_backup_disk'
  API_VERSION = 'v1'
  SECRET_PATH = '../secrets/client_secret2.json'

  def __init__(self):
    credentials = GoogleCredentials.from_stream(self.SECRET_PATH).create_scoped([
        'https://www.googleapis.com/auth/devstorage.read_write'])
    http = httplib2.Http()
    http = credentials.authorize(http)
    self.service = discovery.build('storage', self.API_VERSION, http=http)

  def list(self, prefix):
    req = self.service.buckets().get(bucket=self.BUCKET_NAME)
    resp = req.execute()
    print json.dumps(resp, indent=2)
    fields_to_return = 'nextPageToken,items(name,size,contentType,metadata(my-key))'
    req = self.service.objects().list(bucket=self.BUCKET_NAME, fields=fields_to_return)
    # If you have too many items to list in one request, list_next() will
    # automatically handle paging with the pageToken.
    while req is not None:
      resp = req.execute()
      print json.dumps(resp, indent=2)
      req = self.service.objects().list_next(req, resp)
