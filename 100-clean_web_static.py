#!/usr/bin/python3
"""
Fabric script to automate the deployment and cleaning of archives
on web servers.
"""

from fabric.api import *
from datetime import datetime
from os.path import exists

env.hosts = ['35.237.166.125', '54.167.61.201']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns the path to the created archive on success, None on failure.
    """
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("tar -cvzf {} web_static".format(filename))
    if result.failed:
        return None
    return filename


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    Returns True if successful, False otherwise.
    """
    if not exists(archive_path):
        return False
    
    try:
        put(archive_path, "/tmp/")
        filename = archive_path.split('/')[-1]
        folder_name = "/data/web_static/releases/" + filename.split('.')[0]
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))
        run("rm /tmp/{}".format(filename))
        run("mv {}/web_static/* {}/".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_name))
        print("New version deployed successfully!")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False


def deploy():
    """
    Packs and deploys the web_static content to web servers.
    Calls do_pack() to create the archive and do_deploy() to deploy it.
    Returns True if deployment was successful, False otherwise.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    
    return do_deploy(archive_path)


def do_clean(number=0):
    """
    Deletes out-of-date archives.
    Keeps the most recent 'number' of archives.
    If number is 0 or 1, keep only the most recent version.
    """
    number = 1 if int(number) == 0 else int(number)

    # Local cleanup
    archives = sorted(local("ls -tr versions", capture=True).split())
    [archives.pop() for i in range(number)]
    for archive in archives:
        local("rm -f versions/{}".format(archive))

    # Remote cleanup
    with cd("/data/web_static/releases"):
        archives = sorted(run("ls -tr").split())
        archives = [archive for archive in archives if "web_static_" in archive]
        [archives.pop() for i in range(number)]
        for archive in archives:
            run("rm -rf {}".format(archive))
