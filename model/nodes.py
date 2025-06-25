from dataclasses import dataclass


@dataclass
class Node:
    albumId: int
    title: str
    artistId: int

    def __eq__(self, other):
        return self.albumId == other.albumId
    def __hash__(self):
        return hash(self.albumId)
    def __str__(self):
        return self.title