#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


def unicorn(func, pv, raw_value):
    url = "http://127.0.0.1:8383/function/{}".format(func)
    data = "{{'name': '{name}', 'value': {value}}}".format(
            name=pv, value=raw_value)
    r = requests.post(url, data=data, 
            headers={"Content-Type": "application/json"})
    return r.json()

def test_unicorn():
    pv = 'VA:FE_SCS1:DCH_D709:ANG_CSET'
    val0 = 0.12
    print(unicorn('func_unicorn', pv, val0))

def test():
    #url = 'http://httpbin.org/post'
    #r = requests.post(url, json={'func1': 'fn'})
    #url = 'http://127.0.0.1:5000/api/v1.0/functions'
    #r = requests.get(url)
    pass

def get_func():
    url =  'http://127.0.0.1:5005/functions'
    r = requests.get(url)
    print(r.json())


def update_func():
    url =  'http://127.0.0.1:5050/functions'
    r = requests.put(url + '/user1',
            json={'description': 'new user...',
                  'container_id': '92d2402dcbda',
                  'container_name': 'serene_shannon',
                  'server_url': 'http://127.0.0.1:8887',
                  },
            auth=('dev', 'dev'))
    print(r.json())


def create_user():
    url =  'http://127.0.0.1:5050/users'
    r = requests.post(url,
            json={
                'description': 'new user...',
                'name': 'user1',
                'container_id': '92d2402dcbda',
                'container_name': 'serene_shannon',
                'server_url': 'http://127.0.0.1:8887',
                'admin': 'admin',
            },
            auth=('dev1', 'dev1'),
        )
    print(r)
    print(r.json())


def delete_func():
    url =  'http://127.0.0.1:5050/functions'
    r = requests.delete(url + '/user1', auth=('dev','dev'))
    print(r.json())


if __name__ == '__main__':
    #test_unicorn()
    create_user()
    #update_func()
    #delete_func()
    #get_func()
