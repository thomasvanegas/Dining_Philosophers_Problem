import threading
from time import sleep

# Definición de constantes
n = 5
pensando = 0
hambriento = 1
comiendo = 2

# Definición de semáforos
mutex = threading.Lock()
tenedores = [threading.Lock() for _ in range(n)]
max_filosofos = threading.Semaphore(2)  # Limita la cantidad máxima de filósofos comiendo a 2

# Estado de los filósofos
estado = [pensando] * n

# Función para obtener el índice del tenedor a la izquierda del filósofo i
def izquierda(i):
    return (i + n - 1) % n

# Función para obtener el índice del tenedor a la derecha del filósofo i
def derecha(i):
    return (i + 1) % n

# Función para verificar si un filósofo puede comer
def comprobar(i):
    if estado[i] == hambriento and estado[izquierda(i)] != comiendo and estado[derecha(i)] != comiendo:
        estado[i] = comiendo

# Función para tomar los tenedores
def getTenedores(i):
    max_filosofos.acquire()
    mutex.acquire()
    estado[i] = hambriento
    comprobar(i)
    mutex.release()
    tenedores[i].acquire()
    tenedores[derecha(i)].acquire()

# Función para devolver los tenedores
def setTenedores(i):
    mutex.acquire()
    estado[i] = pensando
    comprobar(izquierda(i))
    comprobar(derecha(i))
    mutex.release()
    tenedores[i].release()
    tenedores[derecha(i)].release()
    max_filosofos.release()

# Función para el comportamiento de los filósofos
def filosofo(i):
    while True:
        print(f"El filósofo [{i}] está pensando...")
        getTenedores(i)
        print(f"El filósofo [{i}] está usando los tenedores [{i},{derecha(i)}]")
        print(f"El filósofo [{i}] está comiendo...")
        sleep(3)
        setTenedores(i)
        print(f"El filósofo [{i}] está devolviendo los tenedores [{i},{derecha(i)}]")

# Programa principal
if __name__ == "__main__":
    hilos = [threading.Thread(target=filosofo, args=(i,)) for i in range(n)]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()