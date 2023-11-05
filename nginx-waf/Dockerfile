FROM owasp/modsecurity-crs:nginx
RUN apt update && apt install python3 -y
RUN apt install python3-pip -y
RUN python3 -m pip install flask

COPY --chmod=700 data/nginx/startup/* /

ENTRYPOINT ./startup.sh
