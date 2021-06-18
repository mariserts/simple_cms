from django.shortcuts import redirect, render
from django.views import View


class HomepageThingDetailView(View):

    template = ''

    def get(self, request, language=None):

        if language is None:
            return redirect('/en/')

        return render(
            request,
            self.template,
            context=self.get_context()
        )

    def get_context(self):
        return {}
