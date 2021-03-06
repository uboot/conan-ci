# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.ecosystem_relationships_builds import EcosystemRelationshipsBuilds  # noqa: F401,E501
from swagger_server.models.ecosystem_relationships_channels import EcosystemRelationshipsChannels  # noqa: F401,E501
from swagger_server.models.ecosystem_relationships_profiles import EcosystemRelationshipsProfiles  # noqa: F401,E501
from swagger_server.models.ecosystem_relationships_repos import EcosystemRelationshipsRepos  # noqa: F401,E501
from swagger_server import util


class EcosystemRelationships(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, builds: EcosystemRelationshipsBuilds=None, channels: EcosystemRelationshipsChannels=None, profiles: EcosystemRelationshipsProfiles=None, repos: EcosystemRelationshipsRepos=None):  # noqa: E501
        """EcosystemRelationships - a model defined in Swagger

        :param builds: The builds of this EcosystemRelationships.  # noqa: E501
        :type builds: EcosystemRelationshipsBuilds
        :param channels: The channels of this EcosystemRelationships.  # noqa: E501
        :type channels: EcosystemRelationshipsChannels
        :param profiles: The profiles of this EcosystemRelationships.  # noqa: E501
        :type profiles: EcosystemRelationshipsProfiles
        :param repos: The repos of this EcosystemRelationships.  # noqa: E501
        :type repos: EcosystemRelationshipsRepos
        """
        self.swagger_types = {
            'builds': EcosystemRelationshipsBuilds,
            'channels': EcosystemRelationshipsChannels,
            'profiles': EcosystemRelationshipsProfiles,
            'repos': EcosystemRelationshipsRepos
        }

        self.attribute_map = {
            'builds': 'builds',
            'channels': 'channels',
            'profiles': 'profiles',
            'repos': 'repos'
        }
        self._builds = builds
        self._channels = channels
        self._profiles = profiles
        self._repos = repos

    @classmethod
    def from_dict(cls, dikt) -> 'EcosystemRelationships':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Ecosystem_relationships of this EcosystemRelationships.  # noqa: E501
        :rtype: EcosystemRelationships
        """
        return util.deserialize_model(dikt, cls)

    @property
    def builds(self) -> EcosystemRelationshipsBuilds:
        """Gets the builds of this EcosystemRelationships.


        :return: The builds of this EcosystemRelationships.
        :rtype: EcosystemRelationshipsBuilds
        """
        return self._builds

    @builds.setter
    def builds(self, builds: EcosystemRelationshipsBuilds):
        """Sets the builds of this EcosystemRelationships.


        :param builds: The builds of this EcosystemRelationships.
        :type builds: EcosystemRelationshipsBuilds
        """

        self._builds = builds

    @property
    def channels(self) -> EcosystemRelationshipsChannels:
        """Gets the channels of this EcosystemRelationships.


        :return: The channels of this EcosystemRelationships.
        :rtype: EcosystemRelationshipsChannels
        """
        return self._channels

    @channels.setter
    def channels(self, channels: EcosystemRelationshipsChannels):
        """Sets the channels of this EcosystemRelationships.


        :param channels: The channels of this EcosystemRelationships.
        :type channels: EcosystemRelationshipsChannels
        """

        self._channels = channels

    @property
    def profiles(self) -> EcosystemRelationshipsProfiles:
        """Gets the profiles of this EcosystemRelationships.


        :return: The profiles of this EcosystemRelationships.
        :rtype: EcosystemRelationshipsProfiles
        """
        return self._profiles

    @profiles.setter
    def profiles(self, profiles: EcosystemRelationshipsProfiles):
        """Sets the profiles of this EcosystemRelationships.


        :param profiles: The profiles of this EcosystemRelationships.
        :type profiles: EcosystemRelationshipsProfiles
        """

        self._profiles = profiles

    @property
    def repos(self) -> EcosystemRelationshipsRepos:
        """Gets the repos of this EcosystemRelationships.


        :return: The repos of this EcosystemRelationships.
        :rtype: EcosystemRelationshipsRepos
        """
        return self._repos

    @repos.setter
    def repos(self, repos: EcosystemRelationshipsRepos):
        """Sets the repos of this EcosystemRelationships.


        :param repos: The repos of this EcosystemRelationships.
        :type repos: EcosystemRelationshipsRepos
        """

        self._repos = repos
