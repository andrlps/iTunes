from database.DB_connect import DBConnect
from model.edges import Node, Edge


class DAO():
    @staticmethod
    def getNodes(durata):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary = True)

        query ="""select distinct a.*
                    from track t, album a 
                    where t.AlbumId = a.AlbumId
                    group by a.AlbumId, a.ArtistId, a.Title
                    having ((sum(t.Milliseconds)/1000)/60) > %s"""

        cursor.execute(query, (durata,))

        result = []

        for row in cursor:
            result.append(Node(row["AlbumId"], row["Title"], row["ArtistId"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getDurata(album):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select ((sum(t.Milliseconds)/1000)/60) as d
from track t, album a 
where t.AlbumId = a.AlbumId
and a.AlbumId = %s
group by a.AlbumId"""

        cursor.execute(query, (album.albumId, ))

        result = []

        for row in cursor:
            result = row["d"]

        cursor.close()
        conn.close()
        return result

    def getEdges(durata, idNodes):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """select distinct t1.AlbumId as n1, t2.AlbumId as n2
from
(select distinct p.PlaylistId, t1.AlbumId
from playlisttrack p, track t,
(select distinct a.AlbumId
from track t, album a 
where t.AlbumId = a.AlbumId
group by a.AlbumId
having ((sum(t.Milliseconds)/1000)/60) > %s) t1
where p.TrackId = t.TrackId
and t1.AlbumId = t.AlbumId) t1,
(select distinct p.PlaylistId, t1.AlbumId
from playlisttrack p, track t,
(select distinct a.AlbumId
from track t, album a 
where t.AlbumId = a.AlbumId
group by a.AlbumId
having ((sum(t.Milliseconds)/1000)/60) > %s) t1
where p.TrackId = t.TrackId
and t1.AlbumId = t.AlbumId) t2
where t1.PlaylistId = t2.PlaylistId
and t1.AlbumId < t2.AlbumId"""

        cursor.execute(query, (durata, durata,))

        result = []

        for row in cursor:
            result.append(Edge(idNodes[row["n1"]], idNodes[row["n2"]]))

        cursor.close()
        conn.close()
        return result
