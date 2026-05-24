from ultralytics import YOLO
import cv2

# Cargar modelo
model = YOLO("yolo12n.pt")

# Abrir cámara
cap = cv2.VideoCapture(0)

while True:

    # Leer cámara
    ret, frame = cap.read()

    if not ret:
        break

    # Detectar objetos
    results = model(frame)

    # Dibujar resultados
    annotated_frame = results[0].plot()

    # Mostrar ventana
    cv2.imshow("Detector IA", annotated_frame)

    # Salir con la tecla Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerrar cámara
cap.release()
cv2.destroyAllWindows()