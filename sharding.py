shard_id = {
    "urn:cts:latinLit:stoa00": 1,
    "urn:cts:latinLit:stoa01": 2,
    "urn:cts:latinLit:phi0": 3,
    "urn:cts:latinLit:phi-rest": 4,
    "urn:cts:latinLit-rest": 5,
    "urn:cts:greekLit:tlg000": 6,
    "urn:cts:greekLit:tlg005": 7,
    "urn:cts:greekLit:tlg006": 8,
    "urn:cts:greekLit:tlg008": 9,
    "urn:cts:greekLit:tlg00-rest": 10,
    "urn:cts:greekLit:tlg052": 11,
    "urn:cts:greekLit:tlg05-rest": 12,
    "urn:cts:greekLit:tlg06": 13,
    "urn:cts:greekLit:tlg0-rest": 14,
    "urn:cts:greekLit:tlg204": 15,
    "urn:cts:greekLit:tlg20-rest": 16,
    "urn:cts:greekLit:tlg2-rest": 17,
    "urn:cts:greekLit:tlg401": 18,
    "urn:cts:greekLit:tlg40": 19,
    "urn:cts:greekLit:tlg4-rest": 20,
    "urn:cts:greekLit:tlg5-rest": 21,
    "urn:cts:greekLit:tlg-rest": 22,
    "urn:cts:greekLit-rest": 23,
}

def get_shard_id(urn_prefix, group):
    if urn_prefix == "urn:cts:greekLit":
        if group.startswith("tlg"):
            if group.startswith(("tlg0", "tlg2", "tlg4", "tlg5")):
                if group.startswith(("tlg00", "tlg05", "tlg06")):
                    if group.startswith(("tlg000", "tlg005", "tlg008", "tlg006")):
                        shard = urn_prefix + ":" + group[:6]
                    elif group.startswith(("tlg052")):
                        shard = urn_prefix + ":" + group[:6]
                    elif group.startswith(("tlg06")):
                        shard = urn_prefix + ":" + group[:5]
                    else:
                        shard = urn_prefix + ":" + group[:5] + "-rest"
                elif group.startswith(("tlg20")):
                    if group.startswith(("tlg204")):
                        shard = urn_prefix + ":" + group[:6]
                    else:
                        shard = urn_prefix + ":" + group[:5] + "-rest"
                elif group.startswith(("tlg40")):
                    if group.startswith(("tlg401")):
                        shard = urn_prefix + ":" + group[:6]
                    else:
                        shard = urn_prefix + ":" + group[:5]
                else:
                    shard = urn_prefix + ":" + group[:4] + "-rest"
            else:
                shard = urn_prefix + ":tlg-rest"
        else:
            shard = urn_prefix + "-rest"
    elif urn_prefix == "urn:cts:latinLit":
        if group.startswith(("stoa00", "stoa01")):
            shard = urn_prefix + ":" + group[:6]
        elif group.startswith("phi"):
            if group.startswith("phi0"):
                shard = urn_prefix + ":phi0"
            else:
                shard = urn_prefix + ":phi-rest"
        else:
            shard = urn_prefix + "-rest"
    else:
        raise ValueError(urn_prefix)

    return shard_id[shard]
