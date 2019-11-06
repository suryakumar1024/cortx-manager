#!/usr/bin/env python3

"""
 ****************************************************************************
 Filename:          consul_storage.py
 _description:      Example of Elasticsearch usage

 Creation Date:     06/10/2019
 Author:            Dmitry Didenko

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""

import asyncio
from datetime import datetime
from time import sleep
import sys

if __name__ == "__main__":
    # Add "csm" module at top
    sys.path.append("../../../../..") # Adds higher directory to python modules path.

from csm.core.data.db.db_provider import (DataBaseProvider, GeneralConfig)
from csm.core.data.access.filters import Compare, And, Or
from csm.core.data.access import Query, SortOrder
from csm.core.blogic.models.alerts import AlertExample



ALERT1 = {'id': 22,
          'alert_uuid': 1,
          'status': "Success",
          'type': "Hardware",
          'enclosure_id': 1,
          'module_name': "SSPL",
          'description': "Some Description",
          'health': "Good",
          'health_recommendation': "Replace Disk",
          'location': "USA",
          'resolved': True,
          'acknowledged': True,
          'severity': 1,
          'state': "Unknown",
          'extended_info': "No",
          'module_type': "FAN",
          'updated_time': datetime.now(),
          'created_time': datetime.now()
          }

ALERT2 = {'id': 23,
          'alert_uuid': 2,
          'status': "Failed",
          'type': "Hardware",
          'enclosure_id': 1,
          'module_name': "SSPL",
          'description': "Some Description",
          'health': "Good",
          'health_recommendation': "Replace Disk",
          'location': "India",
          'resolved': False,
          'acknowledged': False,
          'severity': 1,
          'state': "Unknown",
          'extended_info': "No",
          'module_type': "FAN",
          'updated_time': datetime.now(),
          'created_time': datetime.now()
          }

ALERT3 = {'id': 24,
          'alert_uuid': 3,
          'status': "Failed",
          'type': "Software",
          'enclosure_id': 1,
          'module_name': "SSPL",
          'description': "Some Description",
          'health': "Bad",
          'health_recommendation': "Replace Disk",
          'location': "Russia",
          'resolved': True,
          'acknowledged': True,
          'severity': 1,
          'state': "Unknown",
          'extended_info': "No",
          'module_type': "FAN",
          'updated_time': datetime.now(),
          'created_time': datetime.now()
          }

ALERT4 = {'id': 25,
          'alert_uuid': 4,
          'status': "Success",
          'type': "Software",
          'enclosure_id': 1,
          'module_name': "SSPL",
          'description': "Some Description",
          'health': "Greate",
          'health_recommendation': "Replace Unity",
          'location': "Russia",
          'resolved': False,
          'acknowledged': False,
          'severity': 1,
          'state': "Unknown",
          'extended_info': "No",
          'module_type': "FAN",
          'updated_time': datetime.now(),
          'created_time': datetime.now()
          }


async def example():
    conf = GeneralConfig({
        "databases": {
            "es_db": {
                "import_path": "ElasticSearchDB",
                "config": {
                    "host": "localhost",
                    "port": 9200,
                    "login": "",
                    "password": ""
                }
            }
        },
        "models": [
            {
                "import_path": "csm.core.blogic.models.alerts.AlertExample",
                "database": "es_db",
                "config": {
                    "es_db":
                        {
                            "collection": "alert"
                        }
                }
            }]
    })

    db = DataBaseProvider(conf)

    alert1 = AlertExample(ALERT1)
    alert2 = AlertExample(ALERT2)
    alert3 = AlertExample(ALERT3)
    alert4 = AlertExample(ALERT4)

    await db(AlertExample).store(alert1)
    await db(AlertExample).store(alert2)
    await db(AlertExample).store(alert3)
    await db(AlertExample).store(alert4)

    filter = And(Compare(AlertExample.id, "=", 22),
                 And(Compare(AlertExample.status, "=", "Success"),
                     Compare(AlertExample.id, ">", 1)))

    query = Query().filter_by(filter).order_by(AlertExample.id, SortOrder.DESC)
    res = await db(AlertExample).get(query)
    print(f"Get by query: {[alert.to_primitive() for alert in res]}")

    to_update = {
        'type': "Software",
        'location': "Russia",
        'alert_uuid': 22,
        'resolved': False,
        'created_time': datetime.now()
    }

    await db(AlertExample).update(filter, to_update)

    res = await db(AlertExample).get(query)
    print(f"Get by query after update: {[alert.to_primitive() for alert in res]}")

    _id = 2
    res = await db(AlertExample).get_by_id(_id)
    if res is not None:
        print(f"Get by id = {_id}: {res.to_primitive()}")

    await db(AlertExample).update_by_id(_id, to_update)

    updated_id = to_update['alert_uuid']
    res = await db(AlertExample).get_by_id(updated_id)
    if res is not None:
        print(f"Get by id after update = {_id}: {res.to_primitive()}")

    filter_obj = Or(Compare(AlertExample.id, "=", 1), Compare(AlertExample.id, "=", 2),
                    Compare(AlertExample.id, "=", 22))
    res = await db(AlertExample).count(filter_obj)
    print(f"Count by filter: {res}")

    res = await db(AlertExample).delete(filter_obj)
    print(f"Deleted by filter: {res}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())
    loop.close()