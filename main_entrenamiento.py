# entrenamiento/main_entrenamiento.py
from services.preprocesamiento import cargar_datos, preprocesar_datos
from services.modelo_regresion import entrenar_modelo_regresion, evaluar_modelo_regresion
from services.modelo_lstm import entrenar_modelo_lstm, evaluar_modelo_lstm

# Ruta del archivo CSV
ruta_archivo = 'ruta/al/archivo/historico.csv'

# Cargar y preprocesar datos
datos = cargar_datos(ruta_archivo)
X_train, X_test, y_train_riesgo, y_test_riesgo, y_train_fecha, y_test_fecha = preprocesar_datos(datos)

# Entrenar y evaluar modelo de regresión lineal para el riesgo
modelo_regresion_riesgo = entrenar_modelo_regresion(X_train, y_train_riesgo)
mse_regresion_riesgo = evaluar_modelo_regresion(modelo_regresion_riesgo, X_test, y_test_riesgo)
print(f'MSE del modelo de regresión lineal (riesgo): {mse_regresion_riesgo}')

# Entrenar y evaluar modelo de regresión lineal para la fecha de parto
modelo_regresion_fecha = entrenar_modelo_regresion(X_train, y_train_fecha)
mse_regresion_fecha = evaluar_modelo_regresion(modelo_regresion_fecha, X_test, y_test_fecha)
print(f'MSE del modelo de regresión lineal (fecha de parto): {mse_regresion_fecha}')

# Entrenar y evaluar modelo LSTM para el riesgo
modelo_lstm_riesgo = entrenar_modelo_lstm(X_train, y_train_riesgo)
mse_lstm_riesgo = evaluar_modelo_lstm(modelo_lstm_riesgo, X_test, y_test_riesgo)
print(f'MSE del modelo LSTM (riesgo): {mse_lstm_riesgo}')

# Entrenar y evaluar modelo LSTM para la fecha de parto
modelo_lstm_fecha = entrenar_modelo_lstm(X_train, y_train_fecha)
mse_lstm_fecha = evaluar_modelo_lstm(modelo_lstm_fecha, X_test, y_test_fecha)
print(f'MSE del modelo LSTM (fecha de parto): {mse_lstm_fecha}')
