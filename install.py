# installer for Arduino Weather Station driver
# Copyright 2017 Alec Bennett
# Distributed under the terms of the GNU Public License (GPLv3)

from setup import ExtensionInstaller

def loader():
    return AWSInstaller()

class MeteostickInstaller(ExtensionInstaller):
    def __init__(self):
        super(AWSInstaller, self).__init__(
            version="0.1",
            name='aws',
            description='Collect data from an Arduino connected to a Davis anemometer',
            author="Alec Bennett",
            author_email="wrybread@gmail.com",
            files=[('bin/user', ['bin/user/aws.py'])]
            )
