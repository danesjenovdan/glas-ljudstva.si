import csv
import json
import os
import random
from unicodedata import normalize

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from zahteve.models import Election, Party


class Command(BaseCommand):
    help = "Create candidates for 2026 parliamentary elections"

    def _get_username(self, s):
        s = (
            normalize("NFKD", s)
            .encode("ASCII", "ignore")
            .decode("utf-8")
            .lower()
            .replace(" ", "")
            .replace(".", "")
            .replace("-", "")
            .replace("_", "")
            .replace("!", "")
        )
        if len(s) < 2:
            return ""
        return s

    def _get_password(self, words, seen_passwords):
        max_attempts = 100
        attempt = 0
        while attempt < max_attempts:
            word1 = random.choice(words).capitalize()
            word2 = random.choice(words).capitalize()
            word3 = random.choice(words).capitalize()
            password = f"{word1}{word2}{word3}"
            if password not in seen_passwords:
                seen_passwords.add(password)
                return password
            attempt += 1
        raise CommandError("Could not generate unique password after many attempts.")

    def _read_candidates_csv(self):
        self.stdout.write(f"Reading candidates...")

        candidates = []
        seen_usernames = set()
        seen_passwords = set()

        current_dir = os.path.dirname(os.path.abspath(__file__))

        # read words from json
        pw_path = os.path.join(current_dir, "sl-words.json")
        words = json.load(open(pw_path))
        self.stdout.write(f"Loaded {len(words)} words for password generation.")

        # read file
        file_path = os.path.join(current_dir, "import_2026_candidates.csv")
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # skip the headers

            for row in reader:
                party_name = row[0].strip()
                party_email = row[1].strip()
                party_short_name = row[2].strip()
                party_abbreviation = row[3].strip()
                # other columns are ignored

                abbr = self._get_username(party_abbreviation)

                if not abbr and party_short_name:
                    abbr = self._get_username(party_short_name)

                if not abbr and party_email:
                    email_addr, email_domain = party_email.split("@")
                    if (
                        email_domain.startswith("gmail.")
                        or email_domain.startswith("yahoo.")
                        or email_domain.startswith("hotmail.")
                        or email_domain.startswith("siol.")
                        or email_domain.startswith("proton.")
                        or email_domain.startswith("triera.")
                        or email_domain.startswith("grafika-gracer.")
                    ):
                        email_domain = ""
                    if email_domain:
                        domain_part = email_domain.split(".")[0]
                        abbr = self._get_username(domain_part)

                if not abbr and party_name:
                    abbr = self._get_username(party_name)

                if not abbr:
                    raise CommandError(
                        f"Could not generate username for party: {party_name}"
                    )

                if abbr in seen_usernames:
                    raise CommandError(
                        f"Duplicate username generated: {abbr} for party: {party_name}"
                    )

                seen_usernames.add(abbr)
                username = abbr + "2026"
                password = self._get_password(words, seen_passwords)

                candidates.append(
                    {
                        "username": username,
                        "password": password,
                        "party_name": party_name + " (2026)",
                    }
                )

        return candidates

    def _save_candidates(self, election, candidates_list):
        # write candidates to file
        out_path = "/tmp/candidates_list.csv"
        with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["username", "password", "party_name"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for candidate in candidates_list:
                writer.writerow(candidate)
        self.stdout.write(f"Saved candidates list to: {out_path}")

        # create users and parties
        for candidate in candidates_list:
            username = candidate["username"]
            password = candidate["password"]
            party_name = candidate["party_name"]

            self.stdout.write(f"Creating user: {username}")

            u = User.objects.create_user(
                username=username,
                password=password,
            )
            p = Party.objects.create(
                user=u,
                party_name=party_name,
                proposer="",
                sex="",
                election=election,
            )

    def handle(self, *args, **options):
        election = Election.objects.get(slug="drzavnozborske-volitve-2026")

        candidates_list = self._read_candidates_csv()
        self._save_candidates(election, candidates_list)

        self.stdout.write("DONE")
