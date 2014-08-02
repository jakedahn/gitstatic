#!/usr/bin/env python 

import argparse
import os
import subprocess
import tempfile
import yaml


from git import *


def parse_args():
    ap = argparse.ArgumentParser(description='Build static sites gitstatic style')
    ap.add_argument('--git-url',
                    help='Which git url should we build?',
                    required=True)
    ap.add_argument('--git-ref',
                    help='Which branch or commit should we build?',
                    default='master')
    ap.add_argument('--web-root',
                    help='Where would you like the built assets to live?',
                    default='/var/www')
    args = ap.parse_args()
    return args


def main():
    args = parse_args()

    tmpdir = tempfile.mkdtemp('gitstatic-builder')
    tmpdir_build_path = '%s/gitstatic_build' % tmpdir
    gitstatic_path = '%s/.gitstatic.yml' % tmpdir

    repo = Repo.clone_from(args.git_url, tmpdir) # clone git repo
    # repo.remotes.origin.fetch() # fetch origin
    repo.git.checkout('origin/%s' % args.git_ref, b=args.git_ref) # reset to desired git ref
    if not os.path.isfile(gitstatic_path):
        import pdb; pdb.set_trace()
        raise SystemExit('Error: The repo you are trying to build does NOT '
                         'contain a .gitstatic.yml manifest file.')
    #FIXME(jake): the original builder.sh would grab submodules, we probably want this here too

    # parse gitstatic yml
    with open(gitstatic_path, 'r') as f:
        build_vars = yaml.load(f)

    cname = build_vars.get('cname')
    deploy_path = '%s/%s' % (args.web_root, cname)
    build_script = build_vars.get('build_command').split(' ')

    res = subprocess.call(build_script)

    if res != 0:
        raise SystemExit('Error: Something broke during build phase')

    rsync_cmd = 'rsync --recursive --update --delete --perms %s %s' % (tmpdir_build_path, deploy_path)
    rsync_res = subprocess.call(rsync_cmd.split(' '))

    if rsync_res != 0:
        raise SystemExit('Error: Something broke during rsync')

    print 'Success! %s has been built and is now hosted at %s from path %s' % (args.git_url, cname)


if __name__ == '__main__':
    main()
