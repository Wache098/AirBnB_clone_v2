#!/usr/bin/python3

from fabric.api import *
from os.path import exists

env.hosts = ['35.237.166.125', '54.167.61.201']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers

    Args:
        archive_path (str): Path to the archive file to deploy

    Returns:
        bool: True if all operations were successful, False otherwise
    """
    if not exists(archive_path):
        return False

    try:
        filename = archive_path.split('/')[-1]
        archive_no_ext = filename.split('.')[0]

        remote_tmp = '/tmp/'
        remote_archive = remote_tmp + filename
        remote_folder = '/data/web_static/releases/' + archive_no_ext

        put(archive_path, remote_tmp)
        run('mkdir -p {}'.format(remote_folder))
        run('tar -xzf {} -C {}'.format(remote_archive, remote_folder))
        run('rm {}'.format(remote_archive))
        run('mv {}/web_static/* {}'.format(remote_folder, remote_folder))
        run('rm -rf {}/web_static'.format(remote_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(remote_folder))

        return True

    except Exception as e:
        print(e)
        return False
