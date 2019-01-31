import json
from guillotina import app_settings
from guillotina.db.interfaces import ICockroachStorage
from guillotina.db.interfaces import IPostgresStorage
from guillotina.transactions import get_transaction


def supports_ordering(storage):
    if not app_settings.get('store_json', False):
        return False
    return IPostgresStorage.providedBy(storage) and not ICockroachStorage.providedBy(storage)


async def get_next_order():
    txn = get_transaction()
    conn = await txn.get_connection()
    return await conn.fetchval("SELECT nextval('order_sequence');")


async def get_last_child_position(folder):
    txn = get_transaction()
    if not supports_ordering(txn.storage):
        return await folder.async_len()
    conn = await txn.get_connection()
    results = await conn.fetch('''select json from {}
WHERE parent_id = $1 AND of IS NULL
ORDER BY (json->>'position_in_parent')::int DESC
limit 1'''.format(txn.storage._objects_table_name), folder._p_oid)
    if len(results) > 0:
        item = json.loads(results[0]['json'])
        return item.get('position_in_parent', 0)
    return -1
