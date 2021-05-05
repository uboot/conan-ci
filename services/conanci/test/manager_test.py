from conanci import database
from conanci.manager import Manager

import conanci.test.util as util
import os
import unittest

# Requires:
#
# 1. MySQL database
# docker run --rm -d --name mysql -p 3306:3306 -e MYSQL_DATABASE=conan-ci -e MYSQL_ROOT_PASSWORD=secret mysql:8.0.21


class ManagerTest(unittest.TestCase):
    def setUp(self):
        self.manager = Manager()
        database.reset_database()

    def test_process(self):
        build_output_file = os.path.join(os.path.dirname(__file__), "build_output.json")
        with open(build_output_file) as f:
            build_output = f.read()

        with database.session_scope() as session:
            build = util.create_build()
            session.add(build)
            session.commit()
            build_id = build.id

        self.manager.process(build_id, build_output)

        with database.session_scope() as session:
            build = session.query(database.Build).filter_by(id=build_id).first()
            self.assertIsNotNone(build.package)
            self.assertEqual(build.package.recipe.name, "hello")
