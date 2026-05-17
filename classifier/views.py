from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .model_loader import ImageClassifier

model = ImageClassifier()

@csrf_exempt
def predict(request):
    if request.method != "POST":
        return JsonResponse({"Error": "Only POST Request allowed."}, status=405)
    
    
    if "image" not in request.FILES:
        return JsonResponse({"Error": "No Image provided."}, status=400)
    
    img_file = request.FILES["image"]
    label, confidence, all_probs = model.predict_bytes(img_file.read())

    return JsonResponse({
        "filename": img_file.name,
        "label": label,
        "confidence": confidence,
        "all_probs": all_probs,
    })
