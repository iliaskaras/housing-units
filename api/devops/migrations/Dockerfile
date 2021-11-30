FROM python:3.8.2

ARG migrations_user_id=9002
ARG migrations_group_id=9002

ARG housing_units_api_directory="/usr/local/housing-units-api"

ARG postgresql_connection_uri="postgresql+psycopg2://housing_units_api:123456@housing-units-api-postgresql:5432/housing_units_api"

ENV POSTGRESQL_CONNECTION_URI ${postgresql_connection_uri}

# Install Alembic.
RUN pip3 install \
  alembic==1.7.5 \
  psycopg2==2.8.4

# Create Migrations group and user.
RUN groupadd --system --gid ${migrations_group_id} migrationuser \
  && useradd --system --shell /usr/sbin/nologin --gid migrationuser --uid ${migrations_user_id} migrationuser

# Create Housing Units API directory.
RUN mkdir -p ${housing_units_api_directory}/src

# Copy Housing Units API migrations code.
COPY --chown=migrationuser:migrationuser "api/src" ${housing_units_api_directory}/src/

WORKDIR ${housing_units_api_directory}/src
ENV PYTHONPATH ${housing_units_api_directory}/src
# Set the migrationuser as the user to be used for running the ENTRYPOINT
USER migrationuser
ENTRYPOINT ["alembic", "-x", "postgresql_connection_uri=postgresql+psycopg2://housing_units_api:123456@housing-units-api-postgresql:5432/housing_units_api", "upgrade", "head"]
