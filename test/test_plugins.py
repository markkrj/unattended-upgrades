#!/usr/bin/python3

import json
import os
import shutil


import unattended_upgrade
from test.test_base import TestBase, MockOptions


class TestPlugins(TestBase):

    def setUp(self):
        TestBase.setUp(self)
        # XXX: copy/clean to root.plugins
        self.rootdir = self.make_fake_aptroot(
            template=os.path.join(self.testdir, "root.unused-deps"),
            fake_pkgs=[("test-package", "1.0", {})],
        )
        # create a fake plugin dir, our fake plugin just writes a json
        # dump of it's args
        fake_plugin_dir = os.path.join(self.tempdir, "plugins")
        os.makedirs(fake_plugin_dir, 0o755)
        example_plugin = os.path.join(
            os.path.dirname(__file__), "../examples/plugins/simple.py")
        shutil.copy(example_plugin, fake_plugin_dir)
        os.environ["UNATTENDED_UPGRADES_PLUGIN_PATH"] = fake_plugin_dir
        self.addCleanup(lambda: os.environ.pop("UNATTENDED_UPGRADES_PLUGIN_PATH"))
        # go to a tempdir as the simple.py plugin above will just write a
        # file into cwd
        os.chdir(self.tempdir)

    def test_plugin_happy(self):
        options = MockOptions()
        options.debug = False
        unattended_upgrade.main(options, rootdir=self.rootdir)
        with open("simple-example-postrun-res.json") as fp:
            arg1 = json.load(fp)
        # the log text needs extra processing
        log_dpkg = arg1.pop("log_dpkg")
        log_uu = arg1.pop("log_uu")
        # XXX: add test for pkgs_removed
        self.assertEqual(arg1, {
            "plugin_api": 1,
            "success": True,
            "result_str": "All upgrades installed",
            "pkgs_upgraded": ["test-package"],
            "pkgs_kept": [
                {"origin": "Ubuntu lucid-security", "package": "test-package"},
            ],
            "pkgs_removed": [],
        })
        self.assertTrue(log_dpkg.startswith("Log started:"))
        self.assertTrue(log_uu.startswith("Starting unattended upgrades script"))
        self.assertIn("Packages that will be upgraded: test-package", log_uu)
