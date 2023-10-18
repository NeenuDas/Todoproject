from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import TodoForm
from. models import Task
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView
class TaskListview(ListView):
    model = Task
    template_name='home.html'
    context_object_name = 'task'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'taskdv'

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'taskup'
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')

def demo(request):
    taskdetails = Task.objects.all()
    if request.method=='POST':
        name=request.POST.get('name','')
        priority = request.POST.get('priority','')
        date = request.POST.get('date', '')

        task=Task(name=name,priority=priority,date=date)
        task.save()
    return render(request, "home.html",{'task':taskdetails})


# def details(request):
#     taskdetails=Task.objects.all()
#     return render(request, "details.html",{'task':taskdetails})

def delete(request,taskid):
    taskdel = Task.objects.get(id=taskid)
    if request.method == 'POST':
        taskdel.delete()
        return redirect('/')
    return render(request, "delete.html")


def update(request,id):
    taskup =Task.objects.get(id=id)
    f = TodoForm(request.POST or None,instance=taskup)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'form':f,'task':taskup})






