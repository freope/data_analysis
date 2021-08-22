def new_string(existing_strings=[], length=16, max_trial=100):
    import secrets

    trial = 1
    new_str = secrets.token_hex(length)

    while new_str in existing_strings:
        # 最大試行回数を上回っても新しい文字列を
        # 生成できない場合に例外を発生
        if max_trial == trial:
            raise Exception

        trial += 1
        new_str = secrets.token_hex(length)
                
    return new_str