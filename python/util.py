import socket


class Tracker:
    def __init__(self, obs):
        self.num_rounds = obs.num_rounds
        self.round = obs.round
        self.frame = obs.frame

    def update(self, obs):
        if self.num_rounds != obs.num_rounds:
            raise RuntimeError("number of rounds has changed")

        round_diff = obs.round - self.round
        if round_diff > 1:
            print("missed rounds: from {} to {}".format(self.round, obs.round))

        if round_diff > 0:
            self.round = obs.round
            self.frame = obs.frame
            return

        frame_diff = obs.frame - self.frame
        if frame_diff > 1:
            print("missed frames: from {} to {}".format(self.frame, obs.frame))

        if frame_diff == 0:
            raise RuntimeError("frame was not updated")

        self.frame = obs.frame


class MsgParser:
    def __init__(self):
        self.buff = ""
        self.msg = ""

    def scan(self, in_buff):

        self.buff = self.buff + in_buff

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


def connect(host, port):
    soc = socket.socket()
    soc.bind((host, port))
    soc.listen(5)
    conn, addr = soc.accept()
    return conn