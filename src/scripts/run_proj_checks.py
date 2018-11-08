import os
import sys
import collections


def check_migrations():
    import django

    django.setup()

    from django.apps import apps
    from django.db.migrations.autodetector import MigrationAutodetector
    from django.db.migrations.executor import MigrationExecutor
    from django.db.migrations.state import ProjectState

    executor = MigrationExecutor(connection=None)
    conflicts = executor.loader.detect_conflicts()
    if conflicts:
        name_str = "; ".join(
            "%s in %s" % (", ".join(names), app) for app, names in conflicts.items()
        )
        sys.stdout.write(
            "Conflicting migrations detected; multiple leaf nodes in the "
            "migration graph: (%s).\nTo fix them run "
            "'python manage.py makemigrations --merge'" % name_str
        )
        return conflicts

    autodetector = MigrationAutodetector(
        executor.loader.project_state(), ProjectState.from_apps(apps)
    )
    changes = autodetector.changes(graph=executor.loader.graph)
    if changes:
        sys.stdout.write(
            "Your models have changes that are not yet reflected " "in a migration."
        )
        return changes


def check_mutable_defaults():
    from django.apps import apps

    mutables = (
        collections.MutableMapping,
        collections.MutableSequence,
        collections.MutableSet,
    )
    mutable_fields = []
    for m in apps.get_models(True, True):
        for f in m._meta.get_fields(include_hidden=True):
            if hasattr(f, "get_default"):
                default = f.get_default()
                if isinstance(default, mutables):
                    if id(default) == id(f.get_default()):
                        mutable_fields.append(str(f))
    if mutable_fields:
        sys.stdout.write(
            "You have field defaults referencing same object.\n"
            "Fix it by having a callable as default."
        )
        return mutable_fields


def check_arrayfields():
    """
    Defining ArrayField using existing field will give strange errors
    during tests.
    This check is until we figure out the actual bug or
    able to reproduce the bug consistently.
    """
    from django.apps import apps
    from django.contrib.postgres.fields import ArrayField

    culprits = []
    for m in apps.get_models(True, True):
        fields = m._meta.get_fields(include_hidden=True)
        for f in fields:
            if not isinstance(f, ArrayField):
                continue

            if f.base_field in fields:
                culprits.append(str(f))

    if culprits:
        sys.stdout.write("Do not use an existing field to define ArrayField.\n")
        return culprits


def run_system_checks():
    from django.core.management import execute_from_command_line
    from django.core.management.base import SystemCheckError

    try:
        execute_from_command_line(["manage.py", "check"])
    except SystemCheckError as e:
        return str(e)


def main():
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # setdefault will break. trust me.
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
    return (
        check_migrations()
        or check_mutable_defaults()
        or check_arrayfields()
        or run_system_checks()
    )


if __name__ == "__main__":
    sys.exit(main())
