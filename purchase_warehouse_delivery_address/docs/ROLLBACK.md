# Rollback Plan

The module adds one non-stored related field and two inherited UI/report extensions. It creates no independent transactional table and does not override receipt creation.

If a deployment problem occurs:

1. stop further changes;
2. inspect Odoo.sh logs;
3. revert the Git commit or deploy the last known-good revision;
4. rebuild;
5. uninstall the module if required after reviewing dependencies;
6. verify standard Purchase forms and reports.

Warehouse addresses remain standard Odoo data and are not removed by uninstalling this module.
