"""
کلاس Team - نماینده یک تیم ملی
"""

import random
from utils import poisson_simple


class Team:
    """
    کلاس تیم ملی فوتبال.

    این کلاس اطلاعات پایه، آمار مسابقات و متدهای مربوط به شبیه‌سازی یک تیم را نگهداری می‌کند.
    """

    def __init__(self, name, attack, defense, rank):
        """
        سازنده کلاس Team.

        Args:
            name (str): نام تیم
            attack (int): قدرت حمله (عدد بین 1 تا 100)
            defense (int): قدرت دفاع (عدد بین 1 تا 100)
            rank (int): رتبه فیفا (1 بهترین)
        """
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = ""

    def goal_difference(self):
        """
        محاسبه تفاضل گل تیم.

        Returns:
            int: تفاضل گل (گل زده منهای گل خورده)
        """
        return self.goals_for - self.goals_against

    def reset_stats(self):
        """
        ریست کردن آمار تیم برای شروع یک شبیه‌سازی جدید.
        """
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def simulate_match(self, opponent, is_knockout=False):
        """
        شبیه‌سازی یک مسابقه بین دو تیم.

        Args:
            opponent (Team): تیم حریف
            is_knockout (bool): آیا بازی در مرحله حذفی است؟

        Returns:
            tuple: (گل_خودی, گل_حریف, برنده, نتیجه_پنالتی)
        """
        self_exp = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        opp_exp = (opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8

        self_goals = poisson_simple(self_exp)
        opp_goals = poisson_simple(opp_exp)

        if is_knockout and self_goals == opp_goals:
            self_goals += poisson_simple(self_exp * 0.33)
            opp_goals += poisson_simple(opp_exp * 0.33)

        winner = None
        penalty_text = ""

        if is_knockout and self_goals == opp_goals:
            self_prob = 0.75 + (self.attack - opponent.defense) / 250
            opp_prob = 0.75 + (opponent.attack - self.defense) / 250

            self_prob = max(0.09, min(0.99, self_prob))
            opp_prob = max(0.09, min(0.99, opp_prob))

            self_pens = sum(1 for _ in range(5) if random.random() < self_prob)
            opp_pens = sum(1 for _ in range(5) if random.random() < opp_prob)

            while self_pens == opp_pens:
                self_pens += 1 if random.random() < self_prob else 0
                opp_pens += 1 if random.random() < opp_prob else 0

            penalty_text = f" ({self_pens}-{opp_pens} pens)"
            winner = self if self_pens > opp_pens else opponent

        elif self_goals > opp_goals:
            winner = self
        elif opp_goals > self_goals:
            winner = opponent

        return self_goals, opp_goals, winner, penalty_text