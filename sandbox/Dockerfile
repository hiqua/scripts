FROM debian:bullseye

ENV DEBIAN_FRONTEND noninteractive

COPY sources.list /etc/apt/sources.list

RUN apt-get update && apt-get install -y\
      apt-utils\
      curl\
      fd-find\
      git\
      ipython3\
      locales-all\
      locales\
      neovim\
      nodejs\
      openjdk-11-jdk\ 
      pipenv\
      ripgrep\
      sudo\
      tmux\
      unrar\
      wget\
      zip\
      zsh

# To test systemd feature
# Need to install it later to avoid some packages using it wrongly
RUN apt-get update && apt-get install -y systemctl

ARG user="sb"
ARG UID="1000"
ARG GID="1000"

RUN addgroup --gid $GID somegroup
RUN adduser --uid $UID --gid $GID --gecos "" --disabled-password $user 
RUN printf '%%sudo	ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN adduser $user sudo
RUN touch /var/lib/sudo/lectured/$user

COPY custom.sh /home/$user/custom.sh
RUN chown $UID:$GID /home/$user/custom.sh

USER $user

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN chmod +x /home/$user/custom.sh && /home/$user/custom.sh

RUN sudo chsh -s /bin/zsh $user

WORKDIR /home/$user/mounted

ENV DEBIAN_FRONTEND=


CMD [ "tail" ,"-f", "/dev/null" ]
