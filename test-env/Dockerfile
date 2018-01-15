FROM ubuntu:16.04
MAINTAINER Krzysztof Łuczak

ARG DEBIAN_FRONTEND=noninteractive

# install apt-utils
RUN apt-get update && apt-get install -y apt-utils

# install python2.7 for ansible
RUN apt-get install -y python

# locale
RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8  
ENV LANG pl_PL.UTF-8
ENV LANGUAGE pl_PL:pl
ENV LC_ALL pl_PL.UTF-8

# INSTALL APPS FOR MODULES ------------------------

# install net-tools
RUN apt-get install -y net-tools

# install lshw
RUN apt-get install -y lshw

# install John the Ripper
RUN apt-get install -y john

# dicrectory for aget
RUN mkdir -p /opt/jasmine-agent/
# --------------------------------------------------

# install SSH server
RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:toor' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

#EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
