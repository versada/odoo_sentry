# -*- coding: utf-8 -*-
# This file is part of Odoo. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

import mock
import unittest2

from openerp.addons.odoo_sentry.logutils import SanitizeOdooCookiesProcessor


class TestOdooCookieSanitizer(unittest2.TestCase):

    def test_cookie_as_string(self):
        data = {
            'request': {
                'cookies': 'website_lang=en_us;'
                           'session_id=hello;'
                           'Session_ID=hello;'
                           'foo=bar',
            },
        }

        proc = SanitizeOdooCookiesProcessor(mock.Mock())
        result = proc.process(data)

        self.assertTrue('request' in result)
        http = result['request']
        self.assertEqual(
            http['cookies'],
            'website_lang=en_us;'
            'session_id={m};'
            'Session_ID={m};'
            'foo=bar'.format(
                m=proc.MASK,
            ),
        )

    def test_cookie_as_string_with_partials(self):
        data = {
            'request': {
                'cookies': 'website_lang=en_us;session_id;foo=bar',
            },
        }

        proc = SanitizeOdooCookiesProcessor(mock.Mock())
        result = proc.process(data)

        self.assertTrue('request' in result)
        http = result['request']
        self.assertEqual(
            http['cookies'],
            'website_lang=en_us;session_id;foo=bar'.format(m=proc.MASK),
        )

    def test_cookie_header(self):
        data = {
            'request': {
                'headers': {
                    'Cookie': 'foo=bar;'
                              'session_id=hello;'
                              'Session_ID=hello;'
                              'a_session_id_here=hello',
                },
            },
        }

        proc = SanitizeOdooCookiesProcessor(mock.Mock())
        result = proc.process(data)

        self.assertTrue('request' in result)
        http = result['request']
        self.assertEqual(
            http['headers']['Cookie'],
            'foo=bar;'
            'session_id={m};'
            'Session_ID={m};'
            'a_session_id_here={m}'.format(m=proc.MASK))