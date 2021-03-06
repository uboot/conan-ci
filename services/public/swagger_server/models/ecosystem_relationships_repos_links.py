# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class EcosystemRelationshipsReposLinks(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, related: str=None):  # noqa: E501
        """EcosystemRelationshipsReposLinks - a model defined in Swagger

        :param related: The related of this EcosystemRelationshipsReposLinks.  # noqa: E501
        :type related: str
        """
        self.swagger_types = {
            'related': str
        }

        self.attribute_map = {
            'related': 'related'
        }
        self._related = related

    @classmethod
    def from_dict(cls, dikt) -> 'EcosystemRelationshipsReposLinks':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Ecosystem_relationships_repos_links of this EcosystemRelationshipsReposLinks.  # noqa: E501
        :rtype: EcosystemRelationshipsReposLinks
        """
        return util.deserialize_model(dikt, cls)

    @property
    def related(self) -> str:
        """Gets the related of this EcosystemRelationshipsReposLinks.


        :return: The related of this EcosystemRelationshipsReposLinks.
        :rtype: str
        """
        return self._related

    @related.setter
    def related(self, related: str):
        """Sets the related of this EcosystemRelationshipsReposLinks.


        :param related: The related of this EcosystemRelationshipsReposLinks.
        :type related: str
        """

        self._related = related
