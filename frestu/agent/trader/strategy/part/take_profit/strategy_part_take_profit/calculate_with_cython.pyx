def calculate_with_cython(
        list opening_times, list rates, dict time_to_ix, dict ix_to_time,
        double taking_rate, str position_type):
    cdef:
        int len_rates = len(rates)
        int is_the_last = 1
        list closing_times = []
        str closing_time
        int opening_ix
        int closing_ix
        double opening_rate
        double closing_rate
        double take_profit_rate

    if position_type == 'long':

        for opening_time in opening_times:
            opening_ix = time_to_ix[opening_time]
            opening_rate = rates[opening_ix]

            is_the_last = 1

            take_profit_rate = opening_rate + taking_rate
            for closing_ix in range(opening_ix, len_rates):
                closing_rate = rates[closing_ix]
                if closing_rate >= take_profit_rate:
                    closing_time = ix_to_time[closing_ix]
                    closing_times.append(closing_time)
                    is_the_last *= -1
                    break

            # ロスカットが行われない場合
            if 0 < is_the_last:
                closing_times.append(None)

    elif position_type == 'short':
    
        for opening_time in opening_times:
            opening_ix = time_to_ix[opening_time]
            opening_rate = rates[opening_ix]

            is_the_last = 1

            take_profit_rate = opening_rate - taking_rate
            for closing_ix in range(opening_ix, len_rates):
                closing_rate = rates[closing_ix]
                if closing_rate <= take_profit_rate:
                    closing_time = ix_to_time[closing_ix]
                    closing_times.append(closing_time)
                    is_the_last *= -1
                    break

            # ロスカットが行われない場合
            if 0 < is_the_last:
                closing_times.append(None)
    
    return closing_times