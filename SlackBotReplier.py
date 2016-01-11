import random
import time
from slackclient import SlackClient


class SlackbotReplier(object):
    """

    """

    def __init__(self, token, timeout=1):
        """
        #TODO
        :param token:
        :param timeout:
        :return:
        """
        self.client = SlackClient(token)
        self.timeout = timeout
        self.keywords = self._loadListOfStringsFromFile("keywords.txt")
        self.generalResponses = self._loadListOfStringsFromFile("general_responses.txt")
        self.atReplyResponses = self._loadListOfStringsFromFile("at_reply_responses.txt")

    def run(self):
        """
        #TODO
        :return:
        """
        if self.client.rtm_connect():
            self._getID()
            while True:
                for messageData in self._getMessages():
                    if self._containsAtReply(messageData):
                        self._sendRandomMessageReply(messageData, self.atReplyResponses)
                    elif self._containsKeyword(messageData):
                        self._sendRandomMessageReply(messageData, self.generalResponses)
                time.sleep(self.timeout)
        else:
            raise ValueError("Connection Failed, invalid token?")

    def _loadListOfStringsFromFile(self, filename):
        """

        :param filename:
        :return:
        """
        content = []
        try:
            with open(filename) as file:
                content = file.readlines()
        except (OSError, IOError) as e:
            print "e.errno: {}".format(e.errno) #TODO remove this
            print "WARNING: '{}' not found".format(filename)
        return content

    def _getID(self):
        login_data = self.client.server.login_data
        try:
            self.id = self.client.server.login_data["self"]["id"]
        except:
            print "WARNING: Failed to get bot ID, at replies will not process"

    def _getMessages(self):
        """
        #TODO
        :return:
        """
        for dataBlob in self.client.rtm_read():
            if dataBlob['type'] != 'message':
                continue
            yield dataBlob

    def _containsAtReply(self, messageData):
        """

        :return:
        """
        if self.id and self.id in  messageData['text']:
            return True
        return False

    def _containsKeyword(self, messageData):
        """

        :param messageData:
        :return:
        """
        for keyword in self.keywords:
            if keyword in messageData['text']:
                return True
        return False

    def _sendRandomMessageReply(self, messageData, replyList):
        """

        :param messageData:
        :param replyList:
        :return:
        """
        if replyList:
            reply = replyList[random.randint(0, len(replyList) - 1)]
            print "Sending Reply<{}>: '{}'".format(
                    self._getChannelName(messageData),
                    reply)

    def _replaceSpecialSlackWords(self, messageData, reply):
        """

        :param messageData:
        :param reply:
        :return:
        """
        # Replace @channel
        # TODO
        # Replace @here
        # TODO
        # Replace @user
        # TODO
        pass

    def _getChannelName(self, messageData):
        """

        :param messageData:
        :return:
        """
        try:
            channelName = self.client.server.channels.find(messageData['channel']).name
            return channelName
        except:
            print "WARNING: Failed to find channel name"
            return None
