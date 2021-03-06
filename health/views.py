from django.shortcuts import render
from .models import HealthProfile
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import HealthProfile
from django.shortcuts import redirect
from pyScripts import get_health_score
from pyScripts import get_recommendations
import json
from django.core import serializers

# Create your views here.

def profile(request):
    if(request.user):
        p = HealthProfile.objects.filter(user=request.user)
        if len(p)>0 :
            json_p = json.loads(serializers.serialize('json',[p[0]]))[0]["fields"]
            print("json p")
            print(json_p)
            # json_p["healthcare_costs"] = 100
            recommendations,savings = get_recommendations.processRecommendations(json_p, 1000)
            result = get_health_score.preprocessData(json_p)
            # recommendations = "hello"
            return render(request,'health/profile.html',{'health_profile' : p[0], 'health_score' : result, 'savings' : savings, 'recommendations' : recommendations})
        else:
            return render(request,'health/profile.html')

class HealthProfileDisplay(ListView):
    model = HealthProfile

def handle_profile(request):
    h = HealthProfile()
    if(request.user):
        p = HealthProfile.objects.filter(user=request.user)
        if len(p)>0 :
            print("Profile exists : Reditecting to edit")
            s = "/health/update/"+str(p[0].id)
            return redirect(s)
        else:
            print("Creating new profile")
            return redirect("/health/input")

class HealthProfileCreate(CreateView):
    model = HealthProfile
    fields = ['age','height','weight','ailments','healthcare_costs','tobacco','smoke','drink','exercise','travel_time', 'sleep_time','job_type']
    success_url = reverse_lazy('health:health_profile')
    # initial = {'sleep_time':1}

    def form_valid(self, form):
        form.instance.user = self.request.user
        print("+++++++++++++",form.instance.sleep_time)
        return super().form_valid(form)

class HealthProfileUpdate(UpdateView):
    model = HealthProfile
    fields = ['age','height','weight','ailments','healthcare_costs','tobacco','smoke','drink','exercise','travel_time', 'sleep_time','job_type']
    success_url = reverse_lazy('health:health_profile')
