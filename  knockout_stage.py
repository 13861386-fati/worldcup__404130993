
"""
کلاس KnockoutStage - مدیریت یک مرحله از مراحل حذفی
"""

from match import Match


class KnockoutStage:
    """
    کلاس مدیریت یک مرحله از مراحل حذفی.
    """

    def __init__(self, round_name, matches):
        """
        سازنده کلاس KnockoutStage.

        Args:
            round_name (str): نام مرحله (مثل Round of 16)
            matches (list): لیست مسابقات آن مرحله
        """
        self.round_name = round_name
        self.matches = matches

    def play_round(self):
        """
        اجرای تمام مسابقات این مرحله.
        """
        for match in self.matches:
            match.play()

    def get_winners(self):
        """
        برگرداندن لیست برندگان این مرحله.

        Returns:
            list: لیست تیم‌های برنده
        """
        return [match.winner for match in self.matches if match.winner is not None]