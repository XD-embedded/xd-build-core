from xd.build.core.manifest import *
import os

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

parser_help = 'Show recipe specification'

def add_arguments(parser):
    parser.add_argument(
        'recipe',
        help='recipe (name or path) to show')
    return

def run(args, manifest, env):
    manifest = Manifest(manifest)
    recipe = manifest.get_recipe(args.recipe)
    if recipe is None:
        log.error('recipe not found: %s', args.recipe)
        return 1
    print('#%s# %s%s#'%(os.linesep, recipe.path, os.linesep))
    recipe.parse()
    recipe.dump()
    return
