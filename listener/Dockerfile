FROM python:3.6

RUN mkdir -p /opt/tcl/listener/
RUN mkdir -p /opt/tcl/DB/
WORKDIR /opt/tcl/

COPY DB/ /opt/tcl/DB/
COPY listener/ /opt/tcl/listener/
COPY config.py /opt/tcl/
COPY requirements /opt/tcl/

ARG src="Telegram Chat Listener.session"
ARG target="/opt/tcl/"
COPY ${src} ${target}

RUN pip install --no-cache-dir -r requirements
ENV PYTHONPATH /opt/tcl/

CMD ["python","./listener/main.py"]
