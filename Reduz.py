import streamlit as st
from PIL import Image
import os
import io

MAX_IMAGE_SIZE = 300 * 1024  # 300KB
TARGET_SIZE = (640, 480)


def format_file_size(size_in_bytes):
    """
    Formata o tamanho do arquivo de bytes para KB ou MB.
    """
    if size_in_bytes < 1024 * 1024:  # Menos de 1 MB
        return f"{size_in_bytes / 1024:.2f} KB"
    else:  # 1 MB ou mais
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"


def resize_image(image, target_size=TARGET_SIZE, max_filesize=MAX_IMAGE_SIZE):
    # Redimensionar a imagem mantendo sua proporção
    image.thumbnail(target_size, Image.LANCZOS)

    # Salvar a imagem com alta qualidade e verificar o tamanho do arquivo
    img_byte_arr = io.BytesIO()
    img_quality = 95
    image.save(img_byte_arr, format='JPEG', quality=img_quality)

    # Se o arquivo ainda estiver acima do tamanho máximo, ajustar a qualidade
    while len(img_byte_arr.getvalue()) > max_filesize and img_quality > 10:
        img_quality -= 5
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=img_quality)

    return img_byte_arr


def create_download_button(i, img_byte_arr):
    st.download_button(
        label="Download Imagem Redimensionada",
        data=img_byte_arr.getvalue(),
        file_name=f"image_{i}.jpg",
        key=f"download_button_{i}"
    )

def main():
    st.image('NIDLogo.jpg')
    st.write('Núcleo de Inteligência de Dados - LABCOM')
    st.title("DOWNSCALER")
    st.write('REDUTOR DE IMAGENS')
    st.write("Desenvolvimento NID - Núcleo de Inteligência de Dados - nidlab.com.br")
    st.write('Usar imagens mais leves no seu site facilita o carregamento e a experiência do usuário na sua página. Assim, se você tem imagens de tamanho maior que não precisam ser tão pesadas, basta usar o image-web-resizer para converter várias delas ao mesmo tempo ( redução em lote ) e depois apenas fazer o download das imagens . Você faz o upload das imagens que quiser (limitadas a 200 mega no total). Formatos aceitos: jpg, jpeg, png.')

    uploaded_files = st.file_uploader("Selecione as imagens", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

    if uploaded_files:
        for i, uploaded_file in enumerate(uploaded_files):
            img = Image.open(uploaded_file)

            # Mostrar imagem original
            col1, col2 = st.columns(2)
            with col1:
                st.header("Original")
                st.image(img, caption='Imagem Original', use_column_width=True)
                st.write(f"Dimensões: {img.size[0]} x {img.size[1]} pixels")
                st.write(f"Tamanho do arquivo: {format_file_size(uploaded_file.size)}")

            # Mostrar imagem redimensionada
            img_byte_arr = resize_image(img)
            with col2:
                st.header("Redimensionada")
                resized_img = Image.open(img_byte_arr)
                st.image(resized_img, caption='Imagem Redimensionada', use_column_width=True)
                st.write(f"Dimensões: {resized_img.size[0]} x {resized_img.size[1]} pixels")
                st.write(f"Tamanho do arquivo: {format_file_size(len(img_byte_arr.getvalue()))}")

                # Fornecer link de download para a imagem redimensionada
                create_download_button(i, img_byte_arr)

if __name__ == "__main__":
    main()
