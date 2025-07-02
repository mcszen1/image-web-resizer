import streamlit as st
from PIL import Image
import io

def format_file_size(size_bytes):
    for unit in ['B','KB','MB','GB','TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"

def resize_image(image: Image.Image, max_filesize: int = 200 * 1024) -> io.BytesIO:
    # Converte RGBA ou modo P (com paleta/alpha) para RGB antes de salvar
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    
    img_byte_arr = io.BytesIO()
    img_quality = 95

    # Salva como JPEG
    image.save(img_byte_arr, format="JPEG", quality=img_quality)

    # Reduz qualidade até atingir tamanho máximo
    while img_byte_arr.tell() > max_filesize and img_quality > 10:
        img_quality -= 5
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="JPEG", quality=img_quality)

    img_byte_arr.seek(0)
    return img_byte_arr

def create_download_button(index: int, img_byte_arr: io.BytesIO):
    st.download_button(
        label=f"🔽 Baixar imagem {index+1}",
        data=img_byte_arr,
        file_name=f"resized_{index+1}.jpg",
        mime="image/jpeg"
    )

def main():

    st.image('NIDLogo.jpg')
    st.write('Núcleo de Inteligência de Dados - LABCOM')
    st.title("DOWNSCALER")
    st.write('REDUTOR DE IMAGENS')
    st.write("Desenvolvimento NID - Núcleo de Inteligência de Dados - nidlab.com.br")
    st.write('Usar imagens mais leves no seu site facilita o carregamento e a experiência do usuário na sua página. Assim, se você tem imagens de tamanho maior que não precisam ser tão pesadas, basta usar o image-web-resizer para converter várias delas ao mesmo tempo ( redução em lote ) e depois apenas fazer o download das imagens . Você faz o upload das imagens que quiser (limitadas a 200 mega no total). Formatos aceitos: jpg, jpeg, png.')

    uploaded_files = st.file_uploader(
        "Faça upload de uma ou mais imagens (PNG, JPG, etc.)",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True
    )

    if uploaded_files:
        for idx, uploaded_file in enumerate(uploaded_files):
            image = Image.open(uploaded_file)
            
            st.write(f"🖼️ Imagem original {idx+1}")
            st.image(image, use_container_width=True)
            
            file_size = uploaded_file.size
            st.write("Tamanho do arquivo:", format_file_size(file_size))
            
            resized_io = resize_image(image)
            
            st.write(f"📉 Imagem redimensionada {idx+1}")
            resized_img = Image.open(resized_io)
            st.image(resized_img, use_container_width=True)
            
            new_size = resized_io.getbuffer().nbytes
            st.write("Novo tamanho:", format_file_size(new_size))
            
            create_download_button(idx, resized_io)

if __name__ == "__main__":
    main()

