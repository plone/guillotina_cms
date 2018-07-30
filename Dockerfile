FROM python:3


WORKDIR /usr/src/app

COPY requirements.txt ./
COPY requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install aiohttp_autoreload
RUN pip install aiomonitor
RUN pip install -r requirements-test.txt


COPY . .

RUN python setup.py develop

CMD [ "guillotina" ]
