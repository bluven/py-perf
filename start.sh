#!/usr/bin/env bash

# gunicorn py_perf.wsgi -w 16 -b 0.0.0.0:8000 --access-logfile=-
gunicorn py_perf.wsgi -w 1 -b 0.0.0.0:8000
