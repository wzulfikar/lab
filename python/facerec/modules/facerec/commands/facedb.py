import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import db

description = "search profile or display stats from face recognition db"
usage = "usage: facedb --stat|<name>|<filename>"

def command(args):
    if len(args) < 1:
        print('facedb:', description)
        print(usage)
        exit(1)

    main(*args)


def main(option: str):
    db_conn = db.open()
    if option == "--stat":
        print('showing stats from face recognition db:')
        _showstat(db_conn)
    else:
        _findprofile(db_conn, option)


def _findprofile(db, name_or_file: str) -> None:
    like_tpl = "{} ILIKE '%' || '{}' || '%'"
    query = "SELECT p.id as profile_id, p.name as name, file \
            FROM vectors  v \
            LEFT OUTER JOIN profiles p ON v.profile_id = p.id \
            WHERE {} OR {} \
            ORDER BY p.id".format(like_tpl.format("p.name", name_or_file),
                                  like_tpl.format("file", name_or_file))

    rows = db.query(query)

    profiles = {}
    for row in rows:
        p_id, name, file = row
        if p_id not in profiles:
            profiles[p_id] = {'name': name, 'files': []}
        profiles[p_id]['files'].append(file)

    counter = 0
    for p_id, p in profiles.items():
        counter += 1
        print('''
{}. P.ID: {}
   Name: {}
   Files ({}):
   {}'''.format(counter, p_id, p['name'], len(p['files']), p['files']))

    print()
    print("[DONE] Results found:", len(rows))


def _showstat(db) -> None:
    count_profiles = db.query("SELECT COUNT(*) FROM profiles")
    count_vectors = db.query("SELECT COUNT(*) FROM vectors")
    vectors_without_profiles = db.query(
        "SELECT COUNT(*) FROM vectors WHERE profile_id IS NULL")
    profiles_without_vectors = db.query("SELECT id, name FROM profiles \
                                        WHERE id NOT IN \
                                        (SELECT profile_id FROM vectors)")
    profiles_with_multiple_vectors = db.query("SELECT COUNT(p.id) FROM \
                                              (SELECT COUNT(v.id) id FROM \
                                              profiles p JOIN vectors v \
                                              on p.id = v.profile_id \
                                              GROUP BY p.id \
                                              HAVING COUNT(v.id) > 1) AS p")

    print("""
- # of vectors: {}
- # of profiles: {}
- vectors without profile: {}
- profiles with multiple vectors: {}
- profiles with no vectors ({}):""".format(count_vectors[0][0],
                                           count_profiles[0][0],
                                           vectors_without_profiles[0][0],
                                           profiles_with_multiple_vectors[0][0],
                                           len(profiles_without_vectors)))

    count_max = 5
    count = 0
    for p in profiles_without_vectors:
        count += 1
        print("  Profile #{} - {}".format(p[0], p[1]))
        
        if count == count_max:
            print("  ..and {} more".format(len(profiles_without_vectors) - count_max))
            break

