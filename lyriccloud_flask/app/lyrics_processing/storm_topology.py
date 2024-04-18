from streamparse import Bolt, Spout, Topology, Grouping

class SimpleSpout(Spout):
    def initialize(self, stormconf, context):
        self.lyrics_list = []

    def next_tuple(self):
        if self.lyrics_list:
            lyrics = self.lyrics_list.pop(0)
            self.emit([lyrics])

    def receive_lyrics(self, lyrics_list):
        self.lyrics_list.extend(lyrics_list)


class SimpleBolt(Bolt):
    def initialize(self, stormconf, context):
        pass

    def process(self, tup):
        print(tup.values)

class SimpleTopology(Topology):
    simple_spout = SimpleSpout.spec()
    simple_bolt = SimpleBolt.spec(inputs={simple_spout: Grouping.fields('word')})

    @classmethod
    def run(cls, lyrics_list):
        topology = cls()
        topology.simple_spout.receive_lyrics(lyrics_list)
        return topology.submit()
