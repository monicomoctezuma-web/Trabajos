import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


# PASO 1: CREAR DATOS (Simulación)
# Imagina que tenemos datos de 50 personas.
# Característica (X): Temperatura ambiente en °C (entre 15 y 40 °C)
# Objetivo (y): Número de vasos de agua consumidos al día (aprox 0.4 * temperatura + ruido)

np.random.seed(42)  # Para que siempre salgan los mismos números aleatorios

# Generamos 50 temperaturas aleatorias
X = np.random.randint(15, 40, size=(50, 1))

# Generamos el consumo: (0.4 * temperatura) + un poco de error aleatorio (ruido)
y = (0.4 * X).squeeze() + np.random.randn(50) * 1.2

print("Primeras 5 muestras de datos:")
print(f"Temperatura (°C): {X[:5].flatten()}")
print(f"Vasos de agua:    {np.round(y[:5], 2)}")


# PASO 2: DIVIDIR DATOS (Entrenamiento vs Prueba)
# Guardamos un 20% para validar los resultados.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nDatos para entrenar (Train): {len(X_train)} registros")
print(f"Datos para validar (Test):   {len(X_test)} registros")


# PASO 3: ENTRENAR EL MODELO
modelo = LinearRegression()
modelo.fit(X_train, y_train)

print("\nModelo entrenado con éxito.")
print(f"   Pendiente aprendida (vasos por °C): {modelo.coef_[0]:.4f}")
print(f"   Intercepto (base): {modelo.intercept_:.4f}")


# PASO 4: HACER PREDICCIONES
y_pred = modelo.predict(X_test)

print("\nComparación (Realidad vs Predicción):")
for i in range(5):
    print(f"Registro {i+1}: Real={y_test[i]:.2f} vasos | Predicho={y_pred[i]:.2f} vasos")

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nMétricas de rendimiento:")
print(f"   Error Cuadrático Medio (MSE): {mse:.2f}")
print(f"   R² (Qué tanto explica el modelo): {r2:.2f} (1.0 es perfecto)")


# PASO 5: VISUALIZAR RESULTADOS
plt.figure(figsize=(10, 6))

plt.scatter(X_train, y_train, color='gray', alpha=0.5, label='Datos Entrenamiento')
plt.scatter(X_test, y_test, color='blue', edgecolors='black', label='Datos Prueba (Realidad)')

X_linea = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_linea = modelo.predict(X_linea)
plt.plot(X_linea, y_linea, color='red', linewidth=2, label='Línea de Predicción (Modelo)')

plt.title('Regresión Lineal Simple: Consumo de Agua según Temperatura')
plt.xlabel('Temperatura ambiente (°C)')
plt.ylabel('Vasos de agua consumidos al día')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


# PASO 6: PRUEBA FINAL
nueva_temperatura = np.array([[35]])  # 35°C
vasos_estimados = modelo.predict(nueva_temperatura)

print(f"\nSi la temperatura del día es de 35°C...")
print(f"   El modelo estima un consumo de: {vasos_estimados[0]:.2f} vasos de agua")