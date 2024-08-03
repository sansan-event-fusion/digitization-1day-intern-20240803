FROM python:3.11-slim

RUN apt update && \
	apt install -y \
		locales \
		vim \
		man-db \
		nodejs \
		sudo && \
	rm -rf /var/lib/apt/lists/* && \
	apt clean
RUN pip install poetry
RUN locale-gen ja_JP.UTF-8

RUN useradd -ms /bin/bash -G sudo me && echo 'me ALL=(ALL) NOPASSWD: ALL' >/etc/sudoers.d/me
USER me
WORKDIR /home/me
ENV LANG ja_JP.UTF-8
ENV TZ Asia/Tokyo

CMD ["/bin/bash"]
