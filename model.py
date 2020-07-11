from mongoframes import *
from app import Frame


class ShortLink(Frame):
    _fields = {
        'slug',
        'android',
        'ios',
        'web'
    }


class DeviceLink(SubFrame):
    _fields = {
        'primary',
        'fallback'
    }


def add_short_link(short_link):
    short_link.insert()


def get_link_by_slug(slug, show_id=False):
    if show_id:
        return ShortLink.one(Q.slug == slug)
    return ShortLink.one(Q.slug == slug, projection={'_id': False})


def get_all_links():
    return [sl.to_json_type() for sl in ShortLink.many(projection={'_id': False})]

