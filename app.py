from reservation_db import (
    get_conn,
    init_db,
    seed_games,
    list_available_games,
    reserve_game,
    cancel_user_reservations,
)

DB_PATH = "game.db"

HELP_TEXT = """\
可用指令：
- 想看遊戲種類
- 想預約<遊戲名稱>   例：想預約小瓦隆
- 想取消預約
- 結束
"""


def main() -> None:
    user_id = "小明"  # 你也可以改成 input() 或外部系統帶入

    conn = get_conn(DB_PATH)
    init_db(conn)
    seed_games(conn)

    print("遊戲預約系統啟動！")
    print(HELP_TEXT)

    while True:
        msg = input("輸入訊息：").strip()

        if msg == "結束":
            print("已結束，Bye!")
            break

        if msg == "想看遊戲種類":
            games = list_available_games(conn)
            if not games:
                print("尚可預約遊戲：\n（目前沒有可預約的遊戲）")
            else:
                print("尚可預約遊戲：\n" + "\n".join(games))

        elif msg.startswith("想預約"):
            game_name = msg.replace("想預約", "", 1).strip()
            if not game_name:
                print("格式錯誤：請輸入 想預約<遊戲名稱>（例：想預約小瓦隆）")
            else:
                print(reserve_game(conn, user_id, game_name))

        elif msg == "想取消預約":
            print(cancel_user_reservations(conn, user_id))

        else:
            print("您好！請問需要什麼樣的服務？（輸入「想看遊戲種類」查看指令）")

        print("------------------")


if __name__ == "__main__":
    main()
