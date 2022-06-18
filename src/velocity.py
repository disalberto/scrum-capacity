from common import Common
from operator import attrgetter
import wx.adv
from os import listdir

from estimation import Estimation


def compute_velocity(dir_base_path: str, iteration_depth: int) -> float:
    """
    Function to compute the team's velocity
    The input folder is where we find our estimation jsons, having committed and delivered SPs info
    - If it's not the case (either the committed, or the delivered SPs are missing), the file is discarded
    The estimation jsons are then ordered by iteration end date, from the most recent.
    We take into account for the computation the first fullfilled 'iteration_depth' files
    The velocity for each single file is computed by dividing the delivered SPs by the committed ones.
    Then we take the average of the selected files.

    :param dir_base_path: the base path to look for estimation json files
    :param iteration_depth: the number of files to take for computing the velocity
    :returns: the team velocity
    :rtype: float
    """
    fullpath_list = [f"{dir_base_path}/{x}" for x in listdir(dir_base_path)]

    estimations = []
    for file in fullpath_list:
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
