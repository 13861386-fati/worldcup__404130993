	
"""
کلاس Group - نماینده یک گروه در مرحله گروهی
"""

from match import Match


class Group:
    """
    کلاس مدیریت یک گروه در مرحله گروهی.
    """

    def __init__(self, name, teams):
        """
        سازنده کلاس Group.

        Args:
            name (str): نام گروه (A, B, ...)
            teams (list): لیست 4 تیم گروه
        """
        self.name = name
        self.teams = teams
        self.match_history = []

    def play_all_matches(self):
        """
        اجرای تمام مسابقات گروه (هر تیم با هر تیم دیگر).
        """
        self.match_history = []

        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                match = Match(self.teams[i], self.teams[j], is_knockout=False)
                match.play()
                self.match_history.append(match)

    def get_ranking(self):
        """
        رتبه‌بندی تیم‌های گروه.

        معیارها (به ترتیب):
        1. امتیاز
        2. تفاضل گل
        3. گل زده
        4. قانون بازی مستقیم (Head-to-Head)

        Returns:
            list: لیست تیم‌های مرتب‌شده
        """
        sorted_teams = sorted(
            self.teams,
            key=lambda t: (t.points, t.goal_difference(), t.goals_for),
            reverse=True
        )

        for i in range(len(sorted_teams) - 1):
            t1 = sorted_teams[i]
            t2 = sorted_teams[i + 1]

            if (t1.points == t2.points and
                t1.goal_difference() == t2.goal_difference() and
                t1.goals_for == t2.goals_for):

                for m in self.match_history:
                    if (m.team1 == t1 and m.team2 == t2) or (m.team1 == t2 and m.team2 == t1):
                        if (m.team1 == t2 and m.goals1 > m.goals2) or (m.team2 == t2 and m.goals2 > m.goals1):
                            sorted_teams[i], sorted_teams[i + 1] = sorted_teams[i + 1], sorted_teams[i]
                        break

        return sorted_teams

    def advance_teams(self):
        """
        برگرداندن دو تیم اول گروه برای صعود به مرحله حذفی.

        Returns:
            tuple: (تیم_اول, تیم_دوم)
        """
        ranking = self.get_ranking()
        return ranking[0], ranking[1]