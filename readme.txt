
# to inspect
sqlite3 db.sqlite3

.exit

# insert 
CREATE TABLE dating_aimatch (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user1_id INTEGER,
    user2_id INTEGER,
    message TEXT,
    FOREIGN KEY (user1_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (user2_id) REFERENCES auth_user(id) ON DELETE CASCADE
);


# google signin
pip install google-auth



python manage.py migrate dating zero
python manage.py migrate dating zero --fake  ///Fake the initial migration removal




### remove all migration

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
