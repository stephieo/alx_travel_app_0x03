from django.core.management.base import BaseCommand
from django.conf import settings
import os
import json
import uuid
from json import JSONDecodeError
from ...models import User, Listing, Booking


class Command(BaseCommand):
    help = " this will initialize the app databese with test data. for now its json files only"

    def add_arguments(self, parser):
        ''' defines optional and required arguments to the  command'''
        parser.add_argument('filename', default='app_data.json', type=str)

    def handle(self, *args, **options):
        filename = options['filename']
        file_path = os.path.join(settings.BASE_DIR, filename)

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.seed_users(data.get('users',[]))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found"))
        except JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON format"))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
    
    def seed_users(self, users):
        accepted_roles = [role[0] for role in User.USER_TYPES]
        for user_data in users:
            try:
                user_id = uuid.UUID(user_data.get('user_id'))
                email = user_data.get('email')
                role = user_data.get('role')
                # validating the data from the seeder file
                if User.objects.filter(user_id=user_id).exists()or User.objects.filter(email=email).exists():
                    self.stdout.write(f"ERROR: User {email} exists")
                    self.stdout.write(f"skipping...")
                    continue
                if role not in accepted_roles:
                    self.stdout.write(f"ERROR: This is not a valid user role")
                    self.stdout.write(f"skipping...")
                    continue
                
                self.stdout.write(self.style.INFO(f"Creating user {email}"))
                User.objects.create(
                    user_id=user_id,
                    first_name=user_data.get('first_name'),
                    last_name=user_data.get('last_name'),
                    email=email,
                    password_hash=user_data.get('password_hash'),
                    phone_number=user_data.get('phone_number', None),
                    role=role,
                    created_at=user_data.get('created_at')
                )
                self.stdout.write(self.style.SUCCESS("User successfully created"))
            except ValueError:
                self.stdout.write(f"ERROR: This is not a valid user id")
                self.stdout.write(f"skipping...")

                







