#!/usr/bin/env bash
rsync -a --progress \
      /home/timv/projects/dyna-pi/. \
      login.clsp.jhu.edu:/home/timv/projects/dyna-pi/. \
      --exclude 'results*'
