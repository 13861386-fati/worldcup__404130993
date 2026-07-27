
"""
فایل اصلی برنامه - منوی شبیه‌ساز جام جهانی 2026
"""

from simulator import WorldCupSimulator


def main():
    """
    تابع اصلی برنامه که منو را نمایش می‌دهد و ورودی کاربر را مدیریت می‌کند.
    """
    sim = WorldCupSimulator()

    while True:
        print("\n===== شبیه‌ساز جام جهانی 2026 =====")
        print("1) بارگذاری تیم‌ها از فایل CSV")
        print("2) انجام قرعه‌کشی گروه‌ها")
        print("3) اجرای مرحله گروهی و نمایش جداول")
        print("4) اجرای کامل جام و نمایش قهرمان")
        print("5) شبیه‌سازی 1000 باره و گزارش درصدها")
        print("6) نمایش براکت حذفی")
        print("7) خروج")

        choice = input("انتخاب کنید (1-7): ").strip()

        if choice == '1':
            sim.load_teams_from_csv("worldcup_2026_teams.csv")

        elif choice == '2':
            if not sim.teams:
                print("خطا: ابتدا تیم‌ها را بارگذاری کنید!")
            else:
                sim.seed_and_draw_groups(display=True)

        elif choice == '3':
            if not sim.teams:
                print("خطا: ابتدا تیم‌ها را بارگذاری کنید!")
            else:
                if not sim.groups_drawn:
                    sim.seed_and_draw_groups(display=True)
                sim.run_group_stage(display=True)

        elif choice == '4':
            if not sim.teams:
                print("خطا: ابتدا تیم‌ها را بارگذاری کنید!")
            else:
                sim.run_full_simulation(display=True)

        elif choice == '5':
            if not sim.teams:
                print("خطا: ابتدا تیم‌ها را بارگذاری کنید!")
                continue

            value = input("تعداد شبیه‌سازی (پیش‌فرض 1000): ").strip()
            try:
                num = int(value) if value else 1000
                if num <= 0:
                    print("خطا: تعداد باید مثبت باشد!")
                else:
                    sim.most_likely_champion(num)
            except ValueError:
                print("لطفاً یک عدد صحیح وارد کنید!")

        elif choice == '6':
            if not sim.teams:
                print("خطا: ابتدا تیم‌ها را بارگذاری کنید!")
            else:
                sim.display_bracket()

        elif choice == '7':
            print("خدانگهدار!")
            break

        else:
            print("گزینه نامعتبر!")


if __name__ == "__main__":
    main()