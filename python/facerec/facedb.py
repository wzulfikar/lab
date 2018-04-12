import sys
import postgresql

if len(sys.argv) < 1:
    print("Usage: facedb --stat|<name>|<filename>")
    exit(1)

print("Connecting to DB..")
db = postgresql.open('pq://user:pass@localhost:5434/db')
print("DB connected ✔")


def findprofile(arg: str) -> None:
    like_tpl = "{} ILIKE '%' || '{}' || '%'"
    query = "SELECT p.id as profile_id, p.name as name, file \
            FROM vectors  v \
            LEFT OUTER JOIN profiles p ON v.profile_id = p.id \
            WHERE {} OR {} \
            ORDER BY p.id".format(like_tpl.format("p.name", arg),
                                  like_tpl.format("file", arg))

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


def showstat() -> None:
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

    for p in profiles_without_vectors:
        print("  Profile #{} - {}".format(p[0], p[1]))


arg = sys.argv[1]
if arg == "--stat":
    showstat()
else:
    findprofile(arg)
