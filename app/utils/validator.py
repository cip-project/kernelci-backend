# Copyright (C) 2014 Linaro Ltd.
#
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


def valid_job_json_put(json_doc):
    is_valid = False
    keys = json_doc.keys()

    if 'job' in keys and 'kernel' in keys:
        is_valid |= True

    return is_valid


def valid_subscription_json_put(json_doc):
    is_valid = False
    keys = json_dod.keys()
    return is_valid
