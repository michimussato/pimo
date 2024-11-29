import pytest
from pimo import pimo
import pathlib

__author__ = "Michael Mussato"
__copyright__ = "Michael Mussato"
__license__ = "MIT"


def test_init_files():
    from pimo.pimo import init_files
    from pimo.pimo import (PIMO_FILES,
                           PIMO_DOWNVOTED,
                           PIMO_UPVOTED,
                           PIMO_CURRENT,
                           PIMO_HISTORY)

    init_files()

    assert PIMO_FILES.exists() and PIMO_FILES.is_dir()
    assert PIMO_DOWNVOTED.exists() and PIMO_DOWNVOTED.is_file()
    assert PIMO_UPVOTED.exists() and PIMO_UPVOTED.is_file()
    assert PIMO_CURRENT.exists() and PIMO_CURRENT.is_file()
    assert PIMO_HISTORY.exists() and PIMO_HISTORY.is_file()


@pytest.mark.parametrize("match_aspect", [True, False])
@pytest.mark.parametrize("frame_orientation", pimo.ORIENTATION)
@pytest.mark.parametrize("ascii_art", [True, False])
@pytest.mark.parametrize("ascii_art", [False])
def test_get_rand_image_local(match_aspect, frame_orientation, ascii_art):

    from pimo.pimo import get_rand_image

    rand_image = get_rand_image(
        match_aspect=match_aspect,
        frame_orientation=frame_orientation,
        search_dir=pathlib.Path(__file__).parent / "fixtures" / "LOCAL",
        ascii_art=ascii_art
    )

    assert isinstance(rand_image, pathlib.Path)


# @pytest.mark.parametrize("match_aspect", [True, False])
# @pytest.mark.parametrize("frame_orientation", pimo.ORIENTATION)
# # @pytest.mark.parametrize("ascii_art", [True, False])
# @pytest.mark.parametrize("ascii_art", [False])
# def test_get_rand_image_local_empty(match_aspect, frame_orientation, ascii_art):
#
#     from pimo.pimo import get_rand_image
#
#     with pytest.raises(Exception):
#         rand_image = get_rand_image(
#             match_aspect=match_aspect,
#             frame_orientation=frame_orientation,
#             search_dir=pathlib.Path(__file__).parent / "fixtures" / "LOCAL_EMPTY",
#             ascii_art=ascii_art
#         )
#
#     # assert isinstance(rand_image, pathlib.Path)
