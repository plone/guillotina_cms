import logging
import aioredis
from guillotina import app_settings
from guillotina_cms.interfaces import IPubSubUtility
from guillotina import configure
import ujson
import asyncio
from async_timeout import timeout


logger = logging.getLogger('guillotina_cms')


@configure.utility(provides=IPubSubUtility)
class PubSubUtility:

    def __init__(self, settings=None, loop=None):
        self.subscribers = {}
        self._loop = loop
        self.publisher = None
        self.conn = None
        self.tasks = {}

    async def initialize(self, app=None):
        settings = app_settings['redis']
        self.conn = await aioredis.create_redis(
            (settings['host'], settings['port']),
            timeout=10,
            loop=self._loop)
        self.publisher = await aioredis.create_redis(
            (settings['host'], settings['port']),
            timeout=10,
            loop=self._loop)

    async def finalize(self):
        for channel in self.tasks.values():
            if not channel.done():
                channel.cancel()
        await asyncio.sleep(0.1)
        if self.publisher is not None:
            # In case of tests without redis let finalize pass
            self.publisher.close()
        if self.conn is not None:
            # In case of tests without redis let finalize pass
            self.conn.close()

    async def real_subscribe(self, channel_name):
        channel, = await self.conn.subscribe(channel_name)
        try:
            while channel_name in self.subscribers:
                async with timeout(100):
                    while (await channel.wait_message()):
                        msg = await channel.get(encoding='utf-8')
                        data = ujson.loads(msg)
                        for req, callback in self.subscribers[channel_name].items():
                            if data.get('ruid') != req:
                                await callback(data)
        except asyncio.CancelledError as ex:
            await self.conn.unsubscribe(channel_name)
        except Exception as ex:
            logger.error(f'Problem with redis pubsub', exc_info=True)
        finally:
            try:
                await self.conn.unsubscribe(channel_name)
            except Exception:
                pass

    async def subscribe(self, channel_name, req_id, callback):
        if channel_name in self.subscribers:
            self.subscribers[channel_name][req_id] = callback
        else:
            self.subscribers[channel_name] = {
                req_id: callback
            }
            task = asyncio.ensure_future(
                self.real_subscribe(channel_name))
            self.tasks[channel_name] = task

    async def unsubscribe(self, channel_name, req_id):
        self.tasks.remove(asyncio.current_task())
        del self.subscribers[self.channel_name][req_id]
        if len(self.subscribers[self.channel_name]) == 0:
            await self.conn.unsubscribe(self.channel_name)
            del self.subscribers[self.channel_name]

            if not self.tasks[channel_name].done():
                self.tasks[channel_name].cancel()
            del self.tasks[channel_name]

    async def publish(self, channel_name, data):
        await self.publisher.publish(channel_name, ujson.dumps(data))
