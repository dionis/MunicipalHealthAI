import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def cargar_datos():
    ruta_archivo = r'C:\Users\Ralph\Desktop\backend\archivo.csv'
    try:
        datos = pd.read_csv(ruta_archivo)
        if datos.empty:
            print("El archivo está vacío.")
            return None
        return datos
    except FileNotFoundError:
        print("El archivo no se encuentra.")
        return None
    except pd.errors.EmptyDataError:
        print("El archivo está vacío.")
        return None
    except pd.errors.ParserError:
        print("Error al parsear el archivo.")
        return None
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return None

def procesar_datos(datos):
    # Convertir datos categóricos
    datos['medical_history'] = datos['medical_history'].astype('category').cat.codes

    # Separar características y etiquetas
    X = datos[['age', 'weight', 'height', 'cycle_duration', 'medical_history', 'days_since_last_period']]
    y_riesgo = datos['riesgo']  # Suponiendo que tienes una columna 'riesgo'
    y_fecha_parto = datos['fecha_parto']  # Suponiendo que tienes una columna 'fecha_parto'

    # Escalar los datos
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train_riesgo, y_test_riesgo = train_test_split(X_scaled, y_riesgo, test_size=0.2, random_state=42)
    y_train_fecha, y_test_fecha = train_test_split(y_fecha_parto, test_size=0.2, random_state=42)

    return X_train, X_test, y_train_riesgo, y_test_riesgo, y_train_fecha, y_test_fecha

# Llamada a la función
datos = cargar_datos()
if datos is not None:
    X_train, X_test, y_train_riesgo, y_test_riesgo, y_train_fecha, y_test_fecha = procesar_datos(datos)
    print("Datos cargados y procesados correctamente.")
else:
    print("No se pudo cargar los datos.")
