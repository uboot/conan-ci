import connexion

from conanci import database
from flask import abort
from swagger_server import models


def __createChannel(record: database.Channel):
    return models.Channel(
        id=record.id,
        type="channels",
        attributes=models.ChannelAttributes(
            name=record.name,
            branch=record.branch
        ),
        relationships=models.ProfileRelationships(
            ecosystem=models.RepoRelationshipsEcosystem(
                data=models.RepoRelationshipsEcosystemData(
                    id=record.ecosystem_id,
                    type="ecosystems"
                )
            )
        )
    )


def add_channel(body=None):
    if connexion.request.is_json:
        body = models.ChannelData.from_dict(connexion.request.get_json())  # noqa: E501

    with database.session_scope() as session:
        ecosystem = session.query(database.Ecosystem).filter_by(id=body.data.relationships.ecosystem.data.id).first()
        if not ecosystem:
            abort(400)
        record = database.Channel()
        record.name = body.data.attributes.name
        record.ecosystem = ecosystem
        record.branch = body.data.attributes.branch
        session.add(record)
        session.commit()
        return models.ChannelData(data=__createChannel(record)), 201


def delete_channel(channel_id):
    with database.session_scope() as session:
        record = session.query(database.Channel).filter_by(id=channel_id).first()
        if not record:
            abort(404)
        session.delete(record)
    return None


def get_channel(channel_id):
    with database.session_scope() as session:
        record = session.query(database.Channel).filter_by(id=channel_id).first()
        if not record:
            abort(404)
        return models.ChannelData(data=__createChannel(record))


def update_channel(channel_id, body=None):
    if connexion.request.is_json:
        body = models.ChannelData.from_dict(connexion.request.get_json())  # noqa: E501

    with database.session_scope() as session:
        record = session.query(database.Channel).filter_by(id=channel_id).first()
        if not record:
            abort(404)

        record.name = body.data.attributes.name
        record.branch = body.data.attributes.branch
        return models.ChannelData(data=__createChannel(record))
