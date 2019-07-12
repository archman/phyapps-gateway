# -*- coding: utf-8 -*-

import requests
import os


def update_proxy(uname, target_url, url=None, token=None):
    """post new proxy rule.

    Parameters
    ----------
    uname : str
        User name.
    target_url : str
        Base url of user's notebook server, w/o username.
    url : str
        Base url of proxy server, by default read from `PROXY_BASE`.
    token : str
        String required to communicate with proxy server, by default
        read from `PROXY_TOKEN`.

    Returns
    -------
    ret : str
        Proxy URL of target url.
    """
    # create proxy rule for user/container
    # add proxy url into container as new col
    # update template with proxy url and hide notebook_url
    if url is None:
        if 'PROXY_BASE' in os.environ:
            url = os.environ['PROXY_BASE']
        else:
            return None

    if token is None:
        if 'PROXY_TOKEN' in os.environ:
            token = os.environ['PROXY_TOKEN']
        else:
            token = ''

    purl = url + '/{}/'.format(uname)
    r = requests.post(purl,
            json={
                'target': target_url,
            },
            headers={'Authorization': 'token {}'.format(token)},
        )
    if r.ok:
        return r.url
    else:
        return None


def get_proxy():
    token = '0b20cdf3c951d25936d27fc4405eb23e2e29790b00'
    r = requests.get("http://127.0.0.1:8001/api/routes",
            headers={'Authorization': 'token {}'.format(token)},
        )
    d = r.json()
    print(d.keys())
    print(d['/user1'])


if __name__ == '__main__':
    get_proxy()
