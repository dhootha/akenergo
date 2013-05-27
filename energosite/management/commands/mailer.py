from django.core.management.base import NoArgsCommand, CommandError
from energosite.models import Mailing_List, UserProfile
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from energosite.views import render_kvit
from optparse import make_option


class Command(NoArgsCommand):
    help = "Send a mailing to users who agreed to it"
    args = "--clear"
    option_list = NoArgsCommand.option_list + (
        make_option('--clear_queue', '-c',
            action='store_true',
            dest='clear_queue',
            default=False,
            help='Delete all mailing queue'),
        )

    def handle_noargs(self, **options):

    #        raise CommandError('Poll "%s" doenot exist')
        #        self.stdout.write("Successfully\n")
        if options.get('clear_queue'):
            Mailing_List.objects.all().delete()
            return
            #
        users = User.objects.filter(is_active=True, userprofile__mailing=True)
#        print users
        #        users = UserProfile.objects.filter(user__username__iexact='user')
        for user in users:
        #            print user.email
            if len(user.email.strip()) == 0:
                continue
            mailing_lists = Mailing_List.objects.order_by('date')
            try:
                profile = user.userprofile
                nls = profile.nls
            except UserProfile.DoesNotExist:
                nls = None

            for mail_list in mailing_lists:
                msg = EmailMessage(mail_list.subject, mail_list.content, settings.DEFAULT_FROM_EMAIL,
                    [user.email])
                msg.content_subtype = "html"  # Main content is now text/html
                must_send = True
                if mail_list.kvit:
                    kvitanciya = render_kvit(nls)
                    if kvitanciya:
                        msg.attach('kvitanciya.html', kvitanciya, 'text/html')
                    else:
                        must_send = False

                if must_send:
                    try:
                        msg.send()
                    except:
                        self.stdout.write("Error sending to %s (%s) \n" % (user.username, user.email))





