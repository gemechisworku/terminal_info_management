from django.shortcuts import render, get_object_or_404, redirect
from .models import Terminal
from .forms import TerminalForm

def terminal_list(request):
    terminals = Terminal.objects.all()
    return render(request, 'terminals/terminal_list.html', {'terminals': terminals})

def terminal_detail(request, pk):
    terminal = get_object_or_404(Terminal, pk=pk)
    return render(request, 'terminals/terminal_detail.html', {'terminal': terminal})

def terminal_new(request):
    if request.method == "POST":
        form = TerminalForm(request.POST)
        if form.is_valid():
            terminal = form.save(commit=False)
            terminal.save()
            return redirect('terminal_detail', pk=terminal.pk)
    else:
        form = TerminalForm()
    return render(request, 'terminals/terminal_edit.html', {'form': form})

def terminal_edit(request, pk):
    terminal = get_object_or_404(Terminal, pk=pk)
    if request.method == "POST":
        form = TerminalForm(request.POST, instance=terminal)
        if form.is_valid():
            terminal = form.save(commit=False)
            terminal.save()
            return redirect('terminal_detail', pk=terminal.pk)
    else:
        form = TerminalForm(instance=terminal)
    return render(request, 'terminals/terminal_edit.html', {'form': form})

def terminal_new(request):
    if request.method == "POST":
        form = TerminalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('terminal_list')
    else:
        form = TerminalForm()
    return render(request, 'terminals/terminal_new.html', {'form': form})