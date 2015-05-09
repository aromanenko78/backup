"""Command-line skeleton application for Cloud Storage API.
"""
import sys

from storage_api import StorageApi


def main(argv):
  storage = StorageApi()
  storage.list('')


if __name__ == '__main__':
  main(sys.argv)
