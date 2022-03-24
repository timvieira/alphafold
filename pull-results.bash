#!/usr/bin/env bash

rsync -a --progress \
      login.clsp.jhu.edu:/home/timv/projects/dyna-pi/results-5b/ \
      /home/timv/projects/dyna-pi/results-5b/. \
      --exclude 'cmd-stdout.txt' \
      --exclude 'log.pkl~' \
      --exclude 'log.pkl'
