import json


class ExamplePlugin:
    # Note that each plugin must have a "uu_plugin" attribute
    uu_plugin = "Example plugin for unattended-upgrades"

    def postrun(self, res):
        """
        The postrun function is run after a unattended-upgrades run
        that generated some result. The result is a dict that is
        kept backward compatible.
        """
        # The data in result is a simple python dict that can easily
        # be serialized to json. It contains information like what
        # packages got upgraded, removed and kept back. Also the
        # full u-u log and the dpkg log (if any).
        #
        # Here an example that serialized the data as json to a file
        with open("simple-example-postrun-res.json", "w") as fp:
            json.dump(res, fp)
