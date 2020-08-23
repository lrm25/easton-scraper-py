FROM ubuntu:xenial-20200807

# python/pip
RUN apt update
RUN apt install -y git python3 python3-pip
RUN pip3 install bs4

# scraper
RUN git clone https://github.com/lrm25/easton-scraper-py ~/easton-scraper-py
RUN cd /root/easton-scraper-py/easton_scraper_py/ && python3 scraper.py --days 2
