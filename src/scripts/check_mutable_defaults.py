from __future__ import absolute_import, unicode_literals

import argparse
import ast
import sys
import traceback

mutable_types = [ast.Call, ast.Dict, ast.List, ast.Set]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="files to check")
    args = parser.parse_args(sys.argv[1:])
    retv = 0

    for file_name in args.filenames:
        try:
            ast_obj = ast.parse(open(file_name).read(), filename=file_name)
        except SyntaxError:
            print("{0} - Could not parse ast".format(file_name))
            print()
            print("\t" + traceback.format_exc().replace("\n", "\n\t"))
            print()
            retv = 1
            continue

        for main_node in ast_obj.body:
            for node in ast.walk(main_node):
                if isinstance(node, ast.FunctionDef):
                    for default in node.args.defaults:
                        if any(
                            [
                                isinstance(default, mutable_type)
                                for mutable_type in mutable_types
                            ]
                        ):
                            print(
                                "{}:{}:{} has mutable default arg of type {}".format(
                                    file_name,
                                    node.lineno,
                                    node.name,
                                    type(default).__name__,
                                )
                            )
                            retv = 1
    return retv


if __name__ == "__main__":
    sys.exit(main())
