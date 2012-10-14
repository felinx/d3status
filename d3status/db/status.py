# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#

from d3status.db import Model


class StatusModel(Model):
    def get_status(self):
        status = {"status": {"items": []}}
        items = status["status"]["items"]
        categorys = {}

        rows = self.db.query("select * from status")
        for row in rows:
            categorys.setdefault(row.category, {})[row.service] = row.status

        for category, services in categorys.iteritems():
            items.append({"category": category,
                          "services": services})

        if rows:
            status["count"] = len(items)
            return status
        else:
            return {}

    def update_status(self, status):
        changed_status = {}

        old_status = self.get_status()
        old_status_ = {}
        if old_status:
            for item in old_status["status"]["items"]:
                old_status_[item["category"]] = item["services"]

        for category, services in status.iteritems():
            for name, st in services.iteritems():
                old_st = old_status_[category].get(name, None)
                if old_st is not None and old_st != st:
                    changed_status.setdefault(category, {})[name] = st
                self._update_status(category, name, st)

        return changed_status

    def _update_status(self, category, server_name, status):
        row = self.db.get("select * from status where category=%s and service=%s",
                          category, server_name)
        if not row:
            self.db.execute("insert into status (category, service, status) "
                            "values (%s, %s, %s)",
                            category, server_name, status)
        else:
            self.db.execute("update status set status=%s where id=%s",
                            status, row.id)
