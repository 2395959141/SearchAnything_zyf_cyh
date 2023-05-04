import os  
import streamlit as st  
import tkinter as tk
from tkinter import filedialog
from filegpt import FileGPT

@st.cache_resource()  
def create_filegpt_instance():  
    return FileGPT("sentence-transformers/all-mpnet-base-v2")


def search_database(query, search_types): 
    filegpt = create_filegpt_instance()
    results = filegpt.search(query) 
    # print(results)
    # results = [  
    #     f"文本结果1：{query}",  
    #     f"文本结果2：{query}",  
    #     f"图片结果1：{query}",  
    #     f"音频结果1：{query}",  
    # ]  
    return results  

  
def select_file_or_folder():  
    root = tk.Tk()  
    root.withdraw()  # 隐藏主窗口  
    file_path = filedialog.askopenfilename()  # 打开文件选择对话框  
    return file_path  


# 侧边栏标题  
st.sidebar.title("侧边栏")  
  
# 选择应用程序  
app_choice = st.sidebar.radio("选择应用程序", ["文件浏览器", "搜索应用程序"])  
  
if app_choice == "搜索应用程序":  
    st.title("搜索应用程序")  
    search_query = st.text_input("输入搜索关键词")  
  
    columns = st.columns(3)  
    text_selected = columns[0].checkbox("文本", value=True)  
    image_selected = columns[1].checkbox("图片")  
    audio_selected = columns[2].checkbox("音频")  
  
    if search_query:  
        search_types = []  
        if text_selected:  
            search_types.append("文本")  
        if image_selected:  
            search_types.append("图片")  
        if audio_selected:  
            search_types.append("音频")  
  
        search_results = search_database(search_query, search_types)  
        st.write("搜索结果：")  
        for file_path, file_info in search_results:  
            # 为每个文件创建一个beta_expander  
            expander = st.expander(f"{file_path} - 最小距离：{file_info['min_distance']:.2f}")  
    
            # 在展开器中显示文件的内容  
            for content, distance, page in zip(file_info["content"], file_info["distance"], file_info["page"]):
                expander.write(f"页面：{page}，距离：{distance}\n内容：{content}")
  
elif app_choice == "文件浏览器":  
    st.title("文件浏览器")  
  
    if st.button("选择文件"):  
        selected_file = select_file_or_folder()  
        st.write(f"您选择的文件是：{selected_file}")  