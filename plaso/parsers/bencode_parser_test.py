#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 The Plaso Project Authors.
# Please see the AUTHORS file for details on individual authors.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for Bencode file parser."""

import unittest

# pylint: disable=unused-import
from plaso.formatters import bencode_parser as bencode_formatter
from plaso.lib import event
from plaso.lib import eventdata
from plaso.lib import timelib_test
from plaso.parsers import bencode_parser
from plaso.parsers import test_lib


class BencodeTest(test_lib.ParserTestCase):
  """Tests for Bencode file parser."""

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    self.pre_obj = event.PreprocessObject()
    self._parser = bencode_parser.BencodeParser(self.pre_obj)

  # TODO: Move this to bencode_plugins/tranmission_test.py
  def testTransmissionPlugin(self):
    """Read Transmission activity files and make few tests."""
    test_file = self._GetTestFilePath(['bencode_transmission'])
    event_generator = self._ParseFile(self._parser, test_file)
    event_objects = self._GetEventObjects(event_generator)

    self.assertEqual(len(event_objects), 3)

    event_object = event_objects[0]

    destination_expected = u'/Users/brian/Downloads'
    self.assertEqual(event_object.destination, destination_expected)

    self.assertEqual(event_object.seedtime, 4)

    description_expected = eventdata.EventTimestamp.ADDED_TIME
    self.assertEqual(event_object.timestamp_desc, description_expected)

    expected_timestamp = timelib_test.CopyStringToTimestamp(
        '2013-11-08 15:31:20')
    self.assertEqual(event_object.timestamp, expected_timestamp)

    # Test on second event of first torrent.
    event_object = event_objects[1]
    self.assertEqual(event_object.destination, destination_expected)
    self.assertEqual(event_object.seedtime, 4)

    description_expected = eventdata.EventTimestamp.FILE_DOWNLOADED
    self.assertEqual(event_object.timestamp_desc, description_expected)

    expected_timestamp = timelib_test.CopyStringToTimestamp(
        '2013-11-08 18:24:24')
    self.assertEqual(event_object.timestamp, expected_timestamp)

  def testUTorrentPlugin(self):
    """Parse a uTorrent resume.dat file and make a few tests."""
    test_file = self._GetTestFilePath(['bencode_utorrent'])
    event_generator = self._ParseFile(self._parser, test_file)
    event_objects = self._GetEventObjects(event_generator)

    self.assertEqual(len(event_objects), 4)

    caption_expected = u'plaso test'
    path_expected = u'e:\\torrent\\files\\plaso test'

    # First test on when the torrent was added to the client.
    event_object = event_objects[3]

    self.assertEqual(event_object.caption, caption_expected)

    self.assertEqual(event_object.path, path_expected)

    self.assertEqual(event_object.seedtime, 511)

    description_expected = eventdata.EventTimestamp.ADDED_TIME
    self.assertEqual(event_object.timestamp_desc, description_expected)

    expected_timestamp = timelib_test.CopyStringToTimestamp(
        '2013-08-03 14:52:12')
    self.assertEqual(event_object.timestamp, expected_timestamp)

    # Second test on when the torrent file was completely downloaded.
    event_object = event_objects[2]

    self.assertEqual(event_object.caption, caption_expected)
    self.assertEqual(event_object.path, path_expected)
    self.assertEqual(event_object.seedtime, 511)

    description_expected = eventdata.EventTimestamp.FILE_DOWNLOADED
    self.assertEqual(event_object.timestamp_desc, description_expected)

    expected_timestamp = timelib_test.CopyStringToTimestamp(
        '2013-08-03 18:11:35')
    self.assertEqual(event_object.timestamp, expected_timestamp)

    # Third test on when the torrent was first modified.
    event_object = event_objects[0]

    self.assertEqual(event_object.caption, caption_expected)
    self.assertEqual(event_object.path, path_expected)
    self.assertEqual(event_object.seedtime, 511)

    description_expected = eventdata.EventTimestamp.MODIFICATION_TIME
    self.assertEqual(event_object.timestamp_desc, description_expected)

    expected_timestamp = timelib_test.CopyStringToTimestamp(
        '2013-08-03 18:11:34')
    self.assertEqual(event_object.timestamp, expected_timestamp)

    # Fourth test on when the torrent was again modified.
    event_object = event_objects[1]

    self.assertEqual(event_object.caption, caption_expected)
    self.assertEqual(event_object.path, path_expected)
    self.assertEqual(event_object.seedtime, 511)

    description_expected = eventdata.EventTimestamp.MODIFICATION_TIME
    self.assertEqual(event_object.timestamp_desc, description_expected)

    expected_timestamp = timelib_test.CopyStringToTimestamp(
        '2013-08-03 16:27:59')
    self.assertEqual(event_object.timestamp, expected_timestamp)


if __name__ == '__main__':
  unittest.main()
