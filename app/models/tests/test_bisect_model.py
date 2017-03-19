# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import models.base as modb
import models.bisect as modbs


class TestBisectModel(unittest.TestCase):

    def test_bisect_base_document(self):
        bisect_doc = modbs.BisectDocument("foo")
        self.assertIsInstance(bisect_doc, modb.BaseDocument)

    def test_boot_bisect_document(self):
        bisect_doc = modbs.BootBisectDocument("bar")
        self.assertIsInstance(bisect_doc, modbs.BisectDocument)
        self.assertIsInstance(bisect_doc, modb.BaseDocument)

    def test_bisect_base_document_collection(self):
        bisect_doc = modbs.BisectDocument("foo")
        self.assertEqual(bisect_doc.collection, "bisect")

    def test_bisect_boot_document_collection(self):
        bisect_doc = modbs.BootBisectDocument("foo")
        self.assertEqual(bisect_doc.collection, "bisect")

    def test_bisect_base_from_json(self):
        bisect_doc = modbs.BisectDocument("foo")

        self.assertIsNone(bisect_doc.from_json({}))
        self.assertIsNone(bisect_doc.from_json([]))
        self.assertIsNone(bisect_doc.from_json(()))
        self.assertIsNone(bisect_doc.from_json(""))

    def test_bisect_base_to_dict(self):
        bisect_doc = modbs.BisectDocument("foo")

        expected = {
            "created_on": None,
            "job": None,
            "bisect_data": [],
            "compare_to": None,
            "good_commit": None,
            "good_commit_date": None,
            "good_commit_url": None,
            "bad_commit": None,
            "bad_commit_date": None,
            "bad_commit_url": None,
            "version": None,
            "job_id": None,
            "type": None
        }
        self.assertDictEqual(expected, bisect_doc.to_dict())

    def test_bisect_base_to_dict_with_id(self):
        bisect_doc = modbs.BisectDocument("foo")
        bisect_doc.id = "bar"

        expected = {
            "_id": "bar",
            "created_on": None,
            "job": None,
            "bisect_data": [],
            "compare_to": None,
            "good_commit": None,
            "good_commit_date": None,
            "good_commit_url": None,
            "bad_commit": None,
            "bad_commit_date": None,
            "bad_commit_url": None,
            "version": None,
            "job_id": None,
            "type": None
        }
        self.assertDictEqual(expected, bisect_doc.to_dict())

    def test_bisect_boot_to_dict(self):
        bisect_doc = modbs.BootBisectDocument("foo")
        bisect_doc.id = "bar"
        bisect_doc.board = "baz"
        bisect_doc.version = "1.0"
        bisect_doc.boot_id = "boot-id"
        bisect_doc.build_id = "build-id"
        bisect_doc.job_id = "job-id"

        expected = {
            "_id": "bar",
            "board": "baz",
            "created_on": None,
            "job": None,
            "bisect_data": [],
            "compare_to": None,
            "good_commit": None,
            "good_commit_date": None,
            "good_commit_url": None,
            "bad_commit": None,
            "bad_commit_date": None,
            "bad_commit_url": None,
            "version": "1.0",
            "boot_id": "boot-id",
            "build_id": "build-id",
            "job_id": "job-id",
            "type": "boot",
            "arch": None,
            "defconfig": None,
            "defconfig_full": None
        }
        self.assertDictEqual(expected, bisect_doc.to_dict())

    def test_bisect_base_properties(self):
        bisect_doc = modbs.BootBisectDocument("foo")
        bisect_doc.id = "bar"
        bisect_doc.created_on = "now"
        bisect_doc.job = "fooz"
        bisect_doc.bisect_data = [1, 2, 3]
        bisect_doc.good_commit = "1"
        bisect_doc.good_commit_date = "now"
        bisect_doc.good_commit_url = "url"
        bisect_doc.bad_commit = "2"
        bisect_doc.bad_commit_date = "now"
        bisect_doc.bad_commit_url = "url"

        self.assertEqual(bisect_doc.id, "bar")
        self.assertEqual(bisect_doc.created_on, "now")
        self.assertEqual(bisect_doc.job, "fooz")
        self.assertEqual(bisect_doc.bisect_data, [1, 2, 3])
        self.assertEqual(bisect_doc.good_commit, "1")
        self.assertEqual(bisect_doc.good_commit_date, "now")
        self.assertEqual(bisect_doc.good_commit_url, "url")
        self.assertEqual(bisect_doc.bad_commit, "2")
        self.assertEqual(bisect_doc.bad_commit_date, "now")
        self.assertEqual(bisect_doc.bad_commit_url, "url")

    def test_bisect_boot_properties(self):
        bisect_doc = modbs.BootBisectDocument("foo")
        bisect_doc.board = "bar"

        self.assertEqual(bisect_doc.board, "bar")

    def test_bisect_defconfig_to_dict(self):
        bisect_doc = modbs.DefconfigBisectDocument("foo")
        bisect_doc.id = "bar"
        bisect_doc.build_id = "build-id"
        bisect_doc.defconfig = "defconfig-name"
        bisect_doc.version = "1.0"
        bisect_doc.job = "job"
        bisect_doc.job_id = "job-id"
        bisect_doc.defconfig_full = "defconfig-full"
        bisect_doc.arch = "arm"

        expected = {
            "_id": "bar",
            "created_on": None,
            "job": "job",
            "bisect_data": [],
            "compare_to": None,
            "good_commit": None,
            "good_commit_date": None,
            "good_commit_url": None,
            "bad_commit": None,
            "bad_commit_date": None,
            "bad_commit_url": None,
            "version": "1.0",
            "build_id": "build-id",
            "defconfig": "defconfig-name",
            "job_id": "job-id",
            "defconfig_full": "defconfig-full",
            "arch": "arm",
            "type": "build",
            "git_branch": None
        }

        self.assertDictEqual(expected, bisect_doc.to_dict())
