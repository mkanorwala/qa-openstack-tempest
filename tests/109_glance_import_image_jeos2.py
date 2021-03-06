#!/usr/bin/python

import sys
import os

sys.path.append('./')

from glanceclient import Client
from base_test import BaseTest
import time
import os

def upload_glance_image(file, disk_format='raw', container_format='bare', image_name='jeos1', timeout=60):
    """ Upload glance image file """

    baseTest = BaseTest()
    token = baseTest.token
    endpoint = baseTest.get_service_endpoint('glance')
    endpoint = endpoint.rsplit('/', 1)[0]

    glance = Client('1', endpoint, token)

    start = int(time.time())
    image = glance.images.create(name=image_name, disk_format=disk_format, container_format=container_format, is_public=True)

    image.update(data=open(file, 'rb'))
   
    return baseTest._wait_for_image_status(image.id, 'ACTIVE', 60) 

def test_glance_import_image(file, disk_format='raw', container_format='bare'):
    """ test administrator can deploy a glance image """
    return upload_glance_image(file, 'raw', 'bare', 'jeos_02', 60)

file = os.environ.get('IMAGE_FILE')
if file == None or not os.path.isfile(file):
    print "Can not find the image file %s" %file
    exit(2)

ret = test_glance_import_image(file, 'raw', 'bare')
exit(ret)
