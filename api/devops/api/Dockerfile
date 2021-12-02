FROM python:3.8.2

ARG housing_units_api_user_id=9003
ARG housing_units_api_group_id=9003

# Environment variables such as salt, jwt_secret_key and postgresql_connection_uri should not be desplayed like that
# and instead be passed with some other mechanism that hides these information. Ansible could be used for example.
ARG housing_units_api_directory="/usr/local/housing-units-api"
ARG housing_units_api_environment="local"
ARG async_postgresql_connection_uri="postgresql+asyncpg://housing_units_api:123456@0.0.0.0:5432/housing_units_api"
ARG postgresql_connection_uri="postgresql+psycopg2://housing_units_api:123456@0.0.0.0:5432/housing_units_api"
ARG debug="0"
ARG create_db_tables="0"
ARG secret="32c9c8fd6b25bd81cbe5d64afd835f62cf2ffdd11f9ab321"
ARG algorithm="HS256"

ARG celery_broker_url="redis://localhost:6379"
ARG celery_result_backend="redis://localhost:6379"
ARG socrata_app_token="bMQxufH6NyYPXWyCwtjYVx1OH"

ENV HOUSING_UNITS_API_DIRECTORY ${housing_units_api_directory}
ENV HOUSING_UNITS_API_environment ${housing_units_api_environment}
ENV ASYNC_POSTGRESQL_CONNECTION_URI ${async_postgresql_connection_uri}
ENV POSTGRESQL_CONNECTION_URI ${postgresql_connection_uri}
ENV DEBUG ${debug}
ENV CREATE_DB_TABLES ${create_db_tables}
ENV CELERY_BROKER_URL ${celery_broker_url}
ENV CELERY_RESULT_BACKEND ${celery_result_backend}
ENV SECRET ${secret}
ENV ALGORITHM ${algorithm}
ENV SOCRATA_APP_TOKEN ${socrata_app_token}

# Create Housing Units API group and user.
RUN groupadd --system --gid ${housing_units_api_group_id} housingunitsuser \
  && useradd --system --shell /usr/sbin/nologin \
             --gid housingunitsuser --uid ${housing_units_api_user_id} housingunitsuser

# Create Housing Units API directory.
RUN mkdir -p ${housing_units_api_directory}/src \
  && chown -R housingunitsuser:housingunitsuser ${housing_units_api_directory} \
  && chmod -R 770 ${housing_units_api_directory}

# Copy and install Housing Units API requirements.txt.
COPY --chown=housingunitsuser:housingunitsuser "api/src/requirements.txt" ${housing_units_api_directory}/
RUN pip3 install -r ${housing_units_api_directory}/requirements.txt

# Copy Housing Units API source code.
COPY --chown=housingunitsuser:housingunitsuser "api/src" ${housing_units_api_directory}/src/

# Run Housing Units API.
WORKDIR ${housing_units_api_directory}
ENV PYTHONPATH ${housing_units_api_directory}/src

ENTRYPOINT ["uvicorn", "application.main:app", "--host", "0.0.0.0", "--port", "8000"]
