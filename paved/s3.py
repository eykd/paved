# -*- coding: utf-8 -*-
"""paved.s3 -- Amazon S3 helper functions.

Requires boto.
"""
import time
import datetime
import itertools
import mimetypes
import hashlib

from paver.easy import error, info, options, path, dry, sh, Bunch

import boto

from . import util


util.update(
    options.paved,
    dict(
        s3 = Bunch(
            access_id = '',
            secret = '',
            ),
        )
    )


def open_s3(bucket):
    """
    Opens connection to S3 returning bucket and key
    """
    conn = boto.connect_s3(options.paved.s3.access_id, options.paved.s3.secret)
    try:
        bucket = conn.get_bucket(bucket)
    except boto.exception.S3ResponseError:
        bucket = conn.create_bucket(bucket)
    return bucket


def upload_s3(file_path, bucket_name, file_key, force=False, acl='private'):
    """Upload a local file to S3.
    """
    file_path = path(file_path)
    bucket = open_s3(bucket_name)

    if file_path.isdir():
        # Upload the contents of the dir path.
        paths = file_path.listdir()
        paths_keys = zip(paths, ['%s/%s' % (file_key, p.name) for p in paths])
    else:
        # Upload just the given file path.
        paths_keys = [(file_path, file_key)]

    for p, k in paths_keys:
        headers = {}
        s3_key = bucket.get_key(k)
        if not s3_key:
            from boto.s3.key import Key
            s3_key = Key(bucket, k)

        content_type = mimetypes.guess_type(p)[0]
        if content_type:
            headers['Content-Type'] = content_type
        file_size = p.stat().st_size
        file_data = p.bytes()
        file_md5, file_md5_64 = s3_key.get_md5_from_hexdigest(hashlib.md5(file_data).hexdigest())

        # Check the hash.
        if s3_key.etag:
            s3_md5 = s3_key.etag.replace('"', '')
            if s3_md5 == file_md5:
                info('Hash is the same. Skipping %s' % file_path)
                continue
            elif not force:
                # Check if file on S3 is older than local file.
                s3_datetime = datetime.datetime(*time.strptime(
                    s3_key.last_modified, '%a, %d %b %Y %H:%M:%S %Z')[0:6])
                local_datetime = datetime.datetime.utcfromtimestamp(p.stat().st_mtime)
                if local_datetime < s3_datetime:
                    info("File %s hasn't been modified since last " \
                         "being uploaded" % (file_key))
                    continue
        # File is newer, let's process and upload
        info("Uploading %s..." % (file_key))
        
        try:
            s3_key.set_contents_from_string(file_data, headers, policy=acl, replace=True, md5=(file_md5, file_md5_64))
        except Exception as e:
            error("Failed: %s" % e)
            raise


def download_s3(bucket_name, file_key, file_path, force=False):
    """Download a remote file from S3.
    """
    file_path = path(file_path)
    bucket = open_s3(bucket_name)

    file_dir = file_path.dirname()
    file_dir.makedirs()

    s3_key = bucket.get_key(file_key)
    if file_path.exists():
        file_data = file_path.bytes()
        file_md5, file_md5_64 = s3_key.get_md5_from_hexdigest(hashlib.md5(file_data).hexdigest())

        # Check the hash.
        try:
            s3_md5 = s3_key.etag.replace('"', '')
        except KeyError:
            pass
        else:
            if s3_md5 == file_md5:
                info('Hash is the same. Skipping %s' % file_path)
                return
                
            elif not force:
                # Check if file on S3 is older than local file.
                s3_datetime = datetime.datetime(*time.strptime(
                    s3_key.last_modified, '%a, %d %b %Y %H:%M:%S %Z')[0:6])
                local_datetime = datetime.datetime.utcfromtimestamp(file_path.stat().st_mtime)
                if s3_datetime < local_datetime:
                    info("File at %s is less recent than the local version." % (file_key))
                    return
        
    # If it is newer, let's process and upload
    info("Downloading %s..." % (file_key))
    
    try:
        with open(file_path, 'w') as fo:
            s3_key.get_contents_to_file(fo)
    except Exception as e:
        error("Failed: %s" % e)
        raise
