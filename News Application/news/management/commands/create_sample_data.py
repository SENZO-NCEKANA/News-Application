"""
Management command to create sample data for testing.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from news.models import Publisher, Category, Article, Newsletter

User = get_user_model()


class Command(BaseCommand):
    """
    Command to create sample data for testing.
    """
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        """
        Create sample data.
        """
        # Create publishers
        publisher1, created = Publisher.objects.get_or_create(
            name='Tech News Daily',
            defaults={
                'description': 'Latest technology news and updates',
                'website': 'https://technewsdaily.com'
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created publisher: Tech News Daily')
            )

        publisher2, created = Publisher.objects.get_or_create(
            name='World Affairs',
            defaults={
                'description': 'Global news and current events',
                'website': 'https://worldaffairs.com'
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created publisher: World Affairs')
            )

        # Create categories
        tech_category, created = Category.objects.get_or_create(
            name='Technology',
            defaults={'description': 'Technology news and updates'}
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created category: Technology')
            )

        world_category, created = Category.objects.get_or_create(
            name='World News',
            defaults={'description': 'Global news and events'}
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created category: World News')
            )

        # Create users
        journalist1, created = User.objects.get_or_create(
            username='Aphiwe_tech',
            defaults={
                'email': 'aphiwe@example.com',
                'first_name': 'Aphiwe',
                'last_name': 'Mthembu',
                'role': 'journalist'
            }
        )
        if created:
            journalist1.set_password('testpass123')
            journalist1.save()
            self.stdout.write(
                self.style.SUCCESS('Created journalist: Aphiwe_tech')
            )

        journalist2, created = User.objects.get_or_create(
            username='Kwanele_world',
            defaults={
                'email': 'kwanele@example.com',
                'first_name': 'Kwanele',
                'last_name': 'Ndlovu',
                'role': 'journalist'
            }
        )
        if created:
            journalist2.set_password('testpass123')
            journalist2.save()
            self.stdout.write(
                self.style.SUCCESS('Created journalist: Kwanele_world')
            )

        editor1, created = User.objects.get_or_create(
            username='editor_tech',
            defaults={
                'email': 'editor@technews.com',
                'first_name': 'Mike',
                'last_name': 'Editor',
                'role': 'editor'
            }
        )
        if created:
            editor1.set_password('testpass123')
            editor1.save()
            self.stdout.write(
                self.style.SUCCESS('Created editor: editor_tech')
            )

        reader1, created = User.objects.get_or_create(
            username='reader1',
            defaults={
                'email': 'reader1@example.com',
                'first_name': 'Alice',
                'last_name': 'Reader',
                'role': 'reader'
            }
        )
        if created:
            reader1.set_password('testpass123')
            reader1.save()
            self.stdout.write(
                self.style.SUCCESS('Created reader: reader1')
            )

        # Add journalists to publishers
        publisher1.journalists.add(journalist1)
        publisher2.journalists.add(journalist2)
        publisher1.editors.add(editor1)

        # Create sample articles
        article1, created = Article.objects.get_or_create(
            title='Digital Healthcare Assistant: Diagnosis, Medication Reminders, '
                  'and Health Support',
            defaults={
                'content': (
                    'A comprehensive digital healthcare assistant has been '
                    'developed that revolutionizes patient care through '
                    'three key features: intelligent diagnosis assistance, '
                    'smart medication reminders, and an automated health '
                    'support system. This innovative system uses advanced '
                    'algorithms to analyze symptoms, provide preliminary '
                    'health assessments, and help patients manage their '
                    'medications effectively. The digital assistant '
                    'component offers 24/7 health guidance, answering '
                    'common medical questions and providing personalized '
                    'health recommendations based on individual patient '
                    'profiles and medical history.'
                ),
                'summary': (
                    'Comprehensive digital healthcare assistant featuring '
                    'diagnosis assistance, medication reminders, and '
                    'intelligent health support for 24/7 patient care.'
                ),
                'author': journalist1,
                'publisher': publisher1,
                'category': tech_category,
                'status': 'published',
                'is_approved': True
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    'Created article: Digital Healthcare Assistant...'
                )
            )

        article2, created = Article.objects.get_or_create(
            title='Global Climate Summit Reaches Historic Agreement',
            defaults={
                'content': 'World leaders have reached a historic agreement '
                           'on climate change at the latest global summit. '
                           'The agreement includes ambitious targets for '
                           'reducing carbon emissions and transitioning to '
                           'renewable energy sources.',
                'summary': 'Historic climate agreement reached with ambitious '
                           'emission reduction targets.',
                'author': journalist2,
                'publisher': publisher2,
                'category': world_category,
                'status': 'published',
                'is_approved': True
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created article: Global Climate Summit...')
            )

        # Create sample newsletter
        newsletter1, created = Newsletter.objects.get_or_create(
            title='Weekly Tech Roundup',
            defaults={
                'content': (
                    'This week in technology: major breakthroughs, '
                    'new smartphone releases, and cybersecurity updates.'
                ),
                'author': journalist1,
                'publisher': publisher1
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created newsletter: Weekly Tech Roundup')
            )

        self.stdout.write(
            self.style.SUCCESS('Sample data creation completed successfully!')
        )
