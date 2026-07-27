
"""
کلاس Match - نماینده یک مسابقه
"""

from team import Team


class Match:
    """
    کلاس مدیریت یک مسابقه بین دو تیم.
    """

    def __init__(self, team1, team2, is_knockout=False):
        """
        سازنده کلاس Match.

        Args:
            team1 (Team): تیم اول
            team2 (Team): تیم دوم
            is_knockout (bool): آیا مسابقه حذفی است؟
        """
        self.team1 = team1
        self.team2 = team2
        self.is_knockout = is_knockout
        self.goals1 = 0
        self.goals2 = 0
        self.winner = None
        self.penalty_text = ""

    def play(self):
        """
        اجرای مسابقه و ذخیره نتیجه.

        Returns:
            Team or None: برنده مسابقه (یا None در صورت تساوی در گروهی)
        """
        g1, g2, winner, pen = self.team1.simulate_match(self.team2, self.is_knockout)

        self.goals1 = g1
        self.goals2 = g2
        self.winner = winner
        self.penalty_text = pen

        self.team1.goals_for += g1
        self.team1.goals_against += g2
        self.team2.goals_for += g2
        self.team2.goals_against += g1

        if not self.is_knockout:
            if g1 > g2:
                self.team1.points += 3
            elif g2 > g1:
                self.team2.points += 3
            else:
                self.team1.points += 1
                self.team2.points += 1

        return self.winner