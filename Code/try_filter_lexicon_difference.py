with (
    open('lexicon_difference.txt') as file_in,
    open('lexicon_difference_worst.txt', 'w') as file_out,
):
    for line in file_in:
        if (
            len(line) > 2 and (
                len(line) < 10 or (
                    line[3:7] != '0.00' and line[9] != '0'
                )
            )
        ):
            file_out.write(line)
