from cryptography.fernet import Fernet

def generar_llave():
    
    '''
    Genera la clave de encriptado y la guarda en un archivo
    '''

    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def cargar_llave():
    
    '''
    Carga la llave de encriptado/desencriptado
    '''

    return open("security/secret.key", "rb").read()

def encriptar_mensaje(mensaje: str, llave_encriptacion: bytes):
    
    '''
    permite encriptar el mensaje que reciba como argumento
    ademas debe recibir la llave de encriptacion
    '''

    mensaje_codificado = mensaje.encode()
    encriptado_fernet = Fernet(llave_encriptacion)
    mensaje_encriptado = encriptado_fernet.encrypt(mensaje_codificado)
    return mensaje_encriptado

def desencriptar_mensaje(mensaje_encriptado: bytes, llave_desencriptado: bytes):

    '''
    Desencripta el mensaje siempre y cuando 
    la llave de encriptado sea la correcta
    '''

    encriptado_fernet = Fernet(llave_desencriptado)
    mensaje_desencriptado = encriptado_fernet.decrypt(mensaje_encriptado).decode()
    return mensaje_desencriptado