import sqlite3
from typing import List

DEFAULT_GAMES = ["小瓦隆", "雨聲", "龍捲風"]


def get_conn(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reservation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game TEXT NOT NULL UNIQUE,
            user_id TEXT NULL
        )
        """
    )
    conn.commit()


def seed_games(conn: sqlite3.Connection, games: List[str] = DEFAULT_GAMES) -> None:
    # 避免重複插入
    conn.executemany(
        "INSERT OR IGNORE INTO reservation (game, user_id) VALUES (?, NULL)",
        [(g,) for g in games],
    )
    conn.commit()


def list_available_games(conn: sqlite3.Connection) -> List[str]:
    rows = conn.execute(
        "SELECT game FROM reservation WHERE user_id IS NULL ORDER BY game"
    ).fetchall()
    return [r["game"] for r in rows]


def reserve_game(conn: sqlite3.Connection, user_id: str, game_name: str) -> str:
    # 先確認是否有這款遊戲
    exists = conn.execute(
        "SELECT 1 FROM reservation WHERE game = ?",
        (game_name,),
    ).fetchone()
    if not exists:
        return "並沒有此款遊戲"

    # 只允許尚未被預約時更新
    cur = conn.execute(
        """
        UPDATE reservation
        SET user_id = ?
        WHERE game = ? AND user_id IS NULL
        """,
        (user_id, game_name),
    )
    conn.commit()

    if cur.rowcount == 1:
        return f"已為您預約完成：{game_name}"
    return "此遊戲已被預約！抱歉"


def cancel_user_reservations(conn: sqlite3.Connection, user_id: str) -> str:
    cur = conn.execute(
        "UPDATE reservation SET user_id = NULL WHERE user_id = ?",
        (user_id,),
    )
    conn.commit()

    if cur.rowcount >= 1:
        return "已為您取消預約"
    return "您目前沒有預約任何遊戲"
