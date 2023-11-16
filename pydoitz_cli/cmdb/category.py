import click
import pydoitz
from pydoitz.settings import CategoryConfig


COMMON_CATEGORY_OPTIONS = [
    click.Option(["--objects"]),
    click.Option(["--entries"]),
]


def _get_conf(ctx):
    if not ctx.obj.category_config:
        conf = CategoryConfig(host=ctx.obj.api.host)
        ctx.obj.category_config = conf

    cg = ctx.obj.category_config
    return cg


class CategorySaveCLI(click.MultiCommand):

    @staticmethod
    @click.pass_context
    def save(ctx, objects, entries, **kwargs):
        cat = ctx.obj.category_config.get_by_cli(ctx.info_name).name
        ret = ctx.obj.api.cmdb.category.save(
            object_ids=objects.split(","),
            entry_id=entries,
            category=cat,
            attributes=[kwargs]
        )

    def _create_save_cmd(self, ctx, name, cli_name, fields):
        options = list(COMMON_CATEGORY_OPTIONS)
        for key, data in fields.items():
            param = data["param"]
            opt = click.Option([f"--{param}"])
            options.append(opt)

        cmd = click.Command(name=cli_name,
                            callback=CategorySaveCLI.save,
                            params=options,
                            no_args_is_help=True
        )
        return cmd

    def _get_command_list(self, ctx):
        cmds = []
        category_config = _get_conf(ctx)

        for entry in category_config.entries.values():
            cmds.append(self._create_save_cmd(
                ctx,
                entry.name,
                entry.cli_name,
                entry.fields
            ))
        return cmds

    def list_commands(self, ctx):
        cmds = []
        for cmd in self._get_command_list(ctx):
            cmds.append(cmd.name)
        return cmds

    def get_command(self, ctx, name):
        category_config = _get_conf(ctx)
        entry = category_config.get_by_cli(name)
        if not entry:
            return None

        return self._create_save_cmd(
            ctx,
            entry.name,
            entry.cli_name,
            entry.fields
        )


@click.group()
@click.pass_context
def category(ctx):
    pass


@category.command()
@click.pass_context
def delete(ctx, objects, categories, entries):
    ret = ctx.api.cmdb.category.delete(
        object_ids=objects.split(","),
        entry_id=entries,
        category=ctx.obj.get("name"),
    )


@category.command()
@click.pass_context
def read(ctx, objects, categories):
    ret = ctx.api.cmdb.category.read(
        object_ids=objects.split(","),
        categories=categories.split(","),
    )


@category.command(
        cls=CategorySaveCLI,
        help="Create or save category entries"
)
@click.pass_context
def save(ctx):
    pass
