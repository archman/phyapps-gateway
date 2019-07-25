# -*- coding: utf-8 -*-

import os
from datetime import datetime
import pytz
import tzlocal
from flask import request
from yapf.yapflib.yapf_api import FormatCode

import docker
client = docker.from_env()

# container image names mapping:
cname_map = {
        'phyapps:va': 'tonyzhang/phyapps:va',
        'phyapps:nb': 'tonyzhang/phyapps:nb',
}

# accelerator section names mapping:
VA_MACH = "FRIB_VA"
subm_map = {
        'LEBT': 'LEBT',
        'MEBT': 'MEBT',
        'LINAC': 'LS1FS1',
}

# initla port number:
NB_PORT, SS_PORT = 31000, 32000

# default mount data directory
if 'DPATH' in os.environ:
    DPATH_DEFAULT = os.environ['DPATH']
else:
    DPATH_DEFAULT = os.path.abspath(os.path.curdir)


def utc2local(u_time):
    utc_now = u_time.replace(tzinfo=pytz.utc)
    try:
        l_tz = tzlocal.get_localzone()
        l_time = utc_now.astimezone(l_tz)
    except pytz.UnknownTimeZoneError:
        l_time = utc_now.astimezone()
    return l_time.strftime("%Y-%m-%d %H:%M:%S %Z")


def to_dict(d):
    ret = {}
    for k,v in d.items():
        try:
            ret[k] = float(v)
        except:
            ret[k] = v
    return ret


def get_container_status(cid):
    try:
        return client.containers.get(cid).status
    except:
        return "Unknown"


def get_container_name(cid):
    try:
        return client.containers.get(cid).name
    except:
        return "Unknown"


def get_container_image(cid):
    try:
        return client.containers.get(cid).image
    except:
        return "Unknown"


def get_container_ports(cid):
    try:
        c = client.containers.get(cid)
        ps = c.attrs['NetworkSettings']['Ports']
        return [v[0]['HostPort'] for k,v in ps.items()]
    except:
        return None


def get_container_ctime(cid):
    try:
        c = client.containers.get(cid)
        t0 = c.attrs['Created']
        t0_obj = datetime.strptime(t0[0:-4], '%Y-%m-%dT%H:%M:%S.%f')
        return utc2local(t0_obj)
    except:
        return 'Unknown'


def get_container_uptime(cid):
    try:
        c = client.containers.get(cid)
        time0 = c.attrs['Created']
        t0 = datetime.strptime(time0[0:-4], '%Y-%m-%dT%H:%M:%S.%f')
        t1 = datetime.utcnow()
        return str(t1-t0)
    except:
        return 'Unknown'


def get_container_shortid(cid):
    try:
        return client.containers.get(cid).short_id
    except:
        return  'Unknown'

def get_container_mach(cid):
    """ Returm machine name, only works for phyapps image.
    """
    try:
        c = client.containers.get(cid)
        args = c.attrs['Args']
        return args[args.index('--mach') + 1]
    except:
        return 'Unknown'


def get_container_url(cid, port=8888):
    """ Return server urls.
    """
    try:
        c = client.containers.get(cid)
        ps = c.attrs['NetworkSettings']['Ports']
        all_urls = {
                k: 'http://{0}:{1}'.format(
                    v[0]['HostIp'], v[0]['HostPort'])
                for k,v in ps.items()
        }
        return all_urls.get('{}/tcp'.format(port))
    except:
        return 'Unknown'


def request_json():
    best = request.accept_mimetypes \
            .best_match(['application/json', 'text/html'])
    return best == 'application/json'


def validate_container(name):
    """Validate container with input name, return id and container itself.
    """
    try:
        c = client.containers.get(name)
        return c.id, c
    except:
        return None, None


def get_container(cid):
    try:
        return client.containers.get(cid)
    except:
        return None


def create_new_container(user, **kws):
    """Create new container.

    Parameters
    ----------
    user: User
        User owns new container.

    Keyword Parameters
    ------------------
    'image': image name,
    'mach': machine section,
     other keys: parameters.

    Returns
    -------
    (id, name, nb_url, ss_url): tuple
        id: container id.
        name: container name.
        nb_url: url of nb if available.
        ss_url: url of ss if available.
    """
    image = kws.get('image')
    mach = kws.get('mach', None)
    uname = kws.get('uname')
    dpath = kws.get('dpath', DPATH_DEFAULT)

    token = user.password_hash
    kws1 = {k:v for k,v in kws.items()
            if k not in ['image', 'mach', 'uname', 'dpath']}
    cid, cname, nb_url, ss_url = _create_new_container(
            image, mach, uname, dpath, token, **kws1)
    return cid, cname, nb_url, ss_url


def _create_new_container(image, mach, uname, dpath, token, **kws):
    global NB_PORT, SS_PORT
    image_name = cname_map[image]
    if mach is not None and mach != '':
        # --subm parameter
        command = ['--mach', VA_MACH, '--subm', subm_map[mach]]
    elif mach == '':
        command = []

    nb_url, ss_url = None, None

    command.extend(['--NotebookApp.base_url=' + "'{}/'".format(uname),
                    '--NotebookApp.token=' + "'{}'".format(token),
                    '--NotebookApp.password=' + "''"]
    )

    if 'ss' in image_name:
        NB_PORT += 10
        SS_PORT += 10
        ports = {'8888': ('127.0.0.1', NB_PORT),
                 '4810': ('127.0.0.1', SS_PORT)}
    else:
        NB_PORT += 10
        ports = {'8888': ('127.0.0.1', NB_PORT)}

    try:
        c = client.containers.create(image_name,
                command=command,
                ports=ports,
                #volumes={
                #    dpath: {'bind': "/phyapps", "mode": "ro"},
                #},
                detach=True, tty=True, **kws)
    except:
        return None, 'Unknown', nb_url, ss_url

    nb_url = "http://127.0.0.1:{}".format(NB_PORT)
    ss_url = "http://127.0.0.1:{}".format(SS_PORT)
    return c.id, c.name, nb_url, ss_url
