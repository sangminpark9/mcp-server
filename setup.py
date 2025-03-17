#!/usr/bin/env python
import os
import argparse
import subprocess
import sys
from pathlib import Path

def create_directory_structure():
    """기본 디렉토리 구조 생성"""
    print("디렉토리 구조 생성 중...")
    
    directories = [
        "app",
        "app/api",
        "app/core",
        "app/models",
        "app/schemas",
        "models",
        "models/deepseek",
        "models/llama"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("디렉토리 구조가 생성되었습니다.")

def setup_venv():
    """가상환경 설정"""
    print("가상환경 설정 중...")
    
    if not Path("venv").exists():
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # 운영체제에 따라 활성화 스크립트 경로 지정
    if os.name == "nt":  # Windows
        activate_script = "venv\\Scripts\\activate"
    else:  # Unix/Linux/Mac
        activate_script = "venv/bin/activate"
    
    print(f"가상환경이 설정되었습니다. 다음 명령어로 활성화하세요: source {activate_script}")

def install_dependencies():
    """의존성 패키지 설치"""
    print("의존성 패키지 설치 중...")
    
    # 운영체제에 따라 pip 경로 지정
    if os.name == "nt":  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        pip_path = "venv/bin/pip"
    
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    print("의존성 패키지가 설치되었습니다.")

def download_models(args):
    """모델 다운로드"""
    if not args.download_models:
        print("모델 다운로드를 건너뜁니다. 수동으로 모델을 다운로드하세요.")
        return
    
    print("모델 다운로드 중... (이 작업은 시간이 오래 걸릴 수 있습니다)")
    
    # 운영체제에 따라 python 경로 지정
    if os.name == "nt":  # Windows
        python_path = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        python_path = "venv/bin/python"
    
    # DeepSeek 모델 다운로드
    deepseek_script = """
import os
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"
save_path = "models/deepseek"

print(f"다운로드 중: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print(f"저장 중: {save_path}")
tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)
print("DeepSeek 모델 다운로드 완료!")
"""
    
    # Llama 모델 다운로드
    llama_script = """
import os
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "kfkas/Llama-2-13b-chat-Korean"
save_path = "models/llama"

print(f"다운로드 중: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print(f"저장 중: {save_path}")
tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)
print("Llama 모델 다운로드 완료!")
"""
    
    # DeepSeek 모델 다운로드
    if args.model in ["all", "deepseek"]:
        print("\nDeepSeek 모델 다운로드 중...")
        subprocess.run([python_path, "-c", deepseek_script], check=True)
    
    # Llama 모델 다운로드
    if args.model in ["all", "llama"]:
        print("\nLlama 모델 다운로드 중...")
        subprocess.run([python_path, "-c", llama_script], check=True)
    
    print("모델 다운로드가 완료되었습니다!")

def main():
    parser = argparse.ArgumentParser(description="MCP 서버 설정 스크립트")
    parser.add_argument("--download-models", action="store_true", help="모델 다운로드 여부")
    parser.add_argument("--model", choices=["all", "deepseek", "llama"], default="all", help="다운로드할 모델 선택")
    args = parser.parse_args()
    
    create_directory_structure()
    setup_venv()
    install_dependencies()
    download_models(args)
    
    print("\nMCP 서버 설정이 완료되었습니다!")
    print("서버를 시작하려면 다음 명령어를 실행하세요:")
    print("1. 가상환경 활성화: source venv/bin/activate (Linux/Mac) 또는 venv\\Scripts\\activate (Windows)")
    print("2. 서버 실행: uvicorn app.main:app --reload")
    print("\n또는 Docker를 사용하여 실행:")
    print("docker-compose up -d")

if __name__ == "__main__":
    main()