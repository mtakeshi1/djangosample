from django.shortcuts import render

# Create your views here.

from lisp.lisp.interpreter import evaluate, LispError


def evaluate(request):
    source, stdout, stderr = '','',''
    try:
        source = request.POST.get('inputtext').strip()
        stdout = parse(source)
    except KeyError:
        source = ''
    except LispError as ex:
        stderr = ex.message

    context = {
        'inputtext': source,
        'stdout': stdout,
        'stderr':stderr
    }
    return render(request, 'lisp/index.html', context)
