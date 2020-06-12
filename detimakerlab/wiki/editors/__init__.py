from django.urls.utils import get_callable

from detimakerlab.wiki.conf import settings

_EditorClass = None
_editor = None


def getEditorClass():
    global _EditorClass
    if not _EditorClass:
        _EditorClass = get_callable(settings.EDITOR)
    return _EditorClass


def getEditor():
    global _editor
    if not _editor:
        _editor = getEditorClass()()
    return _editor
