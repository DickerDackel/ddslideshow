image_filter = lambda strip: strip.type == 'IMAGE'  # noqa: E731
transform_filter = lambda strip: strip.type == 'TRANSFORM'  # noqa: E731


def grep(match_fkt, sequence):
    return filter(match_fkt, sequence)


def select(sequence, value=True):
    for strip in sequence:
        strip.select = value


def deselect(sequence):
    select(sequence, False)
