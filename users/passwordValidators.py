from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import re


class ComplexPasswordValidator:
    """
    Validate whether the password contains minimum one uppercase and one digit.
    """
    def validate(self, password, user=None):
        if re.search('[A-Z]', password) is None or re.search('[0-9]', password) is None:
            raise ValidationError(
                _("This password is not enough strong! It does not contain uppercase or number."),
                code='password_is_weak',
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 number and 1 uppercase.")
