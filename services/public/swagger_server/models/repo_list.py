# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.repo import Repo  # noqa: F401,E501
from swagger_server import util


class RepoList(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, data: List[Repo]=None):  # noqa: E501
        """RepoList - a model defined in Swagger

        :param data: The data of this RepoList.  # noqa: E501
        :type data: List[Repo]
        """
        self.swagger_types = {
            'data': List[Repo]
        }

        self.attribute_map = {
            'data': 'data'
        }
        self._data = data

    @classmethod
    def from_dict(cls, dikt) -> 'RepoList':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The RepoList of this RepoList.  # noqa: E501
        :rtype: RepoList
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self) -> List[Repo]:
        """Gets the data of this RepoList.


        :return: The data of this RepoList.
        :rtype: List[Repo]
        """
        return self._data

    @data.setter
    def data(self, data: List[Repo]):
        """Sets the data of this RepoList.


        :param data: The data of this RepoList.
        :type data: List[Repo]
        """
        if data is None:
            raise ValueError("Invalid value for `data`, must not be `None`")  # noqa: E501

        self._data = data