from zope.interface import interfaces


class IWorkflowChangedEvent(interfaces.IObjectEvent):
    """An object workflow has been modified"""
