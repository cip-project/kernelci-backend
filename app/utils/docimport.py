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

import os
import pymongo

from models import (
    DB_NAME,
    DEFCONFIG_ACCEPTED_FILES,
    DefConfigDocument,
    JobDocument,
)

from utils.utc import utc
from datetime import datetime


BASE_PATH = '/var/www/images/kernel-ci'


def import_job_from_json(json_doc, db, base_path=BASE_PATH, callback=None):
    job_dir = json_doc['job']
    kernel_dir = json_doc['kernel']

    import_job(job_dir, kernel_dir, db, base_path)

    if callback:
        callback("DONE")


def import_job(job, kernel, db, base_path=BASE_PATH):
    job_dir = os.path.join(base_path, job, kernel)
    job_id = JobDocument.JOB_ID_FORMAT % (job, kernel)

    docs = []
    doc = JobDocument(job_id, job=job, kernel=kernel)
    doc.created = datetime.now(tz=utc).isoformat()

    docs.append(doc)

    if os.path.isdir(job_dir):
        docs.extend(traverse_defconf_dir(job_dir, job_id))

    save_documents(db, docs)


def traverse_defconf_dir(kernel_dir, job_id):
    defconf_docs = []
    for defconf_dir in os.listdir(kernel_dir):
        defconf_doc = DefConfigDocument(defconf_dir)
        defconf_doc.job_id = job_id

        for dirname, subdirs, files in os.walk(
                os.path.join(kernel_dir, defconf_dir)):
            # Consider only the actual directory and its files.
            subdirs[:] = []
            for key, val in DEFCONFIG_ACCEPTED_FILES.iteritems():
                if key in files:
                    setattr(defconf_doc, val, os.path.join(dirname, key))
        defconf_docs.append(defconf_doc)
    return defconf_docs


def import_all(base_path=BASE_PATH):

    docs = []

    for job_dir in os.listdir(base_path):
        job_id = job_dir
        job_dir = os.path.join(base_path, job_dir)

        for kernel_dir in os.listdir(job_dir):
            doc_id = JobDocument.JOB_ID_FORMAT % (job_id, kernel_dir)
            job_doc = JobDocument(doc_id, job=job_id, kernel=kernel_dir)
            job_doc.created = datetime.now(tz=utc).isoformat()
            docs.append(job_doc)

            kernel_dir = os.path.join(job_dir, kernel_dir)

            docs.extend(traverse_defconf_dir(kernel_dir, doc_id))

    return docs


def save_documents(db, documents):
    for document in documents:
        db[document.collection].save(document.to_dict())


if __name__ == '__main__':
    conn = pymongo.MongoClient()
    db = conn[DB_NAME]

    docs = import_all()
    save_documents(db, docs)

    conn.disconnect()
