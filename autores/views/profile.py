from django.views.generic import TemplateView
from autores.models import Profile
from django.shortcuts import get_object_or_404


class ProfileTemplateView(TemplateView):
    template_name = 'autores/pages/profile.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        profile_id = context.get('pk')
        profile = get_object_or_404(
            Profile.objects.filter(
                pk=profile_id
            ).select_related('author'),
            pk=profile_id
        )
        return self.render_to_response({
            **context,
            'profile': profile
        })