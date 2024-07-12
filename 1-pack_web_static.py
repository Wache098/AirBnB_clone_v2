#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo.
"""
import os
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Creates a .tgz archive from web_static folder.

    Returns:
        Archive path if successfully created, None if failed.
    """
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        print(f"Error packing: {e}")
        return None
