#helpコマンド 全体
commands_description = {
    'help': 'helpコマンド',
    'hello': '社会不適合者による残念な挨拶',
    'chat': '会話モード',
    'learning': '学習モード',
    'poll': '投票コマンド',
    'kyosyu': '挙手コマンド'
}

#コマンドの説明
detailed_commands_description = {
    'help': 'helpコマンド',
    'hello': '元気のない挨拶',
    'chat': 'botと会話するモード',
    'learning': 'botに言葉を学習させるモード',
    'poll': '投票コマンド。タイトル、説明文（任意）、重複投票可能か、選択肢（半角カンマ区切り、最大19択）を入力',
    'kyosyu': '挙手コマンド\n'
            '/kyosyu can - 募集を行う&挙手を行う。timeは半角スペースで区切ると複数挙手可能。typeで確定か仮か補欠か選択、type未入力の場合は確定挙手、memberで他のユーザーの挙手が可能。\n'
            '/kyosyu drop - 挙手を取り下げる。timeに入力された時間の挙手を取り下げる。時間は半角スペースで区切ることで複数指定可能。memberで他のユーザーの挙手の取り下げが可能。\n'
            '/kyosyu now - 現在の募集状況を確認するコマンド。\n'
            '/kyosyu clear - 募集状況をリセットするコマンド。\n'
}