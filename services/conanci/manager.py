import json

from conanci import database


def _process_recipe(recipe_data: dict) -> database.Recipe:
    recipe = database.Recipe()
    recipe.name = recipe_data["name"]
    return recipe


def _process_package(package_data: dict) -> database.Package:
    package = database.Package()
    package.package_id = package_data["id"]
    return package


class Manager(object):
    def process(self, build_id, build_output):
        data = json.loads(build_output)
        with database.session_scope() as session:
            build = session.query(database.Build).filter_by(id=build_id).first()
            for recipe_compound in data["installed"]:
                recipe_data = recipe_compound["recipe"]
                recipe = _process_recipe(recipe_data)
                for package_data in recipe_compound["packages"]:
                    package = _process_package(package_data)
                    package.recipe = recipe
                    if not recipe_data["dependency"]:
                        build.package = package
                session.add(recipe)
