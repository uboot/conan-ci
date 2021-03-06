# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.ecosystem_relationships_profiles_data import EcosystemRelationshipsProfilesData  # noqa: F401,E501
from swagger_server import util


class EcosystemRelationshipsProfiles(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, data: List[EcosystemRelationshipsProfilesData]=None):  # noqa: E501
        """EcosystemRelationshipsProfiles - a model defined in Swagger

        :param data: The data of this EcosystemRelationshipsProfiles.  # noqa: E501
        :type data: List[EcosystemRelationshipsProfilesData]
        """
        self.swagger_types = {
            'data': List[EcosystemRelationshipsProfilesData]
        }

        self.attribute_map = {
            'data': 'data'
        }
        self._data = data

    @classmethod
    def from_dict(cls, dikt) -> 'EcosystemRelationshipsProfiles':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Ecosystem_relationships_profiles of this EcosystemRelationshipsProfiles.  # noqa: E501
        :rtype: EcosystemRelationshipsProfiles
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self) -> List[EcosystemRelationshipsProfilesData]:
        """Gets the data of this EcosystemRelationshipsProfiles.


        :return: The data of this EcosystemRelationshipsProfiles.
        :rtype: List[EcosystemRelationshipsProfilesData]
        """
        return self._data

    @data.setter
    def data(self, data: List[EcosystemRelationshipsProfilesData]):
        """Sets the data of this EcosystemRelationshipsProfiles.


        :param data: The data of this EcosystemRelationshipsProfiles.
        :type data: List[EcosystemRelationshipsProfilesData]
        """

        self._data = data
