FROM python:3.6

RUN mkdir -p /opt/tcl/Front/
RUN mkdir -p /opt/tcl/DB/
WORKDIR /opt/tcl/

COPY DB/ /opt/tcl/DB/
COPY Front/ /opt/tcl/Front/
COPY config.py /opt/tcl/
COPY requirements /opt/tcl/

RUN pip install --no-cache-dir -r requirements
ENV PYTHONPATH /opt/tcl/

CMD ["python","./Front/front.py"]
