# -*- coding: utf-8 -*-

from plone.server.testing import PloneBaseLayer
import unittest
import json


class PserverCMSLayer(PloneBaseLayer):

    @classmethod
    def setUp(cls):
        resp = cls.requester('POST', '/plone/plone/', data=json.dumps({
            "@type": "Document",
            "title": "Welcome",
            "id": "front-page",
            "description": "Description Plone Site"
        }))
        assert resp.status_code == 200

        resp = cls.requester('POST', '/plone/plone/', data=json.dumps({
            "@type": "Item",
            "title": "News",
            "id": "news",
        }))
        assert resp.status_code == 200

        resp = cls.requester('POST', '/plone/plone/', data=json.dumps({
            "@type": "Item",
            "title": "Events",
            "id": "events",
        }))
        assert resp.status_code == 200


class PserverCMSTestCase(unittest.TestCase):
    ''' Adding the OAuth utility '''
    layer = PserverCMSLayer
