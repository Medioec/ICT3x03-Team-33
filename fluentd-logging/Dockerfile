FROM fluent/fluentd:v1.16-debian-1

# Use root account to use apt
USER root

# Install required plugins and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends make gcc g++ libc-dev sudo && \
    sudo gem install fluent-plugin-elasticsearch --no-document && \
    sudo gem sources --clear-all && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Create log directory and set permissions
RUN mkdir -p /fluentd/log/ && chown fluent:fluent /fluentd/log/

# Copy custom Fluentd configuration
COPY ./fluentd.conf /fluentd-logging/etc/

# Switch to Fluentd user
USER fluent