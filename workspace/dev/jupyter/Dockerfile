FROM phidata/jupyter:4.0.5

RUN pip install --upgrade pip

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY workspace/dev/jupyter/config/ /
RUN pip install -r /jupyter_requirements.txt
