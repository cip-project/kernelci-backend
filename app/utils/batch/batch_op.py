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

"""Batch operation classes."""

import handlers.common as hcommon
import handlers.count as hcount
import models
import utils.db


class BatchOperation(object):
    """The base batch operation that can be performed.

    Specialized operations, for count or other collections, should be created
    starting from this class.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        """Create a new `BatchOperation`."""
        self._operation = None
        self._query_args_func = None
        self._database = None
        self.args = []
        self.db_options = None
        self.collection = None
        self.document_id = None
        self.kwargs = {}
        self.limit = None
        self.method = None
        self.operation_id = None
        self.query = None
        self.query_args = {}
        self.skip = None
        self.valid_keys = None

    @property
    def operation(self):
        """Get the (real) operation associated with this batch op.

        It should be a function that will be called when invoking `run()` and
        it should accept `*args` and `**kwargs` parameters.
        """
        return self._operation

    @operation.setter
    def operation(self, value):
        """Set the operation to be performed when invoking `run()`.

        :param value: The operation to set.
        :type value: function
        """
        self._operation = value

    @property
    def query_args_func(self):
        """The function to retrieve the query arguments.

        :return A function.
        """
        if not self._query_args_func:
            self._query_args_func = self.query_args.get
        return self._query_args_func

    @property
    def database(self):
        """The database connection.

        :return A database connection.
        """
        if not self._database:
            self._database = utils.db.get_db_connection(self.db_options)
        return self._database

    def prepare_operation(self):
        """Prepare the operation that needs to be performed.

        This method is automatically called when invoking `run()` to make sure
        all necessary parameters are set up correctly.

        Subclasses should not override this method, but instead override the
        private ones specialized for each HTTP verbs.
        """
        if self.method == "GET":
            self._prepare_get_operation()
        elif self.method == "DELETE":
            self._prepare_delete_operation()
        elif self.method == "POST":
            self._prepare_post_operation()

    def _prepare_get_operation(self):
        """Prepare the necessary parameters for a GET operation."""
        if self.document_id:
            # Get only one document.
            self.operation = utils.db.find_one
            self.args = [
                self.database[self.collection],
                self.document_id
            ]
            self.kwargs = {
                "fields": hcommon.get_query_fields(self.query_args_func)
            }
        else:
            # Get the spec and perform the query, can perform an aggregation
            # as well.
            spec, sort, fields, self.skip, self.limit, unique = \
                hcommon.get_all_query_values(
                    self.query_args_func, self.valid_keys.get(self.method)
                )

            if unique:
                # Perform an aggregate
                self.operation = utils.db.aggregate
                self.args = [
                    self.database[self.collection],
                    unique
                ]
                self.kwargs = {
                    "sort": sort,
                    "fields": fields,
                    "match": spec,
                    "limit": self.limit
                }
            else:
                self.operation = utils.db.find_and_count
                self.args = [
                    self.database[self.collection],
                    self.limit,
                    self.skip,
                ]
                self.kwargs = {
                    "spec": spec,
                    "fields": fields,
                    "sort": sort
                }

    def _prepare_post_operation(self):
        """Prepare the necessary parameters for a POST operation."""
        raise NotImplementedError

    def _prepare_delete_operation(self):
        """Prepare the necessary parameters for a DELETE operation."""
        raise NotImplementedError

    def _prepare_response(self, result):
        """Prepare the response to be returned.

        :param result: The result obtained after invoking the `operation`.
        :return A dictionary
        """
        response = {}
        if self.operation_id:
            response[models.OP_ID_KEY] = self.operation_id

        # find_and_count returns 2 results: the mongodb cursor and the
        # results count.
        if isinstance(result, tuple):
            count = result[1]
            res = []
            if count > 0:
                res = [r for r in result[0]]

            json_obj = {
                models.RESULT_KEY: res,
                models.COUNT_KEY: count}

            if self.limit is not None:
                json_obj[models.LIMIT_KEY] = self.limit

            response[models.RESULT_KEY] = [json_obj]
        else:
            response[models.RESULT_KEY] = result

        return response

    def run(self):
        """Prepare and run this operation.

        This method will invoke the `operation` attribute as a function,
        passing the defined `args` and `kwargs` parameters.
        """
        self.prepare_operation()

        result = self.operation(*self.args, **self.kwargs)
        return self._prepare_response(result)


class BatchBootOperation(BatchOperation):
    """A batch operation for the `boot` collection."""

    def __init__(self):
        super(BatchBootOperation, self).__init__()
        self.valid_keys = models.BOOT_VALID_KEYS


class BatchJobOperation(BatchOperation):
    """A batch operation for the `job` collection."""

    def __init__(self):
        super(BatchJobOperation, self).__init__()
        self.valid_keys = models.JOB_VALID_KEYS


class BatchBuildOperation(BatchOperation):
    """A batch operation for the `build` collection."""

    def __init__(self):
        super(BatchBuildOperation, self).__init__()
        self.valid_keys = models.BUILD_VALID_KEYS


class BatchCountOperation(BatchOperation):
    """A batch operation for the `count` collection."""

    def __init__(self, ):
        super(BatchCountOperation, self).__init__()
        self.valid_keys = models.COUNT_VALID_KEYS

    def _prepare_get_operation(self):
        if self.document_id:
            self.operation = hcount.count_one_collection
            # We use document_id here with the database since we need to count
            # on a different collection.
            self.args = [
                self.database[self.document_id],
                self.document_id,
                self.query_args_func,
                self.valid_keys.get(self.method)
            ]
        else:
            self.operation = hcount.count_all_collections
            self.args = [
                self.database,
                self.query_args_func,
                self.valid_keys.get(self.method)
            ]
