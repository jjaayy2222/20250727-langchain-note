def save_sentences_to_file(sentences, file_path):
    """
    주어진 문자열 리스트를 텍스트 파일에 저장합니다.

    Args:
        sentences (list): 저장할 문자열 리스트
        file_path (str): 저장할 파일 경로
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for sentence in sentences:
            file.write(sentence + '\n')

def save_sentences_to_data_folder(sentences, file_name):
    """
    주어진 문자열 리스트를 /Users/jay/Projects/20250727-langchain-note/08_Embedding/data 폴더 저장하기

    Args:
        sentences (list): 저장할 문자열 리스트
        file_name (str): 저장할 파일 이름
    """
    file_path = f"/Users/jay/Projects/20250727-langchain-note/08_Embedding/data/{file_name}"
    save_sentences_to_file(sentences, file_path)