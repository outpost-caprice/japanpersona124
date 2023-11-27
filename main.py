import openai
import json
import logging
import traceback
from openai import OpenAI
import os

# OpenAIの同期クライアント初期化
OPENAI_api_key = os.getenv("OPENAI_API_KEY") 
def init_openai():
  return OpenAI(api_key=OPENAI_api_key)
# OpenAI API呼び出し関数
def openai_api_call(model, temperature, messages, max_tokens, response_format):
    client = init_openai()
    try:
        # OpenAI API呼び出しを行う
        response = client.chat.completions.create(model=model, temperature=temperature, messages=messages, max_tokens=max_tokens, response_format=response_format)
        return response.choices[0].message.content  # 辞書型アクセスから属性アクセスへ変更
    except Exception as e:
        logging.error(f"OpenAI API呼び出し中にエラーが発生しました: {e}")
        raise
# パラメーターを書き出す
parameter = '''
{
  "properties": {
    "persona1": {
      "type": "string",
      "description": "Output persona. Includes occupation, personality, ideology, religion, beliefs, etc."
    },
    "persona2": {
      "type": "string",  
      "description": "Output persona 2. Includes occupation, personality, ideology, religion, beliefs, etc."
    },
    "persona3": {
      "type": "string",
      "description": "Output persona 3. Includes occupation, personality, ideology, religion, beliefs, etc."
    },
    "persona4": {
      "type": "string",
      "description": "Output persona 4. Includes occupation, personality, ideology, religion, beliefs, etc."
    }
  },
  "required": ["persona1", "persona2", "persona3", "persona4"]
}
'''
# スコアを書き出す
def main():
    try:
        persona = openai_api_call(
            "gpt-4-1106-preview",
            0.6,
            [
                {"role": "user", "content": f'テクノロジーの最先端分野に興味を持つ日本人のペルソナをいくつか考えててください。職業、性格、思想、宗教、信条、性別、家族構成などを考慮して多様性を持たせたキャラクターです。"""{parameter}"""のJSON形式で出力してください。'}
            ],
            4000,
            { "type":"json_object" }
            )
        persona_json = json.loads(persona)
        # 応答を整形して返す
        formatted_score = json.dumps(persona_json, indent=2, ensure_ascii=False)
        print(formatted_score)
    except Exception as e:
        logging.warning(f"ペルソナ作成時にエラーが発生しました。: {e}")
        traceback.print_exc()
        return ""
    
if __name__ == "__main__":
    main()