from typing import Optional, Union
from pythonpackages.nqtr.disabled_solution import DisabledClass

from pythonpackages.renpy_utility.flags import *
from pythonpackages.renpy_utility.renpy_custom_log import *
from pythonpackages.renpy_utility.utility import *


class Button(DisabledClass):
    """Wiki: https://github.com/DRincs-Productions/NQTR-toolkit/wiki/Button"""

    def __init__(
        self,
        name: Optional[str] = None,
        label_name: Optional[str] = None,
        button_icon: Optional[str] = None,
        button_icon_selected: Optional[str] = None,
        picture_in_background: Optional[str] = None,
        picture_in_background_selected: Optional[str] = None,
        xalign: Optional[Union[int, float]] = None,
        yalign: Optional[Union[int, float]] = None,
        disabled: Union[bool, str] = False,
        hidden: Union[bool, str] = False,
        default_label_name: Optional[str] = None,
    ):
        # DisabledClass init
        super().__init__(disabled=disabled)
        # Button init
        self.align = None

        self.name = name
        self.label_name = label_name
        self.button_icon = button_icon
        self.button_icon_selected = button_icon_selected
        self.picture_in_background = picture_in_background
        self.picture_in_background_selected = picture_in_background_selected
        if not xalign == None:
            self.xalign = xalign
        if not yalign == None:
            self.yalign = yalign
        self.hidden = hidden
        self.default_label_name = default_label_name

    @property
    def name(self) -> str:
        """Button name or id, is used to identify the button and in logs"""
        return self._name

    @name.setter
    def name(self, value: Optional[str]):
        self._name = value or ""
        if isNullOrEmpty(self._name):
            log_warn("You have set name to None or empty", "nqtr.button.Button.name")

    @property
    def label_name(self) -> Optional[str]:
        """onClick label name"""
        if not isNullOrEmpty(self._label_name):
            return self._label_name
        elif not isNullOrEmpty(self.default_label_name):
            return self.default_label_name
        else:
            log_warn(
                "In the button " + self.name + ", label_name is null or empty",
                "nqtr.button.Button.label_name",
            )
        return

    @label_name.setter
    def label_name(self, value: Optional[str]):
        self._label_name = value

    @property
    def button_icon(self) -> Optional[str]:
        """Button icon"""
        if not isNullOrEmpty(self._button_icon):
            return self._button_icon
        else:
            log_warn(
                "In the button "
                + self.name
                + ", button_icon is null or empty, use is_button_icon to check if it is a button icon button",
                "nqtr.button.Button.button_icon",
            )
            return None

    @button_icon.setter
    def button_icon(self, value: Optional[str]):
        self._button_icon = value

    @property
    def button_icon_selected(self) -> Optional[str]:
        """Selected button icon"""
        if not isNullOrEmpty(self._button_icon_selected):
            return self._button_icon_selected
        else:
            return self.button_icon

    @button_icon_selected.setter
    def button_icon_selected(self, value: Optional[str]):
        self._button_icon_selected = value

    @property
    def picture_in_background(self) -> Optional[str]:
        """Picture in background: Is an button that is started by clicking on an image in the room."""
        if not isNullOrEmpty(self._picture_in_background):
            return self._picture_in_background
        else:
            log_warn(
                "In the button "
                + self.name
                + ", picture_in_background is null or empty, use is_picture_in_background to check if it is a picture in background button",
                "nqtr.button.Button.picture_in_background",
            )
            return None

    @picture_in_background.setter
    def picture_in_background(self, value: Optional[str]):
        self._picture_in_background = value

    @property
    def picture_in_background_selected(self) -> Optional[str]:
        """Selected picture in background"""
        if not isNullOrEmpty(self._picture_in_background_selected):
            return self._picture_in_background_selected
        else:
            return self.picture_in_background

    @picture_in_background_selected.setter
    def picture_in_background_selected(self, value: Optional[str]):
        self._picture_in_background_selected = value

    @property
    def align(self) -> Optional[tuple[Union[int, float], Union[int, float]]]:
        """X align"""
        return self._align

    @align.setter
    def align(self, value: Optional[tuple[Union[int, float], Union[int, float]]]):
        self._align = value

    @property
    def xalign(self) -> Union[int, float]:
        """X align"""
        if self._align != None:
            return self._align[0]
        else:
            log_warn(
                "In the button "
                + self.name
                + ", you have set align to None, so return 0",
                "nqtr.button.Button.xalign",
            )
            return 0

    @xalign.setter
    def xalign(self, value: Optional[Union[int, float]]):
        if value == None:
            log_warn(
                "In the button "
                + self.name
                + ", you have set xalign to None, use 0 instead",
                "nqtr.button.Button.xalign",
            )
            value = 0
        if self._align == None:
            self._align = (value, 0)
        else:
            self._align = (value, self._align[1])

    @property
    def yalign(self) -> Union[int, float]:
        """Y align"""
        if self._align != None:
            return self._align[1]
        else:
            log_warn(
                "In the button "
                + self.name
                + ", you have set align to None, so return 0",
                "nqtr.button.Button.yalign",
            )
            return 0

    @yalign.setter
    def yalign(self, value: Optional[Union[int, float]]):
        if value == None:
            log_warn(
                "In the button "
                + self.name
                + ", you have set yalign to None, use 0 instead",
                "nqtr.button.Button.yalign",
            )
            value = 0
        if self._align == None:
            self._align = (0, value)
        else:
            self._align = (self._align[0], value)

    @property
    def hidden(self) -> Union[bool, str]:
        """Hidden"""
        return self._hidden

    @hidden.setter
    def hidden(self, value: Union[bool, str]):
        self._hidden = value

    @property
    def default_label_name(self) -> Optional[str]:
        """Default label name"""
        return self._default_label_name

    @default_label_name.setter
    def default_label_name(self, value: Optional[str]):
        self._default_label_name = value

    @property
    def is_button(self) -> bool:
        """This is a button?"""
        return not isNullOrEmpty(self._button_icon)

    @property
    def is_picture_in_background(self) -> bool:
        """This is a is picture in background?"""
        return not isNullOrEmpty(self._picture_in_background)

    def is_hidden(
        self, flags: dict[str, bool] = {}, check_if_has_icon: bool = True
    ) -> bool:
        """ "If hidden is a string: get the value of the flags system"""
        if isinstance(self.hidden, str):
            return get_flags(self.hidden, flags)
        elif (
            check_if_has_icon
            and not self.is_button
            and not self.is_picture_in_background
        ):
            return True
        else:
            return self.hidden
