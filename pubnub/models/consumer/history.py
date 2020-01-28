class PNHistoryResult(object):
    def __init__(self, messages, start_timetoken, end_timetoken):
        self.messages = messages
        self.start_timetoken = start_timetoken
        self.end_timetoken = end_timetoken

    def __str__(self):
        return "History result for range %d..%d" % (self.start_timetoken, self.end_timetoken)

    @classmethod
    def from_json(cls, json_input, crypto, include_timetoken=False, include_meta=False, cipher=None):
        start_timetoken = json_input[1]
        end_timetoken = json_input[2]

        raw_items = json_input[0]
        messages = []

        for item in raw_items:
            if (include_timetoken or include_meta) and isinstance(item, dict) and 'message' in item:
                message = PNHistoryItemResult(item['message'], crypto)
                if include_timetoken and 'timetoken' in item:
                    message.timetoken = item['timetoken']
                if include_meta and 'meta' in item:
                    message.meta = item['meta']

            else:
                message = PNHistoryItemResult(item, crypto)

            if cipher is not None:
                message.decrypt(cipher)

            messages.append(message)

        return PNHistoryResult(
            messages=messages,
            start_timetoken=start_timetoken,
            end_timetoken=end_timetoken
        )


class PNHistoryItemResult(object):
    def __init__(self, entry, crypto, timetoken=None, meta=None):
        self.timetoken = timetoken
        self.meta = meta
        self.entry = entry
        self.crypto = crypto

    def __str__(self):
        return "History item with tt: %s and content: %s" % (self.timetoken, self.entry)

    def decrypt(self, cipher_key):
        self.entry = self.crypto.decrypt(cipher_key, self.entry)
