# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.channel import Channel  # noqa: F401,E501
from swagger_server import util


class ChannelData(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, data: Channel=None):  # noqa: E501
        """ChannelData - a model defined in Swagger

        :param data: The data of this ChannelData.  # noqa: E501
        :type data: Channel
        """
        self.swagger_types = {
            'data': Channel
        }

        self.attribute_map = {
            'data': 'data'
        }
        self._data = data

    @classmethod
    def from_dict(cls, dikt) -> 'ChannelData':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ChannelData of this ChannelData.  # noqa: E501
        :rtype: ChannelData
        """
        return util.deserialize_model(dikt, cls)

    @property
    def data(self) -> Channel:
        """Gets the data of this ChannelData.


        :return: The data of this ChannelData.
        :rtype: Channel
        """
        return self._data

    @data.setter
    def data(self, data: Channel):
        """Sets the data of this ChannelData.


        :param data: The data of this ChannelData.
        :type data: Channel
        """
        if data is None:
            raise ValueError("Invalid value for `data`, must not be `None`")  # noqa: E501

        self._data = data
