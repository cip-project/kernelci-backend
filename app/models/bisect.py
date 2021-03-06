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

"""Bisect mongodb document models."""

import models
import models.base as modb


class BisectDocument(modb.BaseDocument):
    """The bisect document model class."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=invalid-name
    def __init__(self, name):
        self._created_on = None
        self._id = None
        self._version = None

        self.bad_commit = None
        self.bad_commit_date = None
        self.bad_commit_url = None
        self.bisect_data = []
        self.compare_to = None
        self.good_commit = None
        self.good_commit_date = None
        self.good_commit_url = None
        self.job = None
        self.job_id = None
        self.type = None

    @property
    def collection(self):
        """The name of this document collection.

        Where document of this kind will be stored.
        """
        return models.BISECT_COLLECTION

    @property
    def id(self):
        """The ID of this object as returned by mongodb."""
        return self._id

    @id.setter
    def id(self, value):
        """Set the ID of this object with the ObjectID from mongodb.

        :param value: The ID of this object.
        :type value: str
        """
        self._id = value

    @property
    def created_on(self):
        """When this lab object was created."""
        return self._created_on

    @created_on.setter
    def created_on(self, value):
        """Set the creation date of this lab object.

        :param value: The lab creation date, in UTC time zone.
        :type value: datetime
        """
        self._created_on = value

    @property
    def version(self):
        """The schema version of this object."""
        return self._version

    @version.setter
    def version(self, value):
        """Set the schema version of this object.

        :param value: The schema string.
        :type param: str
        """
        self._version = value

    def to_dict(self):
        bisect_dict = {
            models.BISECT_BAD_COMMIT_DATE: self.bad_commit_date,
            models.BISECT_BAD_COMMIT_KEY: self.bad_commit,
            models.BISECT_BAD_COMMIT_URL: self.bad_commit_url,
            models.BISECT_DATA_KEY: self.bisect_data,
            models.BISECT_GOOD_COMMIT_DATE: self.good_commit_date,
            models.BISECT_GOOD_COMMIT_KEY: self.good_commit,
            models.BISECT_GOOD_COMMIT_URL: self.good_commit_url,
            models.COMPARE_TO_KEY: self.compare_to,
            models.CREATED_KEY: self.created_on,
            models.JOB_ID_KEY: self.job_id,
            models.JOB_KEY: self.job,
            models.TYPE_KEY: self.type,
            models.VERSION_KEY: self.version
        }

        if self.id:
            bisect_dict[models.ID_KEY] = self.id

        return bisect_dict

    @staticmethod
    def from_json(json_obj):
        return None


class BootBisectDocument(BisectDocument):
    """The bisect document class for boot bisection."""

    def __init__(self, name):
        super(BootBisectDocument, self).__init__(name)

        self.arch = None
        self.board = None
        self.boot_id = None
        self.build_id = None
        self.defconfig = None
        self.defconfig_full = None
        self.type = "boot"

    def to_dict(self):
        boot_b_dict = super(BootBisectDocument, self).to_dict()
        boot_b_dict[models.ARCHITECTURE_KEY] = self.arch
        boot_b_dict[models.BOARD_KEY] = self.board
        boot_b_dict[models.BOOT_ID_KEY] = self.boot_id
        boot_b_dict[models.BUILD_ID_KEY] = self.build_id
        boot_b_dict[models.DEFCONFIG_FULL_KEY] = self.defconfig_full
        boot_b_dict[models.DEFCONFIG_KEY] = self.defconfig
        return boot_b_dict


class DefconfigBisectDocument(BisectDocument):
    """The bisect document class for build bisection."""

    def __init__(self, name):
        super(DefconfigBisectDocument, self).__init__(name)

        self.arch = None
        self.build_id = None
        self.defconfig = None
        self.defconfig_full = None
        self.git_branch = None
        self.type = "build"

    def to_dict(self):
        def_b_dict = super(DefconfigBisectDocument, self).to_dict()
        def_b_dict[models.ARCHITECTURE_KEY] = self.arch
        def_b_dict[models.BUILD_ID_KEY] = self.build_id
        def_b_dict[models.DEFCONFIG_FULL_KEY] = self.defconfig_full
        def_b_dict[models.DEFCONFIG_KEY] = self.defconfig
        def_b_dict[models.GIT_BRANCH_KEY] = self.git_branch

        return def_b_dict
