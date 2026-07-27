
"""
کلاس WorldCupSimulator - هسته اصلی شبیه‌ساز
"""

import csv
import os
import random

from team import Team
from group import Group
from knockout_stage import KnockoutStage
from match import Match


class WorldCupSimulator:
    """
    کلاس اصلی شبیه‌ساز جام جهانی.

    این کلاس تمام مراحل تورنمنت را مدیریت می‌کند: بارگذاری، قرعه‌کشی، مرحله گروهی، حذفی، شبیه‌سازی ۱۰۰۰ باره و نمایش براکت.
    """

    def __init__(self):
        """سازنده کلاس WorldCupSimulator."""
        self.teams = []
        self.groups = []
        self.champion = None
        self.bracket_matches = []
        self.groups_drawn = False
        self.group_stage_completed = False
        self.knockout_completed = False

    def load_teams_from_csv(self, filename):
        """
        بارگذاری تیم‌ها از فایل CSV.

        Args:
            filename (str): نام فایل CSV

        Returns:
            bool: موفقیت یا شکست عملیات
        """
        if not os.path.exists(filename):
            print(f"خطا: فایل '{filename}' پیدا نشد!")
            return False

        try:
            self.teams = []

            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    self.teams.append(Team(
                        name=row['name'].strip(),
                        attack=int(row['attack']),
                        defense=int(row['defense']),
                        rank=int(row['rank'])
                    ))

            if len(self.teams) != 32:
                print(f"خطا: تعداد تیم‌ها {len(self.teams)} است (باید 32 باشد).")
                return False

            print(f"موفقیت: 32 تیم با موفقیت بارگذاری شدند.")
            return True

        except Exception as e:
            print(f"خطا در خواندن فایل: {e}")
            return False

    def reset_tournament(self):
        """
        بازنشانی کامل آمار تیم‌ها و وضعیت مراحل تورنمنت برای شبیه‌سازی مجدد.
        """
        for t in self.teams:
            t.reset_stats()
        self.groups = []
        self.champion = None
        self.bracket_matches = []
        self.groups_drawn = False
        self.group_stage_completed = False
        self.knockout_completed = False

    def seed_and_draw_groups(self, display=True):
        """
        قرعه‌کشی گروه‌ها بر اساس سیدبندی (رنکینگ فیفا).

        Args:
            display (bool): آیا پیام‌ها نمایش داده شوند؟
        """
        if self.groups_drawn:
            if display:
                print("قرعه‌کشی قبلاً انجام شده است.")
            return

        if len(self.teams) != 32:
            print("خطا: دقیقاً 32 تیم نیاز است.")
            return

        sorted_teams = sorted(self.teams, key=lambda t: t.rank)

        seeds = [
            sorted_teams[0:8],
            sorted_teams[8:16],
            sorted_teams[16:24],
            sorted_teams[24:32]
        ]

        group_names = "ABCDEFGH"
        self.groups = []

        for g in range(8):
            group_teams = []

            for s in range(4):
                chosen = random.choice(seeds[s])
                group_teams.append(chosen)
                seeds[s].remove(chosen)

            self.groups.append(Group(group_names[g], group_teams))

        self.groups_drawn = True

        if display:
            print("قرعه‌کشی گروه‌ها با موفقیت انجام شد.")
            print("\n===== گروه‌های قرعه‌کشی شده =====")

            for group in self.groups:
                print(f"\nGroup {group.name}:")
                for team in group.teams:
                    print(f"  {team.name} (Rank {team.rank})")

    def run_group_stage(self, display=True):
        """
        اجرای مرحله گروهی و نمایش جداول.

        Args:
            display (bool): آیا جداول نمایش داده شوند؟
        """
        if not self.groups_drawn:
            if display:
                print("ابتدا قرعه‌کشی را انجام دهید!")
            return

        if self.group_stage_completed:
            if display:
                print("مرحله گروهی قبلاً انجام شده است.")
            return

        for group in self.groups:
            group.play_all_matches()

            if display:
                print(f"\nGroup {group.name}:")
                for i, t in enumerate(group.get_ranking(), 1):
                    print(f"  {i}. {t.name}: {t.points} pts, GD {t.goal_difference():+d}, GF {t.goals_for}")

        self.group_stage_completed = True

        if display:
            print("\nمرحله گروهی با موفقیت انجام شد.")

    def run_knockout(self, display=True):
        """
        اجرای مراحل حذفی (یک‌هشتم تا فینال).

        Args:
            display (bool): آیا نتایج نمایش داده شوند؟
        """
        if not self.groups_drawn or not self.group_stage_completed:
            if display:
                print("ابتدا مرحله گروهی را کامل کنید!")
            return

        group_winners = [g.advance_teams()[0] for g in self.groups]
        group_runners = [g.advance_teams()[1] for g in self.groups]

        pairs = [
            (group_winners[0], group_runners[1]),
            (group_winners[1], group_runners[0]),
            (group_winners[2], group_runners[3]),
            (group_winners[3], group_runners[2]),
            (group_winners[4], group_runners[5]),
            (group_winners[5], group_runners[4]),
            (group_winners[6], group_runners[7]),
            (group_winners[7], group_runners[6]),
        ]

        def play_round(round_name, matches, bracket):
            stage = KnockoutStage(round_name, [Match(t1, t2, is_knockout=True) for t1, t2 in matches])
            stage.play_round()
            bracket.append((round_name, stage.matches))
            return stage.get_winners()

        self.bracket_matches = []

        w16 = play_round("Round of 16", pairs, self.bracket_matches)
        w8 = play_round("Quarterfinals", [(w16[i], w16[i + 1]) for i in range(0, 8, 2)], self.bracket_matches)
        w4 = play_round("Semifinals", [(w8[0], w8[1]), (w8[2], w8[3])], self.bracket_matches)

        final = Match(w4[0], w4[1], is_knockout=True)
        final.play()
        self.champion = final.winner
        self.bracket_matches.append(("Final", [final]))

        self.knockout_completed = True

        if display:
            print(f"\nCHAMPION: {self.champion.name} ")
            self.display_bracket()

    def run_full_simulation(self, display=True):
        """
        اجرای کامل جام جهانی (مرحله گروهی + حذفی).

        Args:
            display (bool): آیا نتایج نمایش داده شوند?
        """
        if not self.groups_drawn:
            self.seed_and_draw_groups(display=False)

        if not self.group_stage_completed:
            self.run_group_stage(display=False)

        self.run_knockout(display=display)

    def display_bracket(self):
        """نمایش براکت حذفی آخرین شبیه‌سازی."""
        if not self.bracket_matches:
            print("هیچ براکت حذفی برای نمایش وجود ندارد!")
            return

        for round_name, matches in self.bracket_matches:
            print(f"\n===== {round_name} =====")

            for m in matches:
                if m.winner:
                    print(f"{m.team1.name} {m.goals1} - {m.goals2} {m.team2.name}{m.penalty_text} -> Winner: {m.winner.name}")

    def most_likely_champion(self, num_simulations=1000):
        """
        شبیه‌سازی ۱۰۰۰ باره و محاسبه درصد قهرمانی هر تیم.

        Args:
            num_simulations (int): تعداد شبیه‌سازی‌ها
        """
        if num_simulations <= 0:
            print("خطا: تعداد شبیه‌سازی باید بزرگتر از صفر باشد!")
            return

        champion_count = {t.name: 0 for t in self.teams}

        for sim in range(num_simulations):
            for t in self.teams:
                t.reset_stats()

            self.groups_drawn = False
            self.group_stage_completed = False
            self.knockout_completed = False

            self.seed_and_draw_groups(display=False)
            self.run_group_stage(display=False)
            self.run_knockout(display=False)

            champion_count[self.champion.name] += 1

        print(f"\n===== شبیه‌سازی با موفقیت انجام شد =====")
        print(f"\n===== {num_simulations} بار شبیه‌سازی =====")

        for name, count in sorted(champion_count.items(), key=lambda x: -x[1]):
            if count > 0:
                print(f"{name}: {count / num_simulations * 100:.1f}%")