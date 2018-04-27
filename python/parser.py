class JsonParser:
    def __init__(self):
        self.buff = ""
        self.msg = ""

    def scan(self, inBuff):

        self.buff = self.buff + inBuff

        out = ""

        found_start = False
        found_end = False

        for idx in range(len(self.buff)):

            char = self.buff[idx]

            if char == '{':
                found_start = True
                out = out + char
                continue

            if char == '}':
                found_end = True
                end_idx = idx
                out = out + char
                break

            out = out + char

        if found_start and found_end:
            self.buff = self.buff[end_idx + 1:]
            return out

        return None
