FROM postgres:12.3
RUN localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.UTF-8
ENV LANG pt_BR.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update; apt-get -y install gnupg2 wget ca-certificates rpl pwgen software-properties-common gdal-bin
RUN sh -c "echo \"deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -c -s)-pgdg main\" > /etc/apt/sources.list.d/pgdg.list"
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc -O- | apt-key add -
RUN apt-get update; apt-get install -y postgresql-client-12 postgresql-common postgresql-12
RUN apt-get install -y postgresql-contrib  
# Open port 5432 so linked containers can see them
EXPOSE 5432

#Copying test data
COPY ./dump.sql /docker-entrypoint-initdb.d/dump.sql

#Setting environment variables
ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR:pt
ENV LC_ALL=pt_BR.UTF-8
ENV POSTGRES_DB=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DATA=data
ENV TZ=GMT

VOLUME /var/lib/postgresql/data
