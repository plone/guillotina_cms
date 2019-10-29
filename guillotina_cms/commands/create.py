from guillotina.commands import Command
from guillotina.component import get_utility
from guillotina.interfaces import IApplication
from guillotina.interfaces import IDatabase
from guillotina import task_vars
from guillotina import addons
from guillotina.transactions import transaction
from guillotina.content import create_content_in_container
from guillotina.exceptions import ConflictIdOnContainer


class CMSCreateCommand(Command):
    description = "Guillotina cms db initiliazation"

    def get_parser(self):
        parser = super(CMSCreateCommand, self).get_parser()
        parser.add_argument("-d", "--db", help="Database", required=True)
        parser.add_argument("-n", "--name", help="CMS container id", required=True)
        parser.add_argument(
            "-t", "--type", help="CMS conetnt type", default="Container", required=False
        )
        return parser

    async def create(self, arguments, db):
        async with transaction(db=db) as txn:
            tm = task_vars.tm.get()
            root = await tm.get_root(txn=txn)
            obj = await create_content_in_container(
                root, arguments.type, arguments.name, check_security=False
            )

            await addons.install(obj, "cms")
            await addons.install(obj, "dbusers")

    async def run(self, arguments, settings, app):
        root = get_utility(IApplication, name="root")
        if arguments.db in root:
            db = root[arguments.db]
            if IDatabase.providedBy(db):
                print(f"Creating container: {arguments.name}")
                await self.create(arguments, db)
