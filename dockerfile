FROM python:3.7-alpine3.13
RUN apk update && apk  add --no-cache  openssh-client gcc g++ libffi-dev tzdata gcompat libstdc++ curl&& cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime \
    && echo "Asia/Taipei" > /etc/timezone \
    && apk del tzdata 

RUN curl -LO -s https://mirror.openshift.com/pub/openshift-v4/clients/ocp/4.10.9/openshift-client-linux.tar.gz && \
    tar zxf openshift-client-linux*.tar.gz -C /usr/local/bin/
COPY src/requirements.txt .
RUN mkdir -p /root/python
RUN python -m pip install --upgrade pip > /dev/null
RUN pip install -r  requirements.txt > /dev/null
COPY src/. /root/python/
WORKDIR /root/python/
EXPOSE 5000


ENTRYPOINT ["tail","-f","/dev/null"]