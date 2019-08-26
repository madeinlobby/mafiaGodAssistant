def make_reported_string(reasons):
    reason_string = ""
    for reason in reasons:
        reason_string = reason_string + reason.text + ", "

    length = len(reason_string)
    reason_string = reason_string.index(0, length - 1)
    return reason_string


def make_mean(mean, count, number):
    return (mean * count + number) / (count + 1)
