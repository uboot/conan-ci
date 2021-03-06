# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.ecosystem_relationships_profiles_data import EcosystemRelationshipsProfilesData  # noqa: F401,E501
from swagger_server import util


class BuildRelationshipsProfile(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, data: EcosystemRelationshipsProfilesData=None):  # noqa: E501
        """BuildRelationshipsProfile - a model defined in Swagger

        :param data: The data of this BuildRelationshipsProfile.  # noqa: E501
        :type data: EcosystemRelationshipsProfilesData
        """
        self.swagger_types = {
            'data': EcosystemRelationshipsProfilesData
        }

        self.attribute_map = {
            'data': 'data'
        }
        self._data = data

    @classmethod
    def from_dict(cls, dikt) -> 'BuildRelationshipsProfile':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Build_relationships_profile of this BuildRelationshipsProfile.  # noqa: E501
        :rtype: BuildRelationshipsProfile
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self) -> EcosystemRelationshipsProfilesData:
        """Gets the data of this BuildRelationshipsProfile.


        :return: The data of this BuildRelationshipsProfile.
        :rtype: EcosystemRelationshipsProfilesData
        """
        return self._data

    @data.setter
    def data(self, data: EcosystemRelationshipsProfilesData):
        """Sets the data of this BuildRelationshipsProfile.


        :param data: The data of this BuildRelationshipsProfile.
        :type data: EcosystemRelationshipsProfilesData
        """

        self._data = data
