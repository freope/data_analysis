def calculate_ha_open_with_cython(double initial_ha_open, list ha_closings):
    import math
    
    cdef:
        list ha_opens = []
        int ix
        double mean_value
    
    ha_opens.append(initial_ha_open)
    
    for ix in range(len(ha_closings)-1):
        # ともに NaN なら NaN
        if math.isnan(ha_opens[ix]) and math.isnan(ha_closings[ix]):
            ha_opens.append(math.nan)
            continue

        # ha_open だけ NaN なら ha_closing の値を使う
        if math.isnan(ha_opens[ix]):
            ha_opens.append(ha_closings[ix])
            continue

        mean_value = (ha_opens[ix] + ha_closings[ix]) / 2.0
        ha_opens.append(mean_value)
    
    return ha_opens