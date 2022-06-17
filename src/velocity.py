from common import Common
from operator import attrgetter
import wx.adv
from os import listdir

from estimation import Estimation


def compute_velocity(dir_base_path: str, iteration_depth: int):

    fullpath_list = [f"{dir_base_path}/{x}" for x in listdir(dir_base_path)]

    estimations = []
    for file in fullpath_list:
        # TODO externalize this method
        try:
            estimation = Estimation.parse_file(file)
            estimations.append(estimation)

        except IOError:
            wx.LogError("Error parsing or opening '%s'." % file)

    good_estimations = [
        est
        for est in estimations
        if est.delivered_sp is not None and est.committed_sp is not None
    ]

    good_sorted_estimations = sorted(
        good_estimations, key=attrgetter("date_to"), reverse=True
    )
    sorted_reduced_estimations = good_sorted_estimations[0:iteration_depth]

    total_vel: float = 0.0
    for est in sorted_reduced_estimations:
        vel: float = est.delivered_sp / est.committed_sp
        total_vel += vel

    team_velocity = round(
        total_vel / len(sorted_reduced_estimations), Common.ROUND_PRECISION
    )

    return team_velocity
