#!/usr/bin/python3
import os
import random
import json
import requests
import secrets
import string
import base64
import argparse
from faker import Faker
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.columns import Columns
from rich.layout import Layout
from PIL import Image

console = Console()

class PuppetMaster:
    def __init__(self, args):
        self.args = args 
        self.fake = Faker('en_US')
        self.domains = ["proton.me", "tuta.io", "mailfence.com"]
        self.bio_file = "assets/bio.json"
        self.base_folder = "puppets"
        
        self.styles_masculine = ["adventurer", "avataaars", "open-peeps", "notionists", "personas", "pixel-art"]
        self.styles_feminine = ["adventurer", "avataaars", "lorelei", "open-peeps", "notionists", "personas", "pixel-art"]

        self.init_bio_templates()

    def init_bio_templates(self):
        if not os.path.exists(self.bio_file):
            console.print("[bold red]Error:[/] bio.json not found.")
            exit(1)
        with open(self.bio_file, 'r', encoding='utf-8') as f:
            self.templates = json.load(f)

    def generate_secure_password(self, length=16):
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for i in range(length))

    def generate_content_plan(self, category, age, alignment, city, job):
        plan = []

        # --- SOCIAL MEDIA CONTENT ---
        if self.args.content:
            try:
                with open("assets/content.json", 'r', encoding='utf-8') as f:
                    all_content = json.load(f)

                political_pool = all_content["political_posts"].get(alignment, all_content["political_posts"]["center"])
                
                if age < 30:
                    plan.extend(random.sample(political_pool, 2))
                    plan.extend(random.sample(all_content["brainrot_posts"], 2))
                else:
                    plan.extend(random.sample(political_pool, 2))
                    plan.extend(random.sample(all_content["family_life_posts"], 2))
            except Exception as e:
                plan.append(f"Error loading social content: {e}")

        # --- FORUM CONTENT ---
        if self.args.forum_posts:
            try:
                with open("assets/content.json", 'r', encoding='utf-8') as f:
                    all_content = json.load(f)
                
                forum_pool = all_content.get("forum_posts", [])
                if forum_pool:
                    raw_posts = random.sample(forum_pool, min(2, len(forum_pool)))
                    formatted_posts = [p.replace("{city}", city).replace("{job}", job) for p in raw_posts]
                    plan.extend([f"[FORUM THREAD] {p}" for p in formatted_posts])
            except Exception as e:
                plan.append(f"Error loading forum content: {e}")

        if not plan:
            return ["No content generated (use --content or --forum-posts)"]

        random.shuffle(plan)
        return plan

    def generate_social_bio(self, job, city):
        if not self.args.bio:
            return "Bio generation disabled (use --bio)", "none"

        rand = random.random()
        if rand < 0.15: category = "funny"
        elif rand < 0.30: category = "romantic"
        elif rand < 0.45: category = "political"
        elif any(x in job.lower() for x in ['engineer', 'dev', 'tech', 'software']): category = "tech"
        elif any(x in job.lower() for x in ['designer', 'artist', 'marketing']): category = "creative"
        else: category = "general"
            
        template = random.choice(self.templates[category])
        partner = self.fake.first_name()
        bio = template.replace("{job}", job).replace("{city}", city).replace("@Name", f"@{partner}")
        return bio, category

    def generate_full_identity(self):
        gender_code = random.choice(['male', 'female'])
        first_name = self.fake.first_name_male() if gender_code == 'male' else self.fake.first_name_female()
        last_name = self.fake.last_name()
        full_name = f"{first_name} {last_name}"
        job = self.fake.job()
        city = self.fake.city()
        age = random.randint(17, 53)
        alignments = ["far-right", "right", "center", "left", "radical-left", "communist"]
        political_alignment = random.choice(alignments)
        bio, category = self.generate_social_bio(job, city)

        identity = {
            "First Name": first_name, "Last Name": last_name, "Full Name": full_name,
            "Gender": "Male" if gender_code == 'male' else "Female", "Age": age,
            "Birthday": self.fake.date_of_birth(minimum_age=age, maximum_age=age).strftime("%m/%d/%Y"),
            "Political Alignment": political_alignment,
            "Occupation": job, "Street": self.fake.street_address(), "City": city,
            "State": self.fake.state(), "Zipcode": self.fake.zipcode(), "Telephone": self.fake.phone_number(),
            "Biography": bio,
            "Security": {
                "Password": self.generate_secure_password(),
                "Question": "First Pet Name",
                "Answer": self.fake.first_name()
            }
        }
        return full_name, identity, category

    def generate_digital_assets(self, first_name, last_name):
        year = random.randint(88, 99)
        variants = [f"{first_name[0].lower()}{last_name.lower()}{year}", f"{last_name.lower()}{random.randint(10,99)}", f"{first_name.lower()}_{last_name.lower()}", f"nexus.{first_name.lower()}{random.randint(1,9)}"]
        return [{"username": p, "email": f"{p}@{random.choice(self.domains)}"} for p in variants]

    def save_avatar(self, full_name, gender, folder):
        avatar_source = random.choice(["dicebear", "static"])
        seed = full_name.replace(" ", "")
        if avatar_source == "dicebear":
            style = random.choice(self.styles_masculine if gender == "Male" else self.styles_feminine)
            url = f"https://api.dicebear.com/7.x/{style}/svg?seed={seed}&gender={gender.lower()}"
            ext = "svg"
        else:
            url = f"https://static.photos/200x200?random={random.randint(1, 100000)}"
            style = "real_photo"; ext = "jpg"

        try:
            r = requests.get(url, timeout=10)
            filename = f"avatar.{ext}"
            file_path = os.path.join(folder, filename)
            with open(file_path, "wb") as f:
                f.write(r.content)
            if ext == "jpg":
                img = Image.open(file_path)
                data = list(img.getdata())
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(data); clean_img.save(file_path)
            return url, style, filename, os.path.abspath(file_path)
        except Exception:
            return None, "error", None, None

    def run(self):
        console.clear()
        console.print(Panel.fit("[bold cyan]PUPPET MASTER[/bold cyan]\n[white]Visual Persona Generation[/]", border_style="magenta"))

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description="Forging Puppet Data...", total=None)
            full_name, identity, category = self.generate_full_identity()

        clean_name = f"{identity['First Name']}_{identity['Last Name']}".upper()
        puppet_dir = os.path.join(self.base_folder, clean_name)
        os.makedirs(puppet_dir, exist_ok=True)
        
        digital_ids = self.generate_digital_assets(identity["First Name"], identity["Last Name"])
        content_plan = self.generate_content_plan(category, identity["Age"], identity["Political Alignment"], identity["City"], identity["Occupation"])
        avatar_url, avatar_style, avatar_file, avatar_full_path = self.save_avatar(full_name, identity["Gender"], puppet_dir)

        id_table = Table(show_header=True, header_style="bold blue", expand=True, border_style="blue")
        id_table.add_column("Property", style="cyan"); id_table.add_column("Value", style="white")
        for k in ["Full Name", "Gender", "Age", "Birthday", "Political Alignment", "Occupation", "Street", "City", "State", "Telephone"]:
            id_table.add_row(k, str(identity[k]))

        avatar_display = f"[bold yellow]Source:[/] {avatar_style}\n[bold yellow]File:[/] [link=file://{avatar_full_path}]{avatar_file}[/link]\n\n[italic white]To view, open the file in the puppet folder.[/]"
        
        console.print(Columns([
            Panel(id_table, title="[bold blue]Identity Details[/]", border_style="blue", padding=(0,1)),
            Panel(avatar_display, title="[bold magenta]Avatar Metadata[/]", border_style="magenta", padding=(1,2))
        ]))

        sec_content = f"🗝️ [bold yellow]Password:[/] [bold red]{identity['Security']['Password']}[/]\n"
        sec_content += f"❓ [bold yellow]Question:[/] {identity['Security']['Question']}\n"
        sec_content += f" [bold yellow]Answer:[/] {identity['Security']['Answer']}"
        console.print(Panel(sec_content, title="[bold red]Security & Recovery[/]", border_style="red"))

        console.print(Panel(identity["Biography"], title="[bold green]Social Media Bio[/]", border_style="green"))

        acc_info = "\n".join([f"• [cyan]{a['username']}[/] ([yellow]{a['email']}[/])" for a in digital_ids])
        post_info = "\n".join([f"📝 {p}" for p in content_plan])
        
        console.print(Columns([
            Panel(acc_info, title="[bold cyan]Digital Assets[/]", border_style="cyan", expand=True),
            Panel(post_info, title="[bold yellow]Content Plan[/]", border_style="yellow", expand=True)
        ]))

        with open(os.path.join(puppet_dir, "puppet_data.json"), 'w', encoding='utf-8') as f:
            json.dump({"identity": identity, "digital_assets": digital_ids, "content_plan": content_plan, "avatar": avatar_style}, f, indent=4, ensure_ascii=False)

        console.print(f"\n[bold success]✔[/] Persona [bold white]{full_name}[/] stored in [underline]{puppet_dir}/[/]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puppet Master - Persona Generator")
    parser.add_argument('--bio', action='store_true', help="Generate social media bio")
    parser.add_argument('--content', action='store_true', help="Generate social media content plan")
    parser.add_argument('--forum-posts', action='store_true', help="Generate forum question threads")

    args = parser.parse_args()
    PuppetMaster(args).run()
