FROM docker.elastic.co/logstash/logstash:7.5.1

RUN rm -f /usr/share/logstash/pipeline/logstash.conf

USER root 

# COPY mssql-jdbc-9.2.1.jre8.jar ./logstash-core/lib/jars/mssql-jdbc-9.2.1.jre8.jar

# RUN chmod +r ./logstash-core/lib/jars/mssql-jdbc-9.2.1.jre8.jar

RUN logstash-plugin install logstash-input-jdbc