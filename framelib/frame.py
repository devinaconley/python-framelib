"""
methods for frame rendering and message handling
"""

# lib
import json
from importlib import resources
from typing import Literal
from flask import render_template_string, request, make_response, Response

# src
from .models import FrameMessage

# enum types
ButtonActions = Literal['post', 'post_redirect', 'mint', 'link']


def render_frame(
        title: str = None,
        image: str = None,
        content: str = None,
        post_url: str = None,
        button1: str = None,
        button1_action: ButtonActions = None,
        button1_target: str = None,
        button2: str = None,
        button2_action: ButtonActions = None,
        button2_target: str = None,
        button3: str = None,
        button3_action: ButtonActions = None,
        button3_target: str = None,
        button4: str = None,
        button4_action: ButtonActions = None,
        button4_target: str = None,
        input_text: str = None
) -> Response:
    # TODO support cache age, aspect ratio, state data

    # setup context
    # note: we do this because jinja treats None as a defined value
    ctx = {k: v for k, v in locals().items() if v is not None}

    # load template from module data
    pth = resources.files('framelib') / 'templates' / 'frame.html'
    with open(str(pth), 'r') as f:
        src = f.read()

    # render frame template
    html = render_template_string(src, **ctx)

    # response
    res = make_response(html)
    res.status_code = 200
    return res


def message() -> FrameMessage:
    # parse action message
    body = json.loads(request.data)
    msg = FrameMessage(**body)
    return msg