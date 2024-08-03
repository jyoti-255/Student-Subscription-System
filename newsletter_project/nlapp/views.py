from django.shortcuts import render
from .models import StudentModel
from .forms import StudentForm
import requests

def send_sms(ph, text):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = f"message={text}&language=english&route=q&numbers={str(ph)}"
    headers = {
        'authorization': "your_key_here",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

def home(request):
    if request.method == "POST":
        ph = request.POST.get("phone")
        
        if request.POST.get("sub"):
            try:
                usr = StudentModel.objects.get(phone=ph)
                msg = ph + " already registered"
                fm = StudentForm()
                return render(request, "home.html", {"fm": fm, "msg": msg})
            except StudentModel.DoesNotExist:
                data = StudentForm(request.POST)
                if data.is_valid():
                    data.save()
                    send_sms(ph, "Congrats on your subscription!")
                    msg = "Congrats on your subscription!"
                    fm = StudentForm()
                    return render(request, "home.html", {"fm": fm, "msg": msg})
                else:
                    msg = "Form is not valid"
                    return render(request, "home.html", {"fm": data, "msg": msg})

        elif request.POST.get("unsub"):
            try:
                usr = StudentModel.objects.get(phone=ph)
                usr.delete()
                send_sms(ph, "Sorry for your unsubscription")
                msg = "Sorry for your unsubscription"
                fm = StudentForm()
                return render(request, "home.html", {"fm": fm, "msg": msg})
            except StudentModel.DoesNotExist:
                msg = ph + " is not yet subscribed"
                fm = StudentForm()
                return render(request, "home.html", {"fm": fm, "msg": msg})

    else:
        fm = StudentForm()
        return render(request, "home.html", {"fm": fm})

