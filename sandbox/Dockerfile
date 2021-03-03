FROM debian:bullseye

# TODO: hardcoded guid uid

RUN apt-get update && apt-get install -y\
      curl\
      fd-find\
      git\
      neovim\
      nodejs\
      openjdk-11-jdk\ 
      ripgrep\
      sudo\
      tmux\
      wget\
      zsh\
      zip

ARG user="sb"
ARG UID
ARG GID

RUN addgroup --gid $GID somegroup
RUN adduser --uid $UID --gid $GID --gecos "" --disabled-password $user 

RUN printf '%%sudo	ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN adduser $user sudo

RUN touch /var/lib/sudo/lectured/$user

COPY custom.sh /home/$user/custom.sh

RUN chown $UID:$GID /home/$user/custom.sh

USER $user

ENV LANG en_US.UTF-8

# COPY --chown=$UID:$GID custom.sh /home/$user/custom.sh


RUN chmod u+x /home/$user/custom.sh && /home/$user/custom.sh

RUN sudo chsh -s /bin/zsh $user

WORKDIR /home/$user/mounted

CMD [ "tail" ,"-f", "/dev/null" ]

# ENTRYPOINT ["/bin/zsh"]
