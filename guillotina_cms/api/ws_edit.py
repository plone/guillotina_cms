from aiohttp import web
from diff_match_patch import diff_match_patch
from guillotina import app_settings
from guillotina import configure
from guillotina.browser import View
from guillotina.content import get_cached_factory
from guillotina.interfaces import IAsyncBehavior
from guillotina.transactions import get_tm
from guillotina.utils import resolve_dotted_name
from guillotina.interfaces import IResource
from guillotina_cms.interfaces import IPubSubUtility
from guillotina.component import get_utility

import aiohttp
import asyncio
import json
import logging

logger = logging.getLogger('guillotina_cms')

dmp = diff_match_patch()


@configure.service(
    context=IResource, method='GET',
    permission='guillotina.ModifyContent', name='@ws-edit',
    parameters=[{
        "name": "ws_token",
        "in": "query",
        "type": "string",
        "required": True
    }],
    summary='''This is a web socket using google's diff-match-patch algorithm.

Socket payload examples:

    {
        "t": "dmp",
        "f": "guillotina.behaviors.dublincore.IDublincore.title",
        "v": "@@ -1,6 +1,6 @@\n fo\n-o\n+b\n bar"
    }

    {
        "t": "pos",
        "v": {
        }
    }

    {
        "t": "save"
    }

    {
        "t": "load",
        "f": "guillotina.behaviors.dublincore.IDublincore.title"
    }

    {
        "t": "fdmp",
        "f": "guillotina.behaviors.dublincore.IDublincore.title",
        "v": "Hello foo bar"
    }

    {
        "t": "saved"
    }

Operators:

In this example, we use `t` and `v` to describe the payload.

  - "t": type of operation. `pos`: cursor position update
  - "f": only used along with dmp and fdump
  - "v": the value of the operation

Operator values:
  - dmp: diff-match-patch operation
  - fdmp: full dump of a field
  - load: get a field
  - pos: cursor position update
  - save: force saving
  - saved: document saved, reset timer

The only payload we handle is when `t=(dmp|fdmp|load|save|saved)`. Otherwise, everything is
passed along to the other subscribers without interpretation. So if you want to pass
along editor data in any other way, it would be fine.''',)
class WSEdit(View):
    auto_save_delay = 30
    auto_save_handle = None

    async def __call__(self):
        self.data = {}
        self.ws = web.WebSocketResponse()

        tm = get_tm(self.request)
        await tm.abort(self.request)

        try:
            await self.ws.prepare(self.request)
        except ConnectionResetError:
            return {}

        try:
            self.pubsub = get_utility(IPubSubUtility)
            self.channel_name = 'ws-field-edit-{}'.format(
                self.context._p_oid
            )

            # subscribe to redis channel for this context
            asyncio.ensure_future(
                self.pubsub.subscribe(self.channel_name, self.request.uid, self.subscriber_callback))

            self.configure_auto_save()

            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.text:
                    await self.handle_message(msg)
                elif msg.type == aiohttp.WSMsgType.error:
                    logger.debug('resource ws connection closed with exception {0:s}'
                                 .format(self.ws.exception()))
        except asyncio.CancelledError:
            logger.debug('browser closed')
            pass
        finally:
            try:
                await self.pubsub.unsubscribe(self.channel_name, self.request.uid)
                await self.ws.close()  # make sure to close socket
            except:
                pass

        logger.debug('websocket connection closed')

        return {}

    def auto_save_callback(self):
        asyncio.ensure_future(self.save())
        self.configure_auto_save()

    def configure_auto_save(self):
        if self.auto_save_handle is not None:
            self.auto_save_handle.cancel()
        loop = asyncio.get_event_loop()
        self.auto_save_handle = loop.call_later(self.auto_save_delay, self.auto_save_callback)

    async def subscriber_callback(self, data):
        if data['t'] == 'saved':
            # reset our auto save counter
            pass
        await self.ws.send_str(json.dumps(data))  # send along to user

    async def handle_message(self, msg):
        if msg.data == 'close':
            await self.ws.close()
        elif msg.data.lower() in ('ping', 'ping!'):
            pass
        else:
            try:
                data = json.loads(msg.data)
                operation = data['t']
            except:
                self.ws.send_str(json.dumps({
                    't': 'e',
                    'v': 'Not a valid payload'
                }))
                return

            if operation == 'dmp':
                try:
                    await self.apply_edit(data)
                except Exception:
                    await self.ws.send_str(json.dumps({
                        't': 'e',
                        'v': 'Error applying dmp'
                    }))
                    logger.warn('Error applying dmp', exc_info=True)
            elif operation == 'save':
                await self.save()
                self.ws.send_str(json.dumps({
                    't': 'saved'
                }))
                await self.pubsub.publish(
                    self.channel_name,
                    {
                        't': 'saved',
                        'ruid': self.request.uid
                    })
            elif operation == 'saved':
                # reset the counter, only one person needs to save it every 30 seconds
                self.configure_auto_save()
            else:
                # all other operations are just passed through.
                data['ruid'] = self.request.uid
                await self.pubsub.publish(self.channel_name, data)

    async def get_field(self, field_name):
        context = self.context
        if '.' in field_name:
            schema_klass, field_name = field_name.rsplit('.', 1)
            if schema_klass not in self.context.__behaviors__:
                self.ws.send_str(json.dumps({
                    't': 'e',
                    'v': 'Not a valid field on a behavior'
                }))
                return
            schema = resolve_dotted_name(schema_klass)
            if schema is None:
                self.ws.send_str(json.dumps({
                    't': 'e',
                    'v': 'Could not find specified schema'
                }))
                return
            behavior = schema(context)
            context = behavior
        else:
            factory = get_cached_factory(self.context.type_name)
            schema = factory.schema

        try:
            field = schema[field_name]
        except KeyError:
            self.ws.send_str(json.dumps({
                't': 'e',
                'v': 'Not a valid field on a behavior'
            }))
            return
        return context, field

    async def save(self):
        self.request._db_write_enabled = True
        tm = get_tm(self.request)
        txn = await tm.begin(self.request)

        for key, value in self.data.items():
            context, field = await self.get_field(key)
            if IAsyncBehavior.implementedBy(context.__class__):
                # it's a behavior we're editing...
                await context.load()
                await txn.refresh(context.data)
            else:
                await txn.refresh(context)

            setattr(context, field.__name__, value)
            if IAsyncBehavior.implementedBy(context.__class__):
                # it's a behavior we're editing...
                context.data._p_register()
            else:
                context._p_register()

        await tm.commit(txn=txn)

    async def get_value(self, field_name):
        self.request._db_write_enabled = False
        tm = get_tm(self.request)
        txn = await tm.begin(self.request)
        context, field = await self.get_field(field_name)
        if IAsyncBehavior.implementedBy(context.__class__):
            await context.load()
            await txn.refresh(context.data)
        else:
            await txn.refresh(context)
        val = getattr(context, field.__name__)
        await tm.abort(txn=txn)
        return val

    async def apply_edit(self, data):
        field_name = data['f']
        if field_name not in self.data:
            self.data[field_name] = await self.get_value(data['f'])
        value = self.data[field_name]

        dmp_value = data['v']
        value, results = dmp.patch_apply(dmp.patch_fromText(dmp_value), value)
        self.data[field_name] = value

        data['ruid'] = self.request.uid
        await self.pubsub.publish(self.channel_name, data)
