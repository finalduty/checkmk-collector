FROM finalduty/archlinux
MAINTAINER Andy Dustin <andy.dustin@gmail.com>
WORKDIR /git/
CMD /git/api.py

RUN pacman -Sy --noconfirm python2 python2-virtualenv python2-pip; pacman -Scc --noconfirm

ADD virtenv /git/virtenv
ADD api.py /git/api.py

