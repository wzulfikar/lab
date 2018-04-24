import numpy as np
import cv2
import postgresql

class FacerecPG:

    def __init__(self, conf: dict):
        self.db = postgresql.open('pq://{}:{}@{}:{}/{}'.format(
            conf['user'],
            conf['pass'],
            conf['host'],
            conf['port'],
            conf['db']))

        print("FacerecPG initialized. Using DB at {}:{}/{}".format(conf['host'], 
                                                                   conf['port'], 
                                                                   conf['db']))

    def findfaces(self, enc: np.ndarray, limit: int) -> list:
        query = "SELECT file, p.id as profile_id, p.name as name \
                FROM vectors  v \
                LEFT OUTER JOIN profiles p ON v.profile_id = p.id \
                ORDER BY " + \
                "(CUBE(array[{}]) <-> vec_low) + (CUBE(array[{}]) <-> vec_high) \
                ASC LIMIT {}".format(
                    ','.join(str(s) for s in enc[0:63]),
                    ','.join(str(s) for s in enc[64:127]),
                    limit,
                )

        return self.db.query(query)