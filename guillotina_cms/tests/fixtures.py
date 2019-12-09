import json

import pytest
from guillotina import testing
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager


def base_settings_configurator(settings):
    if "applications" in settings:
        settings["applications"].append("guillotina_cms")
    else:
        settings["applications"] = ["guillotina_cms"]


testing.configure_with(base_settings_configurator)


class CMSRequester(ContainerRequesterAsyncContextManager):
    async def __aenter__(self):
        await super().__aenter__()
        await self.requester("POST", "/db/guillotina/@addons", data=json.dumps({"id": "cms"}))
        return self.requester


@pytest.fixture(scope="function")
async def cms_requester(guillotina):
    yield CMSRequester(guillotina)
