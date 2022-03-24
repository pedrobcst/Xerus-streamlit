from Xerus import XRay


def run_xerus(args_xerus: dict, args_analysis: dict) -> XRay:
    xerus_object = XRay(**args_xerus)
    xerus_object.analyze(**args_analysis)
    return xerus_object
