"""Command-line skeleton application for Cloud Storage API.
Usage:
  $ python storage-sample.py

You can also get help on all the command-line flags the program understands
by running:

  $ python storage-sample.py --help

"""

import argparse
import httplib2
import os
import sys
import json

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools
from oauth2client.client import Credentials
from oauth2client.client import GoogleCredentials


# Define sample variables.
_BUCKET_NAME = 'aromanenko_backup_disk'
_API_VERSION = 'v1'

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])


def main(argv):
  flags = parser.parse_args(argv[1:])

  credentials = GoogleCredentials.from_stream('../secrets/client_secret2.json').create_scoped([
      'https://www.googleapis.com/auth/devstorage.read_write',
  ])

  http = httplib2.Http()
  http = credentials.authorize(http)

  # Construct the service object for the interacting with the Cloud Storage API.
  service = discovery.build('storage', _API_VERSION, http=http)

  try:
    req = service.buckets().get(bucket=_BUCKET_NAME)
    resp = req.execute()
    print json.dumps(resp, indent=2)
    fields_to_return = 'nextPageToken,items(name,size,contentType,metadata(my-key))'
    req = service.objects().list(bucket=_BUCKET_NAME, fields=fields_to_return)
    # If you have too many items to list in one request, list_next() will
    # automatically handle paging with the pageToken.
    while req is not None:
      resp = req.execute()
      print json.dumps(resp, indent=2)
      
      req = service.objects().list_next(req, resp)

  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
        "the application to re-authorize")

if __name__ == '__main__':
  main(sys.argv)
