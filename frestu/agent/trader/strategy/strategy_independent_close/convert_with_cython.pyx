def convert_with_cython(
        list opening_timestamps, list closing_timestamps, list closing_times):
    cdef:
        int is_the_last = 1
        list dependent_closing_times = []
        int i_closing
        double closing_timestamp
        double opening_timestamp

    for opening_timestamp in opening_timestamps:
        is_the_last = 1

        # NOTE: opening_timestamps のソートを強制していないので、
        # 計算量が O(n**2) となっている。
        for i_closing, closing_timestamp in enumerate(closing_timestamps):
            if opening_timestamp < closing_timestamp:
                dependent_closing_times.append(closing_times[i_closing])
                is_the_last *= -1
                break

        if 0 < is_the_last:
            dependent_closing_times.append(None)

    return dependent_closing_times