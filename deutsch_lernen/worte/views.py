from django.shortcuts import render
from  .models import wordLearning
import random, json
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt 
def home(request):
    allwords = list(wordLearning.objects.all())
    word = random.choice(allwords)

    wronganswers = random.sample([ch_word.nameturkish for ch_word in allwords if ch_word.nameturkish != word.nameturkish], 2)
    correctanswer = word.nameturkish
    choices = wronganswers + [correctanswer]

    random.shuffle(choices)

    labels = ['A', 'B', 'C']
    choiceswithlabels = list(zip(labels, choices))

    request.session['allwords'] = [{'namedeutsch': w.namedeutsch, 'nameturkish': w.nameturkish} for w in allwords]
    request.session['current_word'] = {'namedeutsch': word.namedeutsch, 'nameturkish': word.nameturkish}



    return render(request, 'worte/index.html', {
        'word': word,
        'correctanswer': correctanswer,
        'choiceswithlabels': choiceswithlabels,
    })

@csrf_exempt 
def back(request):
    # Önceki soruların olduğu bir yığın
    previous_questions = request.session.get('previous_questions', [])
    
    if previous_questions:  # Eğer yığın boş değilse
        pre_word = previous_questions.pop()  # Yığından son soruyu al
        request.session['previous_questions'] = previous_questions  # Güncellenmiş yığını kaydet

        # Şıkları oluştur
        allwords = request.session.get('allwords', [])
        if len(allwords) >= 2:  # Yeterince yanlış cevap varsa
            wronganswers = random.sample(
                [word['nameturkish'] for word in allwords if word['nameturkish'] != pre_word['nameturkish']], 2
            )
        else:
            wronganswers = [word['nameturkish'] for word in allwords]

        correctanswer = pre_word['nameturkish']
        choices = wronganswers + [correctanswer]
        random.shuffle(choices)

        labels = ['A', 'B', 'C']
        choiceswithlabels = list(zip(labels, choices))

        return JsonResponse({
            'success': True,
            'word': pre_word['namedeutsch'],
            'choiceswithlabels': choiceswithlabels,
        })

    # Liste boşsa hata döndür
    return JsonResponse({'success': False, 'error': 'No previous question found'})




@csrf_exempt 
def further(request):
    allwords = list(wordLearning.objects.all())
    next_word = random.choice(allwords)

    # Önceki soruları saklamak için mevcut soruyu listeye ekle
    previous_questions = request.session.get('previous_questions', [])
    current_word = request.session.get('current_word', None)

    if current_word:  # Mevcut soru varsa, önceki listeye ekle
        previous_questions.append(current_word)

    request.session['previous_questions'] = previous_questions  # Session'ı güncelle
    request.session.modified = True  # Session'da değişiklik olduğunu belirt

    # Yeni soru için şıkları oluştur
    wronganswers = random.sample(
        [ch_word.nameturkish for ch_word in allwords if ch_word.nameturkish != next_word.nameturkish], 2
    )
    correctanswer = next_word.nameturkish
    choices = wronganswers + [correctanswer]
    random.shuffle(choices)

    labels = ['A', 'B', 'C']
    choiceswithlabels = list(zip(labels, choices))

    # Mevcut soruyu güncelle
    request.session['current_word'] = {
        'namedeutsch': next_word.namedeutsch,
        'nameturkish': next_word.nameturkish,
    }

    return JsonResponse({
        'success': True,
        'word': next_word.namedeutsch,
        'choiceswithlabels': choiceswithlabels,
    })


@csrf_exempt 
def result(request):
    correct_list = request.session.get('correct_list', [])
    wrong_list = request.session.get('wrong_list', [])

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_choice = data.get('choice')
            current_word = request.session.get('current_word', {})
            correctanswer = current_word.get('nameturkish')

            if user_choice == correctanswer:
                correct_list.append(current_word)
            else:
                wrong_list.append(current_word)

            request.session['correct_list'] = correct_list
            request.session['wrong_list'] = wrong_list

            print(request.session)

            return JsonResponse({
                'success': True,
                'correctlist': list(correct_list),
                'wronglist': list(wrong_list),
            })
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'}, status=400)

    # Eğer GET isteği geldiyse
    elif request.method == 'GET':
        return render(request, 'worte/result.html', {
            'correctlist': correct_list,
            'wronglist': wrong_list,
        })

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


@csrf_exempt 
def result_view(request):
    # Doğru ve yanlış listeleri session'dan alınır
    correct_list = request.session.get('correct_list', [])
    wrong_list = request.session.get('wrong_list', [])

    # Bu listeyi frontend'e result.html ile gönderir
    return render(request, 'worte/result.html', {
        'correctlist': correct_list,
        'wronglist': wrong_list,
    })

