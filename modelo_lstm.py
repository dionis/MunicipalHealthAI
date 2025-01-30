# services/modelo_lstm.py
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam

def entrenar_modelo_lstm(X_train, y_train):
    X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    
    modelo = Sequential()
    modelo.add(LSTM(50, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])))
    modelo.add(Dense(1))  # Cambia a 1 si tienes solo una etiqueta, por ejemplo, 'riesgo'
    modelo.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    
    modelo.fit(X_train, y_train, epochs=200, batch_size=32, verbose=1)
    return modelo

def evaluar_modelo_lstm(modelo, X_test, y_test):
    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))
    predicciones = modelo.predict(X_test)
    mse = mean_squared_error(y_test, predicciones)
    return mse
