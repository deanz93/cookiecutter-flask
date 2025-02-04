"""
Database core module.

This module provides a mixin class for SQLAlchemy models.
"""


class Mixin:
    """Utility Base Class for SQLAlchemy Models.
    Adds `to_dict()` to easily serialize objects to dictionaries.
    """

    def to_dict(self, exclude: list = None) -> dict:
        """
        Converts the object's attributes to a dictionary.
        Args:
            exclude (list): A list of attribute names to exclude from the dictionary.

        Returns:
            dict: A dictionary containing the object's attributes.
        """
        if exclude is None:
            exclude = []
        d_out = {key: val for key, val in self.__dict__.items() if key not in exclude}
        d_out.pop("_sa_instance_state", None)
        d_out["_id"] = d_out.pop("id", None)  # rename id key to interface with response
        return d_out
