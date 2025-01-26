import torch
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.dataloaders import LoadImages
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.torch_utils import select_device

def detect_image(image_path, model_path, device=''):
    # Setare dispozitiv (GPU sau CPU)
    device = select_device(device)

    # Încărcarea modelului
    model = DetectMultiBackend(model_path, device=device)
    stride = model.stride
    img_size = 640  # Asumam o dimensiune standard pentru YOLOv5

    # Incarcarea si preprocesarea imaginii
    dataset = LoadImages(image_path, img_size=img_size, stride=stride, auto=True)

    # Pregatirea modelului pentru inferenta
    model.warmup(imgsz=(1, 3, img_size, img_size))  # specific warmup

    # Rularea inferentei pe imagine
    for path, img, im0s, vid_cap, s in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float() / 255.0  # scalare între 0.0 și 1.0
        if len(img.shape) == 3:
            img = img.unsqueeze(0)

        # Inferenta
        pred = model(img)

        # Aplicarea Non-Max Suppression pentru a filtra predicțiile
        pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45, classes=None, agnostic=False)

        # Procesarea predicțiilor
        for i, det in enumerate(pred):  # Iteram prin detectii
            if len(det):
                # Rescalam cutiile de la dimensiunea img la dimensiunea originală im0
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0s.shape).round()

                # Afișăm rezultatele
                for *xyxy, conf, cls in det:
                    if conf > 0.5:
                        #print(f'In imaginea data s-a gasit clasa: {model.names[int(cls)]}')
                        return (conf, model.names[int(cls)])
    return (0, 0)

# Exemplu de utilizare
#detect_image('./data/images/test10.jpg', './yolov5s.pt')
