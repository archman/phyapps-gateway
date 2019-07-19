# -*- coding: utf-8 -*-

from app import app as application


if __name__ == '__main__':
    #application.run(host="0.0.0.0",
    #                threaded=True,)
    #print(application.view_functions)
    #print(application.url_map)
    application.run(host="0.0.0.0")
