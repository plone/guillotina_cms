# -*- coding: utf-8 -*-
from plone.cms.testing import PserverCMSTestCase


class TestContent(PserverCMSTestCase):

    def test_content(self):
        self.assertEqual(
            self.layer['portal']['news'].portal_type, 'News')
