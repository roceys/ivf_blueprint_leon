# -*- coding: utf-8 -*-
import sys
import os

sys.path.append("../")
from blueprintBase import CBlueprintBase, make_Video
import outputDesc


class CBPInverseColor(CBlueprintBase):

    # input: https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4
    # output: http://test-v.oss-cn-shanghai.aliyuncs.com/hypnos-blueprint/output-8619-449919.mp4
    def __init__(self, userVideo, videoDuration, configDict=dict()):
        super(CBPInverseColor, self).__init__("InverseColor")
        self._width = configDict.get('width', 720)
        self._height = configDict.get('height', 1280)
        self._user_element = userVideo
        self._elemnet_duration = videoDuration
        self._element_type = self.get_elementType_fromValue(userVideo)

    def init_outputDesc(self):
        outputLocation = "*"
        outputAlphaLocation = "*"
        fps = 25.0
        duration = self._elemnet_duration
        bgColor = "RGBA(0,0,0,255)"
        self._outputDesc = outputDesc.create(self._width, self._height, outputLocation, outputAlphaLocation, fps,
                                             duration, bgColor)

    def init_level(self):
        configDict = dict()
        configDict['id'] = 0
        configDict['name'] = "inverse_color"
        configDict['actionNumber'] = 1
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in
                                      range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_Func
        configDict['newelement_func'] = self.newelement_Func
        configDict['baseTime'] = 0
        self._levelConfigs.append(configDict)

    def newLevel_Func(self, configDict):
        levelName = configDict['name']
        times = [(0, self._elemnet_duration)]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "projectionType": "normal",
            "subactions": ["inverseColor"]
        }
        kwargs = {
            'element': configDict['elementNames']
        }
        level = self.create_level_from_action(baseActionDict, configDict, times, **kwargs)
        return level

    def newelement_Func(self, configDict):
        names = configDict['elementNames']
        for i, name in enumerate(names):
            element = {
                'name': name,
                'source': 'designer',
                'type': self._element_type,
                'value': self._user_element
            }
            self._elements.append(element)


def test_effect():
    userVideo = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4"
    videoDuration = 5000

    rotateVideo = make_Video(CBPInverseColor, userVideo, videoDuration)
    print(rotateVideo)


if __name__ == "__main__":
    test_effect()
