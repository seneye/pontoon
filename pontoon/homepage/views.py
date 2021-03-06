from django.shortcuts import render, redirect
from django.urls import reverse

from pontoon.base.models import Locale
from pontoon.base.utils import get_project_locale_from_request


def homepage(request):
    user = request.user

    # Redirect user to the selected home page or '/'.
    if user.is_authenticated() and user.profile.custom_homepage != '':
        # If custom homepage not set yet, set it to the most contributed locale team page
        if user.profile.custom_homepage is None:
            if user.top_contributed_locale:
                user.profile.custom_homepage = user.top_contributed_locale
                user.profile.save(update_fields=['custom_homepage'])

        if user.profile.custom_homepage:
            return redirect('pontoon.teams.team', locale=user.profile.custom_homepage)

    # Guess user's team page or redirect to /teams
    locale = get_project_locale_from_request(request, Locale.objects)
    if locale not in ('en-US', 'en', None):
        start_url = reverse('pontoon.teams.team', kwargs={
            'locale': locale,
        })
    else:
        start_url = reverse('pontoon.teams')

    return render(request, 'homepage.html', {
        'start_url': start_url,
    })
