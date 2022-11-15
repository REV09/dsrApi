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

def encriptar_mensaje(mensaje: str, llaveEncriptacion: bytes):
    
    '''
    permite encriptar el mensaje que reciba como argumento
    ademas debe recibir la llave de encriptacion
    '''

    mensaje_codificado = mensaje.encode()
    encriptado_fernet = Fernet(llaveEncriptacion)
    mensaje_encriptado = encriptado_fernet.encrypt(mensaje_codificado)
    return mensaje_encriptado

def desencriptar_mensaje(mensajeEncriptado: bytes, llaveDesencriptado: bytes):

    '''
    Desencripta el mensaje siempre y cuando 
    la llave de encriptado sea la correcta
    '''

    encriptado_fernet = Fernet(llaveDesencriptado)
    mensaje_desencriptado = encriptado_fernet.decrypt(mensajeEncriptado).decode()
    return mensaje_desencriptado