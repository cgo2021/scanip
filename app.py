import streamlit as st
import pandas as pd
import re, ipaddress
import subprocess

def ping_host(host):
    try:
        result = subprocess.run(
            ["ping", "-n", "1", host],  # Cambia "-c" por "-n" en Windows
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.returncode == 0  # Devuelve True si el ping fue exitoso
    except Exception as e:
        return False

#config
st.set_page_config(page_title="Scanip", page_icon="🤖", layout="wide")

headers = ('IP', 'EQUIPO')
df = pd.DataFrame(columns=headers)  # Crea tabla vacia
ipred = ''
mask = '/30'
prefixes = ['/%d' % i for i in range(30, 23, -1)]
fin = 3

with st.container():
    st.subheader("Esto es solo para probar hacer ping :wave:")
    st.title("Test de ping desde aplicación web")

#ingreso de datos y test
with st.container():
    st.write("---")
    left_column, right_column= st.columns((2))
    with left_column:
        st.header("Ingrese la IP de red y prefijo")
        ipred = st.text_input('IPred').strip()
        if ipred != '':
            ip = ipred.split('.')
            red = ip[0] + '.' + ip[1] + '.' + ip[2] + '.'
        prefix = st.selectbox('Prefijo', options=prefixes)
        st.write(f'IP ingresada: {ipred} con prefijo: {prefix}')
        if st.button('Ping'):
            if bool(re.match(r'^((0|[1-9][0-9]?|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(\.|$)){4}$', ipred)):
                interface = ipaddress.IPv4Interface(ipred + prefix)
                ipr = interface.network             # IP de red
                ip = ipaddress.IPv4Network(ipr)
                inicio = int(str(ip.network_address + 1).split('.')[3])  # Primera dirección
                fin = int(str(ip.broadcast_address).split('.')[3])       # Última dirección
                df = pd.DataFrame(columns=headers)  # Crea tabla vacia
                for r in range(inicio, fin):
                    row = r - inicio + 1
                    host = red + str(r)
                    df.at[row, headers[0]] = host
                    rst = ping_host(host)
                    if rst:
                        df.at[row, headers[1]] = 'OK'
                    else:
                        df.at[row, headers[1]] = 'NO RESPONDE'
            else:
                st.write(f'IP ingresada {ipred} inválida')
                df = pd.DataFrame(columns=headers)  # Crea tabla vacia
            

    with right_column:
        st.header("Resultados de la prueba de ping")
        st.write('Tabla:')
        st.dataframe(df)
