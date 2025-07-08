"""
簡単なテストスクリプト
アプリケーションの基本機能をテストする
"""
import requests
import json
from pathlib import Path


def test_health_check():
    """ヘルスチェックのテスト"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health Check Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False


def test_config_endpoint():
    """設定エンドポイントのテスト"""
    try:
        response = requests.get("http://localhost:8000/config")
        print(f"Config Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Config endpoint test failed: {e}")
        return False


def create_test_text_file():
    """テスト用のテキストファイルを作成"""
    test_content = """これはテストドキュメントです。

このドキュメントには、いくつかの問題が含まれています。
例えば、同じ同じ語句が連続しています。
また、ですます調である調が混在しています。

長い文章のテスト: これは非常に長い文章の例で、文の長さをチェックする機能をテストするために作成されており、推奨される文字数を大幅に超えることで警告が表示されるかどうかを確認することができます。

サーバとサーバーの表記ゆれもあります。
ユーザとユーザーも同様です。

することができます。これは冗長表現の例です。
"""
    
    test_file_path = Path("/tmp/test_document.txt")
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    return test_file_path


def test_file_check():
    """ファイルチェック機能のテスト"""
    # テストファイルを作成
    test_file = create_test_text_file()
    
    try:
        url = "http://localhost:8000/check"
        files = {"files": open(test_file, "rb")}
        
        response = requests.post(url, files=files)
        print(f"File Check Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Total files: {result['total_files']}")
            print(f"Processed files: {result['processed_files']}")
            
            for file_result in result['results']:
                print(f"\nFile: {file_result['filename']}")
                print(f"Status: {file_result['status']}")
                print(f"Text length: {file_result['text_length']}")
                print(f"Issues found: {len(file_result['issues'])}")
                
                for issue in file_result['issues'][:5]:  # 最初の5つの問題のみ表示
                    print(f"  - {issue['type']}: {issue['message']}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"File check test failed: {e}")
        return False
    finally:
        # テストファイルを削除
        if test_file.exists():
            test_file.unlink()


def main():
    """メインテスト関数"""
    print("=== API テスト開始 ===\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Config Endpoint", test_config_endpoint),
        ("File Check", test_file_check),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} テスト ---")
        result = test_func()
        results.append((test_name, result))
        print(f"結果: {'✓ 成功' if result else '✗ 失敗'}")
    
    print("\n=== テスト結果サマリー ===")
    for test_name, result in results:
        print(f"{test_name}: {'✓ 成功' if result else '✗ 失敗'}")
    
    success_count = sum(1 for _, result in results if result)
    print(f"\n成功: {success_count}/{len(results)}")


if __name__ == "__main__":
    main()
