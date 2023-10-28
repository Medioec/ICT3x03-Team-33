FROM fluent/fluentd:latest

# Use root account to use apt
USER root

# Install required plugins and other dependencies
RUN buildDeps="sudo make gcc g++ libc-dev" \
 && apt-get update \
 && apt-get install -y --no-install-recommends $buildDeps \
 && sudo gem install fluent-plugin-elasticsearch --no-document \
 && sudo gem sources --clear-all \
 && apt-get purge -y --auto-remove $buildDeps \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get purge -y --auto-remove \
 && apt-get clean

# Copy custom Fluentd configuration
COPY ./fluentd.conf /fluentd/etc/

# Switch to Fluentd user
USER fluent