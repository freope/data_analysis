def extract_with_cython(list rates, double step_af, double af_max):
    cdef:
        int is_rising = 1
        int ix_switching = 0
        double ep = rates[0]
        double af = 0
        double sar = rates[0]
        list parabolic_sar = []
        int ix
        double rate
        double ep_last
        double sar_last
    
    def __update_ep(ix):
        nonlocal is_rising
        nonlocal ix_switching
        nonlocal ep

        if is_rising > 0:
            ep = max(rates[ix_switching:ix+1])
        else:
            ep = min(rates[ix_switching:ix+1])
    
    def __update_af():
        nonlocal is_rising
        nonlocal ep
        nonlocal ep_last
        nonlocal af
        
        # 上昇トレンド中に EP の最大値が更新されるか、
        # 下降トレンド中に EP の最小値が更新される場合、af を更新
        if ((is_rising > 0 and ep_last < ep)
                or (is_rising < 0 and ep < ep_last)):
            af += step_af

        if af_max < af:
            af = af_max

    for ix, rate in enumerate(rates):
        sar_last = sar
        ep_last = ep
        
        # EP を更新
        __update_ep(ix)

        # AF を更新
        __update_af()

        # SAR を計算
        sar = (ep - sar_last) * af + sar_last

        # 上昇トレンド中に SAR がデータを超えるか、
        # 下降トレンド中に SAR がデータを下回ると切り替え
        if ((is_rising > 0 and rate < sar)
                or (is_rising < 0 and sar < rate)):
            is_rising *= -1
            af = step_af
            sar = ep
            ix_switching = ix

        parabolic_sar.append(sar)

    return parabolic_sar