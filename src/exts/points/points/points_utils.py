from interactions.api.events import MessageCreate
from sqlite3 import Connection


def add_points(conn, db: Connection, ctx: MessageCreate):
    msg = ctx.message
    user = msg.author.display_name
    embed = msg.embeds
    attachments = msg.attachments

    points = 0
    points = points + 1
    points = points + (2 if len(embed) > 0 else 0)
    points = points + (3 if len(attachments) > 0 else 0)

    user_points = retrieve_user_points(conn, db, user)
    print(f'{user} currently has {user_points} points!')

    new_total = user_points + points
    update_user_points(conn, db, user, new_total)

    user_points = retrieve_user_points(conn, db, user)
    print(f'Updated Points! {user} now has {user_points} points!')


def retrieve_user_points(conn, db: Connection, user: str):
    results = db.execute('SELECT Points FROM points WHERE User = ?', (user,)).fetchone()
    user_points = results[0] if results else 0  # Handles if results is null or not
    return user_points


def update_user_points(conn, db: Connection, user: str, points: int):
    db.execute('INSERT OR REPLACE INTO points (User, Points) VALUES (?, ?)', (user, points))
    conn.commit()
