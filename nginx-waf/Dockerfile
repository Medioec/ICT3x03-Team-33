FROM owasp/modsecurity-crs:nginx
RUN apt update && apt install python3 -y
RUN apt install python3-pip -y
RUN python3 -m pip install flask

# Update package lists
RUN apt-get update

# Install ping utility
RUN apt-get install -y iputils-ping

COPY --chmod=700 data/nginx/startup/* /

ENTRYPOINT ./startup.sh
