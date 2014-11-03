from mock import patch
import os
from unittest import TestCase

from utils import temp_dir
from win_agent_archive import (
    add_agents,
    get_source_agent_version,
    main,
)


class FakeArgs:

    def __init__(self, source_agent=None, version=None,
                 verbose=False, dry_run=False):
        self.source_agent = source_agent
        self.version = version
        self.verbose = verbose
        self.dry_run = dry_run


class WinAgentArchive(TestCase):

    def test_main_add(self):
        with patch('win_agent_archive.add_agents') as mock:
            main(['add', 'path/juju-1.21.0-win2012-amd64.tgz'])
            all_args, kwargs = mock.call_args
            args = all_args[0]
            self.assertEqual(
                'path/juju-1.21.0-win2012-amd64.tgz', args.source_agent)
            self.assertFalse(args.verbose)
            self.assertFalse(args.dry_run)

    def test_main_get(self):
        with patch('win_agent_archive.get_agents') as mock:
            main(['get', '1.21.0'])
            all_args, kwargs = mock.call_args
            args = all_args[0]
            self.assertEqual('1.21.0', args.version)
            self.assertFalse(args.verbose)
            self.assertFalse(args.dry_run)

    def test_get_source_agent_version(self):
        self.assertEqual(
            '1.21.0',
            get_source_agent_version('juju-1.21.0-win2012-amd64.tgz'))
        self.assertEqual(
            '1.21-alpha3',
            get_source_agent_version('juju-1.21-alpha3-win2012-amd64.tgz'))
        self.assertEqual(
            '1.21-beta1',
            get_source_agent_version('juju-1.21-beta1-win2012-amd64.tgz'))
        self.assertEqual(
            '1.22.0',
            get_source_agent_version('juju-1.22.0-win2012-amd64.tgz'))
        self.assertEqual(
            '1.21.0',
            get_source_agent_version('juju-1.21.0-win9,1-amd64.tgz'))
        self.assertIs(
            None,
            get_source_agent_version('juju-1.21.0-trusty-amd64.tgz'))
        self.assertIs(
            None,
            get_source_agent_version('juju-1.21.0-win2012-386.tgz'))
        self.assertIs(
            None,
            get_source_agent_version('juju-1.21.0-win2012-amd64.tar.gz'))
        self.assertIs(
            None,
            get_source_agent_version('1.21.0-win2012-amd64.tgz'))

    def test_add_agent_with_bad_source_raises_error(self):
        args = FakeArgs(source_agent='juju-1.21.0-trusty-amd64.tgz')
        with self.assertRaises(ValueError):
            add_agents(args)
